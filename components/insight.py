import streamlit as st

from services.storage import fetch_latest_plant_image_bytes
from services.ai_insights import generate_plant_insight
from services.health import plant_advice


@st.cache_data(ttl=1800, show_spinner=False)
def _cached_insight(timestamp_key, sensor_data, plant_alerts):

    image_bytes = fetch_latest_plant_image_bytes(timestamp_key)

    insight = generate_plant_insight(
        sensor_data,
        plant_alerts,
        image_bytes,
    )

    if insight:
        return image_bytes, insight, True

    fallback = " ".join(
        plant_advice(
            sensor_data["temperature_c"],
            sensor_data["humidity"],
            sensor_data["soil_moisture"],
            sensor_data["light_intensity"],
        )
    )

    return image_bytes, fallback, False


def show_insight(latest, plant_alerts):

    st.subheader("🤖 AI Plant Insight")

    with st.container(border=True):

        image_bytes, text, from_ai = _cached_insight(
            str(latest["time_stamp"]),
            {
                "temperature_c": latest["temperature_c"],
                "humidity": latest["humidity"],
                "soil_moisture": latest["soil_moisture"],
                "light_intensity": latest["light_intensity"],
            },
            plant_alerts,
        )

        if image_bytes:
            st.image(image_bytes, use_container_width=True)
        else:
            st.caption("📷 No camera photo available yet.")

        st.write(text)

        if not from_ai:
            st.caption("Rule-based summary (AI insight unavailable right now).")

    st.divider()
