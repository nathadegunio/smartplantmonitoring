import pandas as pd


def sensor_statistics(df, column):

    if df.empty:
        return {
            "current": 0,
            "min": 0,
            "max": 0,
            "avg": 0,
        }

    return {
        "current": round(df[column].iloc[-1], 1),
        "min": round(df[column].min(), 1),
        "max": round(df[column].max(), 1),
        "avg": round(df[column].mean(), 1),
    }