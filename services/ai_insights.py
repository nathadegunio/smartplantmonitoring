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
climate. You are reviewing an automated monitoring snapshot: a photo of the
plant, its current sensor reading, and its recent historical sensor trend.

Ideal ranges for this plant:
- Temperature: 24-32 C
- Humidity: 50-70%
- Soil moisture: 40-70%
- Light: 10,000-50,000 lux

How to use each source — this distinction matters:
- The PHOTO only tells you what the plant looked like at the moment it was
  captured (leaf color, wilting, posture, visible fruit/flowers, pests or
  discoloration). Use it only to describe visual appearance — do not use it
  to judge current environmental conditions, since it may be old.
- The CURRENT sensor reading and the HISTORICAL trend are the actual basis
  for assessing environmental conditions — whether they're improving,
  worsening, or stable — and for the advice you give.

The photo and the sensor reading are captured independently and may not be
from the same moment — the photo is taken manually by the plant's owner
whenever they choose, while the sensor reading comes from an automated
station reporting every 5 minutes. Both timestamps are given below.

Write a short assessment for the plant's owner.

Rules:
- 3 to 5 short sentences, plain language, no markdown, no headers, no bullet points.
- Start with what the photo visually shows (or say no photo is available).
- Then assess current conditions using the sensor reading and how it compares
  to the recent historical trend (e.g. drying out, stable, improving).
- If the photo and sensor timestamps are more than about 15 minutes apart, briefly
  note that the photo may not reflect current conditions.
- End with one concrete, actionable tip.
"""


def _build_sensor_context(
    sensor_data,
    plant_alerts,
    sensor_timestamp_ph,
    photo_timestamp_ph,
    history_stats,
):

    lines = [
        f"Sensor reading taken at: {sensor_timestamp_ph or 'unknown'}",
        f"Temperature: {sensor_data.get('temperature_c')} C",
        f"Humidity: {sensor_data.get('humidity')}%",
        f"Soil moisture: {sensor_data.get('soil_moisture')}%",
        f"Light intensity: {sensor_data.get('light_intensity')} lux",
        f"Active alerts: {', '.join(plant_alerts) if plant_alerts else 'none'}",
        "",
        "Recent historical sensor trend:",
    ]

    for label, unit, key in (
        ("Temperature", "C", "temperature_c"),
        ("Humidity", "%", "humidity"),
        ("Soil moisture", "%", "soil_moisture"),
        ("Light intensity", "lux", "light_intensity"),
    ):
        stats = (history_stats or {}).get(key, {})
        lines.append(
            f"{label} — min: {stats.get('min')}{unit}, "
            f"max: {stats.get('max')}{unit}, avg: {stats.get('avg')}{unit}"
        )

    lines.append("")
    lines.append(f"Photo taken at: {photo_timestamp_ph or 'no photo available'}")

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
    history_stats=None,
):
    """
    Calls Gemini (Interactions API) acting as a chilli-plant cultivation
    expert, given the latest sensor snapshot, its recent historical trend,
    and (optionally) the latest camera photo — each with its own timestamp,
    since the photo and sensor reading are captured independently. Returns
    a short plain-text insight, or None on any failure so the caller can
    fall back to rule-based advice.
    """

    if not GEMINI_API_KEY:
        return None

    context = _build_sensor_context(
        sensor_data,
        plant_alerts,
        sensor_timestamp_ph,
        photo_timestamp_ph,
        history_stats,
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
        "text": f"{CHILLI_EXPERT_PROMPT}\n\nMonitoring data:\n{context}",
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
