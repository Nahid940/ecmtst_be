import asyncio
from fastapi import FastAPI
from app.database.database import engine, Base
from app.routers import product_router
from app.admin.routers import product_router as admin_product_router
from app.routers import reservation_router
from app.routers import cart_router
from app.routers import order_router
from app.routers import auth_router
from app.workers.reservation_worker import reservation_listener

app = FastAPI(title="E-commerce Product API")

# Include product routes
app.include_router(product_router.router)
app.include_router(admin_product_router.router)
app.include_router(reservation_router.router)
app.include_router(cart_router.router)
app.include_router(order_router.router)
app.include_router(auth_router.router)


# Create tables
@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    asyncio.create_task(reservation_listener())
    


