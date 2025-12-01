from typing import Any

from fastapi import FastAPI
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from app_context import limiter_var

from .analytics import router as analytics_router
from .products import router as products_router
from .users import router as users_router


def create_api_app(main_app_state: Any) -> FastAPI:
    limiter = limiter_var.get()

    app = FastAPI()

    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)  # type: ignore

    app.state.main_app = main_app_state

    app.include_router(products_router)
    app.include_router(users_router)
    app.include_router(analytics_router)
    return app
