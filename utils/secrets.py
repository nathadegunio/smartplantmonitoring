import os

from dotenv import load_dotenv
import streamlit as st

load_dotenv()


def get_secret(key, default=None):
    """
    Reads config from Streamlit secrets (Streamlit Community Cloud),
    falling back to the local .env / OS environment otherwise.

    st.secrets raises StreamlitSecretNotFoundError instead of
    returning a default when no secrets.toml exists at all (as is
    the case for local development), so that has to be guarded
    explicitly rather than relying on st.secrets.get()'s default.
    """

    try:
        if key in st.secrets:
            return st.secrets[key]
    except Exception:
        pass

    return os.getenv(key, default)
