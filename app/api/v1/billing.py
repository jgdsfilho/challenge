from datetime import date

from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.api.v1.crud import (
    create_instance_with_integrity_check,
    search_all_instances_or_raise,
)
from app.api.v1.schemas.billing import BillingSchema, BillingSchemaCreate
from app.core.database import get_async_session
from app.models import Billing

billing_router = APIRouter()


@billing_router.post("/billings", response_model=BillingSchema)
async def create_billing(
    billing: BillingSchemaCreate,
    session: Session = Depends(get_async_session),
):

    billing = Billing(**billing.model_dump())
    billing = await create_instance_with_integrity_check(billing, session)

    return billing


@billing_router.get(
    "/billings/tenants/{tenant_id}/", response_model=list[BillingSchema]
)
async def get_billings_by_tenant(
    tenant_id: str,
    billing_date: date | None = None,
    session: Session = Depends(get_async_session),
):
    filters = {"tenant_id": tenant_id}
    if billing_date:
        filters["billing_date"] = billing_date
    return await search_all_instances_or_raise(Billing, session, **filters)
