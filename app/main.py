from fastapi import FastAPI
from app.routers import exchange

app = FastAPI(title="Exchange Service")

app.include_router(exchange.router)
