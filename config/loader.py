import os
from pathlib import Path

from dotenv import load_dotenv


ENV_FILE = Path(__file__).resolve().parent / ".env"
load_dotenv(ENV_FILE)


def get_api_key(provider):
    key_name = f"{provider.upper()}_API_KEY"
    return os.getenv(key_name)


def get_model(provider):
    model_name = f"{provider.upper()}_MODEL"
    return os.getenv(model_name)


def get_enabled_providers():
    value = os.getenv("ENABLED_PROVIDERS", "")

    if not value.strip():
        return []

    return [
        provider.strip().lower()
        for provider in value.split(",")
        if provider.strip()
    ]