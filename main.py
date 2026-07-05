import streamlit as st
from streamlit_autorefresh import st_autorefresh

# ------------------------------------
# Services
# ------------------------------------

from services.database import (
    get_latest_record,
    get_last_n_records,
)

from services.health import (
    calculate_health,
    device_online,
    get_plant_state,
)

from services.analytics import sensor_statistics

# ------------------------------------
# Components
# ------------------------------------

from components.header import show_header
from components.plant import show_plant
from components.plant_info import show_plant_information
from components.health import show_health
from components.sensor_grid import show_sensor_grid
from components.advice import show_advice
from components.trends import show_trends
from components.history import show_history
from components.stat_card import stat_card

# ------------------------------------
# PAGE CONFIG
# ------------------------------------

st.set_page_config(
    page_title="🌱 Smart Plant Monitor",
    page_icon="🌱",
    layout="centered",
)

# ------------------------------------
# AUTO REFRESH
# ------------------------------------

st_autorefresh(
    interval=60000,
    key="refresh",
)

# ------------------------------------
# LOAD DATA
# ------------------------------------

latest = get_latest_record()

if latest is None:
    st.error("No sensor data available.")
    st.stop()

history = get_last_n_records(1440)

# ------------------------------------
# CALCULATIONS
# ------------------------------------

online = device_online(
    latest["time_stamp"]
)

health = calculate_health(
    latest["temperature_c"],
    latest["humidity"],
    latest["soil_moisture"],
    latest["light_intensity"],
)

plant_state = get_plant_state(
    latest["temperature_c"],
    latest["soil_moisture"],
    latest["light_intensity"],
    online,
)


# ------------------------------------
# HEADER
# ------------------------------------

show_header(
    online,
    health,
    latest["time_stamp"],
)

# ------------------------------------
# PLANT IMAGE
# ------------------------------------

show_plant(plant_state)

st.divider()

# ------------------------------------
# PLANT INFORMATION
# ------------------------------------

show_plant_information()

# ------------------------------------
# HEALTH
# ------------------------------------

show_health(health)

# ------------------------------------
# CURRENT CONDITIONS
# ------------------------------------

show_sensor_grid(latest)

# ------------------------------------
# PLANT ADVICE
# ------------------------------------

show_advice(latest)

# ------------------------------------
# SENSOR TRENDS
# ------------------------------------

show_trends(history)

# ------------------------------------
# TODAY'S SUMMARY
# ------------------------------------

st.subheader("📊 Today's Summary")

temp = sensor_statistics(history, "temperature_c")
humid = sensor_statistics(history, "humidity")
soil = sensor_statistics(history, "soil_moisture")
light = sensor_statistics(history, "light_intensity")

col1, col2 = st.columns(2)

with col1:
    stat_card(
        "🌡",
        "Temperature",
        "°C",
        temp,
    )

with col2:
    stat_card(
        "💧",
        "Humidity",
        "%",
        humid,
    )

col3, col4 = st.columns(2)

with col3:
    stat_card(
        "🌱",
        "Soil Moisture",
        "%",
        soil,
    )

with col4:
    stat_card(
        "☀",
        "Light",
        "Lux",
        light,
    )

st.divider()

# ------------------------------------
# HISTORY
# ------------------------------------

show_history(history)