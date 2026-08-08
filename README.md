# CoinGecko Backend Assignment

This project is a beginner-friendly FastAPI backend.
It fetches crypto data from CoinGecko and gives clean API endpoints.

If you are new, follow the Quick Start section first.

## What This Project Does

- Checks if CoinGecko is reachable
- Returns coin list
- Returns category list
- Returns market data for a coin or category
- Protects main endpoints with API key header
- Caches market data in memory for faster repeated calls

## Quick Start (For Freshers)

1. Clone or open this project folder.
2. Create a virtual environment.
3. Install dependencies.
4. Add a .env file.
5. Run the server.
6. Open Swagger docs and test endpoints.

### Clone this Repo after cloning follow the following steps - 

### Step 1: Create virtual environment

Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

Mac/Linux:

```bash
python -m venv .venv
source .venv/bin/activate
```

### Step 2: Install dependencies

```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

### Step 3: Create .env file in project root from .env.example

Use this sample:

```env
COIN_GECKO_BASE_URL=https://api.coingecko.com/api/v3
COINGECKO_API_KEY=
API_AUTH_KEY=your-local-api-key
WEBHOOK_URL=
APP_VERSION=1.0.0
LOG_LEVEL=INFO
CACHE_TTL_SECONDS=60
```

Important:
- API_AUTH_KEY is required for protected endpoints
- CACHE_TTL_SECONDS must be a number
- COIN_GECKO_BASE_URL should usually stay as shown above

### Step 4: Run server

```bash
uvicorn app.main:app --reload
```

Open:
- API base: http://127.0.0.1:8000
- Swagger UI: http://127.0.0.1:8000/docs

## API Endpoints (Simple View)

Base prefix: /crypto

1. GET /crypto/health
- No API key needed
- Tells if CoinGecko is reachable

2. GET /crypto/coins?page_num=1&per_page=10
- API key required in header: x-api-key
- Returns list of coins

3. GET /crypto/categories?page_num=1&per_page=10
- API key required in header: x-api-key
- Returns list of categories

4. GET /crypto/market-data?coin_id=bitcoin&page_num=1&per_page=10
- API key required in header: x-api-key
- You must pass at least one: coin_id or category

If both coin_id and category are missing, you get 400 error.

## How To Send API Key

Header name:

```text
x-api-key
```

Header value:

```text
Same value as API_AUTH_KEY from your .env file
```

If key is wrong or missing, endpoint returns 401.

## cURL Examples

Health:

```bash
curl http://127.0.0.1:8000/crypto/health
```

Coins:

```bash
curl -H "x-api-key: your-local-api-key" "http://127.0.0.1:8000/crypto/coins?page_num=1&per_page=10"
```

Categories:

```bash
curl -H "x-api-key: your-local-api-key" "http://127.0.0.1:8000/crypto/categories?page_num=1&per_page=10"
```

Market data by coin:

```bash
curl -H "x-api-key: your-local-api-key" "http://127.0.0.1:8000/crypto/market-data?coin_id=bitcoin&page_num=1&per_page=10"
```

## Project Files (Basic Understanding)

- app/main.py: Starts FastAPI app and adds routes
- app/routers/crypto.py: All API endpoints and request validation
- app/services/coingecko.py: Calls CoinGecko API and sends optional webhook
- app/cache.py: In-memory cache with TTL
- app/config.py: Reads env variables
- app/logger.py: Logging helper
- tests/test_endpoints_basic.py: Basic tests

## Caching (Easy Explanation)

- Market data endpoint stores response in memory for some time
- Time is controlled by CACHE_TTL_SECONDS
- Same request before expiry is served from cache
- Cache clears when server restarts

## Optional Webhook

If WEBHOOK_URL is set, project sends a POST webhook after successful market data fetch.
If webhook fails, API still responds normally.

## Run Tests

```bash
pytest -q
```

## Run Lint Check

```bash
ruff check .
```

## Common Beginner Errors

1. Server crashes at startup
- Usually CACHE_TTL_SECONDS missing or not numeric in .env

2. Getting 401 on /coins, /categories, /market-data
- x-api-key header missing or value not same as API_AUTH_KEY

3. Getting 503 from endpoints
- CoinGecko request failed, or no data returned in current implementation

4. Changes in .env not applied
- Stop and restart server after editing .env

## Root Endpoint

GET /

Response:

```json
{
  "message": "Server is up and running"
}
```
