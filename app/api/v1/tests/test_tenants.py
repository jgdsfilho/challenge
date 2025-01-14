import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession


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
    for key, value in payload.items():
        assert response.json()[key] == value


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
    assert response.status_code == 400
    assert response.json() == {
        "message": "Invalid body",
        "detail": f"{missing_field} is required",
    }


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
