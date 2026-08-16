from datetime import datetime
from zoneinfo import ZoneInfo

# Philippine timezone
MANILA = ZoneInfo("Asia/Manila")


# ------------------------------------
# Convert timestamp to datetime
# ------------------------------------
def to_datetime(timestamp):
    """
    Converts a Supabase timestamp
    into a timezone-aware datetime.
    """

    if timestamp is None:
        return None

    if isinstance(timestamp, datetime):
        dt = timestamp

    elif isinstance(timestamp, str):
        dt = datetime.fromisoformat(
            timestamp.replace("Z", "+00:00")
        )

    else:
        return None

    # Assume UTC if timezone missing
    if dt.tzinfo is None:
        dt = dt.replace(
            tzinfo=ZoneInfo("UTC")
        )

    return dt


# ------------------------------------
# UTC -> Philippine Time
# ------------------------------------
def to_manila(timestamp):

    dt = to_datetime(timestamp)

    if dt is None:
        return None

    return dt.astimezone(MANILA)


# ------------------------------------
# Format Timestamp
# ------------------------------------
def format_timestamp(timestamp):

    dt = to_manila(timestamp)

    if dt is None:
        return "Unknown"

    return dt.strftime("%b %d, %Y %I:%M:%S %p")


# ------------------------------------
# Relative Time
# ------------------------------------
def time_ago(timestamp):

    dt = to_manila(timestamp)

    if dt is None:
        return "Unknown"

    now = datetime.now(MANILA)

    diff = now - dt

    seconds = int(diff.total_seconds())

    if seconds < 60:
        return (
            "1 second ago"
            if seconds == 1
            else f"{seconds} seconds ago"
        )

    minutes = seconds // 60

    if minutes < 60:
        return (
            "1 minute ago"
            if minutes == 1
            else f"{minutes} minutes ago"
        )

    hours = minutes // 60

    if hours < 24:
        return (
            "1 hour ago"
            if hours == 1
            else f"{hours} hours ago"
        )

    days = hours // 24

    if days == 1:
        return "Yesterday"

    return f"{days} days ago"


# ------------------------------------
# Round Number
# ------------------------------------
def round_value(value, digits=1):

    if value is None:
        return 0

    return round(float(value), digits)