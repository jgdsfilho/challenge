import uuid

from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlmodel import SQLModel, select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.logging import logging

logger = logging.getLogger(__name__)


async def fetch_instance_or_raise(
    instance_id: uuid.UUID, model: SQLModel, async_session: AsyncSession
):
    try:
        uuid.UUID(instance_id)
    except ValueError:
        logger.error(f"ID is not a valid UUID from {model.__name__}: {instance_id}")
        raise HTTPException(
            status_code=400, detail=f"ID is not a valid UUID from {model.__name__}"
        )

    instance = await async_session.get(model, instance_id)
    if not instance:
        logger.error(f"{model.__name__} not found: {instance_id}")
        raise HTTPException(status_code=404, detail=f"{model.__name__} not found")
    return instance


async def filter_instance_or_raise(
    model: SQLModel, async_session: AsyncSession, **filters
):
    query = select(model)
    for key, value in filters.items():
        query = query.filter(getattr(model, key) == value)

    results = await async_session.exec(query)
    instance = results.first()
    if not instance:
        logger.error(f"{model.__name__} not found: {filter}")
        raise HTTPException(status_code=404, detail=f"{model.__name__} not found")
    return instance


async def create_instance_with_integrity_check(
    instance: SQLModel, async_session: AsyncSession, auto_commit=True
):
    try:
        async_session.add(instance)
        if auto_commit:
            await async_session.commit()
        logger.info(
            f"{instance.__tablename__.capitalize()} instance created: {instance.id}"
        )
    except IntegrityError as e:
        await async_session.rollback()
        error_message = (
            "A unique constraint violation occurred, please check your input."
        )
        logger.error(f"Error creating instance: {e._message}")
        raise HTTPException(status_code=400, detail=error_message)

    return instance


async def update_last_product_price_to_false(
    product_id: uuid.UUID, model, async_session: AsyncSession
):
    last_product_price_query = (
        select(model)
        .filter(model.product_id == product_id)
        .filter(model.is_active == True)  # noqa: E712
    )
    results = await async_session.exec(last_product_price_query)

    last_product_price = results.first()
    if last_product_price:
        last_product_price.is_active = False
        async_session.add(last_product_price)

    return last_product_price
