from datetime import datetime
from zoneinfo import ZoneInfo

# ------------------------------------
# Philippine Timezone
# ------------------------------------
MANILA = ZoneInfo("Asia/Manila")


# ------------------------------------
# Convert timestamp to datetime
# ------------------------------------
def to_datetime(timestamp):
    """
    Convert a Supabase timestamp (string or datetime)
    into a timezone-aware datetime object.
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

    # If timezone missing, assume UTC
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=ZoneInfo("UTC"))

    return dt


# ------------------------------------
# Convert UTC -> Philippine Time
# ------------------------------------
def to_manila(timestamp):
    """
    Convert UTC timestamp to Philippine Time.
    """

    dt = to_datetime(timestamp)

    if dt is None:
        return None

    return dt.astimezone(MANILA)


# ------------------------------------
# Format Timestamp
# ------------------------------------
def format_timestamp(timestamp):
    """
    Example:
    Jul 06, 2026 08:45 PM
    """

    dt = to_manila(timestamp)

    if dt is None:
        return "Unknown"

    return dt.strftime("%b %d, %Y %I:%M:%S %p")


# ------------------------------------
# Time Ago
# ------------------------------------
def time_ago(timestamp):
    """
    Example:
    30 seconds ago
    5 minutes ago
    Yesterday
    """

    dt = to_manila(timestamp)

    if dt is None:
        return "Unknown"

    now = datetime.now(MANILA)

    diff = now - dt

    seconds = int(diff.total_seconds())

    if seconds < 60:
        return "1 second ago" if seconds == 1 else f"{seconds} seconds ago"

    minutes = seconds // 60

    if minutes < 60:
        return "1 minute ago" if minutes == 1 else f"{minutes} minutes ago"

    hours = minutes // 60

    if hours < 24:
        return "1 hour ago" if hours == 1 else f"{hours} hours ago"

    days = hours // 24

    if days == 1:
        return "Yesterday"

    return f"{days} days ago"


# ------------------------------------
# Round Numbers
# ------------------------------------
def round_value(value, digits=1):

    if value is None:
        return 0

    return round(float(value), digits)



# from datetime import datetime


# # ------------------------------------
# # Convert timestamp to datetime
# # ------------------------------------
# def to_datetime(timestamp):
#     """
#     Convert a Supabase timestamp (string or datetime)
#     into a Python datetime object.
#     """

#     if timestamp is None:
#         return None

#     if isinstance(timestamp, datetime):
#         return timestamp

#     if isinstance(timestamp, str):
#         return datetime.fromisoformat(
#             timestamp.replace("Z", "+00:00")
#         )

#     return None


# # ------------------------------------
# # Format Timestamp
# # ------------------------------------
# def format_timestamp(timestamp):
#     """
#     Example:
#     Jul 05, 2026 09:45 AM
#     """

#     timestamp = to_datetime(timestamp)

#     if timestamp is None:
#         return "Unknown"

#     return timestamp.strftime("%b %d, %Y %I:%M:%S %p")


# # ------------------------------------
# # Time Ago
# # ------------------------------------
# def time_ago(timestamp):
#     """
#     Example:
#     30 seconds ago
#     5 minutes ago
#     2 hours ago
#     Yesterday
#     """

#     timestamp = to_datetime(timestamp)

#     if timestamp is None:
#         return "Unknown"

#     now = datetime.now(timestamp.tzinfo)

#     diff = now - timestamp

#     seconds = int(diff.total_seconds())

#     if seconds < 60:
#         if seconds == 1:
#             return "1 second ago"
#         return f"{seconds} seconds ago"

#     minutes = seconds // 60

#     if minutes < 60:
#         if minutes == 1:
#             return "1 minute ago"
#         return f"{minutes} minutes ago"

#     hours = minutes // 60

#     if hours < 24:
#         if hours == 1:
#             return "1 hour ago"
#         return f"{hours} hours ago"

#     days = hours // 24

#     if days == 1:
#         return "Yesterday"

#     return f"{days} days ago"


# # ------------------------------------
# # Round Numbers
# # ------------------------------------
# def round_value(value, digits=1):

#     if value is None:
#         return 0

#     return round(float(value), digits)