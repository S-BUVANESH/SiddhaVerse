# Embedding Generation Report — SiddhaVerse

Generated on: 2026-06-29 12:57:39 UTC
Scope: Step 1 of Phase 3B Semantic Retrieval

## 1. Model Configuration

| Attribute | Configuration |
| :--- | :--- |
| **Model Name** | `intfloat/multilingual-e5-large` |
| **HuggingFace Source** | https://huggingface.co/intfloat/multilingual-e5-large |
| **Model Dimension** | **1024** |
| **Active Computation Device** | `cpu` |
| **Model Load Duration** | **11.08 seconds** |

## 2. Ingestion Benchmarks (Corpus passages)

Measurements taken over a sample of 10 corpus documents containing Tamil/English texts:

- **Total Documents Encoded:** 10
- **Total Encoding Time:** 2.4218 seconds
- **Throughput Rate:** **4.13 documents/second**
- **Average Passage Latency:** **242.18 ms/document**

## 3. Query Benchmarks

Measurements taken over 3 standard search queries:

- **Total Queries Encoded:** 3
- **Average Query Latency:** **77.17 ms/query**

## 4. Verification & Validation Check

- [x] Prepend `"passage: "` instruction for document embeddings (Verified)
- [x] Prepend `"query: "` instruction for search query embeddings (Verified)
- [x] Embedding length strictly equals **1024** (Verified)
- [x] L2 Normalized vector properties (Verified: Cosine distance matches Dot Product)

*Status: **Step 1 PASSED**. Ready to proceed to Step 2 (Qdrant collection setup).*
