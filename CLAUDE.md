# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a **电能质量报告审查系统** (Power Quality Report Audit System) that audits power quality assessment reports. The system takes WORD/PDF reports as input and produces structured audit results covering 20 specific audit checkpoints for compliance verification.

### Key Components

- **rag-server/**: RAG-based backend with MCP server capabilities
  - Ingestion Pipeline: PDF → Markdown → Chunk → Transform → Embedding → Upsert
  - Hybrid Search: Dense + Sparse (BM25) + RRF Fusion + Rerank
  - Pluggable architecture for LLM/Embedding/Reranker/VectorStore
  - MCP Server with Stdio Transport (not HTTP)

- **sgcc-report-audit-app/**: Full-stack application
  - `frontend/`: Vue 3 + Vite + TypeScript dashboard
  - `backend/`: Python FastAPI service for audit orchestration

## Common Development Commands

### RAG Server (rag-server/)

```bash
cd rag-server

# Install dependencies
uv sync

# Run all tests
uv run pytest

# Run specific test types
uv run pytest tests/unit -m unit
uv run pytest tests/integration -m integration
uv run pytest tests/e2e -m e2e

# Run a single test file
uv run pytest tests/unit/test_specific.py -v

# Run MCP server
uv run python scripts/run_mcp_server.py --health
```

### Frontend (sgcc-report-audit-app/frontend/)

```bash
cd sgcc-report-audit-app
./scripts/run_frontend.sh
# Or directly:
npm run dev -- --host 0.0.0.0

# Build
npm run build

# Run unit tests
npm run test:unit
```

### Backend (sgcc-report-audit-app/backend/)

```bash
cd sgcc-report-audit-app
./scripts/run_backend.sh
# Or directly:
uv run python -m sgcc_audit.main
```

## Architecture Overview

### Pluggable Component Architecture

All major components use factory patterns with abstract base classes:

- **LLM**: `src/libs/llm/base_llm.py` → `llm_factory.py`
  - Providers: OpenAI, Qwen, Azure, DeepSeek, VLLM, Ollama

- **Embedding**: `src/libs/embedding/base_embedding.py` → `embedding_factory.py`
  - Providers: OpenAI, BGE, Ollama

- **Reranker**: `src/rerank/base_reranker.py` → `reranker_factory.py`
  - Types: CrossEncoder, LLM, None (pass-through)

- **Vector Store**: `src/storage/vector/base_vector_store.py` → `vector_store_factory.py`
  - Currently: PgVector only

- **Splitter**: `src/ingestion/splitters/base_splitter.py` → `splitter_factory.py`
  - Types: RecursiveCharacter, ParentChild

### Ingestion Pipeline Flow

```
File → Loader (PDF/Word) → Document
  → Splitter → Chunks
  → Transform (ImageCaption, MetadataEnrich)
  → Embedding (Dense + Sparse)
  → Upsert to Vector Store
```

Key files:
- `src/ingestion/pipeline.py`: Pipeline orchestration
- `src/ingestion/loaders/`: File parsing (MarkItDown-based)
- `src/ingestion/splitters/`: Document chunking
- `src/ingestion/transforms/`: Chunk enhancement
- `src/ingestion/upsert/`: Deduplication and storage

### Retrieval Pipeline Flow

```
Query → QueryProcessor (expand/rewrite)
  → Hybrid Retriever (Dense + BM25)
  → RRF Fusion
  → Reranker
  → ResponseBuilder
```

Key files:
- `src/retrieval/retrieval_pipeline.py`: Main orchestration
- `src/retrieval/hybrid_retriever.py`: Dense + Sparse retrieval
- `src/retrieval/rrf_fusion.py`: Reciprocal Rank Fusion
- `src/retrieval/query_processor.py`: Query expansion/rewriting

### MCP Server Tools

Located in `src/mcp_server/tools/`:
- `query_knowledge_hub.py`: Main RAG query
- `ingest_document.py`: Document ingestion
- `retrieve_context.py`: Context retrieval only
- `verify_answer.py`: Answer verification
- `get_document_summary.py`: Document summary
- `list_collections.py`: List vector collections

## Configuration

Configuration is loaded from `rag-server/config/settings.yaml` with environment variable overrides:

Priority: Environment variables > YAML file > Model defaults

Environment variable pattern: `RAG_<COMPONENT>_<SETTING>`

Example:
```yaml
llm:
  provider: qwen
  model: qwen-plus
  api_key: replace-me
  timeout_seconds: 30
retrieval:
  top_k: 5
```

Override via env: `RAG_LLM_MODEL=qwen-max`

## Testing Structure

Tests are organized in `rag-server/tests/`:

```
tests/
├── conftest.py          # Shared fixtures, adds src/ to path
├── unit/                # @pytest.mark.unit - isolated module tests
├── integration/         # @pytest.mark.integration - cross-module tests
└── e2e/                 # @pytest.mark.e2e - full workflow tests
```

pytest.ini configures:
- `asyncio_mode = auto` for async tests
- `log_cli = true` for live logging
- Strict markers to prevent typos

## Key Design Patterns

1. **Local-First**: Default single-machine deployment, PostgreSQL for persistence
2. **Config-Driven**: settings.yaml controls component selection
3. **Zero-Cost Incremental**: SHA256 file hashing to skip unchanged files during ingestion
4. **Trace Observability**: Full ingestion and query tracing with JSONL logs
5. **Parent-Child Chunks**: When k=3+ child chunks from same parent are retrieved, promote to parent document

## Important File Locations

- Core types: `src/core/types.py`
- Settings: `src/core/settings.py`, `config/settings.yaml`
- Factories: `src/factories/`
- Database: `src/storage/db/` (SQLAlchemy + PostgreSQL)
- Image handling: `src/storage/image/`
- Evaluation: `src/evaluation/` (Ragas + custom metrics)

## Development Notes

- The project uses `uv` for Python dependency management
- Each component (LLM, Embedding, etc.) is designed to be swappable via factories
- Tests add `src/` to Python path via conftest.py (no package installation required)
- No HTTP MCP transport - only Stdio Transport for local subprocess mode
- DEV_SPEC.md contains full Chinese-language specification for the project
