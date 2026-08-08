import httpx
import re
from app.config import COIN_GECKO_API_KEY, COIN_GECKO_BASE_URL


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
        return []