from models import OrderItem
from sqlalchemy.orm import Session


class OrderService:
    """Сервис для работы с заказами"""

    def __init__(self, db: Session):
        self.db = db

    def add_item_to_order(self, order, product, quantity):
        """
        Добавляет товар в заказ

        Args:
            order: Объект заказа
            product: Объект товара
            quantity: Количество

        Returns:
            dict: Результат операции
        """
        existing_item = None
        for item in order.items:
            if item.product_id == product.id:
                existing_item = item
                break

        try:
            if existing_item:
                existing_item.quantity += quantity
                existing_item.price_at_time = product.price
                item = existing_item
                self.db.add(item)
            else:
                item = OrderItem(
                    order_id=order.id,
                    product_id=product.id,
                    quantity=quantity,
                    price_at_time=product.price,
                )
                self.db.add(item)

            product.quantity -= quantity

            self.db.commit()
            self.db.refresh(item)
            self.db.refresh(order)

            self._recalculate_order_total(order)

            return {
                "item_id": item.id,
                "quantity": item.quantity,
                "subtotal": float(item.quantity * item.price_at_time),
                "order_total": float(order.total_amount),
            }

        except Exception as e:
            self.db.rollback()
            raise

    def _recalculate_order_total(self, order):
        """Пересчитать общую сумму заказа"""
        total = sum(item.quantity * item.price_at_time for item in order.items)
        order.total_amount = total
        self.db.commit()
        self.db.refresh(order)
