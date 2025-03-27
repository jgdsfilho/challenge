from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.api.v1.crud import (
    create_instance_with_integrity_check,
    fetch_instance_or_raise,
    filter_instance_or_raise,
    update_last_product_price_to_false,
)
from app.api.v1.schemas.products import (
    ProductPriceSchema,
    ProductPriceSchemaCreate,
    ProductSchema,
    ProductSchemaCreate,
    ProductSchemaUpdate,
)
from app.core.database import get_async_session
from app.models import Product, ProductPrice

product_router = APIRouter()


@product_router.post("/products", response_model=ProductSchema)
async def ProductSchemaCreate(
    product: ProductSchemaCreate, session: Session = Depends(get_async_session)
):
    product = Product(**product.model_dump())
    product = await create_instance_with_integrity_check(product, session)
    await session.commit()

    return product


@product_router.patch("/products/{product_id}", response_model=ProductSchema)
async def update_product(
    product_id: str,
    product: ProductSchemaUpdate,
    session: Session = Depends(get_async_session),
):
    product_instance = await fetch_instance_or_raise(product_id, Product, session)

    product_instance.name = product.name
    session.add(product_instance)
    session.commit()
    return product_instance


@product_router.post("/products/{product_id}/prices", response_model=ProductPriceSchema)
async def create_product_price(
    product_id: str,
    product_price: ProductPriceSchemaCreate,
    session: Session = Depends(get_async_session),
):
    product_instance = await fetch_instance_or_raise(product_id, Product, session)

    product_price = ProductPrice(**product_price.model_dump())
    await update_last_product_price_to_false(product_instance.id, ProductPrice, session)

    product_price = await create_instance_with_integrity_check(
        product_price, session, auto_commit=False
    )
    await session.commit()

    return product_price


@product_router.get("/products/{product_id}", response_model=ProductSchema)
async def get_product(product_id: str, session: Session = Depends(get_async_session)):
    product_instance = await fetch_instance_or_raise(product_id, Product, session)
    return product_instance


@product_router.get("/products/", response_model=ProductSchema)
async def get_product_by_sku(
    product_sku: str, session: Session = Depends(get_async_session)
):
    filters = {"product_sku": product_sku}
    product_instance = await filter_instance_or_raise(Product, session, **filters)
    return product_instance


@product_router.get("/products/{product_id}/prices", response_model=ProductPriceSchema)
async def get_product_prices(
    product_id: str, session: Session = Depends(get_async_session)
):
    filters = {"product_id": product_id, "is_active": True}
    product_instance = await filter_instance_or_raise(ProductPrice, session, **filters)
    return product_instance
