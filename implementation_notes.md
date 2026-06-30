# Phase 3C Implementation Notes — SiddhaVerse RAG

**Date**: 2026-06-29

---

## New Files

| File | Purpose |
| :--- | :--- |
| `backend/app/llm.py` | LLMEngine: Gemini API + local simulator fallback |
| `backend/app/rag.py` | RAGPipeline + CitationVerifier orchestration |
| `backend/tests/test_rag.py` | 7-test suite covering all RAG paths |

## Modified Files

| File | Change |
| :--- | :--- |
| `backend/app/main.py` | Added `GET /api/v1/rag` and `POST /api/v1/rag` endpoints |

---

## Key Design Decisions

### 1. LLM Routing
- Checks `GEMINI_API_KEY` env var at runtime.
- If set: calls Gemini API (`gemini-1.5-pro`, configurable via `GEMINI_MODEL`).
- If unset or API fails: falls back to local deterministic simulator.
- Simulator generates citation-grounded answers strictly from injected context.

### 2. Confidence Gating (Two Layers)
- **Layer 1 (Pre-retrieval)**: Checks if lexical hits exist. If zero lexical hits and vector similarity < 0.82, refuses immediately. This catches OOD/nonsense queries before the expensive hybrid retrieval.
- **Layer 2 (Post-retrieval)**: Filters hybrid results to score ≥ 0.55 before building context. Removes semantic noise from the evidence package.

### 3. Citation Verifier
- Regex-based parser: `<cite doc="..." hash="..." />` (allows variable whitespace).
- Two-stage check: doc_id existence, then hash equality.
- On any failure: entire response blocked, warning logged.
- Client receives deduplicated, cleaned citation metadata (hash not exposed).

### 4. Unsupported Query Handler
| Priority | Trigger | Response |
| :--- | :--- | :--- |
| 1 | Empty query | Evidence refusal |
| 2 | Classifier: greeting | Static greeting |
| 3 | Classifier: out_of_scope | Scope refusal |
| 4 | No lexical match + vec < 0.82 | Evidence refusal |
| 5 | Empty post-filter context | Evidence refusal |
| 6 | Citation verification failure | Scholarly integrity block |

---

## Environment Variables

| Variable | Default | Description |
| :--- | :--- | :--- |
| `GEMINI_API_KEY` | _(unset)_ | Enables real LLM inference |
| `GEMINI_MODEL` | `gemini-1.5-pro` | Model to use with Gemini API |
| `RRF_LEXICAL_WEIGHT` | `1.0` | BM25 RRF weight (override to 0.70 for 70/30) |
| `RRF_VECTOR_WEIGHT` | `1.0` | Vector RRF weight (override to 0.30 for 70/30) |
| `ENABLE_RERANKER` | `true` | Enables cross-encoder reranking |
| `RERANKER_MODEL` | `cross-encoder/ms-marco-MiniLM-L-6-v2` | Cross-encoder model |

---

## Known Warnings (Non-blocking)

| Warning | Source | Action |
| :--- | :--- | :--- |
| `PydanticDeprecatedSince20` | `config.py` | Use `ConfigDict` in Phase 3D cleanup |
| `FutureWarning: get_sentence_embedding_dimension` | `embeddings.py` | Rename to `get_embedding_dimension` in Phase 3D |
| `StarletteDeprecationWarning` | `httpx`/`starlette` | Install `httpx2` when upgrading FastAPI |
