import streamlit as st

from utils.constants import (
    APP_TITLE,
    PLANT_NAME,
    PLANT_LOCATION,
)

from utils.helpers import (
    format_timestamp,
    time_ago,
)


def show_header(
    online,
    health,
    timestamp,
):

    st.title(APP_TITLE)

    st.subheader(PLANT_NAME)

    st.caption(PLANT_LOCATION)

    st.caption(
        "ESP32 • DHT22 • BH1750 • Soil Moisture Sensor"
    )

    col1, col2 = st.columns([3, 1])

    with col1:

        if online:
            st.success("🟢 Device Online")
        else:
            st.error("🔴 Device Offline")

    with col2:

        st.metric(
            "Health",
            f"{health}%"
        )

    st.caption(
        f"🕒 Updated {time_ago(timestamp)}"
    )

    st.caption(
        format_timestamp(timestamp)
    )

    st.divider()