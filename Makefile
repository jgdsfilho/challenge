CONTAINER_NAME=magalu-postgres
IMAGE_NAME=catalog_contract_api
POSTGRES_PORT=5432

run-postgres:
	docker run --name ${CONTAINER_NAME} -e POSTGRES_PASSWORD=postgres -e POSTGRES_USER=postgres -e POSTGRES_DB=postgres -p ${POSTGRES_PORT}:${POSTGRES_PORT} -d -v /var/lib/postgresql/data postgres 

stop-postgres:
	@if [ $$(docker ps -aq -f name=$(CONTAINER_NAME)) ]; then \
		docker stop $(CONTAINER_NAME); \
		docker rm $(CONTAINER_NAME); \
	fi

test:
	poetry run pytest -p no:warnings -v

migrations-generate:
	poetry run alembic revision --autogenerate -m "$(ARGS)"

migrations-upgrade:
	poetry run alembic upgrade head

migrations-downgrade:
	poetry run alembic downgrade -1

run-server:
	poetry run uvicorn app.main:app --reload --workers 1 --host 0.0.0.0 --port 8000

build:
	docker build -t $(IMAGE_NAME) .

run-container-api: build run-postgres
	docker run -d -p 8000:8000 --net=host -e DB_ASYNC_CONNECTION_STR=postgresql+asyncpg://postgres:postgres@localhost/postgres --name $(IMAGE_NAME) $(IMAGE_NAME)

lint:
	poetry run ruff check . --fix && poetry run black .

linst-check:
	poetry run ruff check . && poetry run black . --check