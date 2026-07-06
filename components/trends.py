import streamlit as st

from components.charts import sensor_chart
from utils.helpers import to_manila


def show_trends(history):

    st.subheader("📈 Sensor Trends")

    chart_data = history.copy()

    chart_data["time_stamp"] = (
        chart_data["time_stamp"]
        .apply(to_manila)
    )

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
                chart_data,
                column,
                title,
                color,
            )

    st.divider()

# import streamlit as st

# from components.charts import sensor_chart


# def show_trends(history):

#     st.subheader("📈 Sensor Trends")

#     charts = [
#         ("🌡 Temperature", "temperature_c", "#EF5350"),
#         ("💧 Humidity", "humidity", "#42A5F5"),
#         ("🌱 Soil Moisture", "soil_moisture", "#66BB6A"),
#         ("☀ Light Intensity", "light_intensity", "#FBC02D"),
#     ]

#     for title, column, color in charts:

#         with st.expander(
#             title,
#             expanded=(column == "temperature_c")
#         ):

#             sensor_chart(
#                 history,
#                 column,
#                 title,
#                 color,
#             )

#     st.divider()