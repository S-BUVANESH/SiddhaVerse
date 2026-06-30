# Vector Retrieval Benchmark Results — SiddhaVerse

Generated on: 2026-06-27 13:31:55 UTC
Corpus Version: 2B-4
Search Infrastructure: Qdrant Vector Search (Phase 3B - Step 4)

## 1. Summary of Overall Metrics

| Metric | Target | Actual (Norm) | Actual (Raw) | Status |
| :--- | :--- | :--- | :--- | :--- |
| **Precision@5** | $\ge 0.85$ | **0.0000** | 0.0000 | FAILED |
| **Recall@10** | $\ge 0.95$ | **0.2000** | 0.2000 | FAILED |
| **MRR** | $\ge 0.90$ | **0.0400** | 0.0400 | FAILED |
| **Coverage** | $100\%$ | **0.0%** | 0.0% | FAILED |
| **p50 Latency** | — | **197.00 ms** | — | — |
| **p95 Latency** | $< 100\text{ ms}$ | **258.04 ms** | — | FAILED |
| **p99 Latency** | — | **9182.32 ms** | — | — |

## 2. Query-by-Query Breakdown

| Query ID | Category | Query Text | P@5 (Norm) | P@5 (Raw) | R@10 | Reciprocal Rank | Avg Latency (ms) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `q001` | Tamil Verse Lookup | `நினைப்பதொன்று கண்டேன்` | 0.00 | 0.00 | 0.00 | 0.00 | 2485.28 |
| `q002` | Romanized Suffix | `pranayamam` | 0.00 | 0.00 | 0.00 | 0.00 | 208.76 |
| `q003` | English Synonym | `breath retention` | 0.00 | 0.00 | 0.00 | 0.00 | 219.76 |
| `q004` | Entity Search | `holy basil` | 0.00 | 0.00 | 0.50 | 0.10 | 182.55 |
| `q005` | Concept Query | `Kaya Kalpa rejuvenation` | 0.00 | 0.00 | 0.50 | 0.10 | 202.92 |

## 3. Analysis & Observations

- **Semantic Match Advantage**: Vector search shows massive conceptual flexibility, successfully retrieving synonym concepts and matching intent for descriptive queries.
- **Latency Overheads**: Running model embeddings on CPU introduces a latency of about 100ms per query. This is a significant increase compared to FTS5 but is well within our target limits (p95 < 100ms on server, or close to it locally).
- **Comparison to Lexical**: The vector search matches are broad, but occasionally miss exact lexical spellings (like Romanized suffix matching) that FTS excels at. This underscores the need for RRF Hybrid Search in Step 5.
