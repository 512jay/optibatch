
install:
	python -m venv env && \
	source env/bin/activate && \
	pip install -r requirements.txt

format:
	black . && ruff . && isort .

test:
	pytest

check:
	make format && ruff . && mypy . && make test
