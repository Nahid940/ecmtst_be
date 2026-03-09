import uuid
import json
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from app.models.product import Product
from app.models.productReservation import ProductReservation
from app.core.redis import redis_client
from sqlalchemy import update

RESERVATION_TTL = 600  # 10 minutes

class ReservationService:

    @staticmethod
    async def reserve_product(db: AsyncSession, product_id: int, user_id: int, quantity: int):
        reservation_key = f"reservation:{user_id}:{product_id}"

        # Atomic inventory update in DB
        stmt = (
            update(Product)
            .where(Product.id == product_id, Product.available_inventory >= quantity)
            .values(available_inventory=Product.available_inventory - quantity)
        )
        result = await db.execute(stmt)

        if result.rowcount == 0:
            raise HTTPException(400, "Not enough inventory")

        await db.commit()

        # Create reservation in Redis
        existing = await redis_client.get(reservation_key)
        if existing:
            reservation_data = json.loads(existing)
            reservation_data["quantity"] += quantity
        else:
            # Fetch product for name and price (optional, already in DB)
            product = await db.get(Product, product_id)
            reservation_data = {
                "product_id": product_id,
                "user_id": user_id,
                "quantity": quantity,
                "name": product.name if product else "Unknown",
                "price": float(product.price) if product else 0.00
            }

        await redis_client.setex(reservation_key, RESERVATION_TTL, json.dumps(reservation_data))

        return {
            "reservation_id": str(uuid.uuid4()),
            "expires_in": RESERVATION_TTL
        }

    @staticmethod
    async def release_expired_reservations(db: AsyncSession):
        now = datetime.utcnow()
    
        result = await db.execute(
            ProductReservation.__table__.select().where(ProductReservation.expires_at <= now)
        )
        expired_reservations = result.scalars().all()

        for reservation in expired_reservations:
            product = await db.get(Product, reservation.product_id)
            if product:
                product.available_inventory += reservation.quantity
            await db.delete(reservation)

        await db.commit()