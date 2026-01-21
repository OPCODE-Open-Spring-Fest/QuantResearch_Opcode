"""FastAPI application entrypoint for backend API."""

import asyncio
import os
from pathlib import Path

from dotenv import load_dotenv
from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import assets as assets_router
from .routers import auth as auth_router
from .routers import backtest as backtest_router
from .routers import dashboard as dashboard_router
from .routers import positions as positions_router
from .routers import trades as trades_router
from .routers import stocks as stocks_router
from .routers import strategies as strategies_router
from .routers import watchlists as watchlists_router
from .routers import alerts as alerts_router
from .routers import portfolio as portfolio_router
from .routers import optimization as optimization_router
from .utils.ws_manager import redis_listener_loop

# Load environment variables from .env file
env_path = Path(__file__).parent.parent.parent.parent / ".env"
if env_path.exists():
    load_dotenv(env_path)
else:
    load_dotenv()  # Try to load from current directory

app = FastAPI(title="QuantResearch API")

# Configure CORS to allow frontend requests
allowed_origins = [
    "http://localhost:3006",
    "http://localhost:3005",
    "http://localhost:3004",
    "http://localhost:3003",
    "http://localhost:3000",
    "http://127.0.0.1:3006",
    "http://127.0.0.1:3005",
]

# Add environment variable origins if specified
cors_env = os.getenv("CORS_ORIGINS", "")
if cors_env and cors_env != "*":
    allowed_origins.extend(cors_env.split(","))

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins if cors_env != "*" else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
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
app.include_router(dashboard_router.router)
app.include_router(positions_router.router)
app.include_router(trades_router.router)
app.include_router(stocks_router.router)
app.include_router(strategies_router.router)
app.include_router(watchlists_router.router)
app.include_router(alerts_router.router)
app.include_router(portfolio_router.router)
app.include_router(optimization_router.router)

# Health / readiness
router = APIRouter(prefix="/api")


@router.get("/health")
async def health():
    return {"status": "ok"}


app.include_router(router)
