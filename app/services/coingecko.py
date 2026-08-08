import httpx
import re
from app.config import COIN_GECKO_API_KEY, COIN_GECKO_BASE_URL, WEBHOOK_URL
from app.logger import get_logger

logger = get_logger(__name__)


async def send_market_data_webhook(payload: dict) -> None:
    if not WEBHOOK_URL:
        logger.debug("Webhook URL not configured, skipping webhook")
        return
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.post(WEBHOOK_URL, json=payload)
            response.raise_for_status()
        logger.info("Webhook sent successfully")
    except (httpx.RequestError, httpx.HTTPStatusError):
        logger.exception("Webhook send failed")
        return


async def check_health() -> dict:
    headers = {}

    if COIN_GECKO_API_KEY:
        headers["x-cg-demo-api-key"] = COIN_GECKO_API_KEY

    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(f"{COIN_GECKO_BASE_URL}/ping", headers=headers)

        if response.is_success:
            version_string=""
            match = re.search(r"\(V(\d+)\)", response.json().get("gecko_says"))
            if match:
                version_string = f"V{match.group(1)}"
            
            return {"status": "reachable", "coin_gecko_version": version_string}

        return {"status": "unreachable","coin_gecko_version": ""}

    except httpx.RequestError:
        logger.exception("Health check request to CoinGecko failed")
        return {"status": "unreachable","coin_gecko_version": ""}

async def coins_list(page_num: int = 1, per_page: int = 10) -> list[dict]:
    headers = {}

    if COIN_GECKO_API_KEY:
        headers["x-cg-demo-api-key"] = COIN_GECKO_API_KEY

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(f"{COIN_GECKO_BASE_URL}/coins/list", headers=headers)

        response.raise_for_status()
        coins = response.json()

        start_index = (page_num - 1) * per_page
        end_index = start_index + per_page
        return coins[start_index:end_index]

    except (httpx.RequestError, httpx.HTTPStatusError):
        logger.exception("Coins list fetch failed")
        return []


async def categories_list(page_num: int = 1, per_page: int = 10) -> list[dict]:
    headers = {}

    if COIN_GECKO_API_KEY:
        headers["x-cg-demo-api-key"] = COIN_GECKO_API_KEY

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(
                f"{COIN_GECKO_BASE_URL}/coins/categories/list",
                headers=headers,
            )

        response.raise_for_status()
        categories = response.json()

        start_index = (page_num - 1) * per_page
        end_index = start_index + per_page
        return categories[start_index:end_index]

    except (httpx.RequestError, httpx.HTTPStatusError):
        logger.exception("Categories list fetch failed")
        return []


async def coin_market_data(
    coin_id: str | None = None,
    category: str | None = None,
    page_num: int = 1,
    per_page: int = 10,
) -> list[dict]:
    headers = {}

    if COIN_GECKO_API_KEY:
        headers["x-cg-demo-api-key"] = COIN_GECKO_API_KEY

    params = {
        "vs_currency": "cad",
        "page": page_num,
        "per_page": per_page,
    }

    if coin_id:
        params["ids"] = coin_id

    if category:
        params["category"] = category

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(
                f"{COIN_GECKO_BASE_URL}/coins/markets",
                headers=headers,
                params=params,
            )

        response.raise_for_status()
        market_data = response.json()
        logger.info("Market data fetched successfully. Records: %s", len(market_data))

        await send_market_data_webhook(
            {
                "event": "market_data_fetched",
                "served_from_cache": False,
                "coin_id": coin_id,
                "category": category,
                "page_num": page_num,
                "per_page": per_page,
                "result_count": len(market_data),
            }
        )

        return market_data

    except (httpx.RequestError, httpx.HTTPStatusError):
        logger.exception("Market data fetch failed")
        return []