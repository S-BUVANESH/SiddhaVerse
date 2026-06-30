# Embedding Integrity Report — SiddhaVerse

Generated on: 2026-06-27 12:18:35 UTC
Scope: Step 3 of Phase 3B Semantic Retrieval

## 1. Sync & Ingestion Ingestion

- **Total Documents in SQLite:** 1174
- **Total Points in Qdrant:** 1174
- **Skipped Documents (No changes):** 1174
- **Updated Documents (Hashes changed):** 0
- **Newly Embedded Documents:** 0
- **Sync Processing Time (Cleanup Run):** **0.05 seconds**

## 2. Integrity Audit Details

| Audit Verification Gate | Target | Actual | Status |
| :--- | :--- | :--- | :--- |
| **Count Consistency** | SQLite Count == Qdrant Count | SQLite: 1174 \| Qdrant: 1174 | PASSED |
| **Vector Dimensions** | Strictly 1024 floats | 1024 | PASSED |
| **Null/NaN Detections** | 0 vectors containing NaN/null | 0 | PASSED |
| **Payload Schema Match** | Presence of identity keys | Verified | PASSED |

### Audit Summary:
**PASSED**

All verification gates passed successfully. The semantic store is in perfect sync with the primary metadata catalog.

---
*Status: **Step 3 PASSED**. Ready to proceed to Step 4 (Vector search benchmarking).*
