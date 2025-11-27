from typing import Any

from fastapi import FastAPI

from .analytics import router as analytics_router
from .products import router as products_router
from .users import router as users_router


def create_api_app(main_app_state: Any) -> FastAPI:
    app = FastAPI()

    app.state.main_app = main_app_state

    app.include_router(products_router)
    app.include_router(users_router)
    app.include_router(analytics_router)
    return app
