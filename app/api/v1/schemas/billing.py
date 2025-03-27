from datetime import date
from uuid import UUID

from pydantic import BaseModel, field_serializer

from .base import BaseSchema


class BillingSchema(BaseSchema):
    tenant_id: UUID
    total_billing: float
    billing_date: date

    @field_serializer("billing_date")
    def serialize_billing_date(self, billing_date: date, _info) -> str:
        return billing_date.isoformat()


class BillingSchemaCreate(BaseModel):
    tenant_id: str
    total_billing: float
    billing_date: date
