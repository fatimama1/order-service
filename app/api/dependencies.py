from fastapi import HTTPException
from models import Order, Product
from sqlalchemy.orm import Session


def get_order_or_404(order_id: int, db: Session):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Заказ не найден")
    return order


def get_product_or_404(product_id: int, db: Session):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Товар не найден")
    return product


def check_stock(product: Product, quantity: int):
    if product.quantity < quantity:
        raise HTTPException(
            status_code=400,
            detail=f"Недостаточно товара на складе. Доступно: {product.quantity}",
        )
