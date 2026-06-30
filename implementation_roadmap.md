# Phase 3 Implementation Roadmap — SiddhaVerse

## Document Information
- **Role**: Lead Systems Architect  
- **System Version**: v3.1-RC2  
- **Goal**: Step-by-Step AI Retrieval Implementation Roadmap  

---

## 1. Timeline Overview

Phase 3 is divided into five sequential execution milestones. This revised timeline splits retrieval development into separate Lexical (3A) and Semantic (3B) stages, enforcing rigorous quality benchmarking prior to RAG integration.

```
+-------------------------------------------------------------+
| Phase 3A: Hybrid Retrieval Infrastructure (2 Weeks)         |
| - SQLite/PostgreSQL metadata DB, FTS5, FastAPI, Benchmark   |
+-------------------------------------------------------------+
                              |
                              v
+-------------------------------------------------------------+
| Phase 3B: Semantic Retrieval (2 Weeks)                      |
| - Qdrant setup, Embedding pipelines, Hybrid Rank, Eval      |
+-------------------------------------------------------------+
                              |
                              v
+-------------------------------------------------------------+
| Phase 3C: RAG Pipeline Integration (2 Weeks)                |
| - Context builder, LLM connectors, Prompt engineering       |
+-------------------------------------------------------------+
                              |
                              v
+-------------------------------------------------------------+
| Phase 3D: Citation Verification & Security (1 Week)         |
| - Programmatic hash verification, rate limiters, release    |
+-------------------------------------------------------------+
```

---

## 2. Milestone Deep-Dive

---

### Phase 3A: Hybrid Retrieval Infrastructure
- **Objectives**:
  1. Build the unified SQLite database mapping the 1,174 schema-unified documents.
  2. Implement SQLite FTS5 virtual tables and search index matching.
  3. Deploy a lightweight FastAPI backend for search query handling.
  4. Write direct entity lookup tables and relationships matching.
  5. Run search queries benchmarking against ground-truth datasets.
- **Rules**: Strictly **NO** vector embeddings, **NO** LLMs, and **NO** generative output in this phase.
- **Deliverables**:
  - `fts_setup.sql` (schema structure, virtual tables, and database indexes).
  - `fts_search_service.py` (FastAPI search router for lexical and entity queries).
  - `search_benchmark_runner.py` (script executing keyword benchmarks).
- **Estimated Complexity**: Medium
- **Dependencies**: Completed Phase 2B-4 database (`normalized_corpus/`).

---

### Phase 3B: Semantic Retrieval
- **Objectives**:
  1. Deploy a local Docker instance of the Qdrant Vector Database.
  2. Implement the `vector_ingestion_pipeline.py` script using the `multilingual-e5-large` embedding model.
  3. Formulate the incremental indexing logic using SHA-256 dirty-hash flags.
  4. Implement the hybrid ranking pipeline incorporating Reciprocal Rank Fusion (RRF).
  5. Conduct formal retrieval evaluation against benchmark metrics (Precision@5, Recall@10, MRR).
- **Rules**: Strictly **NO** LLM responses or generation. Focus is purely on search retrieval recall.
- **Deliverables**:
  - `qdrant_docker_setup.sh` (compose config).
  - `vector_ingestion_pipeline.py` (vector generation and upsert).
  - `hybrid_retriever.py` (implements RRF rank combining).
  - `retrieval_evaluation_report.md` (benchmark outcomes).
- **Estimated Complexity**: Medium
- **Dependencies**: Phase 3A (FTS5 search infrastructure).

---

### Phase 3C: RAG Pipeline Integration
- **Objectives**:
  1. Implement the **Query Classification Layer** to direct and filter incoming searches.
  2. Implement the **Evidence Builder Layer** to deduplicate, sort, prioritize primary works, and package token contexts.
  3. Build LLM connections for cloud endpoint APIs (Gemini 1.5 Pro) and local models (Gemma 2).
  4. Set up context template formatting.
- **Deliverables**:
  - `query_classifier.py` (routes intents).
  - `evidence_builder.py` (context compile and token budget manager).
  - `rag_service.py` (assembles prompts and calls LLMs).
  - `prompt_templates.json` (versioned system instructions).
- **Estimated Complexity**: Medium
- **Dependencies**: Phase 3B (Semantic Retrieval Engine).

---

### Phase 3D: Citation Verification & Security
- **Objectives**:
  1. Force structured citation tags (`<cite doc="..." hash="..." />`) in system prompts.
  2. Implement regex parser middleware to extract and verify generated hashes against injected payloads.
  3. Put prompt-injection sanitization filters in place.
  4. Deploy backend services to production containers.
- **Deliverables**:
  - `citation_middleware.py` (validates output tags).
  - `security_filters.py` (prompt injection protection).
  - `docker-compose.prod.yml` (production backend setup).
- **Estimated Complexity**: High (due to precision alignment requirements).
- **Dependencies**: Phase 3C (RAG Service).

---

*Report generated by SiddhaVerse Systems Architecture Board, 2026-06-25*
