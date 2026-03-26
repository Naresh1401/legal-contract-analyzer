.PHONY: install setup run-api run-dashboard run docker clean

install:
	pip install -r requirements.txt

setup: install
	python -m src.knowledge.sample_contracts
	python -m src.knowledge.legal_knowledge_loader

run-api:
	uvicorn src.api.app:app --reload --port 8000

run-dashboard:
	streamlit run src/dashboard/app.py --server.port 8501

run: run-api

docker:
	docker-compose up --build

clean:
	rm -rf data/chroma_db __pycache__ src/__pycache__ src/**/__pycache__
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
