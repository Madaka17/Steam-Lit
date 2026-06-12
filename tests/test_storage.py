"""เทสต์ส่วนอ่าน/ตรวจสอบ/บันทึกไฟล์อัปโหลด (src/storage.py)"""

import os

import pytest

from src.data import FEATURE_COLUMNS, TARGET_COLUMN, generate_data
from src.storage import (
    MIN_ROWS,
    ValidationError,
    read_upload,
    save_upload,
    validate_dataset,
)


def _csv_bytes(df) -> bytes:
    return df.to_csv(index=False).encode("utf-8")


def test_read_upload_csv_roundtrip():
    df = generate_data(n=80)
    out = read_upload("data.csv", _csv_bytes(df))
    assert set(out.columns) == set(FEATURE_COLUMNS + [TARGET_COLUMN])
    assert len(out) == 80


def test_read_upload_rejects_unknown_extension():
    with pytest.raises(ValidationError):
        read_upload("data.txt", b"whatever")


def test_validate_accepts_valid_dataset():
    df = generate_data(n=100)
    out = validate_dataset(df)
    assert len(out) == 100
    assert list(out.columns) == FEATURE_COLUMNS + [TARGET_COLUMN]


def test_validate_rejects_missing_columns():
    df = generate_data(n=100).drop(columns=[TARGET_COLUMN])
    with pytest.raises(ValidationError):
        validate_dataset(df)


def test_validate_rejects_too_few_rows():
    df = generate_data(n=MIN_ROWS - 1)
    with pytest.raises(ValidationError):
        validate_dataset(df)


def test_validate_rejects_non_numeric_feature():
    df = generate_data(n=100)
    df["area_sqm"] = df["area_sqm"].astype(object)
    df.loc[0, "area_sqm"] = "ไม่ใช่ตัวเลข"
    with pytest.raises(ValidationError):
        validate_dataset(df)


def test_validate_rejects_non_positive_price():
    df = generate_data(n=100)
    df.loc[0, TARGET_COLUMN] = 0
    with pytest.raises(ValidationError):
        validate_dataset(df)


def test_save_upload_writes_timestamped_file(tmp_path, monkeypatch):
    import src.storage as storage

    monkeypatch.setattr(storage, "UPLOAD_DIR", str(tmp_path))
    data = b"hello,world\n1,2\n"
    path = save_upload("my data.csv", data)

    assert os.path.exists(path)
    assert os.path.basename(path).endswith("_my data.csv")
    with open(path, "rb") as f:
        assert f.read() == data


def test_save_upload_does_not_overwrite(tmp_path, monkeypatch):
    import src.storage as storage

    monkeypatch.setattr(storage, "UPLOAD_DIR", str(tmp_path))
    # บันทึกชื่อเดียวกันสองครั้งติดกัน ต้องได้คนละไฟล์ ไม่ทับกัน
    p1 = save_upload("same.csv", b"a")
    p2 = save_upload("same.csv", b"b")
    assert p1 != p2
    with open(p1, "rb") as f:
        assert f.read() == b"a"
    with open(p2, "rb") as f:
        assert f.read() == b"b"
