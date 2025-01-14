import datetime
import uuid

from sqlmodel import Field, SQLModel


def generate_uuid():
    return uuid.uuid4()


def generate_product_sku():
    return f"SKU-{str(uuid.uuid4().hex[:8].upper())}"


class BaseModel(SQLModel):
    id: uuid.UUID = Field(default_factory=generate_uuid, primary_key=True, unique=True)
    created_at: datetime.datetime = Field(
        default=datetime.datetime.utcnow(), nullable=False
    )
    updated_at: datetime.datetime = Field(
        default_factory=datetime.datetime.utcnow,
        nullable=False,
    )
