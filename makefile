run:
	poetry run python3 main.py

install:
	pip install poetry
	poetry install

format:
	poetry run black .
	poetry run isort .

test:
	poetry run pytest