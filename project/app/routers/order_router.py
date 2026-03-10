from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session, selectinload
from app.database.database import get_db
from app.services.order_service import OrderService
from app.core.security import get_current_user
from app.models import Order, OrderDetail
from app.schemas.order_schema import OrderResponse, OrderItemResponse
from typing import List
from sqlalchemy.future import select

router = APIRouter(prefix="/api", tags=["Checkout"])

@router.post("/checkout")
async def checkout(db: Session = Depends(get_db)):
    order = await OrderService.create_order_from_redis(db)
    return {
        "order_id": order.id,
        "total_amount": float(order.total_amount),
        "message": "Order successfully created!"
    }

@router.get("/orders", response_model=List[OrderResponse])
async def get_orders(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    # Fetch orders
    result = await db.execute(
        select(Order)
        .options(selectinload(Order.items).selectinload(OrderDetail.product))
        .where(Order.user_id == current_user.id)
    )

    orders = result.scalars().all()

    orders_response = []

    for order in orders:
        # Load items
        await db.refresh(order, attribute_names=["items"])

        items_list = []
        for item in order.items:
            # Load related product
            await db.refresh(item, attribute_names=["product"])
            items_list.append(OrderItemResponse(
                id=item.id,
                product_id=item.product_id,
                name=item.product.name,
                quantity=item.quantity,
                price=item.product.price
            ))

        orders_response.append(OrderResponse(
            id      = order.id,
            total_amount    = order.total_amount,
            created_at      = order.created_at,
            created_date    = order.created_at.date().isoformat(),
            created_time    = order.created_at.time().strftime("%H:%M:%S"),
            items           = items_list
        ))

    return orders_response