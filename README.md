# AI-Powered Legal Contract Analyzer

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![LangChain](https://img.shields.io/badge/LangChain-0.2+-green.svg)](https://python.langchain.com/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-teal.svg)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.35+-red.svg)](https://streamlit.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

An LLM-powered contract review system with clause extraction, risk identification, compliance checking, and contract comparison — built with **LangChain** and **Retrieval-Augmented Generation (RAG)**.

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    Streamlit Dashboard                          │
│  ┌──────────┐ ┌──────────┐ ┌───────────┐ ┌──────────────────┐  │
│  │ Upload   │ │ Clause   │ │ Risk      │ │ Compliance       │  │
│  │ Contract │ │ Viewer   │ │ Dashboard │ │ Checker          │  │
│  └────┬─────┘ └────┬─────┘ └─────┬─────┘ └───────┬──────────┘  │
│       │             │             │               │             │
├───────┴─────────────┴─────────────┴───────────────┴─────────────┤
│                      FastAPI Backend                            │
│  /analyze/clauses  /analyze/risks  /check/compliance            │
│  /compare          /summarize      /health                      │
├─────────────────────────────────────────────────────────────────┤
│                     LangChain Agents                            │
│  ┌───────────┐ ┌────────────┐ ┌────────────┐ ┌──────────────┐  │
│  │ Clause    │ │ Risk       │ │ Compliance │ │ Contract     │  │
│  │ Extractor │ │ Analyzer   │ │ Checker    │ │ Comparator   │  │
│  └─────┬─────┘ └──────┬─────┘ └──────┬─────┘ └──────┬───────┘  │
│        │               │              │              │          │
│  ┌─────┴───────────────┴──────────────┴──────────────┴───────┐  │
│  │              Summary Generator                            │  │
│  └───────────────────────┬───────────────────────────────────┘  │
├──────────────────────────┼──────────────────────────────────────┤
│                    RAG Pipeline                                 │
│  ┌───────────────┐  ┌────────────┐  ┌─────────────────────┐    │
│  │ Legal Knowledge│  │ ChromaDB   │  │ OpenAI Embeddings   │    │
│  │ Base (PDFs,   │──│ Vector     │──│ + GPT-4 LLM         │    │
│  │ Templates)    │  │ Store      │  │                     │    │
│  └───────────────┘  └────────────┘  └─────────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
```

## Features

- **Clause Extraction** — Automatically identifies and extracts key contractual clauses (parties, term, indemnification, IP, payment, SLA, etc.) into structured JSON
- **Risk Analysis** — Flags missing clauses, one-sided terms, unlimited liability exposure, and weak termination rights with severity scoring
- **Compliance Checking** — Validates contracts against GDPR, SOC 2, and industry-specific regulatory frameworks with gap analysis
- **Contract Comparison** — Side-by-side diff of two contracts highlighting advantageous/disadvantageous changes with redline summary
- **Executive Summary** — Generates concise summaries with key terms, obligations per party, deadlines, and recommended actions
- **RAG-Powered** — Legal knowledge base with contract templates and regulatory guidelines for context-aware analysis

## Quick Start

### 1. Clone & Install

```bash
git clone https://github.com/nareshsampangi/legal-contract-analyzer.git
cd legal-contract-analyzer
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
cp .env.example .env
# Edit .env and add your OpenAI API key
```

### 3. Initialize Knowledge Base

```python
python -m src.knowledge.sample_contracts      # Generate sample contracts
python -m src.knowledge.legal_knowledge_loader # Build vector store
```

### 4. Run the API

```bash
uvicorn src.api.app:app --reload --port 8000
```

### 5. Launch Dashboard

```bash
streamlit run src/dashboard/app.py --server.port 8501
```

### Docker

```bash
docker-compose up --build
```

## API Endpoints

| Method | Endpoint             | Description               |
|--------|----------------------|---------------------------|
| POST   | `/analyze/clauses`   | Extract contract clauses  |
| POST   | `/analyze/risks`     | Identify risks            |
| POST   | `/check/compliance`  | Compliance gap analysis   |
| POST   | `/compare`           | Compare two contracts     |
| POST   | `/summarize`         | Executive summary         |
| GET    | `/health`            | Health check              |

## Project Structure

```
legal-contract-analyzer/
├── src/
│   ├── agents/
│   │   ├── clause_extractor.py
│   │   ├── risk_analyzer.py
│   │   ├── compliance_checker.py
│   │   ├── contract_comparator.py
│   │   └── summary_generator.py
│   ├── knowledge/
│   │   ├── legal_knowledge_loader.py
│   │   └── sample_contracts.py
│   ├── api/
│   │   └── app.py
│   └── dashboard/
│       └── app.py
├── data/
│   └── contracts/
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── Makefile
└── README.md
```

## Tech Stack

- **LLM Orchestration**: LangChain + LangChain OpenAI
- **Vector Store**: ChromaDB
- **Embeddings**: OpenAI text-embedding-3-small
- **LLM**: GPT-4o
- **Backend**: FastAPI
- **Frontend**: Streamlit
- **Document Parsing**: PyPDF, docx2txt

## Author

**Naresh Sampangi**

## License

This project is licensed under the MIT License.
