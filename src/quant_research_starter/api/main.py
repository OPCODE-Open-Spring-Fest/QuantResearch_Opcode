"""FastAPI application entrypoint for backend API."""

import asyncio
import os

from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import auth as auth_router
from .routers import backtest as backtest_router
from .utils.ws_manager import redis_listener_loop

app = FastAPI(title="QuantResearch API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("CORS_ORIGINS", "*")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    # Start background redis subscription for websocket broadcasting
    loop = asyncio.get_event_loop()
    loop.create_task(redis_listener_loop())


@app.on_event("shutdown")
async def shutdown_event():
    # Nothing special for now
    pass


app.include_router(auth_router.router)
app.include_router(backtest_router.router)
app.include_router(assets_router.router)

# Health / readiness
router = APIRouter(prefix="/api")


@router.get("/health")
async def health():
    return {"status": "ok"}


app.include_router(router)
