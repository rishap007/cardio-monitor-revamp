from pathlib import Path

import joblib
import numpy as np
import pandas as pd


BASE_DIR = Path(__file__).resolve().parent
FEATURES = [
    "age", "sex", "cp", "trestbps", "restecg", "chol", "fbs",
    "thalach", "exang", "oldpeak", "slope", "ca", "thal",
]
MODEL_PATH = BASE_DIR / "heartmodel.pkl"
_model = joblib.load(MODEL_PATH)


def preprocess(age, sex, cp, trestbps, restecg, chol, fbs, thalach,
               exang, oldpeak, slope, ca, thal):
    """Convert the form's labels to the heart.csv encoding and predict."""
    sex_values = {"male": 1, "female": 0}
    cp_values = {
        # Category codes in this CSV were remapped from the original Cleveland data.
        "typical angina": 3,
        "atypical angina": 1,
        "non-anginal pain": 2,
        "asymptomatic": 0,
    }
    yes_no = {"yes": 1, "no": 0}
    slope_values = {
        "upsloping: better heart rate with excercise(uncommon)": 0,
        "flatsloping: minimal change(typical healthy heart)": 1,
        "downsloping: signs of unhealthy heart": 2,
    }
    thal_values = {
        # This CSV uses 1=fixed, 2=normal, 3=reversible.
        "normal": 2,
        "fixed defect: used to be defect but ok now": 1,
        "reversable defect: no proper blood movement when excercising": 3,
    }
    restecg_values = {
        "nothing to note": 0,
        "st-t wave abnormality": 2,
        "possible or definite left ventricular hypertrophy": 1,
    }

    def choice(value, mapping, field):
        try:
            return mapping[str(value).strip().lower()]
        except KeyError as exc:
            raise ValueError("Please select a valid value for {}.".format(field)) from exc

    try:
        row = {
            "age": float(age),
            "sex": choice(sex, sex_values, "sex"),
            "cp": choice(cp, cp_values, "chest pain type"),
            "trestbps": float(trestbps),
            "restecg": choice(restecg, restecg_values, "resting ECG"),
            "chol": float(chol),
            "fbs": choice(fbs, yes_no, "fasting blood sugar"),
            "thalach": float(thalach),
            "exang": choice(exang, yes_no, "exercise induced angina"),
            "oldpeak": float(oldpeak),
            "slope": choice(slope, slope_values, "slope"),
            "ca": float(ca),
            "thal": choice(thal, thal_values, "thal"),
        }
    except (TypeError, ValueError) as exc:
        if isinstance(exc, ValueError) and str(exc).startswith("Please select"):
            raise
        raise ValueError("Enter a valid number for every measurement.") from exc

    values = np.asarray([row[name] for name in FEATURES], dtype=float)
    if not np.isfinite(values).all():
        raise ValueError("Measurements must be finite numbers.")
    if not 1 <= row["age"] <= 120:
        raise ValueError("Age must be between 1 and 120.")
    if not 40 <= row["trestbps"] <= 300:
        raise ValueError("Resting blood pressure must be between 40 and 300.")
    if not 50 <= row["chol"] <= 700:
        raise ValueError("Cholesterol must be between 50 and 700.")
    if not 30 <= row["thalach"] <= 250:
        raise ValueError("Maximum heart rate must be between 30 and 250.")
    if not 0 <= row["oldpeak"] <= 10:
        raise ValueError("ST depression must be between 0 and 10.")
    if not 0 <= row["ca"] <= 3 or not row["ca"].is_integer():
        raise ValueError("Number of major vessels must be an integer from 0 to 3.")

    features = pd.DataFrame([row], columns=FEATURES)
    return int(_model.predict(features)[0])
