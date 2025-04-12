
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

.PHONY: init-db ingest query

init-db:
	@echo "📦 Creating tables in PostgreSQL..."
	python -m database.init_db

ingest:
	@echo "📂 Ingesting latest job folder..."
	python -m ingestion.ingest_job data/sample_job

query:
	@echo "🔍 Checking DB contents..."
	python -m dev.tools.query
