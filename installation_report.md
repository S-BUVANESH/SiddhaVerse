# Installation Report — SiddhaVerse Search Infrastructure

This document outlines the setup, database seeding, and installation verification steps completed for the SiddhaVerse search infrastructure backend (Phase 3A).

## 1. System Environment

- **OS Platform:** Windows (win32)
- **Interpreter:** Python 3.14.4
- **Working Directory:** `d:\Siddha_Wisdom`
- **Database Engine:** SQLite 3 (with FTS5 module enabled)

## 2. Dependency Setup
Dependencies defined in `backend/requirements.txt` were verified for successful import and resolved:
- `fastapi` and `requests` are present and active.
- Pydantic v2 and SQLAlchemy v2 are fully functional on Python 3.14.4.
- All versions cataloged in [dependency_versions.md](file:///d:/Siddha_Wisdom/dependency_versions.md).

## 3. Database Seeding & Enrichment

An enriched database seeder `backend/app/seed_db.py` was developed and executed to build and populate `siddhaverse.db`:
- **Source Files:** Seeder reads from `normalized_corpus/` directory, cross-referencing `search_index.json` to acquire pre-computed keywords and metadata.
- **Relational Tables Created:**
  - `documents`: Stores raw document fields (1,174 records seeded: 1,000 verses, 14 biographies, 22 formulations, 38 plants, 20 manuscripts, 10 classical texts, 70 research articles).
  - `entities`: Stores Siddhar, deity, plant, place, and practice metadata (93 records seeded).
- **Virtual FTS5 Index Created:**
  - `documents_fts`: Virtual full-text indexing table mapping document identifiers to searchable fields.
- **Enrichment Logic:** Appends pre-computed English synonyms, transliterations, and category keywords to the `search_text` field in FTS, facilitating lexical search across language boundaries.

## 4. Verification Procedures

- **Pytest Suite:** Ran `python -m pytest backend/tests`, collecting 15 items. **All 15 tests passed** (100% success rate). Detailed logs are recorded in [test_results.md](file:///d:/Siddha_Wisdom/test_results.md).
- **Retrieval Benchmark Harness:** A benchmarker script `backend/run_benchmarks.py` was written to perform HTTP GET search requests against a FastAPI client and compute retrieval metrics against the ground truth.
- **Search Preprocessing Layer:** Added lexical preprocessing (Romanized suffix-stripping via `suffix_rules.json` and English synonym expansion via `synonym_map.json`) to `SQLiteDocumentRepository` to pass search gates.
- **Benchmark Evaluation:** The search engine successfully passed all target gates. Metrics are cataloged in [benchmark_results.md](file:///d:/Siddha_Wisdom/benchmark_results.md).
