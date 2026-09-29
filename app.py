import streamlit as st
from predict import predict_delays

st.set_page_config(page_title="Flight Delay Predictor", page_icon="✈️")
st.title("✈️ KQ Flight Delay Prediction System")

st.markdown("Predict **Departure** and **Arrival** delays")

col1, col2 = st.columns(2)

with col1:
    origin = st.text_input("Origin Airport", "JFK")
    dest = st.text_input("Destination Airport", "LAX")
    airline = st.text_input("Airline Code", "AA")
    dep_time = st.number_input("Scheduled Departure (HHMM)", 800)
    arr_time = st.number_input("Scheduled Arrival (HHMM)", 1130)

with col2:
    sched_time = st.number_input("Scheduled Time (minutes)", 370)
    distance = st.number_input("Distance (miles)", 2475)
    month = st.slider("Month", 1, 12, 7)
    day = st.slider("Day", 1, 31, 15)
    dow = st.slider("Day of Week (1=Mon)", 1, 7, 2)
    real_dep_delay = st.number_input("Actual Departure Delay (optional)", value=0)

if st.button("Predict Delays", type="primary"):
    data = {
        "ORIGIN_AIRPORT": origin.upper(),
        "DESTINATION_AIRPORT": dest.upper(),
        "AIRLINE": airline.upper(),
        "SCHEDULED_DEPARTURE": int(dep_time),
        "SCHEDULED_ARRIVAL": int(arr_time),
        "SCHEDULED_TIME": int(sched_time),
        "DISTANCE": int(distance),
        "MONTH": int(month),
        "DAY": int(day),
        "DAY_OF_WEEK": int(dow),
    }
    if real_dep_delay != 0:
        data["DEPARTURE_DELAY"] = real_dep_delay

    result = predict_delays(data)

    st.success("Prediction Complete")
    st.metric("Predicted Departure Delay", f"{result['predicted_departure_delay_min']} min", result['status']['departure'])
    st.metric("Predicted Arrival Delay", f"{result['predicted_arrival_delay_min']} min", result['status']['arrival'])
