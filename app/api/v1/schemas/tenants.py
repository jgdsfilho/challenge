from pydantic import BaseModel

from .base import BaseSchema


class TenantSchema(BaseSchema):
    name: str
    email: str


class TenantSchemaCreate(BaseModel):
    name: str
    email: str


class TenantSchemaUpdate(BaseModel):
    name: str
