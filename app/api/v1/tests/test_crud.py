import pytest
from app.api.v1.crud import (
    create_instance_with_integrity_check,
    fetch_instance_or_raise,
    filter_instance_or_raise,
    update_last_product_price_to_false,
)
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException


from app.models import Product, Tenant, ProductPrice, UseUnit


@pytest.mark.asyncio
async def test_fetch_instance_or_raise(
    async_session: AsyncSession,
):
    product = Product(name="test")
    async_session.add(product)
    await async_session.commit()
    product_instance = await fetch_instance_or_raise(
        str(product.id), Product, async_session
    )
    assert product_instance.id == product.id


@pytest.mark.asyncio
async def test_fail_fetch_instance_or_raise_invalid_uuid(
    async_session: AsyncSession,
):
    with pytest.raises(HTTPException):
        await fetch_instance_or_raise("invalid_uuid", Product, async_session)


@pytest.mark.asyncio
async def test_fail_fetch_instance_not_exist(
    async_session: AsyncSession,
):
    with pytest.raises(HTTPException):
        await fetch_instance_or_raise(
            "00000000-0000-0000-0000-000000000000", Product, async_session
        )


@pytest.mark.asyncio
async def test_filter_instance_or_raise(
    async_session: AsyncSession,
):
    product = Product(name="test")
    async_session.add(product)
    await async_session.commit()
    filters = {"name": "test"}
    product_instance = await filter_instance_or_raise(Product, async_session, **filters)
    assert product_instance.id == product.id


@pytest.mark.asyncio
async def test_fail_filter_instance_not_exist(
    async_session: AsyncSession,
):
    with pytest.raises(HTTPException):
        await filter_instance_or_raise(Product, async_session, name="invalid_name")


@pytest.mark.asyncio
async def test_create_instance_with_integrity_check(
    async_session: AsyncSession,
):
    product = Product(name="test")
    product = await create_instance_with_integrity_check(product, async_session)
    assert product.id is not None
    assert product.name == "test"


@pytest.mark.asyncio
async def test_fail_create_instance_with_integrity_check_integrity_error(
    async_session: AsyncSession,
):
    tenant = Tenant(name="test", email="test@test.com")
    tenant_2 = Tenant(name="test2", email="test@test.com")
    tenant = await create_instance_with_integrity_check(tenant, async_session)

    with pytest.raises(HTTPException):
        await create_instance_with_integrity_check(tenant_2, async_session)


@pytest.mark.asyncio
async def test_update_last_product_price_to_false(
    async_session: AsyncSession,
):
    product = Product(name="test")
    product = await create_instance_with_integrity_check(product, async_session)
    product_price = ProductPrice(
        product_id=product.id,
        price=10.0,
        free_allocation=10,
        use_unity=UseUnit.gb_mo,
    )
    product_price = await create_instance_with_integrity_check(
        product_price, async_session
    )
    await update_last_product_price_to_false(product.id, ProductPrice, async_session)
    last_product_price = await filter_instance_or_raise(
        ProductPrice, async_session, product_id=product.id
    )
    assert last_product_price.is_active is False
