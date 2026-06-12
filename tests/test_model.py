"""เทสต์ส่วน data generation และ model training/prediction"""

from src.data import FEATURE_COLUMNS, TARGET_COLUMN, generate_data
from src.model import predict_price, train_model


def test_generate_data_shape():
    df = generate_data(n=500)
    assert len(df) == 500
    assert set(FEATURE_COLUMNS + [TARGET_COLUMN]) == set(df.columns)
    assert (df[TARGET_COLUMN] > 0).all()


def test_generate_data_is_reproducible():
    a = generate_data(n=100, seed=1)
    b = generate_data(n=100, seed=1)
    assert a.equals(b)


def test_train_model_learns_signal():
    df = generate_data(n=1500)
    result = train_model(df)
    # โมเดลควรเรียนรู้รูปแบบจากข้อมูลจำลองได้ดีพอควร
    assert result.r2 > 0.8
    assert result.rmse > 0


def test_predict_returns_reasonable_price():
    df = generate_data(n=1500)
    result = train_model(df)
    features = {
        "area_sqm": 60.0,
        "bedrooms": 2,
        "bathrooms": 1,
        "age_years": 5,
        "floor": 8,
        "distance_bts_km": 1.5,
        "property_type": "คอนโด",
        "district": "สุขุมวิท",
    }
    price = predict_price(result.pipeline, features)
    assert price > 0
