import streamlit as st

from services.storage import upload_plant_image, get_latest_plant_image
from services.ai_insights import generate_plant_insight
from services.health import plant_advice
from services.analytics import sensor_statistics
from utils.helpers import format_timestamp

HISTORY_COLUMNS = (
    "temperature_c",
    "humidity",
    "soil_moisture",
    "light_intensity",
)


@st.cache_data(ttl=86400, show_spinner=False)
def _cached_insight(
    sensor_timestamp_key,
    photo_timestamp_key,
    sensor_data,
    plant_alerts,
    sensor_timestamp_ph,
    photo_timestamp_ph,
    image_bytes,
    history_stats,
):
    """
    Cached on (sensor timestamp, photo timestamp) — a fresh Gemini call
    only happens when either the sensor reading or the photo actually
    changes, not on every autorefresh.
    """

    insight = generate_plant_insight(
        sensor_data,
        plant_alerts,
        sensor_timestamp_ph,
        photo_timestamp_ph,
        image_bytes,
        history_stats,
    )

    if insight:
        return insight, True

    fallback = " ".join(
        plant_advice(
            sensor_data["temperature_c"],
            sensor_data["humidity"],
            sensor_data["soil_moisture"],
            sensor_data["light_intensity"],
        )
    )

    return fallback, False


def show_insight(latest, plant_alerts, history):

    st.subheader("🤖 AI Plant Insight")

    with st.container(border=True):

        photo = st.camera_input("📷 Capture a new photo of your plant")

        if photo is not None:
            photo_id = getattr(photo, "file_id", None)

            if photo_id != st.session_state.get("uploaded_photo_id"):
                if upload_plant_image(photo.getvalue()):
                    st.session_state["uploaded_photo_id"] = photo_id
                else:
                    st.warning(
                        "Photo captured, but uploading it to Supabase failed. "
                        "Check your connection and try again."
                    )

        image_bytes, captured_at_utc = get_latest_plant_image()

        photo_timestamp_ph = (
            format_timestamp(captured_at_utc) if captured_at_utc else None
        )

        if image_bytes:
            caption = (
                f"📷 Photo captured: {photo_timestamp_ph}"
                if photo_timestamp_ph
                else None
            )
            st.image(image_bytes, caption=caption, use_container_width=True)
        else:
            st.caption("No plant photo yet — use the camera above to capture one.")

        sensor_timestamp_ph = format_timestamp(latest["time_stamp"])

        st.caption(
            f"📊 Sensor reading: {sensor_timestamp_ph} — "
            f"🌡 {latest['temperature_c']:.1f}°C  "
            f"💧 {latest['humidity']:.1f}%  "
            f"🌱 {latest['soil_moisture']:.1f}%  "
            f"☀ {latest['light_intensity']:.0f} lux"
        )

        history_stats = {
            column: sensor_statistics(history, column)
            for column in HISTORY_COLUMNS
        }

        text, from_ai = _cached_insight(
            str(latest["time_stamp"]),
            str(captured_at_utc),
            {
                "temperature_c": latest["temperature_c"],
                "humidity": latest["humidity"],
                "soil_moisture": latest["soil_moisture"],
                "light_intensity": latest["light_intensity"],
            },
            plant_alerts,
            sensor_timestamp_ph,
            photo_timestamp_ph,
            image_bytes,
            history_stats,
        )

        st.write(text)

        if not from_ai:
            st.caption("Rule-based summary (AI insight unavailable right now).")

    st.divider()
