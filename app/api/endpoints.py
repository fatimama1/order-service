from api.dependencies import check_stock, get_order_or_404, get_product_or_404
from database import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from models import Client, Order, Product
from schemas import (
    AddItemRequest,
    AddItemResponse,
    ClientResponse,
    ItemResponse,
    OrderResponse,
    ProductResponse,
)
from services.order_service import OrderService
from sqlalchemy.orm import Session

router = APIRouter(prefix="/api/v1", tags=["api"])


@router.post(
    "/orders/{order_id}/items",
    response_model=AddItemResponse,
    status_code=status.HTTP_200_OK,
    summary="Добавить товар в заказ",
    description="""
    Добавляет товар в существующий заказ.
    
    - Если товар уже есть в заказе, увеличивает его количество
    - Если товара нет в наличии, возвращает ошибку 400
    - Если заказ или товар не найдены, возвращает ошибку 404
    """,
)
async def add_item_to_order(
    order_id: int, request: AddItemRequest, db: Session = Depends(get_db)
):
    order = get_order_or_404(order_id, db)
    product = get_product_or_404(request.product_id, db)
    check_stock(product, request.quantity)

    order_service = OrderService(db)
    result = order_service.add_item_to_order(order, product, request.quantity)

    return AddItemResponse(
        success=True,
        message="Товар успешно добавлен в заказ",
        order_id=order_id,
        item=ItemResponse(
            id=result["item_id"],
            product_id=product.id,
            quantity=result["quantity"],
            price_at_time=product.price,
            subtotal=result["subtotal"],
        ),
        order_total=result["order_total"],
    )


@router.get(
    "/orders/{order_id}",
    response_model=OrderResponse,
    summary="Получение информации о заказе.",
)
async def get_order(order_id: int, db: Session = Depends(get_db)):
    order = get_order_or_404(order_id, db)
    return OrderResponse(
        id=order.id,
        client_id=order.client_id,
        status=order.status,
        total_amount=order.total_amount,
        created_at=order.created_at,
    )


@router.get(
    "/products/{product_id}",
    response_model=ProductResponse,
    summary="Получение информации о товаре.",
)
async def get_product(product_id: int, db: Session = Depends(get_db)):
    product = get_product_or_404(product_id, db)
    return ProductResponse(
        id=product.id,
        name=product.name,
        quantity=product.quantity,
        price=product.price,
        category_id=product.category_id,
    )


@router.get(
    "/clients/{client_id}",
    response_model=ClientResponse,
    summary="Получение информации о клиенте.",
)
async def get_client(client_id: int, db: Session = Depends(get_db)):
    client = db.query(Client).filter(Client.id == client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Клиент не найден")

    return ClientResponse(id=client.id, name=client.name, address=client.address)


@router.get("/test-data", response_model=dict, summary="Получение тест инфы.")
async def test_data(db: Session = Depends(get_db)):
    products = db.query(Product).all()
    orders = db.query(Order).all()
    clients = db.query(Client).all()

    return {
        "products": [
            {
                "id": p.id,
                "name": p.name,
                "quantity": p.quantity,
                "price": float(p.price),
            }
            for p in products
        ],
        "orders": [
            {
                "id": o.id,
                "client_id": o.client_id,
                "total_amount": float(o.total_amount),
            }
            for o in orders
        ],
        "clients": [{"id": c.id, "name": c.name} for c in clients],
    }


# SQL запросы из ТЗ
@router.get(
    "/sql/queries",
    response_model=dict,
    summary="Выполнить SQL запросы из тестового задания.",
)
async def sql_queries(db: Session = Depends(get_db)):
    from models import Client, Order
    from sqlalchemy import func

    query_2_1 = (
        db.query(
            Client.name,
            func.coalesce(func.sum(Order.total_amount), 0).label("total_order_amount"),
        )
        .outerjoin(Order, Client.id == Order.client_id)
        .group_by(Client.id, Client.name)
        .all()
    )

    from models import Category
    from sqlalchemy import case

    subquery = (
        db.query(Category.parent_id, func.count(Category.id).label("child_count"))
        .filter(Category.parent_id.isnot(None))
        .group_by(Category.parent_id)
        .subquery()
    )

    query_2_2 = (
        db.query(
            Category.name,
            func.coalesce(subquery.c.child_count, 0).label("direct_children_count"),
        )
        .outerjoin(subquery, Category.id == subquery.c.parent_id)
        .order_by(Category.name)
        .all()
    )

    from datetime import datetime, timedelta

    from sqlalchemy import text

    last_month = datetime.now() - timedelta(days=30)

    top_5_query = text(
        """
        SELECT 
            p.name AS product_name,
            c.name AS top_level_category,
            SUM(oi.quantity) AS total_sold_quantity
        FROM order_items oi
        JOIN orders o ON oi.order_id = o.id
        JOIN products p ON oi.product_id = p.id
        LEFT JOIN categories cat ON p.category_id = cat.id
        LEFT JOIN categories c ON cat.parent_id = c.id
        WHERE o.created_at >= :last_month
        GROUP BY p.id, p.name, c.name
        ORDER BY total_sold_quantity DESC
        LIMIT 5
    """
    )

    query_2_3 = db.execute(top_5_query, {"last_month": last_month}).fetchall()

    return {
        "query_2_1": [
            {"client_name": row[0], "total_order_amount": float(row[1])}
            for row in query_2_1
        ],
        "query_2_2": [
            {"category_name": row[0], "direct_children_count": row[1]}
            for row in query_2_2
        ],
        "query_2_3": [
            {
                "product_name": row[0],
                "top_level_category": row[1],
                "total_sold_quantity": row[2],
            }
            for row in query_2_3
        ],
    }
