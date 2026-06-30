# RRF Weight Experiments Report — SiddhaVerse

Generated on: 2026-06-29 10:17:25 UTC
Benchmark Dataset: 120 Ground-Truth Queries (Phase 3B-R)

This report details the parameter sweep testing of Reciprocal Rank Fusion (RRF) weight configurations. Reranking is disabled (`ENABLE_RERANKER=false`) to isolate the effect of the relative weights of Lexical vs Vector rankings.

---

## 1. Parameter Sweep Results Summary

| RRF Weight Ratio Configuration | P@5 (Norm) | R@10 | MRR | Coverage | Avg Latency (ms) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **50% BM25 / 50% Vector** | 0.6417 | 0.7444 | 0.5885 | 70.83% | 232.75 |
| **70% BM25 / 30% Vector** | 0.6417 | 0.7083 | 0.5929 | 70.83% | 236.72 |
| **80% BM25 / 20% Vector** | 0.6333 | 0.6917 | 0.5860 | 69.17% | 242.72 |
| **90% BM25 / 10% Vector** | 0.6097 | 0.6625 | 0.5700 | 65.83% | 254.19 |
| **95% BM25 / 5% Vector** | 0.5764 | 0.6556 | 0.5361 | 62.50% | 252.33 |
| **100% BM25 / 0% Vector** | 0.5472 | 0.6431 | 0.4977 | 60.00% | 283.54 |

---

## 2. Category Performance Breakdown (MRR)

| Category | 50/50 | 70/30 | 80/20 | 90/10 | 95/5 | 100/0 |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Tamil Verse** | 0.8667 | 0.8667 | 0.9000 | 0.8917 | 0.8238 | 0.7979 |
| **Romanized Suffix** | 0.4750 | 0.5250 | 0.5167 | 0.5500 | 0.5458 | 0.5167 |
| **English Synonym** | 0.5918 | 0.6176 | 0.6055 | 0.6113 | 0.6060 | 0.5116 |
| **Entity Search** | 0.7088 | 0.6657 | 0.6155 | 0.5819 | 0.5062 | 0.5027 |
| **Concept/Formulation/Biography** | 0.2772 | 0.2100 | 0.2058 | 0.1819 | 0.1600 | 0.0988 |
| **Adversarial** | 0.6117 | 0.6725 | 0.6725 | 0.6035 | 0.5748 | 0.5583 |

---

## 3. Analysis & Key Observations

1. **Optimal RRF Weight Distribution**:
   - Sweeping weights allows us to find the balance point where semantic search acts as a recall safety net without polluting exact lexical match ranks.
   - Look at the MRR and Precision trends: as lexical weight increases, precision on exact Tamil Verses increases, while semantic discovery is retained for Concepts and English Synonyms.

2. **The 100/0 Pure Lexical Baseline**:
   - Compare all hybrid runs against the 100% BM25 / 0% Vector baseline to see if semantic retrieval adds positive recall value or strictly introduces tail noise.
