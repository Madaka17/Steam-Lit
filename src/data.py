"""สร้างชุดข้อมูลอสังหาริมทรัพย์จำลองแบบไทย สำหรับเทรนโมเดล XGBoost

ราคาถูกคำนวณจากฟีเจอร์ด้วยสูตรที่สมเหตุสมผล แล้วบวก noise เล็กน้อย
เพื่อให้โมเดลเรียนรู้ความสัมพันธ์ได้จริง
"""

import numpy as np
import pandas as pd

# ตัวคูณราคาตามทำเล (district) — ยิ่งมากยิ่งแพง
DISTRICTS = {
    "สุขุมวิท": 1.60,
    "สีลม/สาทร": 1.55,
    "พญาไท/อารีย์": 1.35,
    "ลาดพร้าว": 1.10,
    "บางนา": 0.95,
    "นนทบุรี": 0.80,
    "รังสิต": 0.70,
}

# ราคาต่อตารางเมตรพื้นฐาน (บาท) ตามประเภทอสังหาฯ
PROPERTY_TYPES = {
    "คอนโด": 110_000,
    "บ้านเดี่ยว": 85_000,
    "ทาวน์เฮาส์": 70_000,
}

FEATURE_COLUMNS = [
    "area_sqm",
    "bedrooms",
    "bathrooms",
    "age_years",
    "floor",
    "distance_bts_km",
    "property_type",
    "district",
]
TARGET_COLUMN = "price"

CATEGORICAL_COLUMNS = ["property_type", "district"]
NUMERIC_COLUMNS = [c for c in FEATURE_COLUMNS if c not in CATEGORICAL_COLUMNS]


def generate_data(n: int = 2000, seed: int = 42) -> pd.DataFrame:
    """สร้าง DataFrame ข้อมูลอสังหาฯ จำลองจำนวน ``n`` แถว

    คืนคอลัมน์ตาม ``FEATURE_COLUMNS`` พร้อมคอลัมน์ราคา ``price``
    """
    rng = np.random.default_rng(seed)

    property_type = rng.choice(
        list(PROPERTY_TYPES), size=n, p=[0.55, 0.20, 0.25]
    )
    district = rng.choice(list(DISTRICTS), size=n)

    # พื้นที่ใช้สอย: คอนโดเล็กกว่าบ้าน
    base_area = np.where(property_type == "คอนโด", 45, 140)
    area_sqm = np.clip(rng.normal(base_area, base_area * 0.35), 22, 400).round(1)

    # จำนวนห้องนอน/ห้องน้ำ สัมพันธ์กับพื้นที่
    bedrooms = np.clip((area_sqm / 35).round(), 1, 5).astype(int)
    bathrooms = np.clip((bedrooms - rng.integers(0, 2, n)), 1, 4).astype(int)

    age_years = rng.integers(0, 31, n)
    # คอนโดมีหลายชั้น บ้านส่วนใหญ่ 1-3 ชั้น
    floor = np.where(
        property_type == "คอนโด",
        rng.integers(1, 41, n),
        rng.integers(1, 4, n),
    )
    distance_bts_km = np.clip(rng.exponential(2.5, n), 0.1, 20).round(2)

    # ----- คำนวณราคา -----
    price_per_sqm = np.array([PROPERTY_TYPES[t] for t in property_type])
    district_mult = np.array([DISTRICTS[d] for d in district])

    age_factor = np.clip(1 - 0.012 * age_years, 0.55, 1.0)
    bts_factor = np.clip(1.18 - 0.035 * distance_bts_km, 0.75, 1.18)
    # คอนโดชั้นสูงแพงขึ้นเล็กน้อย
    floor_factor = np.where(
        property_type == "คอนโด", 1 + 0.004 * floor, 1.0
    )

    price = (
        price_per_sqm
        * district_mult
        * area_sqm
        * age_factor
        * bts_factor
        * floor_factor
    )
    # noise แบบคูณ ±8%
    price *= rng.normal(1.0, 0.08, n)
    price = np.round(price, -3).astype(np.int64)  # ปัดเป็นหลักพัน

    return pd.DataFrame(
        {
            "area_sqm": area_sqm,
            "bedrooms": bedrooms,
            "bathrooms": bathrooms,
            "age_years": age_years,
            "floor": floor,
            "distance_bts_km": distance_bts_km,
            "property_type": property_type,
            "district": district,
            "price": price,
        }
    )
