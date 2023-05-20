PYTEST_FLAGS ?=

install:
	pip install poetry poetry-core
	poetry config virtualenvs.in-project true
	poetry install

run:
	cd src && python3 app.py

lint:
	poetry run black src src/lib
	poetry run isort src src/lib

lint-check:
	poetry run flake8 --ignore=E501,W503 src
	poetry run isort --check-only src
	poetry run mypy src

unittest:
	poetry run pytest $(PYTEST_FLAGS)
test: unittest

check: lint-check test
ci/check: install check
