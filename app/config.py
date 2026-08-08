import os

from dotenv import load_dotenv

load_dotenv()

COIN_GECKO_BASE_URL = os.getenv("COIN_GECKO_BASE_URL")
COIN_GECKO_API_KEY = os.getenv("COINGECKO_API_KEY")
APP_VERSION = os.getenv("APP_VERSION", "1.0.0")