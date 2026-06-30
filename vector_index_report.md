# Vector Index Report — SiddhaVerse

Generated on: 2026-06-27 11:58:16 UTC
Scope: Step 2 of Phase 3B Semantic Retrieval

## 1. Database & Collection Metrics

- **Vector Database:** Qdrant (Embedded mode)
- **Local Path:** `d:\Siddha_Wisdom\qdrant_db`
- **Collection Name:** `siddhaverse_documents`
- **Vector Dimension:** **1024**
- **Distance Metric:** Cosine Similarity
- **Database Setup Time:** **0.03 seconds**

## 2. Payload Schema Indexes
Payload keyword indexes successfully initialized for fast metadata pre-filtering:
- `doc_type`
- `source_work`
- `author`
- `entity_ids`

## 3. Subset Ingestion Benchmarks

- **Subset Ingestion Count:** 50 documents
- **Ingestion Duration:** **18.41 seconds**
- **Average Indexing Latency:** **368.19 ms/document** (includes embedding generation + database write)

## 4. Search Verification (Query: "holy basil")

Top retrieved matches from the indexed subset:

| Rank | Match Score | Document ID | Title | Doc Type |
| :--- | :--- | :--- | :--- | :--- |
| 1 | 0.7708 | `manuscript_ias_pl_033` | Theriyar Karisal (Therapeutic Recipes) | manuscript |
| 2 | 0.7696 | `manuscript_sml_palm_124` | Sarbendra Vaidya Muraigal | manuscript |
| 3 | 0.7644 | `manuscript_saraswati_mahal_001` | Agasthiyar Paripooranam | manuscript |
| 4 | 0.7633 | `manuscript_goml_tam_231` | Varma Suthiram (Pressure Points) | manuscript |
| 5 | 0.7630 | `manuscript_sml_palm_312` | Gunapadam Mooligai (Materia Medica) | manuscript |

## 5. Verification Check list
- [x] Qdrant client running in embedded file-system storage mode (Verified)
- [x] Collection schema maps E5 vectors (Verified)
- [x] Payload indexes initialized on primary metadata tags (Verified)
- [x] Semantic query retrieval returns logical match scores (Verified)

*Status: **Step 2 PASSED**. Ready to proceed to Step 3 (Full corpus indexing with dirty-hash caching).*
