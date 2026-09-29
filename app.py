import streamlit as st
from predict import predict_delays


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Kenya Airways Delay Predictor",
    page_icon="fDtEl.png",
    layout="centered"
)


# ============================================================
# CUSTOM CSS
# ============================================================

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
        border-radius: 8px;
    }

    .stButton > button:hover {
        background-color: #A00D24;
        color: white;
    }

    .prediction-card {
        padding: 1rem;
        border-radius: 10px;
        border: 1px solid #dddddd;
        margin-top: 1rem;
    }

    </style>
""", unsafe_allow_html=True)


# ============================================================
# KENYA AIRWAYS AIRPORTS
# ============================================================

KENYA_AIRWAYS_AIRPORTS = {
    "Nairobi – Jomo Kenyatta International Airport (NBO)": "NBO",
    "Mombasa – Moi International Airport (MBA)": "MBA",
    "Kisumu – Kisumu International Airport (KIS)": "KIS",
    "Malindi – Malindi International Airport (MYD)": "MYD",
    "Eldoret – Eldoret International Airport (EDL)": "EDL",

    "Johannesburg – O.R. Tambo International Airport (JNB)": "JNB",
    "Cape Town – Cape Town International Airport (CPT)": "CPT",

    "Dar es Salaam – Julius Nyerere International Airport (DAR)": "DAR",
    "Zanzibar – Abeid Amani Karume International Airport (ZNZ)": "ZNZ",
    "Kilimanjaro – Kilimanjaro International Airport (JRO)": "JRO",

    "Entebbe – Entebbe International Airport (EBB)": "EBB",
    "Kigali – Kigali International Airport (KGL)": "KGL",
    "Addis Ababa – Bole International Airport (ADD)": "ADD",

    "Lilongwe – Kamuzu International Airport (LLW)": "LLW",
    "Lusaka – Kenneth Kaunda International Airport (LUN)": "LUN",
    "Harare – Robert Gabriel Mugabe International Airport (HRE)": "HRE",

    "Accra – Kotoka International Airport (ACC)": "ACC",
    "Lagos – Murtala Muhammed International Airport (LOS)": "LOS",
    "Abidjan – Félix-Houphouët-Boigny International Airport (ABJ)": "ABJ",
    "Freetown – Lungi International Airport (FNA)": "FNA",
    "Monrovia – Roberts International Airport (ROB)": "ROB",

    "Kinshasa – N'Djili International Airport (FIH)": "FIH",
    "Lubumbashi – Lubumbashi International Airport (FBM)": "FBM",
    "Ndola – Simon Mwansa Kapwepwe International Airport (NLA)": "NLA",

    "Dubai – Dubai International Airport (DXB)": "DXB",
    "Paris – Charles de Gaulle Airport (CDG)": "CDG",
    "London – Heathrow Airport (LHR)": "LHR",
    "Amsterdam – Amsterdam Schiphol Airport (AMS)": "AMS",
    "New York – John F. Kennedy International Airport (JFK)": "JFK",
    "Bangkok – Suvarnabhumi Airport (BKK)": "BKK",
}


# ============================================================
# AIRLINE OPTIONS
# ============================================================

AIRLINES = {
    "Kenya Airways (KQ)": "KQ"
}


# ============================================================
# MONTHS
# ============================================================

MONTHS = {
    1: "January",
    2: "February",
    3: "March",
    4: "April",
    5: "May",
    6: "June",
    7: "July",
    8: "August",
    9: "September",
    10: "October",
    11: "November",
    12: "December"
}


# ============================================================
# DAYS OF WEEK
# ============================================================

DAYS_OF_WEEK = {
    1: "Monday",
    2: "Tuesday",
    3: "Wednesday",
    4: "Thursday",
    5: "Friday",
    6: "Saturday",
    7: "Sunday"
}


# ============================================================
# LOGO
# ============================================================

col_logo = st.columns([1, 2, 1])

with col_logo[1]:
    st.image("fDtEl.png", width=160)


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<p class="main-title">Kenya Airways Delay Predictor</p>',
    unsafe_allow_html=True
)

st.markdown(
    '<p class="sub-title">'
    'Predict Departure & Arrival Delays | Developed by Kilonzi J'
    '</p>',
    unsafe_allow_html=True
)

st.divider()


# ============================================================
# INPUT FORM
# ============================================================

with st.form("prediction_form"):

    st.subheader("✈️ Flight Details")

    col1, col2 = st.columns(2)

    # --------------------------------------------------------
    # LEFT COLUMN
    # --------------------------------------------------------

    with col1:

        # Airline
        airline_name = st.selectbox(
            "Airline *",
            options=list(AIRLINES.keys()),
            index=0
        )

        airline = AIRLINES[airline_name]

        # Origin
        airport_names = list(KENYA_AIRWAYS_AIRPORTS.keys())

        origin_name = st.selectbox(
            "Origin Airport *",
            options=airport_names,
            index=airport_names.index(
                "Nairobi – Jomo Kenyatta International Airport (NBO)"
            )
        )

        origin = KENYA_AIRWAYS_AIRPORTS[origin_name]

        # Destination
        destination_name = st.selectbox(
            "Destination Airport *",
            options=airport_names,
            index=airport_names.index(
                "Johannesburg – O.R. Tambo International Airport (JNB)"
            )
        )

        destination = KENYA_AIRWAYS_AIRPORTS[destination_name]

        # Scheduled departure
        scheduled_departure = st.number_input(
            "Scheduled Departure (HHMM) *",
            min_value=0,
            max_value=2359,
            value=800,
            step=5,
            help="Enter time using 24-hour HHMM format. Example: 0800."
        )

        # Scheduled arrival
        scheduled_arrival = st.number_input(
            "Scheduled Arrival (HHMM) *",
            min_value=0,
            max_value=2359,
            value=1030,
            step=5,
            help="Enter time using 24-hour HHMM format. Example: 1030."
        )


    # --------------------------------------------------------
    # RIGHT COLUMN
    # --------------------------------------------------------

    with col2:

        # Scheduled duration
        scheduled_time = st.number_input(
            "Scheduled Duration (minutes) *",
            min_value=30,
            value=150,
            step=5
        )

        # Distance
        distance = st.number_input(
            "Distance (miles) *",
            min_value=50,
            value=1800,
            step=10
        )

        # Month
        month_name = st.selectbox(
            "Month *",
            options=list(MONTHS.values()),
            index=6
        )

        # Convert month name back to number
        month = list(MONTHS.keys())[
            list(MONTHS.values()).index(month_name)
        ]

        # Day of month
        day = st.number_input(
            "Day of Month *",
            min_value=1,
            max_value=31,
            value=15,
            step=1
        )

        # Day of week
        day_name = st.selectbox(
            "Day of Week *",
            options=list(DAYS_OF_WEEK.values()),
            index=1
        )

        # Convert day name to number
        day_of_week = list(DAYS_OF_WEEK.keys())[
            list(DAYS_OF_WEEK.values()).index(day_name)
        ]


    # ========================================================
    # OPTIONAL INPUT
    # ========================================================

    st.markdown("##### Optional")

    actual_dep_delay = st.number_input(
        "Actual Departure Delay (minutes)",
        min_value=-60,
        value=0,
        step=1,
        help=(
            "Leave as 0 if unknown. Providing the actual departure "
            "delay can improve arrival prediction."
        )
    )


    # ========================================================
    # SUBMIT BUTTON
    # ========================================================

    submitted = st.form_submit_button(
        "🔮 Predict Delays"
    )


# ============================================================
# VALIDATION + PREDICTION
# ============================================================

if submitted:

    errors = []


    # --------------------------------------------------------
    # VALIDATE ORIGIN / DESTINATION
    # --------------------------------------------------------

    if origin == destination:

        errors.append(
            "Origin and destination airports cannot be the same."
        )


    # --------------------------------------------------------
    # VALIDATE DEPARTURE TIME
    # --------------------------------------------------------

    departure_minutes = int(scheduled_departure) % 100

    if departure_minutes > 59:

        errors.append(
            "Invalid Scheduled Departure time. "
            "Minutes cannot be greater than 59."
        )


    # --------------------------------------------------------
    # VALIDATE ARRIVAL TIME
    # --------------------------------------------------------

    arrival_minutes = int(scheduled_arrival) % 100

    if arrival_minutes > 59:

        errors.append(
            "Invalid Scheduled Arrival time. "
            "Minutes cannot be greater than 59."
        )


    # --------------------------------------------------------
    # VALIDATE DURATION
    # --------------------------------------------------------

    if scheduled_time < 30:

        errors.append(
            "Scheduled Duration must be at least 30 minutes."
        )


    # --------------------------------------------------------
    # VALIDATE DISTANCE
    # --------------------------------------------------------

    if distance < 50:

        errors.append(
            "Distance must be at least 50 miles."
        )


    # ========================================================
    # DISPLAY ERRORS
    # ========================================================

    if errors:

        for error in errors:
            st.error(error)


    # ========================================================
    # RUN PREDICTION
    # ========================================================

    else:

        # ----------------------------------------------------
        # PREPARE MODEL INPUT
        # ----------------------------------------------------

        input_data = {

            "ORIGIN_AIRPORT": origin,

            "DESTINATION_AIRPORT": destination,

            "AIRLINE": airline,

            "SCHEDULED_DEPARTURE": int(
                scheduled_departure
            ),

            "SCHEDULED_ARRIVAL": int(
                scheduled_arrival
            ),

            "SCHEDULED_TIME": int(
                scheduled_time
            ),

            "DISTANCE": int(
                distance
            ),

            "MONTH": int(
                month
            ),

            "DAY": int(
                day
            ),

            "DAY_OF_WEEK": int(
                day_of_week
            )
        }


        # ----------------------------------------------------
        # OPTIONAL DEPARTURE DELAY
        # ----------------------------------------------------

        if actual_dep_delay != 0:

            input_data["DEPARTURE_DELAY"] = float(
                actual_dep_delay
            )


        # ----------------------------------------------------
        # PREDICT
        # ----------------------------------------------------

        try:

            with st.spinner(
                "✈️ Analyzing flight and predicting delays..."
            ):

                result = predict_delays(
                    input_data
                )


            # ------------------------------------------------
            # SUCCESS MESSAGE
            # ------------------------------------------------

            st.success(
                "Prediction completed successfully!"
            )


            # ------------------------------------------------
            # SHOW SELECTED FLIGHT
            # ------------------------------------------------

            st.subheader("Flight Information")

            flight_col1, flight_col2, flight_col3 = st.columns(3)

            with flight_col1:

                st.write("**Airline**")
                st.write(airline_name)

            with flight_col2:

                st.write("**Route**")
                st.write(
                    f"{origin} → {destination}"
                )

            with flight_col3:

                st.write("**Travel Day**")
                st.write(
                    f"{day_name}, {month_name} {day}"
                )


            st.divider()


            # =================================================
            # PREDICTION RESULTS
            # =================================================

            st.subheader("📊 Prediction Results")

            col_a, col_b = st.columns(2)


            # ------------------------------------------------
            # DEPARTURE RESULT
            # ------------------------------------------------

            with col_a:

                st.metric(
                    label="🛫 Departure Delay",
                    value=f"{result['departure_delay']} min",
                    delta=result["departure_status"],
                    delta_color="inverse"
                )


            # ------------------------------------------------
            # ARRIVAL RESULT
            # ------------------------------------------------

            with col_b:

                st.metric(
                    label="🛬 Arrival Delay",
                    value=f"{result['arrival_delay']} min",
                    delta=result["arrival_status"],
                    delta_color="inverse"
                )


            # ------------------------------------------------
            # INFORMATION
            # ------------------------------------------------

            st.info(
                "ℹ️ A delay greater than 15 minutes is "
                "considered significant."
            )


        # ====================================================
        # ERROR HANDLING
        # ====================================================

        except Exception as e:

            st.error(
                f"Prediction failed: {str(e)}"
            )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "Kenya Airways Delay Prediction System • "
    "Built with Streamlit + Machine Learning"
)
