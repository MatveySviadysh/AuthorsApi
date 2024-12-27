.PHONY: install run test lint migrate clean format

install:
	pip install -r requirements.txt

run:
	uvicorn app.main:app --reload

test:
	pytest

lint:
	flake8 app tests
	black app tests --check

format:
	black app tests
	isort app tests

migrate:
	alembic upgrade head

clean:
	find . -type d -name __pycache__ -exec rm -r {} +
	find . -type f -name "*.pyc" -delete 