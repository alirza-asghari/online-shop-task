from sqlalchemy import Column, Integer, ForeignKey, Float, DateTime, func
from sqlalchemy.orm import relationship
from database.database_connection import Base


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False, default=1)
    total_price = Column(Float, nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)

    # Relationships
    user = relationship("User", back_populates="orders")  # Link to the User model
    product = relationship("Product", back_populates="orders")  # Link to the Product model
