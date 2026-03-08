from pydantic import BaseModel

class ProductBase(BaseModel):
    name: str
    price: float
    total_inventory: int = 0
    available_inventory: int = 0

class ProductCreate(ProductBase):
    pass

class ProductUpdate(ProductBase):
    pass

class ProductOut(ProductBase):
    id: int

    class Config:
        orm_mode = True