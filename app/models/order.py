from database import Base
from sqlalchemy import Column, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import relationship


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)
    status = Column(String(50), default="pending")
    total_amount = Column(Numeric(10, 2), default=0)
    created_at = Column(String, default="CURRENT_TIMESTAMP")

    client = relationship("Client", back_populates="orders")
    items = relationship("OrderItem", back_populates="order")
