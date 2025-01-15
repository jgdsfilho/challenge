from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from app.api.v1.billing import billing_router
from app.api.v1.contract import contract_router
from app.api.v1.products import product_router
from app.api.v1.tenants import tenant_router
from app.core.database import init_db
from app.core.exceptions import InvalidBody
from app.core.logging import logging

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(tenant_router, prefix="/v1", tags=["Tenats"])
app.include_router(product_router, prefix="/v1", tags=["Products"])
app.include_router(contract_router, prefix="/v1", tags=["Contracts"])
app.include_router(billing_router, prefix="/v1", tags=["Billing"])


@app.exception_handler(InvalidBody)
async def invalid_body_handler(request, exc: InvalidBody):
    logger.warning(f"Invalid body: {exc.message}")
    return JSONResponse(
        status_code=400,
        content={"message": "Invalid body", "detail": exc.message},
    )


@app.get("/ping")
async def pong():
    return {"ping": "pong!"}
