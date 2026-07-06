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

    return (now - latest) <= timedelta(minutes=10)


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

# from datetime import datetime, timedelta, timezone
# from zoneinfo import ZoneInfo

# MANILA = ZoneInfo("Asia/Manila")


# def get_temperature_status(v):

#     if v < 20:
#         return "Too Cold", "#2196F3", 10

#     if v <= 32:
#         return "Ideal", "#2E7D32", 25

#     return "Too Hot", "#D32F2F", 10


# def get_humidity_status(v):

#     if v < 50:
#         return "Dry", "#FB8C00", 20

#     if v <= 80:
#         return "Good", "#2E7D32", 25

#     return "Too Humid", "#039BE5", 20


# def get_soil_status(v):

#     if v < 30:
#         return "Needs Water", "#D32F2F", 15

#     if v <= 70:
#         return "Moist", "#2E7D32", 30

#     return "Too Wet", "#039BE5", 15


# def get_light_status(v):

#     if v < 50:
#         return "Low Light", "#FB8C00", 10

#     if v <= 500:
#         return "Good", "#2E7D32", 20

#     return "Very Bright", "#FDD835", 10


# def calculate_health(temp, hum, soil, light):

#     total = 0

#     total += get_temperature_status(temp)[2]
#     total += get_humidity_status(hum)[2]
#     total += get_soil_status(soil)[2]
#     total += get_light_status(light)[2]

#     return total



# def get_plant_alerts(temp, humidity, soil, light, online):
#     """
#     Returns all current plant alerts based on
#     chilli pepper environmental requirements.
#     """

#     # Device offline takes highest priority
#     if not online:
#         return ["offline"]

#     alerts = []

#     # ----------------------------
#     # Temperature
#     # Ideal: 24–32°C
#     # ----------------------------

#     if temp < 24:
#         alerts.append("cold")

#     elif temp > 32:
#         alerts.append("hot")

#     # ----------------------------
#     # Humidity
#     # Ideal: 50–70%
#     # ----------------------------

#     if humidity < 50:
#         alerts.append("low_humidity")

#     elif humidity > 70:
#         alerts.append("high_humidity")

#     # ----------------------------
#     # Soil Moisture
#     # Ideal: 40–70%
#     # ----------------------------

#     if soil < 40:
#         alerts.append("dry")

#     elif soil > 70:
#         alerts.append("wet")

#     # ----------------------------
#     # Light Intensity
#     # Ideal: 10,000–50,000 Lux
#     # ----------------------------

#     if light < 10000:
#         alerts.append("low_light")

#     elif light > 50000:
#         alerts.append("high_light")

#     # ----------------------------
#     # Healthy
#     # ----------------------------

#     if len(alerts) == 0:
#         alerts.append("happy")

#     return alerts

# # def get_plant_state(temp, soil, light, online):

# #     if not online:
# #         return "offline"

# #     if soil < 30:
# #         return "dry"

# #     if temp > 32:
# #         return "hot"

# #     if light < 50:
# #         return "dark"

# #     return "happy"



# def device_online(timestamp):
#     """
#     Device is online if the latest
#     reading is within the last 10 minutes.
#     """

#     if timestamp is None:
#         return False

#     if isinstance(timestamp, str):
#         timestamp = datetime.fromisoformat(
#             timestamp.replace("Z", "+00:00")
#         )

#     if timestamp.tzinfo is None:
#         timestamp = timestamp.replace(
#             tzinfo=ZoneInfo("UTC")
#         )

#     latest = timestamp.astimezone(MANILA)

#     now = datetime.now(MANILA)

#     return (now - latest) <= timedelta(minutes=10)


# # def device_online(timestamp):
# #     """
# #     Returns True if the latest sensor reading
# #     is within the last 10 minutes.
# #     """

# #     if timestamp is None:
# #         return False

# #     if isinstance(timestamp, str):
# #         timestamp = datetime.fromisoformat(
# #             timestamp.replace("Z", "+00:00")
# #         )

# #     # Assume UTC if timezone missing
# #     if timestamp.tzinfo is None:
# #         timestamp = timestamp.replace(
# #             tzinfo=ZoneInfo("UTC")
# #         )

# #     # Convert both times to Philippine Time
# #     latest = timestamp.astimezone(MANILA)

# #     now = datetime.now(MANILA)

# #     elapsed = now - latest

# #     return elapsed <= timedelta(minutes=10)

# # def device_online(timestamp):
# #     """
# #     Determine whether the ESP32 is online.

# #     Device is considered online if the latest sensor
# #     reading is within the last 10 minutes.
# #     """

# #     if timestamp is None:
# #         return False

# #     # Convert string timestamp from Supabase
# #     if isinstance(timestamp, str):
# #         timestamp = datetime.fromisoformat(
# #             timestamp.replace("Z", "+00:00")
# #         )

# #     # If timestamp has no timezone, assume UTC
# #     if timestamp.tzinfo is None:
# #         timestamp = timestamp.replace(
# #             tzinfo=timezone.utc
# #         )

# #     now = datetime.now(timezone.utc)

# #     diff = (now - timestamp).total_seconds()

# #     # 10 minutes
# #     return diff <= 600



# # Plant Care Summary
# def plant_advice(temp, humidity, soil, light):

#     advice = []

#     if soil < 40:
#         advice.append("💧 Soil is getting dry. Consider watering today.")

#     if temp > 32:
#         advice.append("🌡 Temperature is high. Check if the plant needs shade.")

#     if humidity < 50:
#         advice.append("💨 Air is quite dry.")

#     if light < 1000:
#         advice.append("☀️ Light level seems low for an outdoor chili plant.")

#     if not advice:
#         advice.append("🌱 Your chili pepper is currently in good condition.")

#     return advice