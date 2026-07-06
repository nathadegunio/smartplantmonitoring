# from services.database import get_latest_record

# latest = get_latest_record()

# print(latest)


import os
from dotenv import load_dotenv
from supabase import create_client

# ---------------------------------------------
# Load .env
# ---------------------------------------------
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
TABLE_NAME = os.getenv("TABLE_NAME", "esp32_log")

print("=" * 60)
print("SUPABASE CONNECTION TEST")
print("=" * 60)

print(f"SUPABASE_URL : {SUPABASE_URL}")
print(f"TABLE_NAME   : {TABLE_NAME}")

if not SUPABASE_URL:
    raise ValueError("❌ SUPABASE_URL not found in .env")

if not SUPABASE_KEY:
    raise ValueError("❌ SUPABASE_KEY not found in .env")

# ---------------------------------------------
# Connect
# ---------------------------------------------
try:
    supabase = create_client(
        SUPABASE_URL,
        SUPABASE_KEY
    )

    print("\n✅ Connected to Supabase successfully.")

except Exception as e:
    print("\n❌ Failed to connect.")
    print(e)
    raise

# ---------------------------------------------
# Test query
# ---------------------------------------------
print("\nRetrieving latest sensor record...")

try:

    response = (
        supabase.table(TABLE_NAME)
        .select("*")
        .order("time_stamp", desc=True)
        .limit(1)
        .execute()
    )

    print(f"\nReturned rows: {len(response.data)}")

    if len(response.data) == 0:
        print("\n❌ No records found.")
    else:

        latest = response.data[0]

        print("\n✅ Latest Record:\n")

        for key, value in latest.items():
            print(f"{key:20}: {value}")

except Exception as e:

    print("\n❌ Query failed.")
    print(e)