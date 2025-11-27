import hashlib
from typing import Any, Callable

from fastapi import APIRouter, Depends, Request, Response
from fastapi_cache.decorator import cache

from services import DatabaseService, ProductDatabaseService, get_product_database_service

from ._schema import ProductResponse
from ..utils import key_builder

router = APIRouter(
    prefix='/analytics',
    tags=['analytics'],
)


@router.get(
    '/popular-products',
    response_model=list[ProductResponse],
)
@cache(
    expire=3600,
    key_builder=key_builder,
    namespace='',
)
async def get_popular_products(
    product_database_service: ProductDatabaseService = Depends(get_product_database_service),
):
    products_with_counts = await product_database_service.get_popular_products()
    products_response = [
        ProductResponse(
            **product.__dict__,
            purchase_count=count,
        )
        for product, count in products_with_counts
    ]
    return products_response
