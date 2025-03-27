from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.api.v1.crud import (
    create_instance_with_integrity_check,
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
