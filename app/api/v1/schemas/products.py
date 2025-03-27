from uuid import UUID

from pydantic import BaseModel

from app.core.enums import UseUnit

from .base import BaseSchema


class ProductSchema(BaseSchema):
    name: str
    product_sku: str


class ProductSchemaCreate(BaseModel):
    name: str


class ProductSchemaUpdate(BaseModel):
    name: str


class ProductPriceSchema(BaseSchema):
    product_id: UUID
    price: float
    use_unity: UseUnit
    free_allocation: float


class ProductPriceSchemaCreate(BaseModel):
    product_id: UUID
    price: float
    use_unity: UseUnit
    free_allocation: float
