from sqlalchemy import Column, Integer, String, Float
from app.database.database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    price = Column(Float, nullable=False)
    total_inventory = Column(Integer, default=0)
    available_inventory = Column(Integer, default=0)