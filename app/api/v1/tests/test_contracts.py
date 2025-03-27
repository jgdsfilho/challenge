import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.schemas.products import ProductSchema
from app.api.v1.schemas.tenants import TenantSchema


@pytest.mark.asyncio
async def test_create_contract(
    async_client: AsyncClient,
    async_session: AsyncSession,
):
    response = await async_client.post(
        "/tenants",
        json={"name": "tenant1", "email": "tenant1@my_domain.com"},
    )
    assert response.status_code == 200
    tenant = TenantSchema(**response.json())

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

    response = await async_client.post(
        "/contracts", json={"product_id": str(product.id), "tenant_id": str(tenant.id)}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["product_id"] == str(product.id)
    assert data["tenant_id"] == str(tenant.id)


@pytest.mark.asyncio
async def test_delete_contract(
    async_client: AsyncClient,
    async_session: AsyncSession,
):
    response = await async_client.post(
        "/tenants",
        json={"name": "tenant1", "email": "tenant1@my_domain.com"},
    )
    assert response.status_code == 200
    tenant = TenantSchema(**response.json())

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

    response = await async_client.post(
        "/contracts", json={"product_id": str(product.id), "tenant_id": str(tenant.id)}
    )
    assert response.status_code == 200

    response = await async_client.delete(
        f"/contracts/tenants/{str(tenant.id)}/products/{str(product.id)}"
    )
    assert response.status_code == 204


@pytest.mark.asyncio
async def test_get_contracts_from_a_tenant(
    async_client: AsyncClient,
    async_session: AsyncSession,
):
    response = await async_client.post(
        "/tenants",
        json={"name": "tenant1", "email": "tenant1@my_domain.com"},
    )
    assert response.status_code == 200
    tenant = TenantSchema(**response.json())

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

    response = await async_client.post(
        "/contracts", json={"product_id": str(product.id), "tenant_id": str(tenant.id)}
    )
    assert response.status_code == 200

    response = await async_client.get(f"/contracts/tenants/{str(tenant.id)}")
    assert response.status_code == 200
    data = response.json()
    assert data["product_id"] == str(product.id)
    assert data["tenant_id"] == str(tenant.id)
