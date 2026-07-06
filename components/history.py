import streamlit as st

from utils.helpers import to_manila


def show_history(history):

    st.subheader("📋 Last 30 Days Sensor Readings")

    table = history.copy()

    table = (
        table
        .sort_values(
            "time_stamp",
            ascending=False,
        )
        .head(43200)
    )

    table["time_stamp"] = (
        table["time_stamp"]
        .apply(to_manila)
    )

    table["time_stamp"] = (
        table["time_stamp"]
        .dt.strftime("%b %d, %Y %I:%M:%S %p")
    )

    table = table[
        [
            "time_stamp",
            "temperature_c",
            "humidity",
            "soil_moisture",
            "light_intensity",
        ]
    ]

    table.columns = [
        "Time",
        "🌡 Temperature (°C)",
        "💧 Humidity (%)",
        "🌱 Soil (%)",
        "☀ Light (Lux)",
    ]

    st.dataframe(
        table,
        use_container_width=True,
        hide_index=True,
    )

    csv = table.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        "📥 Download Recent Readings",
        csv,
        "recent_readings.csv",
        "text/csv",
        use_container_width=True,
    )

    st.divider()

# import streamlit as st


# def show_history(history):
#     """
#     Display the latest sensor readings
#     and allow CSV download.
#     """

#     st.subheader("📋 Last 30 Days Sensor Readings")

#     table = history.copy()

#     table = (
#         table
#         .sort_values(
#             "time_stamp",
#             ascending=False,
#         )
#         .head(43200)
#     )

#     table = table[
#         [
#             "time_stamp",
#             "temperature_c",
#             "humidity",
#             "soil_moisture",
#             "light_intensity",
#         ]
#     ]

#     table.columns = [
#         "Time",
#         "🌡 Temperature (°C)",
#         "💧 Humidity (%)",
#         "🌱 Soil (%)",
#         "☀ Light (Lux)",
#     ]

#     table["Time"] = (
#     table["Time"]
#     .pipe(lambda s: __import__("pandas").to_datetime(s, errors="coerce"))
#     .dt.strftime("%b %d, %Y %I:%M:%S %p")
# )

#     st.dataframe(
#         table,
#         use_container_width=True,
#         hide_index=True,
#     )

#     csv = table.to_csv(
#         index=False
#     ).encode("utf-8")

#     st.download_button(
#         label="📥 Download Recent Readings",
#         data=csv,
#         file_name="recent_readings.csv",
#         mime="text/csv",
#         use_container_width=True,
#     )

#     st.divider()