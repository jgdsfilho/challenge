from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.api.v1.crud import (
    create_instance_with_integrity_check,
    fetch_instance_or_raise,
    update_last_product_price_to_false,
)
from app.core.database import get_async_session
from app.models import Product, ProductPrice

product_router = APIRouter()


@product_router.post("/products", response_model=Product)
async def create_product(
    product: Product, session: Session = Depends(get_async_session)
):
    product = Product(name=product.name)
    product = await create_instance_with_integrity_check(product, session)
    await session.commit()

    return product


@product_router.patch("/products/{product_id}", response_model=Product)
async def update_product(
    product_id: str, product: Product, session: Session = Depends(get_async_session)
):
    product_instance = await fetch_instance_or_raise(product_id, Product, session)

    product_instance.name = product.name
    session.add(product_instance)
    session.commit()
    return product_instance


@product_router.post("/products/{product_id}/prices", response_model=ProductPrice)
async def create_product_price(
    product_id: str,
    product_price: ProductPrice,
    session: Session = Depends(get_async_session),
):
    product_instance = await fetch_instance_or_raise(product_id, Product, session)
    from app.core.enums import UseUnit

    product_price = ProductPrice(
        product_id=product_instance.id,
        price=product_price.price,
        free_allocation=product_price.free_allocation,
        use_unity=UseUnit(product_price.use_unity),
    )
    await update_last_product_price_to_false(product_instance.id, ProductPrice, session)

    product_price = await create_instance_with_integrity_check(
        product_price, session, auto_commit=False
    )
    await session.commit()

    return product_price
