import os

from dotenv import load_dotenv

load_dotenv()

COIN_GECKO_BASE_URL = os.getenv("COIN_GECKO_BASE_URL")
COIN_GECKO_API_KEY = os.getenv("COINGECKO_API_KEY")
APP_VERSION = os.getenv("APP_VERSION", "1.0.0")
API_AUTH_KEY = os.getenv("API_AUTH_KEY")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
CACHE_TTL_SECONDS = int(os.getenv("CACHE_TTL_SECONDS"))