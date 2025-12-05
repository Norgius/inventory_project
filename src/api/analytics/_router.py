from fastapi import APIRouter, Depends
from fastapi_cache.decorator import cache

from env_settings import settings
from services import ProductDatabaseService, get_product_database_service

from ._schema import ProductResponse
from ..utils import key_builder

router = APIRouter(
    prefix='/analytics',
    tags=['analytics'],
)


@router.get(
    '/popular-products',
    summary=f'Получить до 5 популярных продуктов за последние {settings.API_SETTINGS.LAST_DAYS_NUMBER} дней',
    response_model=list[ProductResponse],
)
@cache(
    expire=settings.CACHE_CONFIG.POPULAR_PRODUCT_TIMER,
    key_builder=key_builder,
    namespace=settings.CACHE_CONFIG.NAMESPACE.POPULAR_PRODUCTS,
)
async def get_popular_products(
    product_database_service: ProductDatabaseService = Depends(get_product_database_service),
):
    products_with_counts = await product_database_service.get_popular_products()
    products_response = [
        ProductResponse(**product.__dict__, purchase_count=count)
        for product, count in products_with_counts
    ]
    return products_response
