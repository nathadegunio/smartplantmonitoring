import streamlit as st


def sensor_card(
    title,
    value,
    unit,
    icon,
    status,
    color,
):
    """
    Display a sensor card.
    """

    with st.container(border=True):

        st.markdown(f"### {icon} {title}")

        st.markdown(
            f"""
            <h2 style="
                color:{color};
                margin-bottom:0;
            ">
                {value:.1f} {unit}
            </h2>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            f"**{status}**"
        )