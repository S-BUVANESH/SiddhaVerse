# SiddhaVerse API Contract v1.0
# Phase 2B-3.5: API Design Documentation

**Version:** 1.0.0  
**Date:** 2026-06-25  
**Status:** Design specification only — no backend implementation  
**Base URL:** `/api/v1` (to be defined at deployment)  
**Format:** JSON (UTF-8, NFC normalized)  
**Encoding:** All Tamil text returned in UTF-8, Unicode NFC

---

> [!IMPORTANT]
> This document is a **design specification only**. No backend code has been implemented. This contract defines the interface for any future SiddhaVerse web application or static-site API layer.

---

## Global Conventions

### Request Format
- All requests are HTTP GET
- Parameters are URL query strings
- Tamil text parameters must be URL-encoded UTF-8

### Response Envelope

All endpoints return:

```json
{
  "status":    "success" | "not_found" | "error",
  "version":   "1.0",
  "timestamp": "2026-06-25T14:00:00Z",
  "data":      { ... },
  "meta":      {
    "total":       100,
    "page":        1,
    "per_page":    20,
    "total_pages": 5
  }
}
```

### Error Response

```json
{
  "status":  "error",
  "code":    400,
  "message": "Invalid parameter: page must be a positive integer",
  "field":   "page"
}
```

### Standard Error Codes

| Code | Meaning |
|------|---------|
| 400 | Bad request — invalid parameters |
| 404 | Resource not found |
| 422 | Unprocessable entity — valid syntax, invalid semantics |
| 500 | Internal server error |

---

## Endpoint 1: Search

### `GET /api/v1/search`

Full-text search across the SiddhaVerse corpus.

#### Request Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|---------|---------|-------------|
| `q` | string | ✅ Yes | — | Search query (supports Tamil, romanized, English keywords) |
| `doc_type` | string | No | all | Filter: `verse`, `biography`, `plant`, `formulation`, `manuscript`, `classical_text`, `research` |
| `work` | string | No | all | Filter: `Thirumandiram`, `Sivavakkiyam` |
| `author` | string | No | all | Filter: e.g., `Thirumoolar` |
| `entity` | string | No | — | Filter by entity_id: e.g., `deity_shiva` |
| `category` | string | No | — | Filter by entity category: `siddhars`, `deities`, `concepts`, `practices`, `plants`, `places` |
| `confidence` | string | No | all | Filter by min entity confidence: `confirmed`, `probable`, `candidate` |
| `page` | integer | No | 1 | Page number (1-indexed) |
| `per_page` | integer | No | 20 | Results per page (max: 100) |
| `sort` | string | No | `relevance` | `relevance`, `verse_number`, `work`, `author` |

#### Response Schema

```json
{
  "status": "success",
  "data": {
    "query": "Pranayama",
    "results": [
      {
        "document_id":  "thirumandiram_pm_0001",
        "title":        "Thirumandiram - Verse 1",
        "source_work":  "Thirumandiram",
        "author":       "Thirumoolar",
        "collection":   "Tantirams 1-2",
        "verse_number": "1",
        "doc_type":     "verse",
        "tamil_text":   "ஒன்றவன் தானே...",
        "transliteration": "oṉṟavaṉ tāṉē...",
        "entity_ids":   ["deity_shiva", "concept_yoga"],
        "source_url":   "https://www.projectmadurai.org/...",
        "snippet":      "...ஒன்றவன் தானே இரண்டவன் இன்னருள்..."
      }
    ]
  },
  "meta": {
    "total":       352,
    "page":        1,
    "per_page":    20,
    "total_pages": 18,
    "query_time_ms": 45
  }
}
```

#### Example Requests

```
GET /api/v1/search?q=Pranayama
GET /api/v1/search?q=Shiva&doc_type=verse&work=Thirumandiram
GET /api/v1/search?q=Tulsi&category=plants
GET /api/v1/search?entity=deity_shiva&confidence=confirmed
GET /api/v1/search?q=தாமரை  (Tamil text search, URL-encoded)
```

---

## Endpoint 2: Get Verse

### `GET /api/v1/verse/{id}`

Retrieve a single verse document by document_id.

#### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|---------|-------------|
| `id` | string | ✅ Yes | Document ID (e.g., `thirumandiram_pm_0001`) |

#### Response Schema

```json
{
  "status": "success",
  "data": {
    "document_id":    "thirumandiram_pm_0001",
    "title":          "Thirumandiram - Verse 1",
    "source_work":    "Thirumandiram",
    "collection":     "Tantirams 1-2",
    "verse_number":   "1",
    "author":         "Thirumoolar",
    "language":       "Tamil",
    "script":         "Tamil script",
    "tamil_text":     "ஒன்றவன் தானே இரண்டவன் இன்னருள்...",
    "transliteration":"oṉṟavaṉ tāṉē iraṇṭavaṉ iṉṉaruḷ...",
    "english_translation": null,
    "content_hash":   "957b84de5b222bb6...",
    "copyright_status": "public_domain",
    "source_repository": "Project Madurai",
    "source_url":     "https://www.projectmadurai.org/pm_etexts/utf8/pmuni0010.html",
    "acquisition_timestamp": "2026-06-24T17:46:07+00:00",
    "provenance_metadata": {
      "method":    "direct_html_extraction",
      "extractor": "SiddhaVerse Phase 2B-1R",
      "verified":  true,
      "synthetic": false
    },
    "entity_ids": ["deity_shiva", "concept_yoga", "body_light"],
    "normalization": {
      "applied": false,
      "changes": [],
      "normalized_by": "SiddhaVerse Phase 2B-2",
      "normalized_at": "2026-06-24T18:01:29Z"
    },
    "adjacent": {
      "previous": "thirumandiram_pm_0000",
      "next":     "thirumandiram_pm_0002"
    }
  }
}
```

#### Error Cases

```json
{ "status": "not_found", "code": 404, "message": "Verse 'xyz_0001' not found" }
```

#### Example Requests

```
GET /api/v1/verse/thirumandiram_pm_0001
GET /api/v1/verse/sivavakkiyar_pm_0609
```

---

## Endpoint 3: Get Entity

### `GET /api/v1/entity/{id}`

Retrieve a single entity with its full metadata and cross-references.

#### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|---------|-------------|
| `id` | string | ✅ Yes | Entity ID (e.g., `deity_shiva`, `practice_pranayama`) |

#### Query Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `include_verses` | boolean | false | If true, include up to 20 sample verse_ids |
| `include_crossrefs` | boolean | false | If true, include co-occurring entities |

#### Response Schema

```json
{
  "status": "success",
  "data": {
    "entity_id":       "deity_shiva",
    "entity_category": "deities",
    "entity_name":     "Shiva",
    "description":     "The Supreme Deity of Shaiva Siddhanta; cosmic destroyer and yogic ascetic",
    "occurrence_count": 274,
    "dominant_tier":   "probable",
    "false_positive_risk": "low",
    "tier_breakdown":  { "confirmed": 31, "probable": 18, "candidate": 225 },
    "work_distribution": {
      "Thirumandiram": 180,
      "Sivavakkiyam":  94
    },
    "co_occurring_entities": [
      {
        "entity_id":          "deity_shakti",
        "entity_name":        "Shakti",
        "co_occurrence_count": 190,
        "evidence":           "corpus_co_occurrence"
      }
    ],
    "sample_verse_ids": ["thirumandiram_pm_0001", "sivavakkiyar_pm_0609"]
  }
}
```

#### Example Requests

```
GET /api/v1/entity/deity_shiva
GET /api/v1/entity/practice_pranayama?include_verses=true&include_crossrefs=true
GET /api/v1/entity/plant_tulsi
```

---

## Endpoint 4: Get Plant

### `GET /api/v1/plant/{id}`

Retrieve a medicinal plant record.

#### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|---------|-------------|
| `id` | string | ✅ Yes | Plant document ID (e.g., `plant_tulsi`, `plant_vallarai`) |

#### Response Schema

```json
{
  "status": "success",
  "data": {
    "document_id":      "plant_tulsi",
    "title":            "Tulsi — Holy Basil",
    "tamil_name":       "துளசி",
    "scientific_name":  "Ocimum tenuiflorum",
    "siddha_category":  "herbal",
    "description":      "Sacred herb used in Siddha medicine...",
    "therapeutic_uses": ["respiratory", "anti-inflammatory", "adaptogen"],
    "copyright_status": "public_domain",
    "related_formulations": ["formulation_kabasura_kudineer"],
    "verse_mentions":   95,
    "related_entity_id": "plant_tulsi"
  }
}
```

#### Example Requests

```
GET /api/v1/plant/plant_tulsi
GET /api/v1/plant/plant_vallarai
```

---

## Endpoint 5: Get Siddhar

### `GET /api/v1/siddhar/{id}`

Retrieve a Siddhar biography record.

#### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|---------|-------------|
| `id` | string | ✅ Yes | Siddhar document ID (e.g., `siddhar_thirumoolar`) |

#### Query Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `include_verses` | boolean | false | Include sample verse_ids attributed to this Siddhar |
| `include_works` | boolean | false | Include associated classical text records |

#### Response Schema

```json
{
  "status": "success",
  "data": {
    "document_id":   "siddhar_thirumoolar",
    "name":          "Thirumoolar",
    "tamil_name":    "திருமூலர்",
    "period":        "c. 6th–7th century CE",
    "primary_work":  "Thirumandiram",
    "philosophy":    "Shaiva Siddhanta, Kundalini Yoga, Tantra",
    "description":   "Tamil poet-saint and Siddhar whose work Thirumandiram...",
    "verse_count_in_corpus": 608,
    "entity_id":     "siddhar_thirumoolar",
    "copyright_status": "public_domain",
    "sample_verses": ["thirumandiram_pm_0001", "thirumandiram_pm_0002"]
  }
}
```

#### Example Requests

```
GET /api/v1/siddhar/siddhar_thirumoolar
GET /api/v1/siddhar/siddhar_sivavakkiyar?include_verses=true
```

---

## Endpoint 6: Get Work (Classical Text)

### `GET /api/v1/work/{id}`

Retrieve metadata and verse index for a classical Siddha work.

#### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|---------|-------------|
| `id` | string | ✅ Yes | Work ID (e.g., `thirumandiram`, `sivavakkiyam`) |

#### Query Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `collection` | string | all | Filter by collection/tantiram |
| `page` | integer | 1 | Verse page number |
| `per_page` | integer | 50 | Verses per page (max: 100) |

#### Response Schema

```json
{
  "status": "success",
  "data": {
    "work_id":       "thirumandiram",
    "title":         "Thirumandiram",
    "author":        "Thirumoolar",
    "period":        "c. 6th–7th century CE",
    "language":      "Tamil",
    "script":        "Tamil script",
    "total_verses_in_corpus": 608,
    "total_verses_in_work":   3000,
    "corpus_coverage_pct":    20.3,
    "collections": [
      { "name": "Tantirams 1-2", "verse_count": 335 },
      { "name": "Tantiram 3 (Part 2)", "verse_count": 260 },
      { "name": "Tantiram 7", "verse_count": 13 }
    ],
    "verses": [
      {
        "document_id":  "thirumandiram_pm_0001",
        "verse_number": "1",
        "collection":   "Tantirams 1-2",
        "tamil_text":   "ஒன்றவன் தானே..."
      }
    ],
    "source_url": "https://www.projectmadurai.org/pm_etexts/utf8/pmuni0010.html",
    "copyright_status": "public_domain"
  },
  "meta": {
    "total": 608, "page": 1, "per_page": 50, "total_pages": 13
  }
}
```

#### Example Requests

```
GET /api/v1/work/thirumandiram
GET /api/v1/work/sivavakkiyam?collection=Sivavakkiyam+Complete&page=2
```

---

## Endpoint 7: Get Formulation

### `GET /api/v1/formulation/{id}`

Retrieve a Siddha medicine formulation record.

#### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|---------|-------------|
| `id` | string | ✅ Yes | Formulation document ID |

#### Response Schema

```json
{
  "status": "success",
  "data": {
    "document_id":   "formulation_kabasura_kudineer",
    "title":         "Kabasura Kudineer",
    "type":          "herbal decoction",
    "ingredients":   ["Nilavembu", "Sirukurinjan", "Korai kizhangu"],
    "indications":   ["fever", "respiratory infections", "flu"],
    "preparation":   "Boil 1g each of 15 herbs in water...",
    "source":        "AYUSH Ministry approved formulation",
    "copyright_status": "public_domain"
  }
}
```

#### Example Requests

```
GET /api/v1/formulation/formulation_kabasura_kudineer
GET /api/v1/formulation/formulation_nilavembu_kudineer
```

---

## Endpoint 8: List Collections

### `GET /api/v1/collections`

List all navigable collections in the corpus.

#### Response Schema

```json
{
  "status": "success",
  "data": {
    "works": [
      { "id": "thirumandiram", "title": "Thirumandiram", "verse_count": 608 },
      { "id": "sivavakkiyam",  "title": "Sivavakkiyam",  "verse_count": 392 }
    ],
    "entity_categories": [
      { "id": "siddhars",  "label": "Siddhars",  "entity_count": 16 },
      { "id": "deities",   "label": "Deities",   "entity_count": 7  },
      { "id": "concepts",  "label": "Concepts",  "entity_count": 24 },
      { "id": "practices", "label": "Practices", "entity_count": 11 },
      { "id": "plants",    "label": "Plants",    "entity_count": 13 },
      { "id": "places",    "label": "Places",    "entity_count": 7  },
      { "id": "body_terms","label": "Body",      "entity_count": 11 },
      { "id": "symbolic",  "label": "Symbolic",  "entity_count": 4  }
    ],
    "doc_types": [
      { "id": "verse",          "label": "Verses",              "count": 1000 },
      { "id": "biography",      "label": "Siddhar Biographies", "count": 10   },
      { "id": "plant",          "label": "Medicinal Plants",    "count": 30   },
      { "id": "formulation",    "label": "Formulations",        "count": 15   },
      { "id": "manuscript",     "label": "Manuscripts",         "count": 15   },
      { "id": "classical_text", "label": "Classical Texts",     "count": 10   },
      { "id": "research",       "label": "Research Papers",     "count": 70   }
    ],
    "total_documents": 1150,
    "total_entities":  93,
    "corpus_version":  "2B-3"
  }
}
```

#### Example

```
GET /api/v1/collections
```

---

## Endpoint 9: Random Verse

### `GET /api/v1/verse/random`

Return a random verse — useful for discovery features.

#### Query Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `work` | string | all | Limit to `Thirumandiram` or `Sivavakkiyam` |
| `entity` | string | — | Limit to verses containing this entity_id |

#### Response
Same schema as `GET /api/v1/verse/{id}`.

---

## Implementation Notes

### For Static Deployment (No Backend)

The search_index.json and normalized_corpus/ files support a **fully static implementation**:

```javascript
// Load index once
const idx = await fetch('/data/search_index.json').then(r => r.json());

// Search
function search(q) {
  const tokens = q.toLowerCase().split(' ');
  return idx.records.filter(rec =>
    tokens.every(t =>
      (rec.search_text || '').toLowerCase().includes(t) ||
      (rec.keywords || []).some(k => k.toLowerCase().includes(t))
    )
  );
}

// Get verse
async function getVerse(id) {
  return fetch(`/data/normalized_corpus/${id}.json`).then(r => r.json());
}
```

### For Server Deployment

A lightweight backend (Python/FastAPI, Node.js/Express) can expose the JSON files as REST endpoints, adding pagination, sorting, and faceted filtering.

---

*API Contract v1.0 — SiddhaVerse Phase 2B-3.5, 2026-06-25*  
*This is documentation only. No backend implementation has been created.*
