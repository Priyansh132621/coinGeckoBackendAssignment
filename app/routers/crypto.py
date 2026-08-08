from fastapi import APIRouter, Depends, Header, HTTPException, Query
from fastapi.responses import JSONResponse

from app.config import API_AUTH_KEY, APP_VERSION
from app.services.coingecko import (
    categories_list,
    check_health,
    coin_market_data,
    coins_list,
)
from pydantic import BaseModel
router = APIRouter()


def verify_api_key(api_key: str | None = Header(default=None, alias="x-api-key")):
    if not API_AUTH_KEY:
        raise HTTPException(status_code=500, detail="API_AUTH_KEY is not configured")

    if api_key != API_AUTH_KEY:
        raise HTTPException(status_code=401,detail="Invalid or missing API key in header")

class Coin(BaseModel):
    id: str
    symbol: str
    name: str


class Category(BaseModel):
    category_id: str
    name: str


class MarketCoin(BaseModel):
    id: str
    symbol: str
    name: str
    current_price: float | None = None
    market_cap: float | None = None
    market_cap_rank: int | None = None
    total_volume: float | None = None


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


class CategoriesResponse(BaseModel):
    status: str
    categories: list[Category]


class MarketDataResponse(BaseModel):
    status: str
    market_data: list[MarketCoin]

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
async def list_coins(page_num: int = Query(default=1),per_page: int = Query(default=10),
                     _: None = Depends(verify_api_key)):
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


@router.get("/categories", response_model=CategoriesResponse)
async def list_categories(page_num: int = Query(default=1),per_page: int = Query(default=10),
                          _: None = Depends(verify_api_key)):
    try:
        categories = await categories_list(page_num=page_num, per_page=per_page)
        category_list = []

        for category in categories:
            category_item = Category(
                category_id=category["category_id"],
                name=category["name"],
            )
            category_list.append(category_item)

        status_code = 200
        category_status = "available"

        if len(category_list) == 0:
            status_code = 503
            category_status = "unavailable"

        response = {
            "status": category_status,
            "categories": [category.model_dump() for category in category_list],
        }

        return JSONResponse(status_code=status_code, content=response)

    except Exception:
        return JSONResponse(
            status_code=503,
            content={
                "status": "unavailable",
                "categories": [],
            },
        )


@router.get("/market-data", response_model=MarketDataResponse)
async def get_market_data(coin_id: str | None = None,category: str | None = None,
                          page_num: int = Query(default=1), per_page: int = Query(default=10),
                          _: None = Depends(verify_api_key)):

    if not coin_id and not category:
        raise HTTPException(
            status_code=400,
            detail="At least one of coin_id or category must be provided",
        )

    try:
        market_data = await coin_market_data(
            coin_id=coin_id,
            category=category,
            page_num=page_num,
            per_page=per_page,
        )
        market_coin_list = []

        for coin in market_data:
            market_coin_item = MarketCoin(
                id=coin["id"],
                symbol=coin["symbol"],
                name=coin["name"],
                current_price=coin.get("current_price"),
                market_cap=coin.get("market_cap"),
                market_cap_rank=coin.get("market_cap_rank"),
                total_volume=coin.get("total_volume"),
            )
            market_coin_list.append(market_coin_item)

        status_code = 200
        market_status = "available"

        if len(market_coin_list) == 0:
            status_code = 503
            market_status = "unavailable"

        market_data_list = []
        for coin in market_coin_list:
            market_data_list.append(coin.model_dump())

        response = {
            "status": market_status,
            "market_data": market_data_list,
        }

        return JSONResponse(status_code=status_code, content=response)

    except Exception:
        return JSONResponse(
            status_code=503,
            content={
                "status": "unavailable",
                "market_data": [],
            },
        )