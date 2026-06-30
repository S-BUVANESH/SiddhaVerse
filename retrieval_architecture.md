# Retrieval & Embedding Engine Architecture — SiddhaVerse

## Document Information
- **Role**: Lead Systems Architect  
- **System Version**: v3.1-RC2  
- **Scope**: Lexical, Entity, Metadata, and Vector Search Engines  

---

## 1. Multi-Dimensional Retrieval Engine

To handle a corpus scaling to 100,000+ documents, SiddhaVerse will employ a **hybrid retrieval engine** combining traditional databases and vector indices.

```
                  +-----------------------------------------+
                  |               User Query                |
                  +-----------------------------------------+
                                       |
                                       v
                     +-----------------------------------+
                     |      Query Processing Engine      |
                     |  - Intent Classification Layer    |
                     |  - Suffix Stripping & Synonyms    |
                     +-----------------------------------+
                                       |
            +--------------------------+--------------------------+
            |                          |                          |
            v                          v                          v
+-----------------------+  +-----------------------+  +-----------------------+
|    Lexical Retrieval  |  |   Entity Resolution   |  |  Semantic Discovery   |
|  (FTS5 / PG pg_trgm)  |  |  (Explicit ID Match)  |  |  (Qdrant Embeddings)  |
+-----------------------+  +-----------------------+  +-----------------------+
            |                          |                          |
            +--------------------------+--------------------------+
                                       |
                                       v
                     +-----------------------------------+
                     |       Reranking and Fusion        |
                     |    - Reciprocal Rank Fusion       |
                     |    - Cross-Encoder Re-scoring     |
                     +-----------------------------------+
                                       |
                                       v
                     +-----------------------------------+
                     |         Evidence Builder          |
                     |    - Deduplication & Ordering     |
                     |    - Priority Parsing & Tokens    |
                     +-----------------------------------+
```

### A. Keyword & Full-Text Search
- **Technology**: SQLite FTS5 (local development) / PostgreSQL `tsvector` with GIN indexing (production).
- **Index Field**: `search_text` (pre-computed combination of text, transliteration, keywords, titles, and descriptions).
- **Stemming**: Custom token filter for English combined with Phase 2B-4 Romanized suffix rules.

### B. Entity Search
- **Technology**: Relational mapping in SQL (`document_entities` table).
- **Execution**: Directly queries the relational schema using entity markers (e.g., matching `"plant_tulsi"`) to return the target metadata document and linked verses.

### C. Metadata Filtering
- **Execution**: SQL `WHERE` clauses applied to restrict query scopes by `source_work`, `author`, `copyright_status`, and `collection` parameters.

---

## 2. Production Database Strategy & Migrations

To maintain developer agility while scaling to high-availability production environments, SiddhaVerse operates a split database stack.

### Stack Definition:
- **Local Development**: **SQLite FTS5** (serverless, local file-based database containing all unified documents and full-text indexes).
- **Production Environment**: **PostgreSQL** (relational database for metadata and relationships) + **Qdrant** (high-availability vector database with HNSW indexes).

### Data Schema Mapping:

```
SQLite Schema (Local Dev)             PostgreSQL Schema (Production)
+-----------------------+             +-----------------------+
|     documents         |             |       documents       |
|  - document_id (PK)   |             |  - document_id (PK)   |
|  - title, author      |             |  - title, author      |
|  - source_work        |  =======>   |  - source_work        |
|  - collection         |             |  - collection         |
|  - content_hash       |             |  - content_hash       |
|  - metadata (JSON)    |             |  - metadata (JSONB)   |
+-----------------------+             +-----------------------+
                                                 |
                                                 v
                                      +-----------------------+
                                      |     Qdrant Vectors    |
                                      |  - ID (UUIDv5)        |
                                      |  - Vector (1024-dim)  |
                                      |  - Payload (JSON)     |
                                      +-----------------------+
```

### Database Migration Procedures:

1. **Relational Schema Sync**:
   - The PostgreSQL schema mirrors the SQLite tables. Fields of type `JSON` in SQLite are upgraded to PostgreSQL `JSONB` to enable indexed metadata queries.
   - Run alembic / DB migration scripts to apply schemas to production PostgreSQL endpoints.
2. **Data Export & Transformation**:
   - An export script reads from the SQLite instance, serializes the metadata rows, and executes bulk inserts (`pg_copy_from` or multi-row `INSERT`) into PostgreSQL.
3. **Qdrant Vector Upsert**:
   - The migration service computes the UUIDv5 for each document using its `document_id`.
   - The dense vectors are generated from `search_text` and upserted into Qdrant alongside the metadata filtering payloads.

---

## 3. Ranking Strategy

To merge lexical hits, entity records, and semantic discovery rankings, the engine uses a two-stage hybrid ranking pipeline:

### Stage 1: Weighted Reciprocal Rank Fusion (RRF)
RRF merges the ranked lists from lexical ($R_{lex}$) and semantic ($R_{sem}$) pipelines using a weighted scoring function to prevent semantic noise from displacing exact matches. The RRF score for a document $d \in D$ is calculated as:

$$RRF\_Score(d) = w_{lex} \cdot \frac{1}{k + r_{lex}(d)} + w_{sem} \cdot \frac{1}{k + r_{sem}(d)}$$

Where:
- $w_{lex} = 0.70$ (Lexical weight) and $w_{sem} = 0.30$ (Semantic Discovery weight)
- $r_m(d)$ is the rank of document $d$ in system $m$
- $k = 60$ (constant stabilizer)

### Stage 2: Selective Cross-Encoder Reranking (CPU In-Memory)
To satisfy the production requirement of latency p95 < 100 ms, Cross-Encoder reranking is bypassed for primary, lookup-based, and greeting queries. Reranking is selectively enabled for complex conceptual discovery queries, utilizing the lightweight multilingual `cross-encoder/mmarco-mMiniLMv2-L12-H384-v1` model (~470MB RAM footprint). Relevance scores $\ge 0.35$ are retained.

---

## 4. Vector Embedding Strategy

### A. Fields to Embed
1. **Tamil Text (`tamil_text`)**: Captures native linguistic and poetic structures.
2. **Romanized Transliteration (`transliteration`)**: Facilitates phonetic retrieval.
3. **Enriched Context (`search_text`)**: Combines translation notes, synonyms, and metadata to capture high-level conceptual meanings.

### B. Chunking Strategy
- **Verses (Atomic Chunks)**: Stored as single, atomic, indivisible documents.
- **Supporting Metadata (Single Chunks)**: Biographies, plants, formulations, and manuscripts are stored as single documents.
- **Research Literature (Semantic Sliding Window)**: PubMed papers and classical treatises are chunked using a sliding window:
  - **Chunk size**: 256 tokens (approximately 150–200 words).
  - **Overlap**: 50 tokens (to prevent context loss at boundaries).

### C. Metadata Payload Schema
Every vector stored in the database is tagged with a flat metadata payload for filtering:

```json
{
  "document_id": "text_thirumandiram_pm_0127",
  "source_work": "Thirumandiram",
  "collection": "Tantiram 1",
  "author": "Thirumoolar",
  "verse_number": "127",
  "copyright_status": "public_domain",
  "content_hash": "a8f3b20c1d2e...",
  "verified_provenance": true
}
```

---

## 5. Multilingual & Localization Strategy

- **Dual-Language Vectors**: We recommend using a multilingual embedding model (e.g., `multilingual-e5-large` or `sentence-transformers/LaBSE`) that maps Tamil script, English translation, and Romanized transliteration into the same vector space.
- **Cross-Lingual Query Expansion**: English queries are mapped to their Tamil transliterations and canonical entity tags before executing vector search.

---

## 6. Scalability & Incremental Indexing

### Incremental Update Strategy:
1. **Hash Verification**: The ingestion pipeline computes the SHA-256 hash of each document's content field (`tamil_text` or `description`).
2. **Dirty Flag Verification**:
   - If `content_hash` matches an existing record in the database, the record is skipped.
   - If the hash is new, the document is marked as `dirty`, its vectors are computed, and they are upserted into the vector database.
3. **Soft Deletions**: Removed files are marked as `deleted` in SQL, and their corresponding vectors are removed asynchronously from the vector index.

---

*Report generated by SiddhaVerse Systems Architecture Board, 2026-06-25*
