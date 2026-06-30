# Corpus Navigation Report
# Phase 2B-3: Corpus Navigation Layer

**Report Date:** 2026-06-25  
**Phase:** 2B-3  
**Purpose:** Design input for SiddhaVerse website navigation structure

---

## 1. Corpus Overview

| Metric | Value |
|--------|-------|
| Total active documents | **1,150** |
| Authenticated verse documents | **1,000** |
| Supporting metadata documents | **150** |
| Unique entities | **93** |
| Entity mentions | **6,956** |
| Languages | Tamil (87%), English (13%) |
| Source works | Thirumandiram, Sivavakkiyam |
| Copyright status | 100% public domain |
| Provenance coverage | 100% |
| Synthetic content | 0% |

---

## 2. Content Distribution

### By Document Type

| Document Type | Count | % | Description |
|--------------|-------|---|-------------|
| Verse (Tamil) | 1,000 | 87.0% | Authenticated classical verses |
| Research (PubMed) | 70 | 6.1% | Scientific studies on Siddha medicine |
| Medicinal Plants | 30 | 2.6% | Materia medica entries |
| Formulations | 15 | 1.3% | Siddha medicine recipes |
| Manuscripts | 15 | 1.3% | Palm-leaf manuscript catalog |
| Siddhar Biographies | 10 | 0.9% | Life and works of Siddhars |
| Classical Texts | 10 | 0.9% | Work-level metadata |

### By Source Work

| Work | Verses | % | Author | Period |
|------|--------|---|--------|--------|
| Thirumandiram | 608 | 60.8% | Thirumoolar | c. 6–7th CE |
| Sivavakkiyam | 392 | 39.2% | Sivavakkiyar | c. 9–10th CE |

### By Collection (Thirumandiram)

| Collection | Verses |
|-----------|--------|
| Tantirams 1–2 | 335 |
| Tantiram 3 (Part 2) | 260 |
| Tantiram 7 | 13 |

---

## 3. Top Entities — Navigation Anchors

These are the most referenced entities in the corpus. They should serve as **primary navigation anchors** on the SiddhaVerse website.

### 🏆 Top 10 Overall Entities

| Rank | Entity | Category | Verse Mentions |
|------|--------|----------|---------------|
| 1 | Pranayama | Practices | 352 |
| 2 | Murugan | Deities | 349 |
| 3 | Vishnu | Deities | 339 |
| 4 | Tiruvannamalai | Places | 288 |
| 5 | Kumbhaka (Breath Retention) | Practices | 286 |
| 6 | Shiva | Deities | 274 |
| 7 | Prana (Life Force) | Concepts | 259 |
| 8 | Thirumoolar | Siddhars | 248 |
| 9 | Three/Trinity | Symbolic | 210 |
| 10 | Dhyana (Meditation) | Concepts | 202 |

---

## 4. Most Referenced — By Category

### 📖 Most Referenced Concepts (Top 10)

| Concept | Verse Mentions |
|---------|---------------|
| Prana (Life Force) | 259 |
| Dhyana (Meditation) | 202 |
| Shiva-Shakti (Divine Union) | 180 |
| Maya (Cosmic Illusion) | 135 |
| Pranava / OM | 119 |
| Jnana (Wisdom) | 117 |
| Mukti (Liberation) | 92 |
| Nadi (Energy Channels) | 90 |
| Karma / Vinai | 74 |
| Mantra | 67 |

### 🧘 Most Referenced Practices (Top 8)

| Practice | Verse Mentions |
|---------|---------------|
| Pranayama (Breath Control) | 352 |
| Kumbhaka (Breath Retention) | 286 |
| Varma (Vital Points) | 157 |
| Mudra (Gesture Seals) | 77 |
| Ashta Siddhi (Eight Powers) | 43 |
| Kayakalpa (Rejuvenation) | 33 |
| Namashivaya (Mantra) | 29 |
| Bandha (Energy Locks) | 9 |

### 🌿 Most Referenced Plants (Top 8)

| Plant | Scientific Name | Verse Mentions |
|-------|----------------|---------------|
| Vallarai | Centella asiatica | 98 |
| Tulsi / Holy Basil | Ocimum tenuiflorum | 95 |
| Lotus | Nelumbo nucifera | 62 |
| Thippili / Long Pepper | Piper longum | 43 |
| Ginger / Sukku | Zingiber officinale | 24 |
| Keezhanelli | Phyllanthus niruri | 11 |
| Ashwagandha | Withania somnifera | 10 |
| Turmeric | Curcuma longa | 7 |

### 🏛️ Most Referenced Siddhars (Top 8)

| Siddhar | Verse Mentions | Author of |
|---------|---------------|-----------|
| Thirumoolar | 248 | Thirumandiram |
| Sivavakkiyar | 180 | Sivavakkiyam |
| Karuvoorar | 75 | Various alchemical texts |
| Kudambai | 63 | Kudambai Siddhar poems |
| Nandidevar | 52 | Guru of Thirumoolar |
| Bogar | 43 | Bogar 7000 |
| Ramadevar | 30 | Various texts |
| Yugi Muni | 27 | Yugi Chinthamani |

### ⛩️ Most Referenced Sacred Places (Top 5)

| Place | Verse Mentions | Significance |
|-------|---------------|-------------|
| Tiruvannamalai | 288 | Arunachala hill; seat of Shiva |
| Chidambaram | 163 | Nataraja temple; cosmic dance |
| Kashi | 100 | Holy city; Varanasi |
| Madurai | 24 | Tamil cultural capital |
| Potigai | 18 | Mountain abode of Agasthiyar |

### 🕉️ Most Referenced Deities (Top 5)

| Deity | Verse Mentions |
|-------|---------------|
| Murugan | 349 |
| Vishnu | 339 |
| Shiva | 274 |
| Shakti | 201 |
| Brahma | 149 |

---

## 5. Corpus Entity Density

| Work | Total Verses | Verses with Entities | Entity Density |
|------|-------------|---------------------|----------------|
| Thirumandiram | 608 | 601 | 98.8% |
| Sivavakkiyam | 392 | 383 | 97.7% |
| **Combined** | **1,000** | **984** | **98.4%** |

Average entities per verse:
- Thirumandiram: ~6.7 entities/verse
- Sivavakkiyam: ~7.3 entities/verse (higher symbolic density)

---

## 6. Recommended Website Navigation Structure

Based on corpus analysis, the following primary navigation sections are recommended:

```
SIDDHAVERSE
│
├── 📜 VERSE LIBRARY
│   ├── Browse by Work
│   │   ├── Thirumandiram (608 verses)
│   │   │   ├── Tantirams 1–2
│   │   │   ├── Tantiram 3
│   │   │   └── Tantiram 7
│   │   └── Sivavakkiyam (392 verses)
│   ├── Browse by Author
│   │   ├── Thirumoolar
│   │   └── Sivavakkiyar
│   └── Random Verse (Dice Roll Feature)
│
├── 🧘 EXPLORE BY TOPIC
│   ├── Concepts (24 entities)
│   │   ├── Prana · Dhyana · Maya · OM · Liberation · Karma
│   ├── Practices (11 entities)
│   │   ├── Pranayama · Mudra · Kayakalpa · Kumbhaka
│   ├── Deities (7 entities)
│   │   ├── Shiva · Shakti · Murugan · Vishnu · Brahma
│   ├── Sacred Places (7 entities)
│   │   ├── Tiruvannamalai · Chidambaram · Kashi
│   └── Symbols (4 entities)
│       ├── Five Letters · Three/Trinity · Eighteen Siddhars
│
├── 🌿 SIDDHA MEDICINE
│   ├── Medicinal Plants (30 records)
│   ├── Formulations (15 records)
│   └── Research Library (70 papers)
│
├── 🧙 THE SIDDHARS
│   ├── Thirumoolar · Sivavakkiyar · Agasthiyar · Bogar
│   ├── Karuvoorar · Pambatti · Machamuni · Konkanar
│   └── All 16 Siddhars
│
├── 📄 MANUSCRIPTS & TEXTS
│   ├── Classical Text Catalog (10 works)
│   └── Palm-Leaf Manuscripts (15 records)
│
└── 🔍 SEARCH
    ├── Full-text Tamil search
    ├── Entity filter
    └── Advanced (work + author + entity combo)
```

---

## 7. Cross-Reference Navigation Examples

Based on the `entity_cross_reference.json`, these navigable relationships exist in the corpus:

### Pranayama navigates to:
- 352 verse documents
- Top co-occurring entities: Kumbhaka (286 shared verses), Prana (240+), Nadi (85+)
- Works: Thirumandiram (primary), Sivavakkiyam (secondary)

### Shiva navigates to:
- 274 verse documents
- Top co-occurring: Shakti (190+), Murugan (200+), Pranava/OM (100+), Chidambaram (140+)
- Works: Both Thirumandiram and Sivavakkiyam

### Lotus (Thamarai) navigates to:
- 62 verse documents
- Top co-occurring: Prana (50+), Light/Flame (45+), Eye (42+), Shiva (40+)
- Works: Both works (symbol of divine purity)

---

## 8. Coverage Statistics for Quality Assurance

| Dimension | Coverage |
|-----------|---------|
| Verses with Tamil text | 1,000 / 1,000 (100%) |
| Verses with transliteration | 1,000 / 1,000 (100%) |
| Verses with entity links | 984 / 1,000 (98.4%) |
| Verses with source URL | 1,000 / 1,000 (100%) |
| Verses with SHA-256 hash | 1,000 / 1,000 (100%) |
| Documents indexed in search_index.json | 1,150 / 1,150 (100%) |
| Entity cross-references built | 93 / 93 (100%) |
| Provenance metadata present | 1,000 / 1,000 (100%) |
| Synthetic content | 0 / 1,000 (0%) |

---

## 9. Gaps to Address in Phase 2B-4+

| Gap | Documents Affected | Priority |
|-----|-------------------|---------|
| English translations | 1,000 verses (0 translated) | High |
| Remaining Thirumandiram (Tantirams 4–9 via extended parser) | ~1,500 verses | High |
| Expanded Sivavakkiyam (133 remaining from pmuni0269) | 133 verses | Medium |
| Additional Siddhar works (Bogar 7000, Agasthiyar, etc.) | ~2,000 verses | Medium |
| Entity lexicon expansion (alchemical terms, body parts) | All 1,000 verses | Medium |
| Tamil morphological disambiguation | All 1,000 verses | Medium |

---

*Report generated by SiddhaVerse Phase 2B-3, 2026-06-25*

> [!CAUTION]
> **PHASE 2B-3 COMPLETE — AWAITING REVIEW**  
> Per JARVIS protocol, this agent is **PAUSED** and awaiting your approval before any AI-related phase (embeddings, vectorization, knowledge graphs, RAG, or chatbot development).
