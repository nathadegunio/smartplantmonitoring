import base64

import requests

from utils.secrets import get_secret

# -----------------------------------------------------
# Config
# -----------------------------------------------------

GEMINI_API_KEY = get_secret("GEMINI_API_KEY")

GEMINI_MODEL = "gemini-3.1-flash-lite"

GEMINI_ENDPOINT = (
    "https://generativelanguage.googleapis.com/v1beta/interactions"
)

REQUEST_TIMEOUT = 20


# -----------------------------------------------------
# Chilli Plant AI Advisor — expert persona prompt
# -----------------------------------------------------
# This is the "skill": a fixed instruction block that frames every
# request as a chilli pepper (Capsicum annuum) cultivation expert
# reviewing one snapshot in time, so the model doesn't need any
# conversation history to give a grounded, plant-specific answer.
# -----------------------------------------------------

CHILLI_EXPERT_PROMPT = """You are an expert agronomist specializing in chilli
pepper (Capsicum annuum / Sili) cultivation in a tropical outdoor Philippine
climate. You are reviewing one snapshot from an automated monitoring station:
a photo of the plant and its current sensor readings.

Ideal ranges for this plant:
- Temperature: 24-32 C
- Humidity: 50-70%
- Soil moisture: 40-70%
- Light: 10,000-50,000 lux

The photo and the sensor reading are captured independently and may not be
from the same moment — the photo is taken manually by the plant's owner
whenever they choose, while the sensor reading comes from an automated
station reporting every few minutes. Both timestamps are given below.

Look at the photo (leaf color, wilting, posture, visible fruit/flowers, pests
or discoloration if visible) together with the sensor readings, and write a
short assessment for the plant's owner.

Rules:
- 2 to 4 short sentences, plain language, no markdown, no headers, no bullet points.
- Mention what you actually observe in the photo, not just the numbers.
- If the photo and sensor timestamps are more than about 15 minutes apart, briefly
  note that the photo may not reflect current conditions before giving your assessment.
- End with one concrete, actionable tip.
- If the photo doesn't show anything notable, focus on the sensor readings instead.
"""


def _build_sensor_context(sensor_data, plant_alerts, sensor_timestamp_ph, photo_timestamp_ph):

    lines = [
        f"Sensor reading taken at: {sensor_timestamp_ph or 'unknown'}",
        f"Temperature: {sensor_data.get('temperature_c')} C",
        f"Humidity: {sensor_data.get('humidity')}%",
        f"Soil moisture: {sensor_data.get('soil_moisture')}%",
        f"Light intensity: {sensor_data.get('light_intensity')} lux",
        f"Active alerts: {', '.join(plant_alerts) if plant_alerts else 'none'}",
        f"Photo taken at: {photo_timestamp_ph or 'no photo available'}",
    ]

    return "\n".join(lines)


def _extract_output_text(response_json):

    for step in response_json.get("steps", []):

        if step.get("type") != "model_output":
            continue

        for part in step.get("content", []):

            if part.get("type") == "text" and part.get("text"):
                return part["text"].strip()

    return None


def generate_plant_insight(
    sensor_data,
    plant_alerts,
    sensor_timestamp_ph=None,
    photo_timestamp_ph=None,
    image_bytes=None,
):
    """
    Calls Gemini (Interactions API) acting as a chilli-plant cultivation
    expert, given the latest sensor snapshot and (optionally) the latest
    camera photo — each with its own timestamp, since they're captured
    independently. Returns a short plain-text insight, or None on any
    failure so the caller can fall back to rule-based advice.
    """

    if not GEMINI_API_KEY:
        return None

    context = _build_sensor_context(
        sensor_data, plant_alerts, sensor_timestamp_ph, photo_timestamp_ph
    )

    input_parts = []

    if image_bytes:
        input_parts.append({
            "type": "image",
            "mime_type": "image/jpeg",
            "data": base64.b64encode(image_bytes).decode("ascii"),
        })

    input_parts.append({
        "type": "text",
        "text": f"{CHILLI_EXPERT_PROMPT}\n\nCurrent sensor readings:\n{context}",
    })

    payload = {
        "model": GEMINI_MODEL,
        "input": input_parts,
    }

    try:
        response = requests.post(
            GEMINI_ENDPOINT,
            headers={
                "Content-Type": "application/json",
                "x-goog-api-key": GEMINI_API_KEY,
            },
            json=payload,
            timeout=REQUEST_TIMEOUT,
        )

        if response.status_code != 200:
            return None

        return _extract_output_text(response.json())

    except requests.RequestException:
        return None
