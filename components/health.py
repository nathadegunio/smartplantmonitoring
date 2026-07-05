import streamlit as st


def show_health(score):

    st.subheader("❤️ Plant Health")

    st.progress(score / 100)

    st.metric(
        "Overall Health",
        f"{score}%"
    )

    if score >= 90:

        st.success("Excellent")

    elif score >= 70:

        st.warning("Good")

    else:

        st.error("Needs Attention")

    st.divider()