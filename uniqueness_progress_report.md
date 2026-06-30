# Uniqueness Progress Report
# Phase 2B-1R: Real Corpus Acquisition

**Report Date:** 2026-06-24  
**Acquisition Phase:** 2B-1R — Real Corpus Acquisition  
**Comparison Baseline:** Phase 2B-1 Pilot Corpus (500 replicated documents)

---

## Executive Summary

| Metric | Pilot Corpus (Phase 2B-1) | Real Corpus (Phase 2B-1R) | Change |
|--------|--------------------------|---------------------------|--------|
| Total Documents | 500 | 1,000 | +500 (+100%) |
| Unique Verse Bodies | 13 | **1,000** | +987 (+7,592%) |
| Duplicate Verse Bodies | 487 | **0** | -487 |
| Duplication Rate | 97.4% | **0.0%** | -97.4 pp |
| Content Hashes (SHA-256) | 13 distinct | **1,000 distinct** | ✓ |
| Synthetic Content | 0 | **0** | ✓ |
| Provenance Coverage | 100% | **100%** | ✓ |

---

## Phase 2B-1R Uniqueness Verification

### Method
Every acquired verse was assigned a SHA-256 content hash computed on normalised text (collapsed whitespace). Duplicate hashes were **rejected at write time** — no duplicates entered the corpus.

### Results

```
Total documents written:          1,000
Unique content hashes:            1,000
Duplicate content hashes:             0
Duplicate rate:                   0.00%
```

> [!IMPORTANT]
> The duplicate rate of **0.00%** means every single document in the real corpus contains a distinct verse body. The target of ≤ 5% is **exceeded by the maximum possible margin**.

---

## Source Uniqueness Breakdown

| Source File | Work | Collection | Verses Extracted | Written | Duplicates Rejected |
|-------------|------|-----------|-----------------|---------|---------------------|
| pmuni0004.html | Thirumandiram | Tantirams 1–2 | 335 | 335 | 0 |
| pmuni0009_02.html | Thirumandiram | Tantiram 3 (Part 2) | 260 | 260 | 0 |
| pmuni0014.html | Thirumandiram | Tantiram 7 | 13 | 13 | 0 |
| pmuni0269.html | Sivavakkiyam | Complete Collection | 525 | 392* | 0 |
| **TOTAL** | — | — | **1,133** | **1,000** | **0** |

*392 of 525 Sivavakkiyam verses written (target of 1000 reached; remaining 133 available for future expansion)

> [!NOTE]
> Several Thirumandiram part files (pmuni0009_01, pmuni0010_01, pmuni0010_02, pmuni0011_01, pmuni0011_02, pmuni0013, pmuni0015, pmuni0016) parsed 0 candidate verses. This is attributable to structural variation across Project Madurai's multi-part files — the verse-number marker format differs across file series. These files remain available as expansion targets for Phase 2B-2.

---

## Corpus Composition After Phase 2B-1R

| Collection | Documents | % of Verse Corpus |
|-----------|-----------|------------------|
| Thirumandiram (Tantirams 1–2) | 335 | 33.5% |
| Thirumandiram (Tantiram 3 Part 2) | 260 | 26.0% |
| Sivavakkiyam | 392 | 39.2% |
| Thirumandiram (Tantiram 7) | 13 | 1.3% |
| **TOTAL NEW** | **1,000** | **100%** |

---

## Success Criteria Assessment

| Criterion | Target | Achieved | Status |
|-----------|--------|----------|--------|
| Unique Verses | ≥ 1,000 | **1,000** | ✅ PASS |
| Duplicate Rate | ≤ 5% | **0.00%** | ✅ PASS |
| Provenance Coverage | 100% | **100%** | ✅ PASS |
| Synthetic Content | 0 | **0** | ✅ PASS |

**All four success criteria met.**

---

## Archived Pilot Files

| Location | Count | Status |
|----------|-------|--------|
| `raw_documents/archive/` | 500 | Preserved (not deleted) |
| `metadata_registry/archive/` | 500 | Preserved (not deleted) |

The 500 replicated pilot documents have been moved to archive and are no longer part of the active corpus.

---

## Remaining Expansion Capacity

| Source | Available But Not Yet Ingested | Reason |
|--------|-------------------------------|--------|
| Sivavakkiyam (pmuni0269) | 133 verses | Target reached |
| Thirumandiram parts (alternative format) | ~1,500 est. | Parser coverage gap |

**Recommended next action:** Phase 2B-2 — expand parser coverage for remaining Thirumandiram parts and ingest additional Sivavakkiyar verses.
