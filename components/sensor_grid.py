import streamlit as st

from components.card import sensor_card

from services.health import (
    get_temperature_status,
    get_humidity_status,
    get_soil_status,
    get_light_status,
)


def show_sensor_grid(latest):
    """
    Display the current environmental conditions
    measured by the sensors.
    """

    st.subheader("🌡 Current Environmental Conditions")

    # -----------------------------
    # First Row
    # -----------------------------
    col1, col2 = st.columns(2)

    # Temperature
    with col1:

        status, color, _ = get_temperature_status(
            latest["temperature_c"]
        )

        sensor_card(
            title="🌡 Temperature",
            value=latest["temperature_c"],
            unit="°C",
            icon="🌡",
            status=status,
            color=color,
        )

    # Humidity
    with col2:

        status, color, _ = get_humidity_status(
            latest["humidity"]
        )

        sensor_card(
            title="💧 Humidity",
            value=latest["humidity"],
            unit="%",
            icon="💧",
            status=status,
            color=color,
        )

    # -----------------------------
    # Second Row
    # -----------------------------
    col3, col4 = st.columns(2)

    # Soil Moisture
    with col3:

        status, color, _ = get_soil_status(
            latest["soil_moisture"]
        )

        sensor_card(
            title="🌱 Soil Moisture",
            value=latest["soil_moisture"],
            unit="%",
            icon="🌱",
            status=status,
            color=color,
        )

    # Light Intensity
    with col4:

        status, color, _ = get_light_status(
            latest["light_intensity"]
        )

        sensor_card(
            title="☀ Light Intensity",
            value=latest["light_intensity"],
            unit="Lux",
            icon="☀",
            status=status,
            color=color,
        )

    st.divider()
# import streamlit as st

# from components.card import sensor_card

# from services.health import (
#     get_temperature_status,
#     get_humidity_status,
#     get_soil_status,
#     get_light_status,
# )

# def show_sensor_grid(latest):
#     """
#     Display all current sensor readings.
#     """

#     st.subheader("🌡 Current Conditions")

#     col1, col2 = st.columns(2)

#     with col1:

#         status, color, _ = get_temperature_status(
#             latest["temperature_c"]
#         )

#         sensor_card(
#             "🌡 Temperature",
#             latest["temperature_c"],
#             "°C",
#             "🌡",
#             status,
#             color,
#         )

#     with col2:

#         status, color, _ = get_humidity_status(
#             latest["humidity"]
#         )

#         sensor_card(
#             "💧 Humidity",
#             latest["humidity"],
#             "%",
#             "💧",
#             status,
#             color,
#         )

#     col3, col4 = st.columns(2)

#     with col3:

#         status, color, _ = get_soil_status(
#             latest["soil_moisture"]
#         )

#         sensor_card(
#             "🌱 Soil Moisture",
#             latest["soil_moisture"],
#             "%",
#             "🌱",
#             status,
#             color,
#         )

#     with col4:

#         status, color, _ = get_light_status(
#             latest["light_intensity"]
#         )

#         sensor_card(
#             "☀ Light Intensity",
#             latest["light_intensity"],
#             "Lux",
#             "☀",
#             status,
#             color,
#         )

#     st.divider()