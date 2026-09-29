import streamlit as st
from predict import predict_delays

# Page config
st.set_page_config(
    page_title="KQ Flight Delay Predictor",
    page_icon="✈️",
    layout="centered"
)

# Custom CSS
st.markdown("""
    <style>
    .main-title {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1E3A5F;
        text-align: center;
    }
    .sub-title {
        text-align: center;
        color: #5A6A7A;
        margin-bottom: 2rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #1E88E5;
        color: white;
        height: 3rem;
        font-size: 1.1rem;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown('<p class="main-title">✈️ Flight Delay Predictor</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Predict Departure & Arrival Delays using Machine Learning</p>', unsafe_allow_html=True)

st.divider()

# Input Form
with st.form("flight_form"):
    st.subheader("Flight Details")

    col1, col2 = st.columns(2)

    with col1:
        origin = st.text_input("Origin Airport (e.g. JFK)", value="JFK")
        dest = st.text_input("Destination Airport (e.g. LAX)", value="LAX")
        airline = st.text_input("Airline Code (e.g. AA)", value="AA")
        dep_time = st.number_input("Scheduled Departure (HHMM)", min_value=0, max_value=2359, value=800)
        arr_time = st.number_input("Scheduled Arrival (HHMM)", min_value=0, max_value=2359, value=1130)

    with col2:
        sched_time = st.number_input("Scheduled Duration (minutes)", min_value=30, value=370)
        distance = st.number_input("Distance (miles)", min_value=50, value=2475)
        month = st.selectbox("Month", options=list(range(1, 13)), index=6)
        day = st.number_input("Day of Month", min_value=1, max_value=31, value=15)
        dow = st.selectbox("Day of Week", 
                           options=[1,2,3,4,5,6,7],
                           format_func=lambda x: ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"][x-1],
                           index=1)

    st.markdown("#### Optional")
    real_dep_delay = st.number_input(
        "Actual Departure Delay (minutes) — leave 0 if unknown",
        min_value=-50,
        value=0,
        help="If you already know the departure delay, enter it for a more accurate arrival prediction."
    )

    submitted = st.form_submit_button("Predict Delays")

# Prediction
if submitted:
    with st.spinner("Predicting..."):
        input_data = {
            "ORIGIN_AIRPORT": origin.strip().upper(),
            "DESTINATION_AIRPORT": dest.strip().upper(),
            "AIRLINE": airline.strip().upper(),
            "SCHEDULED_DEPARTURE": int(dep_time),
            "SCHEDULED_ARRIVAL": int(arr_time),
            "SCHEDULED_TIME": int(sched_time),
            "DISTANCE": int(distance),
            "MONTH": int(month),
            "DAY": int(day),
            "DAY_OF_WEEK": int(dow),
        }

        if real_dep_delay != 0:
            input_data["DEPARTURE_DELAY"] = float(real_dep_delay)

        try:
            result = predict_delays(input_data)

            st.success("Prediction Completed!")

            # Results
            col_a, col_b = st.columns(2)

            with col_a:
                st.metric(
                    label="Departure Delay",
                    value=f"{result['departure_delay']} min",
                    delta=result['departure_status'],
                    delta_color="inverse"
                )

            with col_b:
                st.metric(
                    label="Arrival Delay",
                    value=f"{result['arrival_delay']} min",
                    delta=result['arrival_status'],
                    delta_color="inverse"
                )

            st.info("Note: Delays > 15 minutes are considered significant.")

        except Exception as e:
            st.error(f"Something went wrong: {e}")

# Footer
st.divider()
st.caption("Built with Machine Learning • HistGradientBoosting • Streamlit")
