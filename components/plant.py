import streamlit as st


def show_plant(alerts):
    """
    Display the current chilli plant status.

    - Offline has highest priority.
    - Healthy displays only one message.
    - Otherwise display ALL active alerts.
    """

    # ---------------------------------
    # DEVICE OFFLINE
    # ---------------------------------

    if alerts == ["offline"]:

        st.markdown("# 📡")

        st.error("Device Offline. No recent sensor data has been received.")

        return

    # ---------------------------------
    # HEALTHY
    # ---------------------------------

    if alerts == ["happy"]:

        st.markdown("# 🌶️🌿")

        st.success(
            "Your chilli plant is growing under ideal environmental conditions."
        )

        return

    # ---------------------------------
    # MULTIPLE ALERTS
    # ---------------------------------

    st.markdown("# 🌶️")

    st.subheader("Current Plant Status")

    messages = {

        # Temperature
        "cold":
            "🥶 Temperature is too low (<24°C). Move the plant to a warmer location or protect it from cold conditions.",

        "hot":
            "🥵 Temperature is too high (>32°C). Provide shade and increase watering frequency if necessary.",

        # Humidity
        "low_humidity":
            "💨 Humidity is too low (<50%). Increase humidity by misting or placing nearby water sources.",

        "high_humidity":
            "🌫️ Humidity is too high (>70%). Improve air circulation to reduce fungal disease risk.",

        # Soil Moisture
        "dry":
            "🥀 Soil moisture is too low (<40%). Water the plant soon.",

        "wet":
            "💦 Soil moisture is too high (>70%). Delay watering to avoid root rot.",

        # Light
        "low_light":
            "🌑 Light intensity is too low (<10,000 Lux). Move the plant to a brighter location or provide supplemental lighting.",

        "high_light":
            "☀️ Light intensity is very high (>50,000 Lux). Monitor for heat stress and provide shade during peak afternoon sunlight.",
    }

    for alert in alerts:

        if alert in messages:
            st.markdown(messages[alert])

# import streamlit as st


# def show_plant(status):
#     """
#     Display the plant status using large emojis.
#     """

#     emoji = "🌿"
#     title = "Your chilli plant looks healthy!"
#     color = "green"

#     if status == "dry":
#         emoji = "🥀"
#         title = "I'm thirsty!"
#         color = "orange"

#     elif status == "hot":
#         emoji = "🥵"
#         title = "It's too hot!"
#         color = "red"

#     elif status == "dark":
#         emoji = "🌑"
#         title = "I need more sunlight!"
#         color = "goldenrod"

#     elif status == "offline":
#         emoji = "📡"
#         title = "Sensor is offline"
#         color = "gray"

#     st.markdown(
#         f"""
#         <div style="
#             text-align:center;
#             padding:20px;
#             border-radius:18px;
#             background-color:#F8F9FA;
#             border:1px solid #E0E0E0;
#             margin-bottom:10px;
#         ">
#             <div style="font-size:90px;">
#                 {emoji}
#             </div>

#             <div style="
#                 font-size:24px;
#                 font-weight:bold;
#                 color:{color};
#             ">
#                 {title}
#             </div>
#         </div>
#         """,
#         unsafe_allow_html=True,
#     )


# import streamlit as st


# def show_plant(status):

#     image = "assets/plant_happy.png"

#     if status == "dry":

#         image = "assets/plant_thirsty.png"

#     elif status == "hot":

#         image = "assets/plant_hot.png"

#     elif status == "dark":

#         image = "assets/plant_dark.png"

#     elif status == "offline":

#         image = "assets/plant_offline.png"

#     st.image(
#         image,
#         use_container_width=True,
#     )