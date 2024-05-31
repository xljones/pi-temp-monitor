.PHONY: install
install:
	python -m venv venv && \
	source venv/bin/activate && \
	python -m pip install -r requirements.txt

.PHONY: format
format:
	python -m isort app && \
	python -m black app

.PHONY: test
test: static-tests pytest

.PHONY: static-tests
static-tests:
	python -m flake8 app && \
	python -m mypy app && \
	python -m black --check app && \
	python -m isort --check app
