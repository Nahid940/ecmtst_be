from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.product import Product
from app.schemas.product_schema import ProductCreate, ProductUpdate, ProductPartialUpdate

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
        return {
            "status"  : "success",
            "message" : "Product Created Successfully",
            "product": {
                "id": db_product.id,
                "name": db_product.name,
                "price": db_product.price,
                "total_inventory": db_product.total_inventory,
                "available_inventory": db_product.available_inventory,
            }
        }

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
    async def partial_update_product(db: AsyncSession, product_id: int, product: ProductPartialUpdate):
        db_product = await db.get(Product, product_id)
        if db_product:
            for field, value in product.dict(exclude_unset=True).items():
                setattr(db_product, field, value)
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