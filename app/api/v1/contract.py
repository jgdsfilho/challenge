from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.api.v1.crud import (
    create_instance_with_integrity_check,
    filter_instance_or_raise,
)
from app.api.v1.schemas.contract import ContractSchema, ContractSchemaCreate
from app.core.database import get_async_session
from app.models import Contract

contract_router = APIRouter()


@contract_router.post("/contracts", response_model=ContractSchema)
async def create_contract(
    contract: ContractSchemaCreate,
    session: Session = Depends(get_async_session),
) -> ContractSchema:
    contract = Contract(**contract.model_dump())
    contract = await create_instance_with_integrity_check(contract, session)

    return contract


@contract_router.delete(
    "/contracts/tenants/{tenant_id}/products/{product_id}", status_code=204
)
async def delete_contract(
    tenant_id: str,
    product_id: str,
    session: Session = Depends(get_async_session),
) -> None:
    filters = {"tenant_id": tenant_id, "product_id": product_id}
    contract_instance = await filter_instance_or_raise(Contract, session, **filters)
    contract_instance.is_active = False
    session.add(contract_instance)
    await session.commit()


@contract_router.get("/contracts/tenants/{tenant_id}", response_model=ContractSchema)
async def get_contract_by_tenant(
    tenant_id: str,
    session: Session = Depends(get_async_session),
) -> ContractSchema:
    filters = {"tenant_id": tenant_id}
    contract_instance = await filter_instance_or_raise(Contract, session, **filters)
    return contract_instance
