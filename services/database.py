import os
import pandas as pd
import streamlit as st
from supabase import create_client

# -----------------------------------------------------
# Load environment variables
# -----------------------------------------------------

SUPABASE_URL = st.secrets.get(
    "SUPABASE_URL",
    os.getenv("SUPABASE_URL")
)

SUPABASE_KEY = st.secrets.get(
    "SUPABASE_KEY",
    os.getenv("SUPABASE_KEY")
)

TABLE_NAME = st.secrets.get(
    "TABLE_NAME",
    os.getenv("TABLE_NAME", "esp32_log")
)

# -----------------------------------------------------
# Safety Check
# -----------------------------------------------------

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError(
        "Missing SUPABASE_URL or SUPABASE_KEY."
    )

# -----------------------------------------------------
# Create Client
# -----------------------------------------------------

supabase = create_client(
    SUPABASE_URL,
    SUPABASE_KEY,
)

# -----------------------------------------------------
# Helper
# -----------------------------------------------------

def convert_to_ph_time(df):
    """
    Convert UTC timestamps from Supabase
    into Philippine Time.
    """

    if df.empty:
        return df

    if "time_stamp" in df.columns:

        df["time_stamp"] = (
            pd.to_datetime(
                df["time_stamp"],
                utc=True,
                errors="coerce",
            )
            .dt.tz_convert("Asia/Manila")
        )

    return df


# -----------------------------------------------------
# Latest Record
# -----------------------------------------------------

def get_latest_record():

    response = (
        supabase.table(TABLE_NAME)
        .select("*")
        .order("time_stamp", desc=True)
        .limit(1)
        .execute()
    )

    if not response.data:
        return None

    df = pd.DataFrame(response.data)

    df = convert_to_ph_time(df)

    return df.iloc[0].to_dict()


# -----------------------------------------------------
# Recent Records
# -----------------------------------------------------

def get_recent_records(limit=100):

    response = (
        supabase.table(TABLE_NAME)
        .select("*")
        .order("time_stamp", desc=True)
        .limit(limit)
        .execute()
    )

    df = pd.DataFrame(response.data)

    return convert_to_ph_time(df)


# -----------------------------------------------------
# All Records
# -----------------------------------------------------

def get_all_records():

    response = (
        supabase.table(TABLE_NAME)
        .select("*")
        .order("time_stamp", desc=True)
        .execute()
    )

    df = pd.DataFrame(response.data)

    return convert_to_ph_time(df)


# -----------------------------------------------------
# Between Dates
# -----------------------------------------------------

def get_records_between(start_date, end_date):

    response = (
        supabase.table(TABLE_NAME)
        .select("*")
        .gte("time_stamp", start_date)
        .lte("time_stamp", end_date)
        .order("time_stamp")
        .execute()
    )

    df = pd.DataFrame(response.data)

    return convert_to_ph_time(df)


# -----------------------------------------------------
# Last N Records
# -----------------------------------------------------

def get_last_n_records(limit=50):

    response = (
        supabase.table(TABLE_NAME)
        .select("*")
        .order("time_stamp", desc=True)
        .limit(limit)
        .execute()
    )

    df = pd.DataFrame(response.data)

    df = convert_to_ph_time(df)

    if not df.empty:
        df = df.sort_values(
            "time_stamp"
        )

    return df


# import os
# import pandas as pd
# import streamlit as st
# from supabase import create_client

# # -----------------------------------------------------
# # Load environment variables (LOCAL + CLOUD SAFE)
# # -----------------------------------------------------

# SUPABASE_URL = st.secrets.get("SUPABASE_URL", os.getenv("SUPABASE_URL"))
# SUPABASE_KEY = st.secrets.get("SUPABASE_KEY", os.getenv("SUPABASE_KEY"))
# TABLE_NAME = st.secrets.get("TABLE_NAME", os.getenv("TABLE_NAME", "esp32_log"))

# # -----------------------------------------------------
# # Safety check (IMPORTANT for debugging)
# # -----------------------------------------------------
# if not SUPABASE_URL or not SUPABASE_KEY:
#     raise ValueError(
#         "Missing SUPABASE_URL or SUPABASE_KEY. "
#         "Check Streamlit Secrets or .env file."
#     )

# # -----------------------------------------------------
# # Create Supabase Client
# # -----------------------------------------------------
# supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


# # -----------------------------------------------------
# # Get Latest Sensor Reading
# # -----------------------------------------------------
# def get_latest_record():
#     response = (
#         supabase.table(TABLE_NAME)
#         .select("*")
#         .order("time_stamp", desc=True)
#         .limit(1)
#         .execute()
#     )

#     return response.data[0] if response.data else None


# # -----------------------------------------------------
# # Get Recent Records
# # -----------------------------------------------------
# def get_recent_records(limit=100):
#     response = (
#         supabase.table(TABLE_NAME)
#         .select("*")
#         .order("time_stamp", desc=True)
#         .limit(limit)
#         .execute()
#     )

#     return pd.DataFrame(response.data)


# # -----------------------------------------------------
# # Get All Records
# # -----------------------------------------------------
# def get_all_records():
#     response = (
#         supabase.table(TABLE_NAME)
#         .select("*")
#         .order("time_stamp", desc=True)
#         .execute()
#     )

#     return pd.DataFrame(response.data)


# # -----------------------------------------------------
# # Get Records Between Dates
# # -----------------------------------------------------
# def get_records_between(start_date, end_date):
#     response = (
#         supabase.table(TABLE_NAME)
#         .select("*")
#         .gte("time_stamp", start_date)
#         .lte("time_stamp", end_date)
#         .order("time_stamp")
#         .execute()
#     )

#     return pd.DataFrame(response.data)


# # -----------------------------------------------------
# # Last N Records
# # -----------------------------------------------------
# def get_last_n_records(limit=50):
#     response = (
#         supabase.table(TABLE_NAME)
#         .select("*")
#         .order("time_stamp", desc=True)
#         .limit(limit)
#         .execute()
#     )

#     df = pd.DataFrame(response.data)

#     if not df.empty:
#         df = df.sort_values("time_stamp")

#     return df