from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database.database_connection import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    orders = relationship("Order", back_populates="product")