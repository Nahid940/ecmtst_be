from fastapi import FastAPI
from app.database.database import engine, Base
from app.routers import product_router
from app.admin.routers import product_router as admin_product_router
from app.routers import reservation_router
import asyncio

app = FastAPI(title="E-commerce Product API")

# Include product routes
app.include_router(product_router.router)
app.include_router(admin_product_router.router)
app.include_router(reservation_router.router)


# Create tables
@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)