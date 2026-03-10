from pydantic import BaseModel

from typing import List, Optional
from datetime import datetime


class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int
    price: float

class OrderCreate(BaseModel):
    user_id: int
    items: List[OrderItemCreate]


# Response Schemas
class OrderItemResponse(BaseModel):
    id:int
    product_id: int
    name: str
    quantity: int
    price: float

    class Config:
        from_attributes = True   # (orm_mode=True in older versions)


class OrderResponse(BaseModel):
    id: int
    total_amount: float
    created_at : datetime
    created_date: str
    created_time: str
    items: List[OrderItemResponse]

    class Config:
        from_attributes = True