from fastapi import FastAPI

from app.routers.crypto import router as crypto_router
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

