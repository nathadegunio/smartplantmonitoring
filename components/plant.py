import streamlit as st


def show_plant(status):

    image = "assets/plant_happy.png"

    if status == "dry":

        image = "assets/plant_thirsty.png"

    elif status == "hot":

        image = "assets/plant_hot.png"

    elif status == "dark":

        image = "assets/plant_dark.png"

    elif status == "offline":

        image = "assets/plant_offline.png"

    st.image(
        image,
        use_container_width=True,
    )