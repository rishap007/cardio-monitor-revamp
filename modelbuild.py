"""Train and save the local heart disease prediction model."""

from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score, classification_report
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler


BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "heart.csv"
MODEL_PATH = BASE_DIR / "heartmodel.pkl"
FEATURES = [
    "age", "sex", "cp", "trestbps", "restecg", "chol", "fbs",
    "thalach", "exang", "oldpeak", "slope", "ca", "thal",
]


def build_model() -> None:
    data = pd.read_csv(DATA_PATH, encoding="utf-8-sig")
    missing = set(FEATURES + ["target"]) - set(data.columns)
    if missing:
        raise ValueError(f"heart.csv is missing required columns: {sorted(missing)}")

    # In this CSV, 4 for ca and 0 for thal are missing-value sentinels.
    data["ca"] = data["ca"].replace(4, np.nan)
    data["thal"] = data["thal"].replace(0, np.nan)

    # In this copy of the dataset, target=1 is disease-absent and target=0
    # is disease-present. Normalize to the usual convention: 1 means disease.
    target = 1 - data["target"]
    x_train, x_test, y_train, y_test = train_test_split(
        data[FEATURES], target, test_size=0.2, random_state=0,
        stratify=data["target"],
    )
    model = make_pipeline(
        SimpleImputer(strategy="most_frequent"),
        StandardScaler(),
        KNeighborsClassifier(n_neighbors=7),
    )
    model.fit(x_train, y_train)

    predictions = model.predict(x_test)
    print(f"Holdout accuracy: {accuracy_score(y_test, predictions):.3f}")
    print(classification_report(y_test, predictions, zero_division=0))

    joblib.dump(model, MODEL_PATH)
    print(f"Saved model to {MODEL_PATH}")


if __name__ == "__main__":
    build_model()
