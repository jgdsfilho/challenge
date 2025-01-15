import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession


@pytest.mark.asyncio
async def test_create_billing(async_client: AsyncClient, async_session: AsyncSession):
    response = await async_client.post(
        "/tenants",
        json={"name": "tenant1", "email": "tenant1@my_domain.com"},
    )
    assert response.status_code == 200
    tenant_id = response.json()["id"]

    payload = {
        "tenant_id": tenant_id,
        "total_billing": 10.1,
        "billing_date": "2021-01-01",
    }
    response = await async_client.post(
        "/billings",
        json=payload,
    )
    assert response.status_code == 200
    data = response.json()
    for key in payload:
        assert data[key] == payload[key]
