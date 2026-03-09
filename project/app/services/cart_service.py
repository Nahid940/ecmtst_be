import json
import asyncio
from typing import List
from app.schemas.cart_schema import CartItem, CartResponse
from app.models.product import Product  # assuming you have a Product model
from sqlalchemy.orm import Session
from app.core.redis import redis_client

class CartService:
    @staticmethod

    async def get_cart(user_id: int, db: Session) -> CartResponse:
        """
        Retrieve all reservations for a user from Redis
        """
        # 1. Scan all reservation keys
        keys = await redis_client.keys("reservation:*")
        items: List[CartItem] = []

        for key in keys:
            # get reservation data
            data_raw = await redis_client.get(key)
            if not data_raw:
                continue
            data = json.loads(data_raw)

            if data.get("user_id") != user_id:
                continue  # skip other users

            # get remaining TTL in seconds
            remaining_seconds = await redis_client.ttl(key)
            if remaining_seconds <= 0:
                continue  # skip expired

            item = CartItem(
                reservation_id=key.split(":")[1],
                product_id=data["product_id"],
                quantity=data["quantity"],
                remaining_seconds=remaining_seconds,
                name= data['name'] if 'name' in data else "Unknown",
                price= data['price'] if 'price' in data else 0.00
            )
            items.append(item)

        return CartResponse(items=items)