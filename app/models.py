import datetime
import uuid
from decimal import Decimal

from sqlalchemy.orm import validates
from sqlalchemy.schema import Index
from sqlmodel import Column, Enum, Field

from app.core.enums import UseUnit
from app.core.exceptions import InvalidBody
from app.core.models import BaseModel, generate_product_sku


class Tenant(BaseModel, table=True):
    __tablename__ = "tenants"

    name: str = Field(nullable=False)
    email: str = Field(unique=True, nullable=False)

    @validates("email")
    def validate_email(self, key, email):
        if not email:
            raise InvalidBody("Email is required")
        return email

    @validates("name")
    def validate_name(self, key, name):
        if not name:
            raise InvalidBody("Name is required")
        return name


class Product(BaseModel, table=True):
    __tablename__ = "products"

    name: str = Field(unique=True, index=True)
    product_sku: str = Field(
        unique=True, index=True, nullable=False, default_factory=generate_product_sku
    )


class ProductPrice(BaseModel, table=True):
    __tablename__ = "product_prices"

    product_id: uuid.UUID = Field(foreign_key="products.id")
    price: float = Field(nullable=False)
    use_unity: UseUnit = Field(sa_column=Column(Enum(UseUnit)))
    free_allocation: float = Field(default=Decimal(0.0))
    is_active: bool = Field(default=True)

    @validates("price")
    def validate_price(self, key, price):
        if price < 0:
            raise ValueError("Price must be positive")
        return price


Index(
    "uq_prices_per_product",
    ProductPrice.is_active,
    ProductPrice.product_id,
    unique=True,
    postgresql_where=(ProductPrice.is_active == True),  # noqa: E712
)


class Contract(BaseModel, table=True):
    __tablename__ = "contracts"

    tenant_id: uuid.UUID = Field(foreign_key="tenants.id")
    product_id: uuid.UUID = Field(foreign_key="products.id")
    is_active: bool = True


Index(
    "uq_active_contract_tenant_product_active",
    Contract.tenant_id,
    Contract.product_id,
    Contract.is_active,
    unique=True,
    postgresql_where=(Contract.is_active == True),  # noqa: E712
)


class Billing(BaseModel, table=True):
    __tablename__ = "billings"

    tenant_id: uuid.UUID = Field(foreign_key="tenants.id")
    total_billing: float = Field(nullable=False)
    billing_date: datetime.date = Field(nullable=False)
    is_active: bool = True


Index(
    "uq_active_billing_tenant",
    Billing.tenant_id,
    Billing.is_active,
    Billing.billing_date,
    unique=True,
    postgresql_where=(Billing.is_active == True),  # noqa: E712
)
