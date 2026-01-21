.PHONY: install test lint run docker-build docker-up

install:
	python -m pip install -e ".[dev]"

test:
	python -m pytest

lint:
	python -m ruff check .

run:
	uvicorn app.main:app --reload

docker-build:
	docker build -t ai-native-microservice:local .

docker-up:
	docker compose up --build
