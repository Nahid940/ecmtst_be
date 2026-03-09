from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.database import get_db
from app.services.reservation_service import ReservationService
from app.schemas.reserve_schema import ReserveRequest

router = APIRouter(prefix="/api/reserve", tags=["Reserve"])

# @router.post("/product/{product_id}")
# async def reserve_product_router(product_id: int, 
#         request  : ReserveRequest,
#         db: AsyncSession = Depends(get_db)):
#     reservation = await ReservationService.reserve_product(db, product_id, request.user_id, request.quantity)
#     return {
#         "message": "Product reserved",
#         "reservation_id": reservation.id,
#         "expires_at": reservation.expires_at
#     }

@router.post("/product/{product_id}")
async def reserve_product_router(product_id: int, request: ReserveRequest, db: AsyncSession = Depends(get_db)):

    reservation = await ReservationService.reserve_product(
        db,
        product_id,
        request.user_id,
        request.quantity
    )

    return {
        "message": "Product reserved",
        **reservation
    }
