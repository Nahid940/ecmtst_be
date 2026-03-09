from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.product import Product
from app.schemas.product_schema import ProductCreate, ProductUpdate

class ProductService:

    @staticmethod
    async def get_products(db: AsyncSession):
        result = await db.execute(select(Product))
        return result.scalars().all()

    @staticmethod
    async def get_product(db: AsyncSession, product_id: int):
        result = await db.get(Product, product_id)
        return result