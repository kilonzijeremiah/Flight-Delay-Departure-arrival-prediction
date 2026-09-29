import pandas as pd
import joblib

# Load models once
dep_model = joblib.load("departure_delay_model.joblib")
arr_model = joblib.load("arrival_delay_model.joblib")

def predict_delays(flight_data: dict) -> dict:
    """
    Predict both departure and arrival delay.
    
    Example input:
    {
        "ORIGIN_AIRPORT": "JFK",
        "DESTINATION_AIRPORT": "LAX",
        "AIRLINE": "AA",
        "SCHEDULED_DEPARTURE": 800,
        "SCHEDULED_ARRIVAL": 1130,
        "SCHEDULED_TIME": 370,
        "DISTANCE": 2475,
        "MONTH": 7,
        "DAY": 15,
        "DAY_OF_WEEK": 2,
        "DEPARTURE_DELAY": 12          # optional – if not given, arrival prediction is less accurate
    }
    """
    df = pd.DataFrame([flight_data])

    # Departure prediction (doesn't need DEPARTURE_DELAY)
    dep_features = [
        'ORIGIN_AIRPORT', 'DESTINATION_AIRPORT', 'AIRLINE',
        'SCHEDULED_DEPARTURE', 'SCHEDULED_ARRIVAL',
        'SCHEDULED_TIME', 'DISTANCE', 'MONTH', 'DAY', 'DAY_OF_WEEK'
    ]
    dep_pred = dep_model.predict(df[dep_features])[0]

    # Arrival prediction
    if 'DEPARTURE_DELAY' in flight_data:
        arr_features = dep_features + ['DEPARTURE_DELAY']
        arr_pred = arr_model.predict(df[arr_features])[0]
    else:
        # If real departure delay is unknown, use the predicted one
        df['DEPARTURE_DELAY'] = dep_pred
        arr_features = dep_features + ['DEPARTURE_DELAY']
        arr_pred = arr_model.predict(df[arr_features])[0]

    return {
        "predicted_departure_delay_min": round(float(dep_pred), 1),
        "predicted_arrival_delay_min": round(float(arr_pred), 1),
        "status": {
            "departure": "Delayed" if dep_pred > 15 else "On-time",
            "arrival": "Delayed" if arr_pred > 15 else "On-time"
        }
    }

# ------- Example usage -------
if __name__ == "__main__":
    example = {
        "ORIGIN_AIRPORT": "JFK",
        "DESTINATION_AIRPORT": "LAX",
        "AIRLINE": "AA",
        "SCHEDULED_DEPARTURE": 800,
        "SCHEDULED_ARRIVAL": 1130,
        "SCHEDULED_TIME": 370,
        "DISTANCE": 2475,
        "MONTH": 7,
        "DAY": 15,
        "DAY_OF_WEEK": 2
    }
    print(predict_delays(example))
