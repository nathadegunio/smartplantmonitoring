import os
from dotenv import load_dotenv
from supabase import create_client
import pandas as pd

# -----------------------------------------------------
# Load Environment Variables
# -----------------------------------------------------
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
TABLE_NAME = os.getenv("TABLE_NAME")

# -----------------------------------------------------
# Create Supabase Client
# -----------------------------------------------------
supabase = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)


# -----------------------------------------------------
# Get Latest Sensor Reading
# -----------------------------------------------------
def get_latest_record():

    response = (
        supabase.table(TABLE_NAME)
        .select("*")
        .order("time_stamp", desc=True)
        .limit(1)
        .execute()
    )

    if len(response.data) == 0:
        return None

    return response.data[0]


# -----------------------------------------------------
# Get Recent Records
# -----------------------------------------------------
def get_recent_records(limit=100):

    response = (
        supabase.table(TABLE_NAME)
        .select("*")
        .order("time_stamp", desc=True)
        .limit(limit)
        .execute()
    )

    return pd.DataFrame(response.data)


# -----------------------------------------------------
# Get All Records
# -----------------------------------------------------
def get_all_records():

    response = (
        supabase.table(TABLE_NAME)
        .select("*")
        .order("time_stamp", desc=True)
        .execute()
    )

    return pd.DataFrame(response.data)


# -----------------------------------------------------
# Get Records Between Dates
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

    return pd.DataFrame(response.data)

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

    if df.empty:
        return df

    # Oldest → Newest for charts
    df = df.sort_values("time_stamp")

    return df