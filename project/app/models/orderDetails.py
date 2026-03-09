from sqlalchemy import Column, Integer, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from app.database.database import Base


class OrderDetail(Base):
    __tablename__ = "order_details"

    id = Column(Integer, primary_key=True, index=True)

    order_id = Column(Integer, ForeignKey("orders.id"))

    product_id = Column(Integer)

    quantity = Column(Integer)

    price = Column(Numeric(10,2))

    order = relationship("Order", back_populates="items")