from api import router
from database import Base, engine
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Order Management API",
    description="Тестовое задание: управление заказами",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


@app.get("/", tags=["root"])
async def root():
    """Корневой эндпоинт"""
    return {
        "message": "Order Management API",
        "version": "1.0.0",
        "docs": "/docs",
        "endpoints": {
            "add_item": "POST /api/v1/orders/{order_id}/items",
            "get_order": "GET /api/v1/orders/{order_id}",
            "get_product": "GET /api/v1/products/{product_id}",
            "get_client": "GET /api/v1/clients/{client_id}",
            "test_data": "GET /api/v1/test-data",
            "sql_queries": "GET /api/v1/sql/queries",
        },
    }


@app.get("/health", tags=["health"])
async def health_check():
    """Проверка здоровья приложения"""
    return {"status": "healthy", "service": "order-management"}
