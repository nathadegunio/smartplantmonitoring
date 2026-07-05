from datetime import datetime, timezone


def get_temperature_status(v):

    if v < 20:
        return "Too Cold", "#2196F3", 10

    if v <= 32:
        return "Ideal", "#2E7D32", 25

    return "Too Hot", "#D32F2F", 10


def get_humidity_status(v):

    if v < 50:
        return "Dry", "#FB8C00", 20

    if v <= 80:
        return "Good", "#2E7D32", 25

    return "Too Humid", "#039BE5", 20


def get_soil_status(v):

    if v < 30:
        return "Needs Water", "#D32F2F", 15

    if v <= 70:
        return "Moist", "#2E7D32", 30

    return "Too Wet", "#039BE5", 15


def get_light_status(v):

    if v < 50:
        return "Low Light", "#FB8C00", 10

    if v <= 500:
        return "Good", "#2E7D32", 20

    return "Very Bright", "#FDD835", 10


def calculate_health(temp, hum, soil, light):

    total = 0

    total += get_temperature_status(temp)[2]
    total += get_humidity_status(hum)[2]
    total += get_soil_status(soil)[2]
    total += get_light_status(light)[2]

    return total


def get_plant_state(temp, soil, light, online):

    if not online:
        return "offline"

    if soil < 30:
        return "dry"

    if temp > 32:
        return "hot"

    if light < 50:
        return "dark"

    return "happy"


def device_online(timestamp):

    dt = datetime.fromisoformat(
        timestamp.replace("Z", "+00:00")
    )

    now = datetime.now(timezone.utc)

    diff = (now - dt).total_seconds()

    return diff <= 180



# Plant Care Summary
def plant_advice(temp, humidity, soil, light):

    advice = []

    if soil < 40:
        advice.append("💧 Soil is getting dry. Consider watering today.")

    if temp > 32:
        advice.append("🌡 Temperature is high. Check if the plant needs shade.")

    if humidity < 50:
        advice.append("💨 Air is quite dry.")

    if light < 1000:
        advice.append("☀️ Light level seems low for an outdoor chili plant.")

    if not advice:
        advice.append("🌱 Your chili pepper is currently in good condition.")

    return advice