# RAG Research Assistant

A complete Retrieval-Augmented Generation system with FastAPI backend and Streamlit frontend for intelligent document Q&A.

## Quick Start

### 1. Clone & Setup Backend
```bash
git clone https://github.com/muhammedafsalpm/rag-research-assistant.git
cd rag-research-assistant/backend

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Configure environment (edit with your API keys)
copy .env.example .env  # Windows
# cp .env.example .env  # Mac/Linux
```

### 2. Configure Environment
Edit `backend/.env`:
```env
# MongoDB (required)
MONGO_URI=mongodb://localhost:27017
MONGO_DB=rag_db

# LLM (choose one)
LLM_PROVIDER=GEMINI  # or OLLAMA or HUGGINGFACE
LLM_MODEL=gemini-2.0-flash
LLM_API_KEY=your_key_here
```

### 3. Setup Frontend
```bash
# New terminal
cd rag-research-assistant/frontend

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Mac/Linux

# Install dependencies
pip install -r requirements.txt
```

## How to Run

### Terminal 1: Start Backend
```bash
cd rag-research-assistant/backend
venv\Scripts\activate
uvicorn main:app --reload --port 8000
```

### Terminal 2: Start Frontend
```bash
cd rag-research-assistant/frontend
venv\Scripts\activate
streamlit run app.py --server.port 8501
```

## Access

| Component | URL | Purpose |
|-----------|-----|---------|
| **Frontend UI** | http://localhost:8501 | Upload & query documents |
| **API Docs** | http://localhost:8000/docs | API reference |
| **Backend API** | http://localhost:8000/api/v1 | REST endpoints |

## How to Use

1. **Upload PDFs** → Navigate to Upload Documents page, select PDF
2. **Get Document ID** → Save the ID shown after upload
3. **Ask Questions** → Go to Query Assistant, enter your question
4. **View Chunks** → Check View Document Chunks to see processed text

## Project Structure
```
rag-research-assistant/
├── backend/           # FastAPI server (MongoDB + ChromaDB + LLMs)
├── frontend/          # Streamlit UI (Upload + Query + View)
└── README.md
```

## Supported LLMs

- **Google Gemini** (Recommended) - Fast and accurate
- **Ollama** (Local) - Run models locally
- **HuggingFace** - Open-source models

## Tech Stack

- **Backend**: FastAPI, MongoDB, ChromaDB
- **Frontend**: Streamlit
- **AI**: Sentence Transformers, Multiple LLM providers
- **Storage**: AWS S3 (optional)

## API Reference

```bash
# Upload PDF
curl -X POST -F "file=@document.pdf" http://localhost:8000/api/v1/upload

# Query documents
curl -X POST -H "Content-Type: application/json" \
  -d '{"question": "What is this about?"}' \
  http://localhost:8000/api/v1/query
```

## License

MIT License - see [LICENSE](LICENSE) file for details.

---

**Need Help?** Open an issue on [GitHub](https://github.com/muhammedafsalpm/rag-research-assistant/issues)
```

## Why this README works:

1. **Minimal** - Only essential information
2. **Professional** - Clean formatting with emojis
3. **Actionable** - Direct commands to copy/paste
4. **Clear Flow** - Setup → Run → Use
5. **Quick Reference** - URLs table, commands table
6. **GitHub Ready** - Links to issues, clean structure

## Additional files you might want:

### `.gitignore` (in root)
```gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdk/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# Virtual Environment
venv/
venv_frontend/
env/
ENV/
env.bak/
venv.bak/

# IDE
.vscode/
.idea/
*.swp
*.swo

# Environment files
.env
.env.local
.env.dev
.env.prod

# Database
*.db
*.sqlite
*.sqlite3

# ChromaDB
.chromadb/

# Logs
*.log

# OS
.DS_Store
Thumbs.db
```

### `LICENSE` (in root - MIT License template)
```text
MIT License

Copyright (c) 2025 Muhammed Afsal P M

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.




















<!-- # RAG Research Assistant Backend

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

**Note**: Configure AWS S3 credentials in `.env` for document storage functionality. -->
