import streamlit as st
from predict import predict_delays

# Page config - using the KQ logo as icon
st.set_page_config(
    page_title="Kenya Airways Delay Predictor",
    page_icon="fDtEl.png",          # ← your logo as browser tab icon
    layout="centered"
)

# Custom styling
st.markdown("""
    <style>
    .main-title {
        font-size: 2.1rem;
        font-weight: 700;
        color: #C8102E;
        text-align: center;
        margin-bottom: 0.2rem;
        margin-top: 0.5rem;
    }
    .sub-title {
        text-align: center;
        color: #333333;
        margin-bottom: 1.5rem;
        font-size: 1.05rem;
    }
    .stButton > button {
        width: 100%;
        height: 3rem;
        font-size: 1.1rem;
        background-color: #C8102E;
        color: white;
        border: none;
    }
    .stButton > button:hover {
        background-color: #A00D24;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# ---------- LOGO ----------
col_logo = st.columns([1, 2, 1])
with col_logo[1]:
    st.image("fDtEl.png", width=160)

# Header
st.markdown('<p class="main-title">Kenya Airways Delay Predictor</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Predict Departure & Arrival Delays | Powered by Machine Learning</p>', unsafe_allow_html=True)

st.divider()

# Input Form
with st.form("prediction_form"):
    st.subheader("Flight Details")

    col1, col2 = st.columns(2)

    with col1:
        origin = st.text_input("Origin Airport *", value="NBO", placeholder="e.g. NBO")
        destination = st.text_input("Destination Airport *", value="JNB", placeholder="e.g. JNB")
        airline = st.text_input("Airline Code *", value="KQ", placeholder="e.g. KQ")
        scheduled_departure = st.number_input("Scheduled Departure (HHMM) *", min_value=0, max_value=2359, value=800)
        scheduled_arrival = st.number_input("Scheduled Arrival (HHMM) *", min_value=0, max_value=2359, value=1030)

    with col2:
        scheduled_time = st.number_input("Scheduled Duration (minutes) *", min_value=30, value=150)
        distance = st.number_input("Distance (miles) *", min_value=50, value=1800)
        month = st.selectbox("Month *", options=list(range(1, 13)), index=6)
        day = st.number_input("Day of Month *", min_value=1, max_value=31, value=15)
        day_of_week = st.selectbox(
            "Day of Week *",
            options=[1, 2, 3, 4, 5, 6, 7],
            format_func=lambda x: ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"][x-1],
            index=1
        )

    st.markdown("##### Optional")
    actual_dep_delay = st.number_input(
        "Actual Departure Delay (minutes)",
        min_value=-60,
        value=0,
        help="Leave as 0 if unknown. Providing the real departure delay improves arrival prediction accuracy."
    )

    submitted = st.form_submit_button("Predict Delays")

# ---------- VALIDATION + PREDICTION ----------
if submitted:
    errors = []

    if not origin or not origin.strip():
        errors.append("Origin Airport is required.")
    if not destination or not destination.strip():
        errors.append("Destination Airport is required.")
    if not airline or not airline.strip():
        errors.append("Airline Code is required.")

    if origin and len(origin.strip()) < 3:
        errors.append("Origin Airport code should be at least 3 characters (e.g. NBO).")
    if destination and len(destination.strip()) < 3:
        errors.append("Destination Airport code should be at least 3 characters (e.g. JNB).")

    if scheduled_departure % 100 > 59:
        errors.append("Invalid Scheduled Departure time (minutes cannot be more than 59).")
    if scheduled_arrival % 100 > 59:
        errors.append("Invalid Scheduled Arrival time (minutes cannot be more than 59).")

    if scheduled_time < 30:
        errors.append("Scheduled Duration must be at least 30 minutes.")
    if distance < 50:
        errors.append("Distance must be at least 50 miles.")

    if errors:
        for err in errors:
            st.error(err)
    else:
        input_data = {
            "ORIGIN_AIRPORT": origin.strip().upper(),
            "DESTINATION_AIRPORT": destination.strip().upper(),
            "AIRLINE": airline.strip().upper(),
            "SCHEDULED_DEPARTURE": int(scheduled_departure),
            "SCHEDULED_ARRIVAL": int(scheduled_arrival),
            "SCHEDULED_TIME": int(scheduled_time),
            "DISTANCE": int(distance),
            "MONTH": int(month),
            "DAY": int(day),
            "DAY_OF_WEEK": int(day_of_week),
        }

        if actual_dep_delay != 0:
            input_data["DEPARTURE_DELAY"] = float(actual_dep_delay)

        try:
            with st.spinner("Predicting delays..."):
                result = predict_delays(input_data)

            st.success("Prediction completed!")

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

            st.info("Note: A delay greater than 15 minutes is considered significant.")

        except Exception as e:
            st.error(f"Prediction failed: {str(e)}")

# Footer
st.divider()
st.caption("Kenya Airways Delay Prediction System • Built with Streamlit + Machine Learning")
