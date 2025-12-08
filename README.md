# RAG Research Assistant Backend

A FastAPI-based Retrieval-Augmented Generation system for document Q&A with multiple LLM providers.

## Quick Start

### 1. Environment Setup
```bash
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Mac/Linux
pip install -r requirements.txt
```

### 2. Configuration
Create `.env` file:
```env
# MongoDB
MONGO_URI=mongodb://localhost:27017
MONGO_DB=rag_db

# LLM (choose one)
LLM_PROVIDER=GEMINI
LLM_MODEL=gemini-2.0-flash
LLM_API_KEY=your_key_here
```

### 3. Run Application
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/upload` | Upload PDF document |
| POST | `/api/v1/query` | Query documents with questions |
| GET | `/api/v1/chunks/{doc_id}` | Retrieve document chunks |

## LLM Providers

```env
# Gemini (Google)
LLM_PROVIDER=GEMINI
LLM_MODEL=gemini-2.0-flash

# Ollama (Local)
LLM_PROVIDER=OLLAMA
LLM_MODEL=llama3.2

# HuggingFace
LLM_PROVIDER=HUGGINGFACE
LLM_MODEL=google/gemma-2-2b-it
```

## Architecture

- **Document Processing**: PDF → Text → Chunks → Embeddings
- **Vector Store**: ChromaDB with cosine similarity
- **Metadata Store**: MongoDB for documents and chunks
- **LLM Integration**: Multiple provider support

## Project Structure
```
app/
├── routes/rag.py           # API endpoints
├── services/               # Business logic
│   ├── mongo_service.py   # MongoDB operations
│   ├── vector_service.py  # ChromaDB & embeddings
│   └── llm_service.py     # LLM integrations
└── utils/                  # Utilities
```

## Requirements
- Python 3.8+
- MongoDB
- LLM API key (for cloud providers)

## Access
- API: `http://localhost:8000/api/v1`
- Docs: `http://localhost:8000/docs`

---

**Note**: Configure AWS S3 credentials in `.env` for document storage functionality.
