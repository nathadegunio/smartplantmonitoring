import streamlit as st


def show_plant(status):
    """
    Display the plant status using large emojis.
    """

    emoji = "🌿"
    title = "Your chilli plant looks healthy!"
    color = "green"

    if status == "dry":
        emoji = "🥀"
        title = "I'm thirsty!"
        color = "orange"

    elif status == "hot":
        emoji = "🥵"
        title = "It's too hot!"
        color = "red"

    elif status == "dark":
        emoji = "🌑"
        title = "I need more sunlight!"
        color = "goldenrod"

    elif status == "offline":
        emoji = "📡"
        title = "Sensor is offline"
        color = "gray"

    st.markdown(
        f"""
        <div style="
            text-align:center;
            padding:20px;
            border-radius:18px;
            background-color:#F8F9FA;
            border:1px solid #E0E0E0;
            margin-bottom:10px;
        ">
            <div style="font-size:90px;">
                {emoji}
            </div>

            <div style="
                font-size:24px;
                font-weight:bold;
                color:{color};
            ">
                {title}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


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