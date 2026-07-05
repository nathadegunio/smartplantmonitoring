import streamlit as st


def show_plant_information():

    with st.container(border=True):

        st.subheader("🌶️ Plant Information")

        c1, c2 = st.columns(2)

        with c1:
            st.metric(
                "Plant",
                "Sili"
            )

        with c2:
            st.metric(
                "Location",
                "Outdoor Yard"
            )