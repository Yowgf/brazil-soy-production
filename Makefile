PYTEST_FLAGS ?=

install:
	pip install poetry poetry-core
	poetry config virtualenvs.in-project true
	poetry install

run:
	cd bsp && python3 app.py

lint:
	poetry run black bsp bsp/lib
	poetry run isort bsp bsp/lib

lint-check:
	poetry run flake8 --ignore=E501,W503 bsp
	poetry run isort --check-only bsp
	poetry run mypy bsp

unittest:
	poetry run pytest $(PYTEST_FLAGS)

test: unittest

check: lint-check test
ci/check: install check
