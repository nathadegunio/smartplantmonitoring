from datetime import datetime


# ------------------------------------
# Convert timestamp to datetime
# ------------------------------------
def to_datetime(timestamp):
    """
    Convert a Supabase timestamp (string or datetime)
    into a Python datetime object.
    """

    if timestamp is None:
        return None

    if isinstance(timestamp, datetime):
        return timestamp

    if isinstance(timestamp, str):
        return datetime.fromisoformat(
            timestamp.replace("Z", "+00:00")
        )

    return None


# ------------------------------------
# Format Timestamp
# ------------------------------------
def format_timestamp(timestamp):
    """
    Example:
    Jul 05, 2026 09:45 AM
    """

    timestamp = to_datetime(timestamp)

    if timestamp is None:
        return "Unknown"

    return timestamp.strftime("%b %d, %Y %I:%M:%S %p")


# ------------------------------------
# Time Ago
# ------------------------------------
def time_ago(timestamp):
    """
    Example:
    30 seconds ago
    5 minutes ago
    2 hours ago
    Yesterday
    """

    timestamp = to_datetime(timestamp)

    if timestamp is None:
        return "Unknown"

    now = datetime.now(timestamp.tzinfo)

    diff = now - timestamp

    seconds = int(diff.total_seconds())

    if seconds < 60:
        if seconds == 1:
            return "1 second ago"
        return f"{seconds} seconds ago"

    minutes = seconds // 60

    if minutes < 60:
        if minutes == 1:
            return "1 minute ago"
        return f"{minutes} minutes ago"

    hours = minutes // 60

    if hours < 24:
        if hours == 1:
            return "1 hour ago"
        return f"{hours} hours ago"

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