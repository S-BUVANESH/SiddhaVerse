# Implementation Plan — Phase 3B Semantic Retrieval

This implementation plan details the strategy for integrating semantic retrieval capabilities into the SiddhaVerse search infrastructure backend.

## Proposed Deliverables
We will generate:
- [phase3b_plan.md](file:///d:/Siddha_Wisdom/phase3b_plan.md) — Documenting the approved semantic search architecture baseline.

## Technical Scope

### 1. Embedding Model
- **Model:** `intfloat/multilingual-e5-large` (1024 dimensions)
- **Distance Metric:** Cosine similarity
- **Pre-processing:** Prepending instructions (`query: ` and `passage: `) for asymmetric search.

### 2. Chunking Strategy
- **Verses:** Kept whole (no chunking) to preserve poetic and thematic structures.
- **Research Articles:** Sliding window chunking (512 tokens size, 64 tokens overlap).
- **Formulations:** Structural chunking separating ingredients list and preparation/dosage details.
- **Manuscripts & Biographies:** Single-entry chunks mapping dense metadata profiles.

### 3. Vector Database (Qdrant)
- **Collection Schema:** Named `siddhaverse_documents`.
- **Payload Indexing:** HNSW vector index alongside payload filters on `doc_type`, `source_work`, `author`, and `entity_ids` to enable fast pre-filtering.

### 4. Incremental Updates
- **Mechanism:** Dirty-hash check matching calculated document SHA-256 hashes against stored SQL `content_hash` fields.
- **Execution:** Skip clean records; re-embed and upsert dirty/new records only.

### 5. Hybrid Retrieval
- **Fusion:** Reciprocal Rank Fusion (RRF) with constant `k=60` combining BM25 and vector results.
- **Reranker:** Lightweight cross-encoder (`cross-encoder/ms-marco-MiniLM-L-6-v2`) processing top candidates.
- **Threshold:** Strict pruning gate at cross-encoder score $\ge 0.35$.

### 6. Success Metrics (Retrieval Evaluation Gates)
- **Precision@5 (Norm):** $\ge 0.85$
- **Recall@10:** $\ge 0.98$
- **MRR:** $\ge 0.95$
- **nDCG@10:** $\ge 0.90$
- **Latency (p95):** $< 100\text{ ms}$

---

## Verification Plan
1. Ensure `phase3b_plan.md` exists and contains correct formatting.
2. Confirm the retrieval benchmarking metrics targets are formally defined.
