import plotly.graph_objects as go
import streamlit as st


def sensor_chart(df, column, title, color):

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=df["time_stamp"],
            y=df[column],
            mode="lines",
            line=dict(
                color=color,
                width=3,
            ),
        )
    )

    fig.update_layout(

        title=title,

        height=280,

        margin=dict(
            l=20,
            r=20,
            t=40,
            b=20,
        ),

        xaxis_title="",

        yaxis_title="",

        template="plotly_white",

        showlegend=False,
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
    )