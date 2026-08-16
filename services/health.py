from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

MANILA = ZoneInfo("Asia/Manila")


# ----------------------------------------------------
# Temperature
# Ideal: 24–32°C
# ----------------------------------------------------
def get_temperature_status(v):

    if v < 24:
        return "Cold", "#2196F3", 10

    if v <= 32:
        return "Ideal", "#2E7D32", 25

    return "Hot", "#D32F2F", 10


# ----------------------------------------------------
# Humidity
# Ideal: 50–70%
# ----------------------------------------------------
def get_humidity_status(v):

    if v < 50:
        return "Low Humidity", "#FB8C00", 10

    if v <= 70:
        return "Ideal", "#2E7D32", 25

    return "High Humidity", "#039BE5", 10


# ----------------------------------------------------
# Soil Moisture
# Ideal: 40–70%
# ----------------------------------------------------
def get_soil_status(v):

    if v < 40:
        return "Dry", "#D32F2F", 10

    if v <= 70:
        return "Moist", "#2E7D32", 25

    return "Wet", "#039BE5", 10


# ----------------------------------------------------
# Light Intensity
# Ideal: 10,000–50,000 Lux
# ----------------------------------------------------
def get_light_status(v):

    if v < 10000:
        return "Low Light", "#FB8C00", 10

    if v <= 50000:
        return "Ideal", "#2E7D32", 25

    return "Very Bright", "#FDD835", 10


# ----------------------------------------------------
# Overall Plant Health
# Maximum = 100%
# ----------------------------------------------------
def calculate_health(temp, hum, soil, light):

    total = (
        get_temperature_status(temp)[2]
        + get_humidity_status(hum)[2]
        + get_soil_status(soil)[2]
        + get_light_status(light)[2]
    )

    return total


# ----------------------------------------------------
# Active Plant Alerts
# ----------------------------------------------------
def get_plant_alerts(temp, humidity, soil, light, online):

    if not online:
        return ["offline"]

    alerts = []

    # Temperature
    if temp < 24:
        alerts.append("cold")
    elif temp > 32:
        alerts.append("hot")

    # Humidity
    if humidity < 50:
        alerts.append("low_humidity")
    elif humidity > 70:
        alerts.append("high_humidity")

    # Soil Moisture
    if soil < 40:
        alerts.append("dry")
    elif soil > 70:
        alerts.append("wet")

    # Light
    if light < 10000:
        alerts.append("low_light")
    elif light > 50000:
        alerts.append("high_light")

    if len(alerts) == 0:
        alerts.append("happy")

    return alerts


# ----------------------------------------------------
# Device Online Checker
# ----------------------------------------------------
def device_online(timestamp):

    if timestamp is None:
        return False

    if isinstance(timestamp, str):
        timestamp = datetime.fromisoformat(
            timestamp.replace("Z", "+00:00")
        )

    if timestamp.tzinfo is None:
        timestamp = timestamp.replace(
            tzinfo=ZoneInfo("UTC")
        )

    latest = timestamp.astimezone(MANILA)

    now = datetime.now(MANILA)

    # Sensors upload every 30 minutes, so allow some buffer above that
    # before flagging the device offline.
    return (now - latest) <= timedelta(minutes=40)


# ----------------------------------------------------
# Plant Care Recommendations
# ----------------------------------------------------
def plant_advice(temp, humidity, soil, light):

    advice = []

    # Temperature
    if temp < 24:
        advice.append(
            "🥶 Temperature is below the ideal range. Move the plant to a warmer location or protect it from cold conditions."
        )

    elif temp > 32:
        advice.append(
            "🥵 Temperature is above the ideal range. Provide shade and increase watering frequency if necessary."
        )

    # Humidity
    if humidity < 50:
        advice.append(
            "💨 Humidity is low. Increase humidity by misting the plant or placing nearby water sources."
        )

    elif humidity > 70:
        advice.append(
            "🌫️ Humidity is high. Improve air circulation to reduce fungal disease risk."
        )

    # Soil
    if soil < 40:
        advice.append(
            "🥀 Soil moisture is low. Water the plant soon."
        )

    elif soil > 70:
        advice.append(
            "💦 Soil moisture is high. Delay watering to avoid root rot."
        )

    # Light
    if light < 10000:
        advice.append(
            "🌑 Light intensity is too low. Move the plant to a brighter location or provide supplemental lighting."
        )

    elif light > 50000:
        advice.append(
            "☀️ Light intensity is very high. Monitor for heat stress and provide shade during peak afternoon sunlight."
        )

    if len(advice) == 0:
        advice.append(
            "🌱 All environmental conditions are within the recommended range for healthy chilli plant growth."
        )

    return advice