"""เทสต์ชั้นความปลอดภัย — sanitize ชื่อไฟล์, เพดานขนาด/แถว, โควตา archive"""

import os

import pytest

from src.data import generate_data
from src.security import sanitize_filename
from src.storage import (
    MAX_ROWS,
    MAX_UPLOAD_BYTES,
    ValidationError,
    read_upload,
    save_upload,
    validate_dataset,
)


# ----- sanitize_filename: กัน path traversal -----

def test_sanitize_strips_path_traversal():
    assert sanitize_filename("../../etc/passwd") == "passwd"
    assert sanitize_filename("..\\..\\windows\\system32.csv") == "system32.csv"


def test_sanitize_keeps_thai_and_normal_names():
    assert sanitize_filename("ข้อมูลบ้าน 2569.csv") == "ข้อมูลบ้าน 2569.csv"
    assert sanitize_filename("data-v2.xlsx") == "data-v2.xlsx"


def test_sanitize_replaces_dangerous_chars():
    out = sanitize_filename("a;rm -rf /<b>.csv")
    assert "/" not in out and ";" not in out and "<" not in out


def test_sanitize_never_returns_empty():
    assert sanitize_filename("....") == "upload"
    assert sanitize_filename("") == "upload"


# ----- เพดานขนาดไฟล์และจำนวนแถว -----

def test_read_upload_rejects_oversized_file():
    big = b"x" * (MAX_UPLOAD_BYTES + 1)
    with pytest.raises(ValidationError):
        read_upload("big.csv", big)


def test_read_upload_corrupt_files_raise_validation_error():
    # ไฟล์พังทุกแบบต้องเป็น ValidationError (หน้าเว็บจับได้) ไม่หลุด traceback
    with pytest.raises(ValidationError):
        read_upload("fake.xlsx", b"not a real excel file")
    with pytest.raises(ValidationError):
        read_upload("fake.csv", bytes([0xFF, 0xFE, 0x00, 0x9C]) * 50)


def test_read_upload_caps_rows_at_parse_time():
    # CSV เกินเพดานต้องถูกตัดตอนอ่าน (กัน bomb) แล้วไป reject ที่ validate
    import src.storage as storage

    header = "a,b\n"
    rows = "1,2\n" * (storage.MAX_ROWS + 500)
    df = read_upload("big.csv", (header + rows).encode())
    assert len(df) == storage.MAX_ROWS + 1


def test_validate_rejects_too_many_rows():
    df = generate_data(n=200)
    # จำลองเกินเพดานโดยไม่ต้องสร้างจริง 100k แถว: ตรวจว่า MAX_ROWS ถูกใช้
    import pandas as pd

    huge = pd.concat([df] * ((MAX_ROWS // 200) + 1), ignore_index=True)
    with pytest.raises(ValidationError):
        validate_dataset(huge)


# ----- โควตา Upload Archive -----

def test_archive_quota_evicts_oldest(tmp_path, monkeypatch):
    import src.storage as storage

    monkeypatch.setattr(storage, "UPLOAD_DIR", str(tmp_path))
    monkeypatch.setattr(storage, "ARCHIVE_QUOTA_BYTES", 250)

    p1 = storage.save_upload("a.csv", b"x" * 100)
    os.utime(p1, (1, 1))  # ทำให้ p1 เก่าสุดแบบชัดเจน
    p2 = storage.save_upload("b.csv", b"y" * 100)

    # ไฟล์ที่สาม (100B) ทำให้รวมเกิน 250 → ไฟล์เก่าสุด (p1) ต้องถูกลบ
    p3 = storage.save_upload("c.csv", b"z" * 100)

    assert not os.path.exists(p1)
    assert os.path.exists(p2)
    assert os.path.exists(p3)


def test_audit_log_records_user(tmp_path, monkeypatch):
    import src.storage as storage

    monkeypatch.setattr(storage, "UPLOAD_DIR", str(tmp_path))
    storage.save_upload("data.csv", b"abc", user="someone@example.com")

    log = (tmp_path / "audit.log").read_text(encoding="utf-8")
    assert "someone@example.com" in log
    assert "data.csv" in log
