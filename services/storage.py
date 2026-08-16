from services.database import supabase
from utils.secrets import get_secret

SUPABASE_BUCKET = get_secret("SUPABASE_BUCKET", "app-files")

LATEST_IMAGE_PATH = "latest.jpg"


def upload_plant_image(image_bytes):
    """
    Uploads/overwrites the single latest plant photo. Only one photo is
    ever kept in the bucket — this always replaces it, there is no
    history of past captures.
    """

    try:
        supabase.storage.from_(SUPABASE_BUCKET).upload(
            LATEST_IMAGE_PATH,
            image_bytes,
            file_options={"content-type": "image/jpeg", "upsert": "true"},
        )
        return True
    except Exception:
        return False


def get_latest_plant_image():
    """
    Returns (image_bytes, captured_at_utc) for the latest plant photo,
    or (None, None) if no photo has been uploaded yet or the bucket is
    unreachable. captured_at_utc is the storage object's UTC timestamp
    (as returned by Supabase), to be converted to PH time by the caller.
    """

    try:
        entries = supabase.storage.from_(SUPABASE_BUCKET).list()
    except Exception:
        return None, None

    match = next(
        (e for e in entries if e.get("name") == LATEST_IMAGE_PATH),
        None,
    )

    if not match:
        return None, None

    try:
        image_bytes = supabase.storage.from_(SUPABASE_BUCKET).download(
            LATEST_IMAGE_PATH
        )
    except Exception:
        return None, None

    captured_at = match.get("updated_at") or match.get("created_at")

    return image_bytes, captured_at
