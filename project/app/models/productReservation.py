from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from app.database.database import Base
from sqlalchemy.orm import relationship
from datetime import datetime

class ProductReservation(Base):
    __tablename__ = "product_reservations"

    id          = Column(Integer, primary_key=True, index=True)
    product_id  = Column(Integer, ForeignKey("products.id"))
    user_id     = Column(Integer)
    quantity    = Column(Integer)
    reserved_at = Column(DateTime, default=datetime.utcnow)
    expires_at  = Column(DateTime)

    product     = relationship("Product", back_populates="productReservations")