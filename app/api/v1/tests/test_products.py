import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.schemas.products import ProductPriceSchema, ProductSchema


@pytest.mark.asyncio
async def test_create_product(async_client: AsyncClient, async_session: AsyncSession):
    response = await async_client.post(
        "/products",
        json={"name": "Product 1"},
    )
    assert response.status_code == 200
    product = ProductSchema(**response.json())
    assert product.name == "Product 1"
    assert product.product_sku.startswith("SKU-")


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
    product = ProductSchema(**response.json())

    response = await async_client.post(
        f"/products/{str(product.id)}/prices",
        json={
            "product_id": str(product.id),
            "price": 10.1,
            "free_allocation": 2.5,
            "use_unity": "GB/Mo",
        },
    )
    assert response.status_code == 200
    product_price = ProductPriceSchema(**response.json())
    assert product_price.price == 10.1
    assert product_price.free_allocation == 2.5
    assert product_price.use_unity == "GB/Mo"


@pytest.mark.asyncio
async def test_create_and_update_product_price(
    async_client: AsyncClient, async_session: AsyncSession
):
    response = await async_client.post(
        "/products",
        json={"name": "Product 1"},
    )
    assert response.status_code == 200
    product = ProductSchema(**response.json())

    response = await async_client.post(
        f"/products/{str(product.id)}/prices",
        json={
            "product_id": str(product.id),
            "price": 10.1,
            "free_allocation": 2.5,
            "use_unity": "GB/Mo",
        },
    )
    assert response.status_code == 200
    product_price = ProductPriceSchema(**response.json())
    assert product_price.price == 10.1
    assert product_price.free_allocation == 2.5
    assert product_price.use_unity == "GB/Mo"

    response = await async_client.post(
        f"/products/{str(product.id)}/prices",
        json={
            "product_id": str(product.id),
            "price": 20.2,
            "free_allocation": 5.0,
            "use_unity": "GB/Mo",
        },
    )
    assert response.status_code == 200
    product_price = ProductPriceSchema(**response.json())
    assert product_price.price == 20.2
    assert product_price.free_allocation == 5.0
    assert product_price.use_unity == "GB/Mo"


@pytest.mark.asyncio
async def test_fail_create_product_price_missing_product(
    async_client: AsyncClient, async_session: AsyncSession
):
    response = await async_client.post(
        "/products/67f68a4b-5522-44b3-be6c-7c8597519a35/prices",
        json={
            "product_id": "67f68a4b-5522-44b3-be6c-7c8597519a35",
            "price": 10.1,
            "free_allocation": 2.5,
            "use_unity": "GB/Mo",
        },
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Product not found"}


@pytest.mark.asyncio
async def test_get_product(async_client: AsyncClient, async_session: AsyncSession):
    payload = {"name": "Product 1"}
    response = await async_client.post(
        "/products",
        json=payload,
    )
    assert response.status_code == 200
    product = ProductSchema(**response.json())

    response = await async_client.get(f"/products/{product.id}")
    assert response.status_code == 200
    product = ProductSchema(**response.json())
    assert product.name == payload["name"]


@pytest.mark.asyncio
async def test_get_product_price(
    async_client: AsyncClient, async_session: AsyncSession
):
    payload = {"name": "Product 1"}
    response = await async_client.post(
        "/products",
        json=payload,
    )
    assert response.status_code == 200
    product = ProductSchema(**response.json())

    product_price_payload = {
        "product_id": str(product.id),
        "price": 10.1,
        "free_allocation": 2.5,
        "use_unity": "GB/Mo",
    }
    response = await async_client.post(
        f"/products/{str(product.id)}/prices",
        json=product_price_payload,
    )
    assert response.status_code == 200

    response = await async_client.get(f"/products/{str(product.id)}/prices")
    assert response.status_code == 200
    product_price = ProductPriceSchema(**response.json())
    assert product_price.product_id == product.id
    assert product_price.price == product_price_payload["price"]
    assert product_price.free_allocation == product_price_payload["free_allocation"]
    assert product_price.use_unity == product_price_payload["use_unity"]
