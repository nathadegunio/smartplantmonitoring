import streamlit as st

from components.charts import sensor_chart


def show_trends(history):

    st.subheader("📈 Sensor Trends")

    charts = [
        ("🌡 Temperature", "temperature_c", "#EF5350"),
        ("💧 Humidity", "humidity", "#42A5F5"),
        ("🌱 Soil Moisture", "soil_moisture", "#66BB6A"),
        ("☀ Light Intensity", "light_intensity", "#FBC02D"),
    ]

    for title, column, color in charts:

        with st.expander(
            title,
            expanded=(column == "temperature_c")
        ):

            sensor_chart(
                history,
                column,
                title,
                color,
            )

    st.divider()