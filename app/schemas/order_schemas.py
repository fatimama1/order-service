from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, Field


class AddItemRequest(BaseModel):
    product_id: int = Field(..., gt=0, description="ID товара")
    quantity: int = Field(..., gt=0, description="Количество товара")


class ItemResponse(BaseModel):
    id: int
    product_id: int
    quantity: int
    price_at_time: Decimal
    subtotal: Decimal
    created_at: Optional[datetime] = None


class AddItemResponse(BaseModel):
    success: bool
    message: str
    order_id: int
    item: ItemResponse
    order_total: Decimal


class OrderResponse(BaseModel):
    id: int
    client_id: int
    status: str
    total_amount: Decimal
    created_at: datetime


class ProductResponse(BaseModel):
    id: int
    name: str
    quantity: int
    price: Decimal
    category_id: Optional[int] = None


class ClientResponse(BaseModel):
    id: int
    name: str
    address: Optional[str] = None
