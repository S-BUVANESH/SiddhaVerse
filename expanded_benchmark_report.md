# Expanded Benchmark Report — SiddhaVerse

Generated on: 2026-06-29
Corpus Version: 2B-4
Scope: Phase 3B-R (Retrieval Refinement - Step 3B-R.1)

This report documents the design and distribution of the expanded 120-query evaluation dataset. This dataset acts as the target verification gate for lexical, semantic, and hybrid retrieval.

---

## 1. Category Distribution

The evaluation suite contains **120 queries** distributed evenly across six key search scenarios:

| Category | Size | Scope / Query Target | Example Query | Expected Relevant IDs |
| :--- | :--- | :--- | :--- | :--- |
| **Tamil Verse** | 20 | Exact/partial Tamil string lookups in classical verses. | `"நினைப்பதொன்று கண்டிலேன்"` | `sivavakkiyar_pm_0616` |
| **Romanized Suffix** | 20 | Romanized Sanskrit/Tamil script queries for yogic and medical terms. | `"vaasi yogam"` | `classic_thirumandiram`, `sivavakkiyar_pm_0613` |
| **English Synonym** | 20 | Mapping English botanical and physiological terms to classical concepts. | `"indian gooseberry"` | `plant_nelli` |
| **Entity Search** | 20 | Specific queries for Siddhars, scriptures, plant names, and recipes. | `"Agasthiyar"` | `siddhar_agasthiyar`, `classic_agasthiyar_soumya_sagaram` |
| **Concept/Formulation/Biography** | 20 | Complex clinical questions, recipes, ingredient lists, and biographical details. | `"siddha formulation for respiratory fever"` | `formulation_kabasura_kudineer` |
| **Adversarial** | 20 | Challenging user inputs (misspellings, ambiguity, out-of-scope, short terms). | `"kabasura kudiner recipe"` | `formulation_kabasura_kudineer` |

---

## 2. Adversarial Query Breakdowns

To ensure the retrieval engine is production-ready and resilient to imperfect user inputs, the 20 adversarial queries are categorized as follows:

1. **Spelling Variations (5)**: Includes common typos like `"pranyama"` or `"algastiar"` matching classical Sanskrit/Tamil terms.
2. **Ambiguity / Multi-Match (5)**: Single-word ambiguous terms like `"oil"`, `"root"`, or `"fever"` mapping to multiple formulations/plants.
3. **Multi-Intent Combinations (3)**: Intersecting concepts like `"tulsi plant and nilavembu kudineer"` mapping across multiple distinct entities.
4. **Out-of-Scope (4)**: General knowledge queries (e.g. `"what is the capital of France?"`) expecting `[]` (empty results).
5. **Very Short Term Truncation (3)**: 2-character queries (e.g. `"va"`, `"o"`, `"si"`) to verify the engine handles short inputs without crashing or returning excessive noise.

---

## 3. Ground-Truth Data Source

- **File Path:** [`d:\Siddha_Wisdom\expanded_benchmark_ground_truth.json`](file:///d:/Siddha_Wisdom/expanded_benchmark_ground_truth.json)
- **Status:** Generated and verified against the current SQLite schema. Every expected document ID has been validated to exist in `siddhaverse.db`.

*Status: **Step 3B-R.1 PASSED**. Ready to proceed to Step 3B-R.2 (Reranker ablation benchmarking).*
