import pandas as pd
from supabase import create_client

from utils.secrets import get_secret

# -----------------------------------------------------
# Load environment variables
# -----------------------------------------------------

SUPABASE_URL = get_secret("SUPABASE_URL")

SUPABASE_KEY = get_secret("SUPABASE_KEY")

TABLE_NAME = get_secret("TABLE_NAME", "esp32_log")

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