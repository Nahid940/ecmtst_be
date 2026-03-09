from pydantic import BaseModel
from typing import Optional

class ProductBase(BaseModel):
    name: str
    price: float
    total_inventory: int = 0
    available_inventory: int = 0

class ProductCreate(ProductBase):
    pass

class ProductUpdate(ProductBase):
    pass

class ProductPartialUpdate(BaseModel):
    name: Optional[str]
    price: Optional[float]
    total_inventory: Optional[int]
    available_inventory: Optional[int]

class ProductOut(ProductBase):
    id: int

    class Config:
        orm_mode = True

class ProductResponse(BaseModel):
    status: str
    message: str
    product: ProductOut
