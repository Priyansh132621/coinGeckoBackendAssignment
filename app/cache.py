import time
from app.config import CACHE_TTL_SECONDS
cache_store = {}


def get(key: str):
    cache_value = cache_store.get(key)
    if cache_value is None:
        return None
    if time.time() > cache_value["expires_at"]:
        del cache_store[key]
        return None
    return cache_value["data"]


def set(key: str, data) -> None:
    cache_store[key] = {
        "data": data,
        "expires_at": time.time() + CACHE_TTL_SECONDS,
    }
