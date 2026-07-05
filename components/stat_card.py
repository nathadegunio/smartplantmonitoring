import streamlit as st


def stat_card(
    emoji,
    title,
    unit,
    stats,
):

    with st.container(border=True):

        st.subheader(f"{emoji} {title}")

        st.metric(
            "Current",
            f"{stats['current']} {unit}",
        )

        c1, c2 = st.columns(2)

        with c1:
            st.caption("⬇ Lowest")
            st.write(f"**{stats['min']} {unit}**")

        with c2:
            st.caption("⬆ Highest")
            st.write(f"**{stats['max']} {unit}**")

        st.caption("Average")

        st.write(f"**{stats['avg']} {unit}**")