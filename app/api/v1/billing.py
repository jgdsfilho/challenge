from datetime import datetime

from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.api.v1.crud import (
    create_instance_with_integrity_check,
)
from app.core.database import get_async_session
from app.models import Billing

billing_router = APIRouter()


@billing_router.post("/billings", response_model=Billing)
async def create_billing(
    billing: Billing,
    session: Session = Depends(get_async_session),
):
    billing_date = datetime.strptime(billing.billing_date, "%Y-%m-%d").date()

    billing = Billing(
        tenant_id=billing.tenant_id,
        total_billing=billing.total_billing,
        billing_date=billing_date,
    )
    billing = await create_instance_with_integrity_check(billing, session)

    return billing
