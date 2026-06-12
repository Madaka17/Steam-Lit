"""เทรน / ทำนาย / บันทึก-โหลด โมเดล XGBoost สำหรับคาดการณ์ราคาอสังหาฯ

จัดการ feature เชิงหมวดหมู่ (property_type, district) ด้วย one-hot encoding
ผ่าน scikit-learn Pipeline เพื่อให้ขั้นตอน predict สอดคล้องกับตอน train
"""

from __future__ import annotations

import os
from dataclasses import dataclass

import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from xgboost import XGBRegressor

from .data import (
    CATEGORICAL_COLUMNS,
    FEATURE_COLUMNS,
    NUMERIC_COLUMNS,
    TARGET_COLUMN,
)

MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "model.joblib")


@dataclass
class TrainResult:
    """ผลลัพธ์จากการเทรน: โมเดล + เมตริก + ข้อมูลสำหรับวาดกราฟ"""

    pipeline: Pipeline
    rmse: float
    mae: float
    r2: float
    y_test: pd.Series
    y_pred: pd.Series
    feature_importance: pd.Series


def _build_pipeline(**xgb_params) -> Pipeline:
    preprocess = ColumnTransformer(
        transformers=[
            (
                "cat",
                OneHotEncoder(handle_unknown="ignore"),
                CATEGORICAL_COLUMNS,
            ),
            ("num", "passthrough", NUMERIC_COLUMNS),
        ]
    )
    params = dict(
        n_estimators=400,
        max_depth=5,
        learning_rate=0.05,
        subsample=0.9,
        colsample_bytree=0.9,
        random_state=42,
    )
    params.update(xgb_params)
    return Pipeline(
        [("preprocess", preprocess), ("model", XGBRegressor(**params))]
    )


def _feature_names(pipeline: Pipeline) -> list[str]:
    return list(pipeline.named_steps["preprocess"].get_feature_names_out())


def train_model(df: pd.DataFrame, test_size: float = 0.2, **xgb_params) -> TrainResult:
    """เทรนโมเดลจาก DataFrame แล้วคืน :class:`TrainResult`"""
    X = df[FEATURE_COLUMNS]
    y = df[TARGET_COLUMN]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=42
    )

    pipeline = _build_pipeline(**xgb_params)
    pipeline.fit(X_train, y_train)

    y_pred = pipeline.predict(X_test)
    rmse = mean_squared_error(y_test, y_pred) ** 0.5
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    importance = pd.Series(
        pipeline.named_steps["model"].feature_importances_,
        index=_feature_names(pipeline),
    ).sort_values(ascending=False)

    return TrainResult(
        pipeline=pipeline,
        rmse=float(rmse),
        mae=float(mae),
        r2=float(r2),
        y_test=y_test.reset_index(drop=True),
        y_pred=pd.Series(y_pred, name="y_pred"),
        feature_importance=importance,
    )


def predict_price(pipeline: Pipeline, features: dict) -> float:
    """ทำนายราคาจาก dict ของฟีเจอร์ 1 รายการ"""
    row = pd.DataFrame([features], columns=FEATURE_COLUMNS)
    return float(pipeline.predict(row)[0])


def save_model(pipeline: Pipeline, path: str = MODEL_PATH) -> None:
    joblib.dump(pipeline, path)


def load_model(path: str = MODEL_PATH) -> Pipeline:
    return joblib.load(path)


def model_exists(path: str = MODEL_PATH) -> bool:
    return os.path.exists(path)
