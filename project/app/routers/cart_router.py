from fastapi import APIRouter, Depends
from app.services.cart_service import CartService
from app.schemas.cart_schema import CartResponse
from app.database.database import get_db
from sqlalchemy.orm import Session
from app.core.security import get_current_user


router = APIRouter(prefix="/api", tags=["Cart"])


@router.get("/cart/", response_model=CartResponse)
async def get_cart(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    cart = await CartService.get_cart(current_user.id, db)
    return cart