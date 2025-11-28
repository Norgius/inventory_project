import pytest
from httpx import AsyncClient


@pytest.mark.asyncio(loop_scope="session")
async def test_analytics_popular_product(client: AsyncClient):
    response = await client.get('api/v1/analytics/popular-products')
    payload = response.json()

    assert response.status_code == 200
    assert len(payload) == 5
    assert payload[0].get('purchase_count') == 3
    assert payload[1].get('purchase_count') == 2
    assert payload[-1].get('purchase_count') == 1


@pytest.mark.asyncio(loop_scope="session")
async def test_analytics_popular_product_cache(client: AsyncClient, clear_cache):
    response = await client.get('api/v1/analytics/popular-products')

    assert response.status_code == 200
    assert response.headers.get('x-fastapi-cache') == 'MISS'

    response = await client.get('api/v1/analytics/popular-products')

    assert response.status_code == 200
    assert response.headers.get('x-fastapi-cache') == 'HIT'
