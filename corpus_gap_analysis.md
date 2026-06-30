# SiddhaVerse Corpus Gap Analysis

This document analyzes the current status of the pilot corpus, identifies remaining gaps, and outlines recommended targets for large-scale ingestion.

## Current Balanced Coverage (150 Documents)
With the execution of Phase 2A.5, the pilot corpus has achieved initial representation across all primary domains:

| Domain | Pilot Count | Focus Area | Status |
| :--- | :---: | :--- | :--- |
| **Siddhars** | 10 | Biographies of 10 major pathinein Siddhargal | **INITIALIZED** |
| **Plants** | 30 | Botanical nomenclature and chemical constituents of 30 core herbs | **ESTABLISHED** |
| **Formulations** | 15 | Traditional preparation recipes from the Siddha Formulary of India | **INITIALIZED** |
| **Manuscripts** | 15 | Catalog records of palm-leaf manuscripts from EAP810, IFP, and GOML | **INITIALIZED** |
| **Classics** | 10 | Metadata and structural outlines of classical texts (e.g. Thirumandiram) | **INITIALIZED** |
| **Research** | 70 | Peer-reviewed pharmacological and clinical trials from PMC | **ESTABLISHED** |

---

## Identified Gaps & Missing Domains

Despite the balancing phase, several critical domains remain underrepresented and require large-scale acquisition in Phase 2B:

1. **Granular Formulation Ingredients (Rasa/Veerya/Vipaka):**
   - *Current Status:* Only 15 formulations are ingested, containing ingredients and simple preparation methods.
   - *Gap:* Lacks chemical interaction schemas and detailed pharmacology of combined minerals (*Bhasmas* and *Parpams*).
   - *Target:* Ingest all 400+ entries in the Siddha Formulary of India (SFI).

2. **Palm-Leaf Manuscript Transcriptions (Raw Tamil Verses):**
   - *Current Status:* Manuscript registries are metadata-only (titles and catalogs).
   - *Gap:* Lacks the raw, transcribed Tamil verse text needed for semantic search and NLP models.
   - *Target:* Ingest transcribed texts from TVA's digitized library (e.g., EAP810 digitized transcription subsets).

3. **Varma Kalai (Siddha Traumatology and Pressure Points):**
   - *Current Status:* Included only as a subtopic in 2 manuscript catalog records.
   - *Gap:* Lacks specific anatomical mappings, pressure point pathways, and therapeutic methods.
   - *Target:* Ingest Varma-specific classical manuals such as *Varma Kannadi* and *Varma Suthiram*.

---

## Recommended Ingestion Targets for Phase 2B

We recommend prioritizing the following targets during large-scale acquisition to build the largest freely accessible Siddha library:

| Source Repository | Target Category | Estimated Document Count | Action Plan |
| :--- | :--- | :---: | :--- |
| **Pharmacopoeia Commission (PCIM&H)** | Formulations & Plants | 500+ | Ingest all published monographs from the Siddha Pharmacopoeia of India (SPI) and SFI. |
| **Tamil Virtual Academy (TVA)** | Classical Songs & Lyrics | 10,000+ verses | Bulk scrape public-domain Tamil Siddhar poems (e.g. Sithar Padalgal collection). |
| **British Library (EAP810 / EAP1217)** | Palm Leaf Transcriptions | 500+ | Download CC-licensed XML catalog mappings and public domain Tamil transcriptions. |
| **IMPPAT Database** | Phytochemical Profiles | 1,000+ | Map chemical compound linkages for all registered Siddha medicinal plants. |
| **PMC / EuropePMC** | Scientific Papers | 1,000+ | Ingest open-access pharmacology validation papers using automated API pipelines. |
