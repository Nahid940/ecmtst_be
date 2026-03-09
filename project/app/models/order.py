from sqlalchemy import Column, Integer, Numeric, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship
from app.database.database import Base


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    total_amount = Column(Numeric(10, 2), nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="orders")
    
    items = relationship(
        "OrderDetail",
        back_populates="order",
        cascade="all, delete-orphan"
    )