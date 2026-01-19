from database import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship


class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    address = Column(String)

    orders = relationship("Order", back_populates="client")
