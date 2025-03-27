from http import HTTPStatus

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.schemas.tenants import TenantSchema


@pytest.mark.asyncio
async def test_create_tenant(
    async_client: AsyncClient,
    async_session: AsyncSession,
):
    payload = {"name": "tenant1", "email": "tenant1@my_domain.com"}
    response = await async_client.post(
        "/tenants",
        json=payload,
    )
    assert response.status_code == 200

    tenant = TenantSchema(**response.json())
    for key, value in payload.items():
        assert getattr(tenant, key) == value


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "payload,missing_field",
    [
        ({"namee": "tenant1", "email": "tenant1@my_domain.com"}, "Name"),
        ({"name": "tenant2", "emaill": "tenant2@my_domain.com"}, "Email"),
    ],
    ids=["missing_name", "missing_email"],
)
async def test_fail_create_tenant_with_error_payload(
    missing_field: str,
    payload: dict,
    async_client: AsyncClient,
    async_session: AsyncSession,
):
    response = await async_client.post(
        "/tenants",
        json=payload,
    )
    response_json = response.json()["detail"][0]
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert response_json["msg"] == "Field required"
    assert response_json["type"] == "missing"
    assert response_json["input"] == payload


@pytest.mark.asyncio
async def test_fail_create_tenant_when_already_exist_tenant(
    async_client: AsyncClient,
    async_session: AsyncSession,
):
    payload = {"name": "tenant1", "email": "tenant1@my_domain.com"}
    response = await async_client.post(
        "/tenants",
        json=payload,
    )
    assert response.status_code == 200

    response = await async_client.post(
        "/tenants",
        json=payload,
    )
    assert response.status_code == 400
    assert response.json() == {
        "detail": "A unique constraint violation occurred, please check your input.",
    }


@pytest.mark.asyncio
async def test_get_tenant_with_id(
    async_client: AsyncClient,
    async_session: AsyncSession,
):
    payload = {"name": "tenant1", "email": "tenant1@my_domain.com"}
    response = await async_client.post(
        "/tenants",
        json=payload,
    )
    assert response.status_code == 200
    tenant_id = response.json()["id"]

    response = await async_client.get(f"/tenants/{tenant_id}")
    assert response.status_code == 200
    tenant = TenantSchema(**response.json())
    for key, value in payload.items():
        assert getattr(tenant, key) == value


@pytest.mark.asyncio
async def test_get_tenant_with_email(
    async_client: AsyncClient,
    async_session: AsyncSession,
):
    payload = {"name": "tenant1", "email": "tenant1@my_domain.com"}
    response = await async_client.post(
        "/tenants",
        json=payload,
    )
    assert response.status_code == 200

    response = await async_client.get(f"/tenants/?email={payload['email']}")
    assert response.status_code == 200
    tenant = TenantSchema(**response.json())
    for key, value in payload.items():
        assert getattr(tenant, key) == value


@pytest.mark.asyncio
async def test_fail_get_tenant_with_email_not_exist(
    async_client: AsyncClient,
    async_session: AsyncSession,
):
    response = await async_client.get("/tenants/?email=tenant_not_exist@my_domain.com")
    assert response.status_code == 404
    assert response.json() == {"detail": "Tenant not found"}


@pytest.mark.asyncio
async def test_update_tenant(
    async_client: AsyncClient,
    async_session: AsyncSession,
):
    payload = {"name": "tenant1", "email": "tenant1@my_domain.com"}
    response = await async_client.post(
        "/tenants",
        json=payload,
    )
    assert response.status_code == 200
    tenant_id = response.json()["id"]

    payload["name"] = "tenant1_updated"
    response = await async_client.patch(f"/tenants/{tenant_id}", json=payload)
    assert response.status_code == 200
    tenant = TenantSchema(**response.json())
    for key, value in payload.items():
        assert getattr(tenant, key) == value
