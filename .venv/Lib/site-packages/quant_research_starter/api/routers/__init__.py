"""API routers package."""

from fastapi import APIRouter

router = APIRouter()

from . import auth as auth_router  # noqa: E402,F401
from . import backtest as backtest_router  # noqa: E402,F401
from . import assets as assets_router  # noqa: E402,F401
