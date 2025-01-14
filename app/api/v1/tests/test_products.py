import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession


@pytest.mark.asyncio
async def test_create_product(async_client: AsyncClient, async_session: AsyncSession):
    response = await async_client.post(
        "/products",
        json={"name": "Product 1"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Product 1"
    assert data["product_sku"].startswith("SKU-")


@pytest.mark.asyncio
async def test_fail_create_duplicated_product(
    async_client: AsyncClient, async_session: AsyncSession
):
    response = await async_client.post(
        "/products",
        json={"name": "Product 1"},
    )
    assert response.status_code == 200

    response = await async_client.post(
        "/products",
        json={"name": "Product 1"},
    )
    assert response.status_code == 400
    assert response.json() == {
        "detail": "A unique constraint violation occurred, please check your input."
    }


@pytest.mark.asyncio
async def test_create_product_price(
    async_client: AsyncClient, async_session: AsyncSession
):
    response = await async_client.post(
        "/products",
        json={"name": "Product 1"},
    )
    assert response.status_code == 200
    product_id = response.json()["id"]

    response = await async_client.post(
        f"/products/{product_id}/prices",
        json={"price": 10.1, "free_allocation": 2.5, "use_unity": "GB/Mo"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["price"] == 10.1
    assert data["free_allocation"] == 2.5
    assert data["use_unity"] == "GB/Mo"


@pytest.mark.asyncio
async def test_create_and_update_product_price(
    async_client: AsyncClient, async_session: AsyncSession
):
    response = await async_client.post(
        "/products",
        json={"name": "Product 1"},
    )
    assert response.status_code == 200
    product_id = response.json()["id"]

    response = await async_client.post(
        f"/products/{product_id}/prices",
        json={"price": 10.1, "free_allocation": 2.5, "use_unity": "GB/Mo"},
    )
    assert response.status_code == 200

    response = await async_client.post(
        f"/products/{product_id}/prices",
        json={"price": 20.2, "free_allocation": 5.0, "use_unity": "GB/Mo"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["price"] == 20.2
    assert data["free_allocation"] == 5.0
    assert data["use_unity"] == "GB/Mo"


@pytest.mark.asyncio
async def test_fail_create_product_price_missing_product(
    async_client: AsyncClient, async_session: AsyncSession
):
    response = await async_client.post(
        "/products/67f68a4b-5522-44b3-be6c-7c8597519a35/prices",
        json={"price": 10.1, "free_allocation": 2.5, "use_unity": "GB/Mo"},
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Product not found"}
