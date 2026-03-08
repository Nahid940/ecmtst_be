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

    @staticmethod
    async def create_product(db: AsyncSession, product: ProductCreate):
        db_product = Product(**product.dict())
        db.add(db_product)
        await db.commit()
        await db.refresh(db_product)
        return db_product

    @staticmethod
    async def update_product(db: AsyncSession, product_id: int, product: ProductUpdate):
        db_product = await db.get(Product, product_id)
        if db_product:
            for key, value in product.dict().items():
                setattr(db_product, key, value)
            await db.commit()
            await db.refresh(db_product)
        return db_product

    @staticmethod
    async def delete_product(db: AsyncSession, product_id: int):
        db_product = await db.get(Product, product_id)
        if db_product:
            await db.delete(db_product)
            await db.commit()
        return db_product