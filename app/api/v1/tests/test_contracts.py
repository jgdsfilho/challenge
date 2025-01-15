import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession


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
    tenant_id = response.json()["id"]

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
        "/contracts", json={"product_id": product_id, "tenant_id": tenant_id}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["product_id"] == product_id
    assert data["tenant_id"] == tenant_id


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
    tenant_id = response.json()["id"]

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
        "/contracts", json={"product_id": product_id, "tenant_id": tenant_id}
    )
    assert response.status_code == 200

    response = await async_client.delete(
        f"/contracts/tenants/{tenant_id}/products/{product_id}"
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
    tenant_id = response.json()["id"]

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
        "/contracts", json={"product_id": product_id, "tenant_id": tenant_id}
    )
    assert response.status_code == 200

    response = await async_client.get(f"/contracts/tenants/{tenant_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["product_id"] == product_id
    assert data["tenant_id"] == tenant_id
