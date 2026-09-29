import pandas as pd
import joblib
from sklearn.base import BaseEstimator, TransformerMixin

# ============================================================
# IMPORTANT: Define the custom class BEFORE loading the models
# ============================================================
class TimeToMinutes(BaseEstimator, TransformerMixin):
    def __init__(self, columns):
        self.columns = columns

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        X = X.copy()
        for col in self.columns:
            X[col] = (X[col] // 100) * 60 + (X[col] % 100)
        return X


# Now load the models (class is already defined)
dep_model = joblib.load("departure_delay_model.joblib")
arr_model = joblib.load("arrival_delay_model.joblib")


def predict_delays(data: dict) -> dict:
    df = pd.DataFrame([data])

    base_cols = [
        'ORIGIN_AIRPORT', 'DESTINATION_AIRPORT', 'AIRLINE',
        'SCHEDULED_DEPARTURE', 'SCHEDULED_ARRIVAL',
        'SCHEDULED_TIME', 'DISTANCE',
        'MONTH', 'DAY', 'DAY_OF_WEEK'
    ]

    # Predict Departure Delay
    dep_pred = float(dep_model.predict(df[base_cols])[0])

    # Predict Arrival Delay
    if data.get("DEPARTURE_DELAY") is not None:
        df["DEPARTURE_DELAY"] = data["DEPARTURE_DELAY"]
    else:
        df["DEPARTURE_DELAY"] = dep_pred

    arr_cols = base_cols + ["DEPARTURE_DELAY"]
    arr_pred = float(arr_model.predict(df[arr_cols])[0])

    return {
        "departure_delay": round(dep_pred, 1),
        "arrival_delay": round(arr_pred, 1),
        "departure_status": "Delayed" if dep_pred > 15 else "On-time",
        "arrival_status": "Delayed" if arr_pred > 15 else "On-time"
    }
