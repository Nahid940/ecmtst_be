from pydantic import BaseModel
from typing import List


class CartItem(BaseModel):
    reservation_id: str
    product_id: int
    quantity: int
    remaining_seconds: int
    name: str = None  # optional, from product DB
    price: float = None  # optional, from product DB


class CartResponse(BaseModel):
    items: List[CartItem]