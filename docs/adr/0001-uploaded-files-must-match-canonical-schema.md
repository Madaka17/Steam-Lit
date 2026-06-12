# Uploaded training files must match the Canonical Schema

The app lets users upload a CSV/Excel file to train the model. We require every
uploaded file to contain exactly the Canonical Schema (the eight feature columns
plus `price`) and reject anything else, rather than supporting arbitrary columns
with a user-chosen target.

## Considered Options

- **Fixed schema (chosen).** Validate on upload; reuse the existing
  `ColumnTransformer`/`XGBRegressor` pipeline in `src/model.py` unchanged.
- **Arbitrary columns.** Let users pick the target and auto-detect feature
  types, building the preprocessing pipeline dynamically.

## Why

The entire modeling pipeline is hard-wired to the fixed column names. Supporting
arbitrary columns would require rebuilding preprocessing dynamically — a large
change for a demo whose value is showing XGBoost on Thai property data, not
being a general-purpose AutoML tool. The cost of reversing this later (moving to
a dynamic pipeline) is real, so we record the deliberate scope limit here.

## Consequences

A future reader wondering "why does it reject my CSV?" should look here: the
restriction is intentional. Lifting it means reworking `src/model.py` and the
upload validation in `src/storage.py`.
