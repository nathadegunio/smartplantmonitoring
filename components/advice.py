import streamlit as st

from services.health import plant_advice


def show_advice(latest):

    st.subheader("💡 Plant Care Summary")

    advice = plant_advice(
        latest["temperature_c"],
        latest["humidity"],
        latest["soil_moisture"],
        latest["light_intensity"],
    )

    for item in advice:

        st.info(item)

    st.divider()