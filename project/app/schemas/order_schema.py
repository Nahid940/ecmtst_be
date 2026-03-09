from pydantic import BaseModel

from typing import List, Optional


class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int
    price: float

class OrderCreate(BaseModel):
    user_id: int
    items: List[OrderItemCreate]


# Response Schemas
class OrderItemResponse(BaseModel):
    product_id: int
    quantity: int
    price: float

    class Config:
        from_attributes = True   # (orm_mode=True in older versions)


class OrderResponse(BaseModel):
    id: int
    user_id: int
    total_amount: float
    items: List[OrderItemResponse]

    class Config:
        from_attributes = True