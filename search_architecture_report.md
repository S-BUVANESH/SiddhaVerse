# Search Architecture Report
# Phase 2B-3: Search Infrastructure

**Report Date:** 2026-06-25  
**Phase:** 2B-3 — Search Architecture  
**Index File:** `search_index.json`  
**Documents Indexed:** 1,150

---

## 1. Architecture Overview

The SiddhaVerse search index is a **flat-file JSON index** designed for human-readable browsing, static site integration, and client-side keyword search — without any server-side search engine, LLM, or AI system.

### Design Principles
- **No AI.** Search is lexical — text substring and keyword matching only.
- **No embeddings.** No vector similarity. No semantic inference.
- **Human-first.** Every search result links to a real, verifiable document.
- **Statically deployable.** The index is a single JSON file usable in any web frontend.

---

## 2. Index Structure

The `search_index.json` contains:

```json
{
  "index_version":      "2B-3",
  "generated_at":       "2026-06-25T13:52:53Z",
  "total_documents":    1150,
  "searchable_fields":  ["search_text", "keywords", "title",
                         "source_work", "author", "entity_ids"],
  "records": [ ... ]
}
```

### Per-Document Record Schema

| Field | Type | Description |
|-------|------|-------------|
| `document_id` | string | Unique ID (primary key) |
| `title` | string | Human-readable title |
| `source_work` | string | Thirumandiram, Sivavakkiyam, etc. |
| `author` | string | Thirumoolar, Sivavakkiyar, etc. |
| `collection` | string | Sub-collection or tantiram |
| `verse_number` | string | Verse number within work |
| `language` | string | Tamil / English |
| `doc_type` | string | verse / biography / formulation / plant / manuscript / classical_text / research |
| `entity_ids` | array | List of matched entity IDs |
| `keywords` | array | Auto-generated keyword list |
| `search_text` | string | Combined Tamil text + transliteration + metadata for full-text search |
| `source_url` | string | Original source URL |
| `copyright_status` | string | public_domain / open_access |

---

## 3. Search Coverage

| Metric | Value |
|--------|-------|
| Total documents indexed | 1,150 |
| Verse documents | 1,000 |
| Non-verse documents | 150 |
| Documents with Tamil text searchable | 1,000 |
| Documents with entity keywords | 984 |
| Documents with source URL | 1,000 |
| **Search coverage (entity-linked)** | **98.4%** |
| **Search coverage (full text)** | **100%** |

> [!IMPORTANT]
> All 1,150 documents are indexed in `search_index.json`. Every document is reachable via title, keyword, entity, author, or source_work search. Search coverage: **100%**.

---

## 4. Searchable Dimensions

Users can discover content by searching any of the following dimensions:

| Dimension | How Implemented | Example Query |
|-----------|----------------|--------------|
| **Verse text (Tamil)** | `search_text` field contains original Tamil | "ஒன்றவன் தானே" |
| **Verse text (Roman)** | `search_text` includes transliteration | "onravan thane" |
| **Siddhar** | `keywords` + `entity_ids` | "Thirumoolar", "siddhar_thirumoolar" |
| **Plant** | `keywords` + `entity_ids` | "Tulsi", "plant_tulsi" |
| **Concept** | `keywords` + `entity_ids` | "Yoga", "Kundalini", "concept_yoga" |
| **Deity** | `keywords` + `entity_ids` | "Shiva", "deity_shiva" |
| **Practice** | `keywords` + `entity_ids` | "Pranayama", "practice_pranayama" |
| **Place** | `keywords` + `entity_ids` | "Chidambaram", "place_chidambaram" |
| **Formulation** | `keywords` + `doc_type=formulation` | "Kabasura Kudineer" |
| **Work / Collection** | `source_work`, `collection` | "Thirumandiram", "Tantiram 3" |
| **Author** | `author` field | "Thirumoolar" |
| **Document type** | `doc_type` filter | verse, biography, plant, manuscript |

---

## 5. Keyword Generation Strategy

Keywords are algorithmically derived from document metadata — not manually tagged and not AI-generated:

1. **Metadata keywords**: author, source_work, collection, language, copyright_status, repository name
2. **Entity keywords**: each entity_id is converted to its English name and appended
3. **Type keywords**: document category tags added (e.g., "Tamil verse", "Shaiva Siddhanta", "Siddha medicine")

**Example keyword set for a Thirumandiram verse:**
```json
["Thirumandiram", "Tamil verse", "Shaiva Siddhanta", "yoga", "tantra",
 "Thirumoolar", "Tamil", "public_domain", "Project Madurai",
 "Shiva", "Pranayama", "Nadi", "Eye", "Light/Flame"]
```

---

## 6. Document Type Distribution

| Type | Count | % | Searchable via |
|------|-------|---|----------------|
| verse | 1,000 | 87.0% | Tamil text, transliteration, entities, keywords |
| research | 70 | 6.1% | Title, abstract, keywords |
| plant | 30 | 2.6% | Plant name, Tamil name, description |
| formulation | 15 | 1.3% | Formulation name, ingredients |
| manuscript | 15 | 1.3% | Repository, manuscript ID, description |
| biography | 10 | 0.9% | Siddhar name, description |
| classical_text | 10 | 0.9% | Title, author, description |

---

## 7. Recommended Frontend Implementation

For the SiddhaVerse website, the following search flow is recommended (no backend required):

```
User Types Query
      ↓
Client-side: Load search_index.json (once, cached)
      ↓
Tokenize query → lowercase → split on spaces
      ↓
Filter records where ANY of:
  • search_text.toLowerCase().includes(token)
  • keywords includes token
  • entity_ids includes token
  • author.toLowerCase().includes(token)
  • source_work.toLowerCase().includes(token)
      ↓
Return matching document_ids → display title, verse_number, source_work
      ↓
User clicks → load normalized_corpus/{document_id}.json → display full verse
```

This is a pure static implementation — no server, no database, no AI.

---

## 8. Filter Facets for Website Navigation

Based on the index structure, the following filter facets are recommended:

| Facet | Values |
|-------|--------|
| **Work** | Thirumandiram, Sivavakkiyam |
| **Document Type** | Verse, Biography, Plant, Formulation, Manuscript, Research |
| **Author** | Thirumoolar, Sivavakkiyar, Agasthiyar, Bogar, etc. |
| **Entity Category** | Siddhars, Deities, Places, Concepts, Practices, Plants |
| **Collection** | Tantirams 1–2, Tantiram 3 (Part 2), Sivavakkiyam Complete, etc. |
| **Language** | Tamil, English |

---

*Report generated by SiddhaVerse Phase 2B-3, 2026-06-25*
