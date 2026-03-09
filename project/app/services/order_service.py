import json
from sqlalchemy import select
from app.models.order import Order
from app.models.orderDetails import OrderDetail
from app.models.product import Product  # for price lookup
from app.schemas.order_schema import OrderResponse
from app.core.redis import redis_client
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

class OrderService:

    @staticmethod
    async def create_order_from_redis(db: AsyncSession):

        user_id = 1

        keys = await redis_client.keys("reservation:*")
        if not keys:
            raise HTTPException(status_code=404, detail="Your cart is empty!!")

        order_items = []

        for key in keys:
            raw = await redis_client.get(key)
            if not raw:
                continue
            data = json.loads(raw)

            if data.get("user_id") != user_id:
                continue

            ttl = await redis_client.ttl(key)
            if ttl <= 0:
                continue

            order_items.append({
                "reservation_id": key,
                "product_id": data["product_id"],
                "quantity": data["quantity"]
            })

        if not order_items:
            raise Exception("No valid reservations available for checkout.")

        product_ids = [item["product_id"] for item in order_items]

        products = await db.execute(
            select(Product).where(Product.id.in_(product_ids))
        )
        products = products.scalars().all()

        product_map = {p.id: p for p in products}

        total_amount = 0
        for item in order_items:
            product = product_map.get(item["product_id"])
            if not product:
                raise Exception(f"Product {item['product_id']} not found.")
            item["price"] = float(product.price)
            item["name"] = product.name
            total_amount += item["price"] * item["quantity"]

        
        order = Order(
            user_id=user_id,
            total_amount=total_amount
        )
        db.add(order)
        await db.flush()

        for item in order_items:
            detail = OrderDetail(
                order_id=order.id,
                product_id=item["product_id"],
                quantity=item["quantity"],
                price=item["price"]
            )
            db.add(detail)

            # Remove reservation from Redis
            await redis_client.delete(item["reservation_id"])

        await db.commit()
        await db.refresh(order)

        return order