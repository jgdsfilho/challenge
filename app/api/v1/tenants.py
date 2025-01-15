from fastapi import APIRouter, Depends
from sqlmodel import Session
from sqlmodel.ext.asyncio.session import AsyncSession

from app.api.v1.crud import (
    create_instance_with_integrity_check,
    fetch_instance_or_raise,
    filter_instance_or_raise,
)
from app.core.database import get_async_session
from app.models import Tenant

tenant_router = APIRouter()


@tenant_router.post("/tenants", response_model=Tenant)
async def create_tenant(
    tenant: Tenant, session: AsyncSession = Depends(get_async_session)
):
    tenant = Tenant(name=tenant.name, email=tenant.email)
    tenant = await create_instance_with_integrity_check(tenant, session)
    await session.commit()
    return tenant


@tenant_router.patch("/tenants/{tenant_id}", response_model=Tenant)
async def update_tenant(
    tenant_id: str, tenant: Tenant, session: Session = Depends(get_async_session)
):
    tenant_instace = await fetch_instance_or_raise(tenant_id, Tenant, session)

    tenant_instace.name = tenant.name
    session.add(tenant_instace)
    await session.commit()
    return tenant_instace


@tenant_router.get("/tenants/{tenant_id}", response_model=Tenant)
async def get_tenant(tenant_id: str, session: Session = Depends(get_async_session)):
    tenant_instance = await fetch_instance_or_raise(tenant_id, Tenant, session)
    return tenant_instance


@tenant_router.get("/tenants/", response_model=Tenant)
async def get_tenant_by_email(
    email: str, session: Session = Depends(get_async_session)
):
    filters = {"email": email}
    tenant_instance = await filter_instance_or_raise(Tenant, session, **filters)
    return tenant_instance
