from fastapi import FastAPI
from app.database.database import engine, Base
from app.routers import product_router
import asyncio

app = FastAPI(title="E-commerce Product API")

# Include product routes
app.include_router(product_router.router)

# Create tables
@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)