from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse

from app.config import APP_VERSION
from app.services.coingecko import check_health, coins_list
from pydantic import BaseModel
router = APIRouter()

class Coin(BaseModel):
    id: str
    symbol: str
    name: str


class CoinGeckoHealth(BaseModel):
    status: str
    coin_gecko_version: str


class HealthResponse(BaseModel):
    status: str
    app_version: str
    coingecko: CoinGeckoHealth


class CoinsResponse(BaseModel):
    status: str
    coins: list[Coin]

@router.get("/health", response_model=HealthResponse)
async def health_check():
    coingecko = await check_health()

    application_status=""
    status_code=200

    if coingecko["status"] == "reachable":
        application_status = "healthy"
    else:
        status_code = 503
        application_status = "degraded"

    response = {
        "status": application_status,
        "app_version": APP_VERSION,
        "coingecko": coingecko,
    }

    return JSONResponse(
        status_code=status_code,
        content=response,
    )

@router.get("/coins", response_model=CoinsResponse)
async def list_coins(page_num: int = Query(default=1),per_page: int = Query(default=10)):
    try:
        coins = await coins_list(page_num=page_num, per_page=per_page)
        coin_list = []

        for coin in coins:
            coin_item = Coin(
                id=coin["id"],
                symbol=coin["symbol"],
                name=coin["name"],
            )
            coin_list.append(coin_item)

        status_code = 200
        coins_status = "available"

        if len(coin_list) == 0:
            status_code = 503
            coins_status = "unavailable"

        response = {
            "status": coins_status,
            "coins": [coin.model_dump() for coin in coin_list],
        }

        return JSONResponse(status_code=status_code, content=response)

    except Exception:
        return JSONResponse(
            status_code=503,
            content={
                "status": "unavailable",
                "coins": [],
            },
        )