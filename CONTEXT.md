# Real Estate Price Predictor

A Streamlit app that trains an XGBoost model to predict Thai property prices.
This glossary fixes the language used across the app's data, training, and
prediction surfaces.

## Language

**Canonical Schema**:
The required shape of any dataset used for training — the eight feature columns
(`area_sqm`, `bedrooms`, `bathrooms`, `age_years`, `floor`, `distance_bts_km`,
`property_type`, `district`) plus the `price` target. Every Training Dataset
must conform to it.
_Avoid_: format, layout, structure

**Training Dataset**:
A tabular dataset (synthetic or user-uploaded) that conforms to the Canonical
Schema and is fed to the model for training.
_Avoid_: input data, file, sheet

**Uploaded Dataset**:
A Training Dataset that a user supplies as a CSV or Excel file, as opposed to
the built-in synthetic dataset.
_Avoid_: user file, custom data

**Data Source**:
The origin of the Training Dataset chosen for a training run — either
"synthetic" (the built-in generated dataset) or "uploaded" (an Uploaded
Dataset). The user selects one per run.
_Avoid_: dataset mode, input type

**Upload Archive**:
The `data/uploads/` folder where every validated Uploaded Dataset is saved
under a non-overwriting timestamped name, serving as the backup of user data.
_Avoid_: backup folder, storage

**Active Model**:
The single trained model persisted at `model.joblib` and loaded by the
prediction surface. Each training run overwrites it, regardless of Data Source.
_Avoid_: current model, saved model
