build:
	docker-compose build

up:
	docker-compose up -d

down:
	docker-compose down

run: down build up

logs:
	docker-compose logs -f

restart: down up

clean: down
	docker-compose rm -f
	docker volume rm $$(docker volume ls -q | grep order-service) 2>/dev/null || true

init-db:
	@echo "Инициализация базы данных..."
	docker-compose exec db psql -U postgres -d order_db -c "\dt"

shell:
	docker-compose exec app bash

psql:
	docker-compose exec db psql -U postgres -d order_db

lint:
	@echo "=== Запуск black ==="
	black --check app/
	@echo ""
	@echo "=== Запуск isort ==="
	isort --check-only app/
	@echo ""
	@echo "=== Запуск flake8 ==="
	flake8 app/
	@echo ""
	@echo "=== Запуск mypy ==="
	mypy app/

format:
	black app/
	isort app/

check: lint