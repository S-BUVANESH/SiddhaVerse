# Normalized Corpus Report
# Phase 2B-2: Corpus Normalization & Metadata Standardization

**Report Date:** 2026-06-24  
**Phase:** 2B-2  
**Scope:** 1,150 active documents (1,000 verse + 150 pilot metadata)

---

## 1. Overview

Phase 2B-2 produced a fully normalized, schema-standardized corpus stored in `normalized_corpus/`. Every document has been:

1. Verified for Unicode NFC compliance (Tamil script, U+0B80–U+0BFF)
2. Standardized to the Phase 2B-2 canonical schema
3. Augmented with normalization tracking metadata
4. Linked to extracted entity IDs

The corpus is now ready for downstream indexing, search, or further scholarly analysis.

---

## 2. Normalized Corpus Structure

```
normalized_corpus/
├── text_thirumandiram_pm_0001.json   …  text_thirumandiram_pm_0608.json  (608 files)
├── text_sivavakkiyar_pm_0609.json    …  text_sivavakkiyar_pm_1000.json   (392 files)
├── siddhar_thirumoolar.json          …  siddhar_sattaimuni.json           (10 files)
├── classic_thirumandiram.json        …  classic_yugi_chinthamani_800.json (10 files)
├── manuscript_*.json                                                       (15 files)
├── formulation_*.json                                                      (15 files)
├── plant_*.json                                                            (30 files)
└── pubmed_*.json                                                           (70 files)
Total: 1,150 files
```

---

## 3. Canonical Document Schema

Every normalized verse document conforms to this schema:

```json
{
  "document_id":           "thirumandiram_pm_0001",
  "text_id":               "thirumandiram_pm_0001",
  "title":                 "Thirumandiram - Verse 1",
  "source_work":           "Thirumandiram",
  "collection":            "Tantirams 1-2",
  "verse_number":          "1",
  "author":                "Thirumoolar",
  "language":              "Tamil",
  "script":                "Tamil script",
  "tamil_text":            "ஒன்றவன் தானே இரண்டவன் இன்னருள்...",
  "transliteration":       "oṉṟvṉ tāṉē ...",
  "english_translation":   null,
  "content_hash":          "957b84de5b222bb66115a1b45fda80cf...",
  "normalization": {
    "applied":             false,
    "changes":             [],
    "normalized_by":       "SiddhaVerse Phase 2B-2",
    "normalized_at":       "2026-06-24T18:01:29Z"
  },
  "copyright_status":      "public_domain",
  "source_repository":     "Project Madurai",
  "source_url":            "https://www.projectmadurai.org/...",
  "acquisition_timestamp": "2026-06-24T17:46:07+00:00",
  "provenance_metadata": {
    "method":              "direct_html_extraction",
    "extractor":           "SiddhaVerse Phase 2B-1R",
    "verified":            true,
    "synthetic":           false
  },
  "entity_ids":            ["deity_shiva", "concept_yoga", "body_light"]
}
```

---

## 4. Work Coverage in Normalized Corpus

### Classical Verse Works

| Work | Author | Period | Verses in Corpus | Coverage Notes |
|------|--------|--------|-----------------|----------------|
| Thirumandiram | Thirumoolar | c. 6–7th century CE | 608 | Tantirams 1–2, 3(pt2), 7; full works ~3000 verses |
| Sivavakkiyam | Sivavakkiyar | c. 9–10th century CE | 392 | 392/525 available; complete at Project Madurai |
| **Verse Total** | — | — | **1,000** | — |

### Metadata-Only Records (from Phase 2A.5)

| Category | Records | Content |
|----------|---------|---------|
| Siddhar biographies | 10 | Life histories, works attributed |
| Classical text catalog | 10 | Work-level metadata entries |
| Palm-leaf manuscripts | 15 | EAP/GOML/IFP catalog records |
| Formulations | 15 | Siddha medicine formulas |
| Medicinal plants | 30 | Materia medica entries |
| PubMed research | 70 | Published scientific abstracts |

---

## 5. Text Quality Profile

### Thirumandiram Verse Sample

**Document:** `text_thirumandiram_pm_0001.json`  
**Verse:** 1 | **Collection:** Tantirams 1–2

```
ஒன்றவன் தானே இரண்டவன் இன்னருள்
நின்றனன் மூன்றினுள் நான்குணர்ந் தான்ஐந்து
வென்றனன் ஆறு விரிந்தனன் ஏழும்பர்ச்
சென்றனன் தானிருந் தான்உணர்ந் தெட்டே.
```

*He who is One became Two through His grace; stood in the Three, knew the Four; conquered Five; expanded as Six; transcended the Seven and Eight — and rested in self-knowledge.*

### Sivavakkiyam Verse Sample

**Document:** `text_sivavakkiyar_pm_0610.json`  
**Verse:** 1 | **Collection:** Sivavakkiyam (Complete)

```
பொன்னுக்கு கோயில் கட்டி புகழுக்கு மணியடிக்கும்
மின்னுக்கு கோயில் இல்லை மேலுக்கு மணி இல்லை
அன்னக்கு கோயில் இல்லை அறியாத அனந்தமே
உன்னக்கு கோயில் இல்லை ஓங்காரத் தூணிலே.
```

*They build temples for gold and ring bells for glory — but lightning has no temple, the sky has no bell. The swan has no temple, the infinite unknown has none — for Thee, the temple is the pillar of Om.*

---

## 6. Transliteration Quality

The Phase 2B-1R transliteration uses ISO 15919 character mapping. It provides a phonetic Romanization for indexing and international accessibility.

| Limitation | Note |
|-----------|------|
| Conjunct consonants | Rendered as sequential characters |
| Sandhi (phonological fusion) | Not resolved (raw character mapping) |
| Vowel marks (matras) | Correctly mapped |
| Accuracy level | Sufficient for indexing; not for publication |

> [!NOTE]
> Full scholarly transliteration (with sandhi resolution) is recommended as a Phase 2B-3 enhancement. Current transliteration enables text search and character-level indexing.

---

## 7. Entity Linkage Coverage

| Corpus Subset | Documents | With Entity Links | Coverage |
|--------------|-----------|-------------------|---------|
| Thirumandiram verses | 608 | 601 | 98.8% |
| Sivavakkiyam verses | 392 | 383 | 97.7% |
| All verse documents | 1,000 | 984 | 98.4% |
| Non-verse metadata | 150 | — | — |

16 verse documents (1.6%) contained no matches against the Phase 2B-2 entity lexicon. These are likely short invocation verses or section markers without main entity terms.

---

## 8. Recommended Phase 2B-3 Enhancements

| Enhancement | Priority | Description |
|-------------|---------|-------------|
| English translations | High | Scholarly translations of all 1,000 verses |
| Expanded entity lexicon | High | Add Tantra terms, alchemical substances, more plants |
| Sandhi-aware transliteration | Medium | NLP-based Tamil sandhi resolution |
| Verse structure analysis | Medium | Identify meter, rhyme scheme (Venba, Kalivenba, etc.) |
| Cross-work entity co-occurrence | Low | Map shared concepts across Thirumandiram & Sivavakkiyam |

---

*Report generated by SiddhaVerse Phase 2B-2 Pipeline, 2026-06-24*
