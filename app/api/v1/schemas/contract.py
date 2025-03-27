from uuid import UUID

from pydantic import BaseModel

from .base import BaseSchema


class ContractSchema(BaseSchema):
    tenant_id: UUID
    product_id: UUID


class ContractSchemaCreate(BaseModel):
    tenant_id: UUID
    product_id: UUID
