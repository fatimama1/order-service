from database import Base
from sqlalchemy import CheckConstraint, Column, ForeignKey, Integer, Numeric
from sqlalchemy.orm import relationship


class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    price_at_time = Column(Numeric(10, 2), nullable=False)

    __table_args__ = (CheckConstraint("quantity > 0", name="check_quantity_positive"),)

    order = relationship("Order", back_populates="items")
    product = relationship("Product", back_populates="order_items")
