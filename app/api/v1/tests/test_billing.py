import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.schemas.billing import BillingSchema
from app.api.v1.schemas.tenants import TenantSchema


@pytest.mark.asyncio
async def test_create_billing(async_client: AsyncClient, async_session: AsyncSession):
    response = await async_client.post(
        "/tenants",
        json={"name": "tenant1", "email": "tenant1@my_domain.com"},
    )
    assert response.status_code == 200
    tenant = TenantSchema(**response.json())

    payload = {
        "tenant_id": str(tenant.id),
        "total_billing": 10.1,
        "billing_date": "2021-01-01",
    }
    response = await async_client.post(
        "/billings",
        json=payload,
    )
    assert response.status_code == 200
    billing = BillingSchema(**response.json()).model_dump()
    assert billing["tenant_id"] == tenant.id
    assert billing["total_billing"] == 10.1
    assert billing["billing_date"] == "2021-01-01"
