import streamlit as st


def show_plant(alerts):
    """
    Display all active plant alerts.
    """

    # ------------------------
    # Offline
    # ------------------------

    if alerts == ["offline"]:

        st.markdown("# 📡")

        st.error("Device Offline")

        return

    # ------------------------
    # Healthy
    # ------------------------

    if alerts == ["happy"]:

        st.markdown("# 🌶️🌿")

        st.success("Your chilli plant is healthy!")

        return

    # ------------------------
    # Multiple Alerts
    # ------------------------

    st.markdown("# 🌶️")

    st.subheader("Current Plant Status")

    for alert in alerts:

        if alert == "hot":
            st.error("🥵 Temperature is too high.")

        elif alert == "cold":
            st.warning("🥶 Temperature is too low.")

        elif alert == "dry":
            st.warning("🥀 Soil moisture is too low. Water the plant.")

        elif alert == "wet":
            st.info("💦 Soil is too wet.")

        elif alert == "dark":
            st.warning("🌑 Light intensity is too low.")

        elif alert == "low_humidity":
            st.warning("💨 Air humidity is too low.")

        elif alert == "high_humidity":
            st.info("🌫️ Air humidity is too high.")

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