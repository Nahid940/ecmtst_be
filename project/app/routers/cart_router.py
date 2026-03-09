from fastapi import APIRouter, Depends
from app.services.cart_service import CartService
from app.schemas.cart_schema import CartResponse
from app.database.database import get_db
from sqlalchemy.orm import Session


router = APIRouter(prefix="/api", tags=["Cart"])


@router.get("/cart/{user_id}", response_model=CartResponse)
async def get_cart(user_id: int, db: Session = Depends(get_db)):
    cart = await CartService.get_cart(user_id, db)
    return cart