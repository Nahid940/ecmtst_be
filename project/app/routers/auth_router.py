# app/routers/auth_router.py
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.user_schema import UserCreate, UserLogin, Token
from app.services.user_service import UserService
from app.database.database import get_db

router = APIRouter(prefix="/api/auth", tags=["Auth"])

@router.post("/register", response_model=Token)
async def register(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    user = await UserService.register(db, user_data)
    token = await UserService.login(db, user_data.email, user_data.password)
    return token

@router.post("/login", response_model=Token)
async def login(user_data: UserLogin, db: AsyncSession = Depends(get_db)):
    return await UserService.login(db, user_data.email, user_data.password)