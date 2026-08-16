import requests

from utils.secrets import get_secret

SUPABASE_URL = get_secret("SUPABASE_URL")

SUPABASE_BUCKET = get_secret("SUPABASE_BUCKET", "app-files")

LATEST_IMAGE_PATH = "latest.jpg"

REQUEST_TIMEOUT = 10


def get_latest_plant_image_url(cache_key=None):
    """
    Public URL for the ESP32-CAM's latest capture.

    `cache_key` (e.g. the latest sensor reading's timestamp) is appended
    as a query string so the browser doesn't keep showing a stale cached
    photo after the ESP32-CAM overwrites latest.jpg.
    """

    if not SUPABASE_URL:
        return None

    url = (
        f"{SUPABASE_URL}/storage/v1/object/public/"
        f"{SUPABASE_BUCKET}/{LATEST_IMAGE_PATH}"
    )

    if cache_key is not None:
        url = f"{url}?t={cache_key}"

    return url


def fetch_latest_plant_image_bytes(cache_key=None):
    """
    Downloads the latest plant photo so it can be sent to Gemini.
    Returns None if the bucket is empty, unreachable, or not yet public.
    """

    url = get_latest_plant_image_url(cache_key)

    if not url:
        return None

    try:
        response = requests.get(url, timeout=REQUEST_TIMEOUT)

        if response.status_code != 200:
            return None

        return response.content

    except requests.RequestException:
        return None
