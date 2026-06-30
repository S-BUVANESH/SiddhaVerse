# SiddhaVerse Source Ranking Matrix

This matrix ranks all 30 discovered sources based on a **Composite Ingestion Score** designed to optimize the acquisition pipeline.

## Scoring Methodology
The **Composite Score** (0-100) is calculated as follows:
- **Trust Score Weight (40%):** Promotes validated, authoritative repositories.
- **Priority Weight (40%):** Reflects editorial urgency (Critical=100, High=80, Medium=50, Low=20).
- **Acquisition Ease (20%):** Inversely proportional to difficulty (Difficulty 1 = 100 points, Difficulty 10 = 10 points).

$$\text{Composite Score} = (\text{Trust Score} \times 10) \times 0.4 + \text{Priority Score} \times 0.4 + (11 - \text{Difficulty}) \times 10 \times 0.2$$

---

## Ingestion Priority Ranking

| Rank | Title | Source Type | Priority | Difficulty | Access Type | Composite Score |
| :---: | :--- | :--- | :--- | :---: | :--- | :---: |
| 1 | Central Council for Research in Siddha (CCRS) | Government Publication | **CRITICAL** | 2 | `partially_open` | **98.0** |
| 2 | National Institute of Siddha (NIS) | Government Publication | **CRITICAL** | 3 | `partially_open` | **96.0** |
| 3 | Pharmacopoeia Commission for Indian Medicine & Homoeopathy (PCIM&H) | Government Publication | **CRITICAL** | 3 | `partially_open` | **96.0** |
| 4 | British Library Endangered Archives Programme | Palm Leaf | **CRITICAL** | 4 | `open` | **94.0** |
| 5 | Tamil University Department of Siddha Medicine | Research Paper | **CRITICAL** | 4 | `partially_open` | **93.2** |
| 6 | PubMed Central Siddha Medicine Articles | Research Paper | **HIGH** | 1 | `open` | **92.0** |
| 7 | WHO Traditional Medicine Monographs | Government Publication | **HIGH** | 1 | `open` | **92.0** |
| 8 | Tamil Virtual Academy Digital Library | Book | **CRITICAL** | 4 | `open` | **92.0** |
| 9 | Thanjavur Maharaja Serfoji's Sarasvati Mahal Library | Palm Leaf | **CRITICAL** | 6 | `partially_open` | **90.0** |
| 10 | Tamil Digital Library (TVA Portal) | Book | **CRITICAL** | 5 | `open` | **90.0** |
| 11 | Botanical Survey of India (BSI) Plant Database | Government Publication | **HIGH** | 2 | `open` | **89.2** |
| 12 | Government Oriental Manuscripts Library (GOML) Chennai | Palm Leaf | **CRITICAL** | 6 | `partially_open` | **89.2** |
| 13 | Journal of Research in Siddha Medicine (JRSM) | Research Paper | **HIGH** | 2 | `open` | **89.2** |
| 14 | National Medicinal Plants Board (NMPB) | Government Publication | **HIGH** | 2 | `open` | **89.2** |
| 15 | ICMR Quality Standards of Indian Medicinal Plants | Research Paper | **HIGH** | 3 | `partially_open` | **88.0** |
| 16 | AYUSH Research Portal | Research Paper | **HIGH** | 3 | `open` | **87.2** |
| 17 | Directorate of Indian Medicine and Homoeopathy (DIMH) Tamil Nadu | Government Publication | **HIGH** | 3 | `partially_open` | **87.2** |
| 18 | IMPPAT: Indian Medicinal Plants, Phytochemistry And Therapeutics | Research Paper | **HIGH** | 3 | `open` | **87.2** |
| 19 | Journal of Siddha (JOS) | Research Paper | **HIGH** | 3 | `partially_open` | **86.0** |
| 20 | French Institute of Pondicherry (IFP) Digital Collections | Palm Leaf | **HIGH** | 6 | `open` | **82.0** |
| 21 | Institute of Asian Studies Chennai | Palm Leaf | **HIGH** | 5 | `partially_open` | **82.0** |
| 22 | Connemara Public Library | Book | **HIGH** | 6 | `partially_open` | **81.2** |
| 23 | Dr. U. V. Swaminatha Iyer Library | Palm Leaf | **HIGH** | 6 | `partially_open` | **81.2** |
| 24 | Internet Archive Siddhar Literature Collection | Book | **HIGH** | 4 | `open` | **80.0** |
| 25 | Roja Muthiah Research Library (RMRL) | Book | **HIGH** | 7 | `restricted` | **79.2** |
| 26 | Directory of Open Access Journals (DOAJ) | Research Paper | **MEDIUM** | 2 | `open` | **77.2** |
| 27 | ScienceDirect Siddha Research Literature | Research Paper | **MEDIUM** | 3 | `partially_open` | **76.0** |
| 28 | SpringerLink Siddha Pharmacology Literature | Research Paper | **MEDIUM** | 3 | `partially_open` | **76.0** |
| 29 | CSIR-National Botanical Research Institute (NBRI) | Research Paper | **MEDIUM** | 4 | `partially_open` | **73.2** |
| 30 | Traditional Knowledge Digital Library (TKDL) | Government Publication | **MEDIUM** | 10 | `restricted` | **62.0** |

## Pipeline Action Plan

### Tier 1: Immediate Acquisition (Score >= 88.0)
*These sources represent the foundation of the corpus. They combine critical status or high trust with very low difficulty barriers (open APIs, direct downloads, or clean digitization).*
- **Central Council for Research in Siddha (CCRS)** (Score: 98.0) - Official scientific reference layer under AYUSH. Ingestion should focus on extracting official clinical definitions, safety guidelines, and research summaries.
- **National Institute of Siddha (NIS)** (Score: 96.0) - Premium academic institute for post-graduate education and research. Store metadata, abstract summaries, and public research brochures.
- **Pharmacopoeia Commission for Indian Medicine & Homoeopathy (PCIM&H)** (Score: 96.0) - Establishes legal quality standards and formulas. Essential for the formulations and plants registries.
- **British Library Endangered Archives Programme** (Score: 94.0) - Extremely high value for palm leaf discovery under CC licenses. EAP810 contains manuscripts on Siddha medicine.
- **Tamil University Department of Siddha Medicine** (Score: 93.2) - Core educational and research department focusing on Tamil palm leaf medicine transcription and analysis.
- **PubMed Central Siddha Medicine Articles** (Score: 92.0) - Highest-trust scientific evidence layer. Download and extract full-text files that are marked Open Access/Creative Commons.
- **WHO Traditional Medicine Monographs** (Score: 92.0) - Global reference layer. Provides regulatory validation and safety profiles for plants.
- **Tamil Virtual Academy Digital Library** (Score: 92.0) - Primary repository for classical Tamil texts and digitized publications. Ingestion must prioritize out-of-copyright classical songs.
- **Thanjavur Maharaja Serfoji's Sarasvati Mahal Library** (Score: 90.0) - One of the oldest libraries in Asia. Holds rare palm leaf manuscripts and early printed books. Acquisition is restricted; metadata is publicly cataloged.
- **Tamil Digital Library (TVA Portal)** (Score: 90.0) - Key acquisition portal for digitized historical prints. Check individual book publishing dates for copyright status (generally pre-1956 is safe).
- **Botanical Survey of India (BSI) Plant Database** (Score: 89.2) - Vital for cross-referencing plant taxonomy, scientific names, and confirming species classification.
- **Government Oriental Manuscripts Library (GOML) Chennai** (Score: 89.2) - Major state-owned repository of palm-leaves. Part of the Department of Archaeology's digitization initiative.
- **Journal of Research in Siddha Medicine (JRSM)** (Score: 89.2) - Specialized peer-reviewed journal for Siddha. Highly structured metadata and abstracts.
- **National Medicinal Plants Board (NMPB)** (Score: 89.2) - Authoritative botanical registry for identifying plants and mapping vernacular names to scientific nomenclature.
- **ICMR Quality Standards of Indian Medicinal Plants** (Score: 88.0) - Authoritative monograph publications from ICMR. Highly valuable for chemical validation of Siddha plants.

### Tier 2: Secondary Processing (Score 70.0 - 87.9)
*Sources containing premium research or rare digital books, but presenting moderate acquisition barriers (requires basic web scraping, bulk PDF extraction, or structural cleaning).*
- **AYUSH Research Portal** (Score: 87.2) - Meta-registry for AYUSH research. Restrict to harvesting metadata, abstracts, and DOIs for clinical validation.
- **Directorate of Indian Medicine and Homoeopathy (DIMH) Tamil Nadu** (Score: 87.2) - State licensing authority for Siddha medicine. Reference source for official list of licensed formulations and standards.
- **IMPPAT: Indian Medicinal Plants, Phytochemistry And Therapeutics** (Score: 87.2) - Excellent scientific dataset linking Siddha plants to chemical formulations and active components. Use for entity relationship modeling.
- **Journal of Siddha (JOS)** (Score: 86.0) - Academic journal published by NIS. Extract peer-reviewed data on clinical findings.
- **French Institute of Pondicherry (IFP) Digital Collections** (Score: 82.0) - Premier collection of digitized palm-leaves. Excellent repository for historical manuscript structures.
- **Institute of Asian Studies Chennai** (Score: 82.0) - Published detailed descriptive catalogues of palm-leaf manuscripts in Tamil, which are crucial for finding Siddha references.
- **Connemara Public Library** (Score: 81.2) - National depository library. Holds rare early-printed monographs on Siddha medicine which are in the public domain.
- **Dr. U. V. Swaminatha Iyer Library** (Score: 81.2) - Holds a major collection of classical Tamil palm leaves. Important reference for verifying textual variations.
- **Internet Archive Siddhar Literature Collection** (Score: 80.0) - Contains out-of-copyright scans. Check individual upload metadata for license details.
- **Roja Muthiah Research Library (RMRL)** (Score: 79.2) - Exceptional archive of early printed materials. Access is largely restricted; use for cataloging metadata and tracking historical printing of texts.
- **Directory of Open Access Journals (DOAJ)** (Score: 77.2) - Registry of open-access publications, useful for discovering legal research PDFs on Siddha.
- **ScienceDirect Siddha Research Literature** (Score: 76.0) - High-quality research database. Extract abstract summaries, keywords, and DOIs for validation.
- **SpringerLink Siddha Pharmacology Literature** (Score: 76.0) - Highly vetted scientific papers. Extract metadata and abstract text only.
- **CSIR-National Botanical Research Institute (NBRI)** (Score: 73.2) - High-quality research institute focusing on plant conservation and medicinal testing.

### Tier 3: Reference & Manual Cataloging (Score < 70.0)
*Restricted databases (like TKDL) or extremely hard-to-harvest palm-leaf manuscripts. These should be treated as metadata reference layers or cataloged manually.*
- **Traditional Knowledge Digital Library (TKDL)** (Score: 62.0) - Prior-art protection database. Strictly a reference source since access is highly restricted. Do not attempt direct web acquisition; use for schema validation and mapping of public records.
