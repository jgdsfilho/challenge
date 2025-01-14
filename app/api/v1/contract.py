from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.api.v1.crud import (
    create_instance_with_integrity_check,
    filter_instance_or_raise,
)
from app.core.database import get_async_session
from app.models import Contract

contract_router = APIRouter()


@contract_router.post("/contracts", response_model=Contract)
async def create_contract(
    contract: Contract,
    session: Session = Depends(get_async_session),
):
    contract = Contract(
        tenant_id=contract.tenant_id,
        product_id=contract.product_id,
    )
    contract = await create_instance_with_integrity_check(contract, session)

    return contract


@contract_router.delete(
    "/contracts/tenants/{tenant_id}/products/{product_id}", status_code=204
)
async def delete_contract(
    tenant_id: str,
    product_id: str,
    session: Session = Depends(get_async_session),
):
    filters = {"tenant_id": tenant_id, "product_id": product_id}
    contract_instance = await filter_instance_or_raise(Contract, session, **filters)
    contract_instance.is_active = False
    session.add(contract_instance)
    await session.commit()
