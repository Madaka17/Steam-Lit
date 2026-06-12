"""อ่าน / ตรวจสอบ / บันทึก Training Dataset ที่ผู้ใช้อัปโหลด (CSV/Excel)

- :func:`read_upload`      อ่านไฟล์ที่อัปโหลดเป็น DataFrame ตามนามสกุล
- :func:`validate_dataset` ตรวจให้ตรง Canonical Schema (ดู CONTEXT.md)
- :func:`save_upload`      บันทึกไฟล์ที่ผ่านการตรวจลง Upload Archive (data/uploads/)

ดูคำศัพท์ Canonical Schema / Upload Archive ได้ใน CONTEXT.md
"""

from __future__ import annotations

import io
import os
from datetime import datetime

import pandas as pd

from .data import (
    CATEGORICAL_COLUMNS,
    FEATURE_COLUMNS,
    NUMERIC_COLUMNS,
    TARGET_COLUMN,
)
from .security import sanitize_filename

# Upload Archive — โฟลเดอร์เก็บไฟล์ที่ผ่านการตรวจ ไม่ทับของเดิม
UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "uploads")

# คอลัมน์ทั้งหมดที่ Canonical Schema ต้องมี
REQUIRED_COLUMNS = FEATURE_COLUMNS + [TARGET_COLUMN]

# จำนวนแถวขั้นต่ำที่เทรนแล้วมีความหมาย
MIN_ROWS = 50

# ----- เพดานความปลอดภัย (แอปเปิด public) -----
MAX_UPLOAD_BYTES = 10 * 1024 * 1024  # 10MB — เช็คซ้ำกับ maxUploadSize ใน config.toml
MAX_ROWS = 100_000  # กัน CSV/Excel ยักษ์ที่ทำให้เทรนค้างหรือ RAM หมด
ARCHIVE_QUOTA_BYTES = 200 * 1024 * 1024  # โควตารวมของ Upload Archive (200MB)

EXCEL_SUFFIXES = (".xlsx", ".xls")


class ValidationError(ValueError):
    """ข้อมูลที่อัปโหลดไม่ผ่านการตรวจตาม Canonical Schema"""


def read_upload(filename: str, data: bytes) -> pd.DataFrame:
    """อ่านไฟล์อัปโหลด (CSV/Excel) เป็น DataFrame ตามนามสกุลไฟล์"""
    if len(data) > MAX_UPLOAD_BYTES:
        raise ValidationError(
            f"ไฟล์ใหญ่เกิน {MAX_UPLOAD_BYTES // (1024 * 1024)}MB "
            f"(ได้รับ {len(data) / (1024 * 1024):.1f}MB)"
        )
    name = filename.lower()
    buffer = io.BytesIO(data)
    if not name.endswith((".csv",) + EXCEL_SUFFIXES):
        raise ValidationError(
            f"ไม่รองรับไฟล์ชนิดนี้: {filename} — รองรับเฉพาะ .csv, .xlsx, .xls"
        )
    # nrows จำกัดตั้งแต่ตอน parse — กัน Excel bomb ที่ขยายใหญ่เกิน RAM
    # (+1 เพื่อให้ validate_dataset ตรวจเกินเพดานแล้ว reject ได้)
    try:
        if name.endswith(".csv"):
            return pd.read_csv(buffer, nrows=MAX_ROWS + 1)
        return pd.read_excel(buffer, nrows=MAX_ROWS + 1)
    except Exception as exc:
        # ไฟล์พัง/encoding แปลก/ไม่ใช่ไฟล์จริง — แปลงเป็น ValidationError
        # เพื่อให้หน้าเว็บแสดงข้อความสุภาพ ไม่หลุด traceback ให้ผู้ใช้ public
        raise ValidationError(
            "ไฟล์เสียหายหรือรูปแบบไม่ถูกต้อง — เปิดอ่านไม่ได้ "
            "ลองบันทึกใหม่เป็น CSV (UTF-8) หรือ .xlsx แล้วอัปโหลดอีกครั้ง"
        ) from exc


def validate_dataset(df: pd.DataFrame) -> pd.DataFrame:
    """ตรวจ DataFrame ให้ตรง Canonical Schema แล้วคืน df ที่จัดชนิดคอลัมน์เรียบร้อย

    raises :class:`ValidationError` พร้อมข้อความอธิบายเมื่อไม่ผ่าน
    """
    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        raise ValidationError("ไฟล์ขาดคอลัมน์ที่ต้องมี: " + ", ".join(missing))

    if len(df) < MIN_ROWS:
        raise ValidationError(
            f"ข้อมูลมีเพียง {len(df)} แถว — ต้องมีอย่างน้อย {MIN_ROWS} แถว"
        )

    if len(df) > MAX_ROWS:
        raise ValidationError(
            f"ข้อมูลมี {len(df):,} แถว — เกินเพดาน {MAX_ROWS:,} แถว"
        )

    df = df[REQUIRED_COLUMNS].copy()

    # คอลัมน์ตัวเลขและราคา ต้องแปลงเป็นตัวเลขได้ทั้งหมด
    num_cols = NUMERIC_COLUMNS + [TARGET_COLUMN]
    for col in num_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    bad = [c for c in num_cols if df[c].isna().any()]
    if bad:
        raise ValidationError(
            "พบค่าที่ไม่ใช่ตัวเลขหรือว่างในคอลัมน์: " + ", ".join(bad)
        )

    if (df[TARGET_COLUMN] <= 0).any():
        raise ValidationError("คอลัมน์ price ต้องเป็นค่าบวกทุกแถว")

    for col in CATEGORICAL_COLUMNS:
        df[col] = df[col].astype(str)

    return df.reset_index(drop=True)


def _enforce_archive_quota(incoming_bytes: int) -> None:
    """ลบไฟล์เก่าสุดออกจาก Upload Archive จนกว่าไฟล์ใหม่จะลงได้ในโควตา"""
    files = [
        os.path.join(UPLOAD_DIR, f)
        for f in os.listdir(UPLOAD_DIR)
        if not f.startswith(".") and f != "audit.log"
    ]
    files.sort(key=os.path.getmtime)  # เก่าสุดก่อน
    total = sum(os.path.getsize(f) for f in files)
    while files and total + incoming_bytes > ARCHIVE_QUOTA_BYTES:
        oldest = files.pop(0)
        total -= os.path.getsize(oldest)
        os.remove(oldest)


def _audit(user: str, saved_name: str, size: int) -> None:
    """จดบันทึกการอัปโหลด (ใคร/ไฟล์อะไร/ขนาด/เมื่อไหร่) ลง audit log"""
    line = f"{datetime.now().isoformat()}\t{user}\t{saved_name}\t{size}\n"
    with open(os.path.join(UPLOAD_DIR, "audit.log"), "a", encoding="utf-8") as f:
        f.write(line)


def save_upload(filename: str, data: bytes, user: str = "dev") -> str:
    """บันทึกไฟล์ดิบลง Upload Archive ด้วยชื่อ timestamp (ไม่ทับของเดิม) แล้วคืน path

    ชื่อไฟล์ถูก sanitize กัน path traversal, คุมโควตารวมของ archive,
    และจดผู้อัปโหลดลง audit log
    """
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    _enforce_archive_quota(len(data))
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    safe = sanitize_filename(filename)
    path = os.path.join(UPLOAD_DIR, f"{stamp}_{safe}")
    # กันชนกรณีบันทึกชื่อเดิมในวินาทีเดียวกัน — เติมลำดับเพื่อไม่ให้ทับ
    root, ext = os.path.splitext(path)
    counter = 1
    while os.path.exists(path):
        path = f"{root}-{counter}{ext}"
        counter += 1
    with open(path, "wb") as f:
        f.write(data)
    _audit(user, os.path.basename(path), len(data))
    return path
