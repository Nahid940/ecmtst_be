from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.product_schema import ProductCreate, ProductUpdate, ProductOut, ProductResponse, ProductPartialUpdate
from app.admin.products.product_service import ProductService
from app.database.database import get_db

router = APIRouter(prefix="/api/admin/products", tags=["Products"])

@router.get("/", response_model=list[ProductOut])
async def list_products(db: AsyncSession = Depends(get_db)):
    return await ProductService.get_products(db)

@router.get("/{product_id}", response_model=ProductOut)
async def get_product(product_id: int, db: AsyncSession = Depends(get_db)):
    product = await ProductService.get_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.post("/", response_model=ProductResponse)
async def create_product(product: ProductCreate, db: AsyncSession = Depends(get_db)):
    return await ProductService.create_product(db, product)

@router.put("/{product_id}", response_model=ProductOut)
async def update_product(product_id: int, product: ProductUpdate, db: AsyncSession = Depends(get_db)):
    updated = await ProductService.update_product(db, product_id, product)
    if not updated:
        raise HTTPException(status_code=404, detail="Product not found")
    return updated

@router.patch("/{product_id}", response_model=ProductOut)
async def partial_update_product(product_id: int, product: ProductUpdate, db: AsyncSession = Depends(get_db)):
    updated = await ProductService.partial_update_product(db, product_id, product)
    if not updated:
        raise HTTPException(status_code=404, detail="Product not found")
    return updated

@router.delete("/{product_id}", response_model=ProductOut)
async def delete_product(product_id: int, db: AsyncSession = Depends(get_db)):
    deleted = await ProductService.delete_product(db, product_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Product not found")
    return deleted