-- Категории
CREATE TABLE IF NOT EXISTS categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    parent_id INTEGER REFERENCES categories(id)
);

-- Товары
CREATE TABLE IF NOT EXISTS products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    quantity INTEGER NOT NULL CHECK (quantity >= 0),
    price DECIMAL(10, 2) NOT NULL CHECK (price >= 0),
    category_id INTEGER REFERENCES categories(id)
);

-- Клиенты
CREATE TABLE IF NOT EXISTS clients (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    address TEXT
);

-- Заказы
CREATE TABLE IF NOT EXISTS orders (
    id SERIAL PRIMARY KEY,
    client_id INTEGER NOT NULL REFERENCES clients(id),
    status VARCHAR(50) DEFAULT 'pending',
    total_amount DECIMAL(10, 2) DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Позиции заказа
CREATE TABLE IF NOT EXISTS order_items (
    id SERIAL PRIMARY KEY,
    order_id INTEGER NOT NULL REFERENCES orders(id),
    product_id INTEGER NOT NULL REFERENCES products(id),
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    price_at_time DECIMAL(10, 2) NOT NULL,
    UNIQUE(order_id, product_id)
);

-- Тестовые данные
INSERT INTO categories (id, name, parent_id) VALUES
(1, 'Электроника', NULL),
(2, 'Компьютеры', 1),
(3, 'Телефоны', 1),
(4, 'Ноутбуки', 2),
(5, 'Компьютеры', 2),
(6, 'Смартфоны', 3),
(7, 'Кнопочные', 3)
ON CONFLICT (id) DO NOTHING;

INSERT INTO products (id, name, quantity, price, category_id) VALUES
(1, 'iPhone 15', 50, 99999.99, 6),
(2, 'MacBook Pro', 30, 149999.99, 4),
(3, 'Nokia 3310', 100, 4999.99, 7),
(4, 'Игровой ПК', 20, 79999.99, 5)
ON CONFLICT (id) DO NOTHING;

INSERT INTO clients (id, name, address) VALUES
(1, 'Иван Иванов', 'Москва, ул. Пушкина, 1'),
(2, 'Петр Петров', 'Санкт-Петербург, Невский пр., 10')
ON CONFLICT (id) DO NOTHING;

INSERT INTO orders (id, client_id, status, total_amount) VALUES
(1, 1, 'pending', 0),
(2, 2, 'completed', 249999.97)
ON CONFLICT (id) DO NOTHING;

INSERT INTO order_items (id, order_id, product_id, quantity, price_at_time) VALUES
(1, 2, 1, 1, 99999.99),
(2, 2, 2, 1, 149999.99)
ON CONFLICT (id) DO NOTHING;