import pandas as pd
import numpy as np
import joblib
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OrdinalEncoder
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.model_selection import train_test_split

# --------------------------
# Custom Transformer
# --------------------------
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

# --------------------------
# Feature sets
# --------------------------
BASE_FEATURES = [
    'ORIGIN_AIRPORT', 'DESTINATION_AIRPORT', 'AIRLINE',
    'SCHEDULED_DEPARTURE', 'SCHEDULED_ARRIVAL',
    'SCHEDULED_TIME', 'DISTANCE',
    'MONTH', 'DAY', 'DAY_OF_WEEK'
]

ARRIVAL_FEATURES = BASE_FEATURES + ['DEPARTURE_DELAY']

categorical = ['ORIGIN_AIRPORT', 'DESTINATION_AIRPORT', 'AIRLINE']
time_cols = ['SCHEDULED_DEPARTURE', 'SCHEDULED_ARRIVAL']
numeric_base = ['SCHEDULED_TIME', 'DISTANCE', 'MONTH', 'DAY', 'DAY_OF_WEEK']
numeric_arr = numeric_base + ['DEPARTURE_DELAY']

def build_pipeline(numeric_features):
    preprocessor = ColumnTransformer([
        ('cat', OrdinalEncoder(handle_unknown='use_encoded_value', unknown_value=-1), categorical),
        ('num', 'passthrough', numeric_features),
        ('time', 'passthrough', time_cols),
    ])
    
    model = HistGradientBoostingRegressor(
        max_iter=200,
        learning_rate=0.08,
        max_depth=10,
        min_samples_leaf=20,
        random_state=42
    )
    
    return Pipeline([
        ('time', TimeToMinutes(time_cols)),
        ('prep', preprocessor),
        ('model', model)
    ])

# --------------------------
# Load & prepare data
# --------------------------
# df = pd.read_csv("flights.csv")  # ← uncomment and set your path

X_base = df[BASE_FEATURES]
y_dep = df['DEPARTURE_DELAY']
y_arr = df['ARRIVAL_DELAY']

X_train, X_test, y_dep_train, y_dep_test, y_arr_train, y_arr_test = train_test_split(
    X_base, y_dep, y_arr, test_size=0.2, random_state=42
)

# Arrival data needs DEPARTURE_DELAY
X_arr_train = df.loc[X_train.index, ARRIVAL_FEATURES]
X_arr_test  = df.loc[X_test.index, ARRIVAL_FEATURES]

# --------------------------
# Train
# --------------------------
print("Training Departure Delay model...")
dep_model = build_pipeline(numeric_base)
dep_model.fit(X_train, y_dep_train)

print("Training Arrival Delay model (with DEPARTURE_DELAY)...")
arr_model = build_pipeline(numeric_arr)
arr_model.fit(X_arr_train, y_arr_train)

# --------------------------
# Quick evaluation
# --------------------------
from sklearn.metrics import mean_absolute_error, r2_score

print("\nDeparture Delay → MAE:", round(mean_absolute_error(y_dep_test, dep_model.predict(X_test)), 2))
print("Arrival Delay   → MAE:", round(mean_absolute_error(y_arr_test, arr_model.predict(X_arr_test)), 2))

# --------------------------
# Save models
# --------------------------
joblib.dump(dep_model, "departure_delay_model.joblib")
joblib.dump(arr_model, "arrival_delay_model.joblib")
print("\nModels saved successfully!")
