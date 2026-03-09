# app/services/user_service.py
from select import select

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from app.models.user import User
from app.core.hash import hash_password, verify_password
from app.core.security import create_access_token
from sqlalchemy import select
from app.models.user import User

class UserService:

    @staticmethod
    async def register(db: AsyncSession, user_data):
        # Check if email exists
        existing = await db.execute(
            User.__table__.select().where(User.email == user_data.email)
        )
        if existing.scalars().first():
            raise HTTPException(400, "Email already registered")

        new_user = User(
            name        = user_data.name,
            email       = user_data.email,
            password    = hash_password(user_data.password)
        )
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)
        return new_user


    @staticmethod
    async def login(db: AsyncSession, email: str, password: str):
        result = await db.execute(
            select(User).where(User.email == email)
        )
        user = result.scalars().first()
        if not user or not verify_password(password, user.password):
            raise HTTPException(401, "Invalid credentials")

        token = create_access_token({"user_id": user.id, "email": user.email})
        return {"access_token": token, "token_type": "bearer"}