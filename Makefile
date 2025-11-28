lint: ## Проверяет линтерами код в репозитории
	uvx --python 3.12 ruff check ./

format: ## Запуск автоформатера
	uvx --python 3.12 ruff check --fix ./

migrations: ## Создать миграции
	docker compose run --rm --workdir /opt/app/ backend alembic revision --autogenerate

migrate: ## Провести миграции
	docker compose run --rm --workdir /opt/app/ backend alembic upgrade head

test: ## Запустить тесты
	docker compose run --rm --workdir /opt/app/ backend-test pytest
