import uuid
import json
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from app.models.productReservation import ProductReservation
from app.models.product import Product
from app.core.redis import redis_client

RESERVATION_TTL = 60  # 1 minutes

class ReservationService:

    @staticmethod
    async def reserve_product(db: AsyncSession, product_id: int, user_id: int, quantity: int):
        
        product = await db.get(Product, product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")

        if product.available_inventory < quantity:
            raise HTTPException(status_code=400, detail="Not enough inventory")

        product.available_inventory -= quantity

        # expires_at = datetime.utcnow() + timedelta(minutes=RESERVATION_MINUTES)
        # reservation = ProductReservation(
        #     product_id=product_id,
        #     user_id=user_id,
        #     quantity=quantity,
        #     reserved_at=datetime.utcnow(),
        #     expires_at=expires_at
        # )
        # db.add(reservation)

        await db.commit()

        reservation_id = str(uuid.uuid4())

        reservation_data = {
            "product_id": product_id,
            "user_id": user_id,
            "quantity": quantity
        }

        # store in redis with expiration
        await redis_client.setex(
            f"reservation:{reservation_id}",
            RESERVATION_TTL,
            json.dumps(reservation_data)
        )

        # await db.refresh(reservation)

        return {
            "reservation_id": reservation_id,
            "expires_in": RESERVATION_TTL
        }

    @staticmethod
    async def release_expired_reservations(db: AsyncSession):
        """Call this periodically or via Celery/BackgroundTask"""
        now = datetime.utcnow()
        result = await db.execute(
            ProductReservation.__table__.select().where(ProductReservation.expires_at <= now)
        )
        expired_reservations = result.scalars().all()

        for reservation in expired_reservations:
            # Restore inventory
            product = await db.get(ProductReservation, reservation.product_id)
            if product:
                product.available_inventory += reservation.quantity
            # Delete reservation
            await db.delete(reservation)

        await db.commit()
