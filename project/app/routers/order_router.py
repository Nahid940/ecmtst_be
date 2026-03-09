from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.services.order_service import OrderService

router = APIRouter(prefix="/api", tags=["Checkout"])

@router.post("/checkout")
async def checkout(db: Session = Depends(get_db)):
    order = await OrderService.create_order_from_redis(db)
    return {
        "order_id": order.id,
        "total_amount": float(order.total_amount),
        "message": "Order successfully created!"
    }