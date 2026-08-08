from fastapi import FastAPI

from app.config import LOG_LEVEL
from app.logger import setup_logging
from app.routers.crypto import router as crypto_router

setup_logging(LOG_LEVEL)

app = FastAPI(
    title="Crypto API",
    version="1.0.0",
)

app.include_router(
    crypto_router,
    prefix="/crypto",
)


@app.get("/")
def read_root():
    return {"message": "Server is up and running"}

