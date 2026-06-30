# SiddhaVerse Acquisition Report (Phase 2A.5 Balancing Update)

This report details the audit log of the Phase 2A/2A.5 Controlled Ingestion Pilot and Balancing phase. It contains details on all attempts, including failures and their specific causes.

## Acquisition Executive Summary
- **Total Ingestion Attempts:** 162
- **Successful Ingestions:** 150
- **Failed Ingestions:** 12
- **Verification Status:** Fully Verified, Schema Compliant, and Balanced

---

## Ingested Documents Statistics
- **PubMed Research Papers:** 70 (SUCCESS)
- **NMPB Plant Profiles:** 30 (SUCCESS)
- **Siddhar Biographies:** 10 (SUCCESS)
- **Palm-Leaf Manuscript Records:** 15 (SUCCESS)
- **Classical Tamil Texts:** 10 (SUCCESS)
- **Traditional Formulations:** 15 (SUCCESS)

---

## Verification of Failed PMC Records
The following 12 PubMed records were queried during search and flagged as **FAILED** due to missing fields (either Title or Abstract) which are mandatory for down-stream processing:

1. **PMID 1740712** ("Anatomic divisions.")
   - *Cause:* Missing Abstract. Very old (1991) indexed citation without digitized abstract text.
2. **PMID 24823405** ("Mudi-chood.")
   - *Cause:* Missing Abstract. Brief correspondence or case note without abstract content.
3. **PMID 35342137** ("Imported Ayurvedic Medicine and Lead Poisoning.")
   - *Cause:* Missing Abstract. Short letter or editorial without abstract text.
4. **PMID 37553150** ("Lead toxicity from Ayurvedic medicines.")
   - *Cause:* Missing Abstract. Brief comment or clinical alert without abstract.
5. **PMID 18630252** ("Bioethics and ayurveda.")
   - *Cause:* Missing Abstract. Brief review or opinion piece without abstract.
6. **PMID 2049699** ("Ayurvedic medicine.")
   - *Cause:* Missing Abstract. Very old (1991) brief commentary without abstract.
7. **PMID 31044769** ("Low-Cost Pharma.")
   - *Cause:* Missing Abstract. Editorial or brief brief commentary without abstract.
8. **PMID 40507208** ("PMID 40507208")
   - *Cause:* Missing Title. Record has an abstract but lacks a title field in the database.
9. **PMID 34274185** ("Earliest details of dermatology by Ayurveda.")
   - *Cause:* Missing Abstract. Historical note or short communication without abstract.
10. **PMID 39736959** ("PMID 39736959")
   - *Cause:* Missing Title. Record has an abstract but lacks a title field in the database.
11. **PMID 26600632** ("Role of pharmacology for integration of modern medicine and Ayurveda.")
   - *Cause:* Missing Abstract. Brief conference or editorial note without abstract.
12. **PMID 6797562** ("Indian childhood cirrhosis.")
   - *Cause:* Missing Abstract. Very old (1981) index citation without abstract.

---

## Detailed Ingestion Log

| # | Source Repository | Document Title | Document Type | License Status | Status | Note |
| :---: | :--- | :--- | :--- | :--- | :---: | :--- |
| 1 | PubMed Central | Ayurvedic medicine for schizophrenia. | Research Paper | `free_full_text` | **SUCCESS** | *N/A* |
| 2 | PubMed Central | Traditional Indian spices and their health significance. | Research Paper | `free_full_text` | **SUCCESS** | *N/A* |
| 3 | PubMed Central | Lead encephalopathy due to traditional medicines. | Research Paper | `free_full_text` | **SUCCESS** | *N/A* |
| 4 | PubMed Central | Uses of turmeric in dentistry: an update. | Research Paper | `free_full_text` | **SUCCESS** | *N/A* |
| 5 | PubMed Central | Ayurvedic treatments for diabetes mellitus. | Research Paper | `free_full_text` | **SUCCESS** | *N/A* |
| 6 | PubMed Central | Introduction to 'Rasashaastra' the Iatrochemistry of Ayurveda. | Research Paper | `free_full_text` | **SUCCESS** | *N/A* |
| 7 | PubMed Central | An overview on ashwagandha: a Rasayana (rejuvenator) of Ayurveda. | Research Paper | `free_full_text` | **SUCCESS** | *N/A* |
| 8 | PubMed Central | Mainstreaming AYUSH: an ethical analysis. | Research Paper | `free_full_text` | **SUCCESS** | *N/A* |
| 9 | PubMed Central | The development of Terminalia chebula Retz. (Combretaceae) in clinical research. | Research Paper | `free_full_text` | **SUCCESS** | *N/A* |
| 10 | PubMed Central | Phytochemical and pharmacological properties of Gymnema sylvestre: an important  | Research Paper | `free_full_text` | **SUCCESS** | *N/A* |
| 11 | PubMed Central | Venthamarai chooranam, a polyherbal Siddha medicine, alleviates hypertension via | Research Paper | `free_full_text` | **SUCCESS** | *N/A* |
| 12 | PubMed Central | Effects of Ashwagandha (roots of Withania somnifera) on neurodegenerative diseas | Research Paper | `free_full_text` | **SUCCESS** | *N/A* |
| 13 | PubMed Central | Approaches in fostering quality parameters for medicinal botanicals in the India | Research Paper | `free_full_text` | **SUCCESS** | *N/A* |
| 14 | PubMed Central | Curcumin: a potential candidate in prevention of cancer via modulation of molecu | Research Paper | `free_full_text` | **SUCCESS** | *N/A* |
| 15 | PubMed Central | Pharmacologic overview of Withania somnifera, the Indian Ginseng. | Research Paper | `free_full_text` | **SUCCESS** | *N/A* |
| 16 | PubMed Central | Genome-wide analysis correlates Ayurveda Prakriti. | Research Paper | `free_full_text` | **SUCCESS** | *N/A* |
| 17 | PubMed Central | Withania somnifera: From prevention to treatment of cancer. | Research Paper | `free_full_text` | **SUCCESS** | *N/A* |
| 18 | PubMed Central | Ayurpharmacoepidemiology en Route to Safeguarding Safety and Efficacy of Ayurved | Research Paper | `free_full_text` | **SUCCESS** | *N/A* |
| 19 | PubMed Central | Benefits of antioxidant supplements for knee osteoarthritis: rationale and reali | Research Paper | `free_full_text` | **SUCCESS** | *N/A* |
| 20 | PubMed Central | Plants used to treat diabetes in Sri Lankan Siddha Medicine - An ethnopharmacolo | Research Paper | `free_full_text` | **SUCCESS** | *N/A* |
| 21 | PubMed Central | Therapeutic Uses of Triphala in Ayurvedic Medicine. | Research Paper | `free_full_text` | **SUCCESS** | *N/A* |
| 22 | PubMed Central | Thraatchathi Chooranam, protects cardiomyocytes against oxidative stress. | Research Paper | `free_full_text` | **SUCCESS** | *N/A* |
| 23 | PubMed Central | Ayurveda metallic-mineral 'Bhasma'-associated severe liver injury. | Research Paper | `free_full_text` | **SUCCESS** | *N/A* |
| 24 | PubMed Central | An Overview on Genistein and its Various Formulations. | Research Paper | `free_full_text` | **SUCCESS** | *N/A* |
| 25 | PubMed Central | History of the Growing Burden of Cancer in India: From Antiquity to the 21st Cen | Research Paper | `free_full_text` | **SUCCESS** | *N/A* |
| 26 | PubMed Central | Ayurveda and COVID-19: Where psychoneuroimmunology and the meaning response meet | Research Paper | `free_full_text` | **SUCCESS** | *N/A* |
| 27 | PubMed Central | Health System Development in Nepal. | Research Paper | `free_full_text` | **SUCCESS** | *N/A* |
| 28 | PubMed Central | AYUSH for COVID-19: Science or Superstition? | Research Paper | `free_full_text` | **SUCCESS** | *N/A* |
| 29 | PubMed Central | A Comprehensive Review and Perspective on Anticancer Mechanisms of Withaferin A  | Research Paper | `free_full_text` | **SUCCESS** | *N/A* |
| 30 | PubMed Central | Swarna Bindu Prashana-an Ancient Approach to Improve the Infant's Immunity. | Research Paper | `free_full_text` | **SUCCESS** | *N/A* |
| 31 | PubMed Central | The Microbiome in Health and Disease from the Perspective of Modern Medicine and | Research Paper | `free_full_text` | **SUCCESS** | *N/A* |
| 32 | PubMed Central | A comprehensive review on potential therapeutics interventions for COVID-19. | Research Paper | `free_full_text` | **SUCCESS** | *N/A* |
| 33 | PubMed Central | Ayurgenomics and Modern Medicine. | Research Paper | `free_full_text` | **SUCCESS** | *N/A* |
| 34 | PubMed Central | Ayurveda and Epigenetics. | Research Paper | `free_full_text` | **SUCCESS** | *N/A* |
| 35 | PubMed Central | Safety of Ashwagandha Root Extract: A Randomized, Placebo-Controlled, study in H | Research Paper | `free_full_text` | **SUCCESS** | *N/A* |
| 36 | PubMed Central | Herbal immune-boosters: Substantial warriors of pandemic Covid-19 battle. | Research Paper | `free_full_text` | **SUCCESS** | *N/A* |
| 37 | PubMed Central | A Systematic Review and Meta-Analysis of Ayurvedic Herbal Preparations for Hyper | Research Paper | `free_full_text` | **SUCCESS** | *N/A* |
| 38 | PubMed Central | Kabasura Kudineer (KSK), a poly-herbal Siddha medicine, reduced SARS-CoV-2 viral | Research Paper | `free_full_text` | **SUCCESS** | *N/A* |
| 39 | PubMed Central | Phytochemistry, Food Application, and Therapeutic Potential of the Medicinal Pla | Research Paper | `free_full_text` | **SUCCESS** | *N/A* |
| 40 | PubMed Central | Withaferin A in the Treatment of Liver Diseases: Progress and Pharmacokinetic In | Research Paper | `free_full_text` | **SUCCESS** | *N/A* |
| 41 | PubMed Central | Withaferin A: From Ancient Remedy to Potential Drug Candidate. | Research Paper | `free_full_text` | **SUCCESS** | *N/A* |
| 42 | PubMed Central | Curcumin and Weight Loss: Does It Work? | Research Paper | `free_full_text` | **SUCCESS** | *N/A* |
| 43 | PubMed Central | COMMENT: Ayurveda awaits a new dawn. | Research Paper | `free_full_text` | **SUCCESS** | *N/A* |
| 44 | PubMed Central | Some thoughts on the undergraduate Ayurveda curriculum. | Research Paper | `free_full_text` | **SUCCESS** | *N/A* |
| 45 | PubMed Central | Confessions of an Ayurveda professor. | Research Paper | `free_full_text` | **SUCCESS** | *N/A* |
| 46 | PubMed Central | "Confessions of an Ayurveda professor" - A wake up call. | Research Paper | `free_full_text` | **SUCCESS** | *N/A* |
| 47 | PubMed Central | [Recommendations of the committee on complementary medicine and nutrition in ayu | Research Paper | `free_full_text` | **SUCCESS** | *N/A* |
| 48 | PubMed Central | Rise of Siddha medicine: causes and constructions in the Madras Presidency (1920 | Research Paper | `free_full_text` | **SUCCESS** | *N/A* |
| 49 | PubMed Central | Of odysseys and miracles: A narrative approach on therapeutic mobilities for ayu | Research Paper | `free_full_text` | **SUCCESS** | *N/A* |
| 50 | PubMed Central | Curiosity and Creative Experimentation Among Psychiatrists in India. | Research Paper | `free_full_text` | **SUCCESS** | *N/A* |
| 51 | PubMed Central | Give truth a chance. | Research Paper | `free_full_text` | **SUCCESS** | *N/A* |
| 52 | PubMed Central | Deluded confession: Response to Kishor Patwardhan. | Research Paper | `free_full_text` | **SUCCESS** | *N/A* |
| 53 | PubMed Central | Antimalarial potential of Kerala Ayurvedic Water "Pathimugam". | Research Paper | `free_full_text` | **SUCCESS** | *N/A* |
| 54 | PubMed Central | Effects of  | Research Paper | `free_full_text` | **SUCCESS** | *N/A* |
| 55 | PubMed Central | Adverse events in India's Ayush interventions for cervical and lumbar spondylosi | Research Paper | `free_full_text` | **SUCCESS** | *N/A* |
| 56 | PubMed Central | Can Ayurveda medicine supplement modern medical treatments in chronic disease ma | Research Paper | `free_full_text` | **SUCCESS** | *N/A* |
| 57 | PubMed Central | Ayurveda therapy in the management of epilepsy. | Research Paper | `free_full_text` | **SUCCESS** | *N/A* |
| 58 | PubMed Central | Ayurveda Management of Allergic Rhinitis: Protocol for a Randomized Controlled T | Research Paper | `free_full_text` | **SUCCESS** | *N/A* |
| 59 | PubMed Central | Ayurvedic Ingredients in Dermatology: A Call for Research. | Research Paper | `free_full_text` | **SUCCESS** | *N/A* |
| 60 | PubMed Central | Efficacy, side effects, adherence, affordability, and procurement of dietary sup | Research Paper | `free_full_text` | **SUCCESS** | *N/A* |
| 61 | PubMed Central | Quantifying Withanolides in Plasma: Pharmacokinetic Studies and Analytical Metho | Research Paper | `free_full_text` | **SUCCESS** | *N/A* |
| 62 | PubMed Central | Revisiting the tridosha paradigm of Ayurveda. | Research Paper | `free_full_text` | **SUCCESS** | *N/A* |
| 63 | PubMed Central | Confused mystification of Ayurvedic concepts. | Research Paper | `free_full_text` | **SUCCESS** | *N/A* |
| 64 | PubMed Central | Computer-aided discovery of dual-target compounds for Alzheimer's from ayurvedic | Research Paper | `free_full_text` | **SUCCESS** | *N/A* |
| 65 | PubMed Central | Enhancing healthspan with Ashwagandha (Withania somnifera): a comprehensive revi | Research Paper | `free_full_text` | **SUCCESS** | *N/A* |
| 66 | PubMed Central | Overview of Ayurveda and Ashwagandha: Bioactive Phytochemicals and Potential App | Research Paper | `free_full_text` | **SUCCESS** | *N/A* |
| 67 | PubMed Central | The Role of  | Research Paper | `free_full_text` | **SUCCESS** | *N/A* |
| 68 | PubMed Central | Cerebral Edema Secondary to Heavy Metal Toxicity From Siddha Medicine: A Case Re | Research Paper | `free_full_text` | **SUCCESS** | *N/A* |
| 69 | PubMed Central | The Clinical Implications of Ashwagandha ( | Research Paper | `free_full_text` | **SUCCESS** | *N/A* |
| 70 | PubMed Central | Traditional veterinary medicine in India. | Research Paper | `free_full_text` | **SUCCESS** | *N/A* |
| 71 | PubMed Central | Anatomic divisions. | Research Paper | `free_full_text` | **FAILED** | *Missing Abstract. Very old (1991) indexed citation without digitized abstract text.* |
| 72 | PubMed Central | Mudi-chood. | Research Paper | `free_full_text` | **FAILED** | *Missing Abstract. Brief correspondence or case note without abstract content.* |
| 73 | PubMed Central | Imported Ayurvedic Medicine and Lead Poisoning. | Research Paper | `free_full_text` | **FAILED** | *Missing Abstract. Short letter or editorial without abstract text.* |
| 74 | PubMed Central | Lead toxicity from Ayurvedic medicines. | Research Paper | `free_full_text` | **FAILED** | *Missing Abstract. Brief comment or clinical alert without abstract.* |
| 75 | PubMed Central | Bioethics and ayurveda. | Research Paper | `free_full_text` | **FAILED** | *Missing Abstract. Brief review or opinion piece without abstract.* |
| 76 | PubMed Central | Ayurvedic medicine. | Research Paper | `free_full_text` | **FAILED** | *Missing Abstract. Very old (1991) brief commentary without abstract.* |
| 77 | PubMed Central | Low-Cost Pharma. | Research Paper | `free_full_text` | **FAILED** | *Missing Abstract. Editorial or brief brief commentary without abstract.* |
| 78 | PubMed Central | PMID 40507208 | Research Paper | `free_full_text` | **FAILED** | *Missing Title. Record has an abstract but lacks a title field in the database.* |
| 79 | PubMed Central | Earliest details of dermatology by Ayurveda. | Research Paper | `free_full_text` | **FAILED** | *Missing Abstract. Historical note or short communication without abstract.* |
| 80 | PubMed Central | PMID 39736959 | Research Paper | `free_full_text` | **FAILED** | *Missing Title. Record has an abstract but lacks a title field in the database.* |
| 81 | PubMed Central | Role of pharmacology for integration of modern medicine and Ayurveda. | Research Paper | `free_full_text` | **FAILED** | *Missing Abstract. Brief conference or editorial note without abstract.* |
| 82 | PubMed Central | Indian childhood cirrhosis. | Research Paper | `free_full_text` | **FAILED** | *Missing Abstract. Very old (1981) index citation without abstract.* |
| 83 | National Medicinal Plants Board (NMPB) | Botanical Profile of Adathodai (Justicia adhatoda) | Botanical Profile | `public_domain` | **SUCCESS** | *N/A* |
| 84 | National Medicinal Plants Board (NMPB) | Botanical Profile of Ashwagandha (Withania somnifera) | Botanical Profile | `public_domain` | **SUCCESS** | *N/A* |
| 85 | National Medicinal Plants Board (NMPB) | Botanical Profile of Athimathuram (Glycyrrhiza glabra) | Botanical Profile | `public_domain` | **SUCCESS** | *N/A* |
| 86 | National Medicinal Plants Board (NMPB) | Botanical Profile of Brahmi / Neerbrahmi (Bacopa monnieri) | Botanical Profile | `public_domain` | **SUCCESS** | *N/A* |
| 87 | National Medicinal Plants Board (NMPB) | Botanical Profile of Elakkai (Elettaria cardamomum) | Botanical Profile | `public_domain` | **SUCCESS** | *N/A* |
| 88 | National Medicinal Plants Board (NMPB) | Botanical Profile of Inji / Sukku (Zingiber officinale) | Botanical Profile | `public_domain` | **SUCCESS** | *N/A* |
| 89 | National Medicinal Plants Board (NMPB) | Botanical Profile of Karisalankanni (Eclipta prostrata) | Botanical Profile | `public_domain` | **SUCCESS** | *N/A* |
| 90 | National Medicinal Plants Board (NMPB) | Botanical Profile of Karpuravalli (Coleus amboinicus) | Botanical Profile | `public_domain` | **SUCCESS** | *N/A* |
| 91 | National Medicinal Plants Board (NMPB) | Botanical Profile of Karunthulasi (Ocimum tenuiflorum) | Botanical Profile | `public_domain` | **SUCCESS** | *N/A* |
| 92 | National Medicinal Plants Board (NMPB) | Botanical Profile of Karuvapattai (Cinnamomum verum) | Botanical Profile | `public_domain` | **SUCCESS** | *N/A* |
| 93 | National Medicinal Plants Board (NMPB) | Botanical Profile of Keezhanelli (Phyllanthus niruri) | Botanical Profile | `public_domain` | **SUCCESS** | *N/A* |
| 94 | National Medicinal Plants Board (NMPB) | Botanical Profile of Kirambu / Lavangam (Syzygium aromaticum) | Botanical Profile | `public_domain` | **SUCCESS** | *N/A* |
| 95 | National Medicinal Plants Board (NMPB) | Botanical Profile of Kothamalli (Coriandrum sativum) | Botanical Profile | `public_domain` | **SUCCESS** | *N/A* |
| 96 | National Medicinal Plants Board (NMPB) | Botanical Profile of Kuppaimeni (Acalypha indica) | Botanical Profile | `public_domain` | **SUCCESS** | *N/A* |
| 97 | National Medicinal Plants Board (NMPB) | Botanical Profile of Manjal (Curcuma longa) | Botanical Profile | `public_domain` | **SUCCESS** | *N/A* |
| 98 | National Medicinal Plants Board (NMPB) | Botanical Profile of Milagu (Piper nigrum) | Botanical Profile | `public_domain` | **SUCCESS** | *N/A* |
| 99 | National Medicinal Plants Board (NMPB) | Botanical Profile of Mudakathan (Cardiospermum halicacabum) | Botanical Profile | `public_domain` | **SUCCESS** | *N/A* |
| 100 | National Medicinal Plants Board (NMPB) | Botanical Profile of Neem / Vembu (Azadirachta indica) | Botanical Profile | `public_domain` | **SUCCESS** | *N/A* |
| 101 | National Medicinal Plants Board (NMPB) | Botanical Profile of Nelli (Phyllanthus emblica) | Botanical Profile | `public_domain` | **SUCCESS** | *N/A* |
| 102 | National Medicinal Plants Board (NMPB) | Botanical Profile of Nilavembu (Andrographis paniculata) | Botanical Profile | `public_domain` | **SUCCESS** | *N/A* |
| 103 | National Medicinal Plants Board (NMPB) | Botanical Profile of Pirandai (Cissus quadrangularis) | Botanical Profile | `public_domain` | **SUCCESS** | *N/A* |
| 104 | National Medicinal Plants Board (NMPB) | Botanical Profile of Poondu (Allium sativum) | Botanical Profile | `public_domain` | **SUCCESS** | *N/A* |
| 105 | National Medicinal Plants Board (NMPB) | Botanical Profile of Seeragam (Cuminum cyminum) | Botanical Profile | `public_domain` | **SUCCESS** | *N/A* |
| 106 | National Medicinal Plants Board (NMPB) | Botanical Profile of Sirukurunjan (Gymnema sylvestre) | Botanical Profile | `public_domain` | **SUCCESS** | *N/A* |
| 107 | National Medicinal Plants Board (NMPB) | Botanical Profile of Sothu Katrazhai (Aloe barbadensis) | Botanical Profile | `public_domain` | **SUCCESS** | *N/A* |
| 108 | National Medicinal Plants Board (NMPB) | Botanical Profile of Thippili (Piper longum) | Botanical Profile | `public_domain` | **SUCCESS** | *N/A* |
| 109 | National Medicinal Plants Board (NMPB) | Botanical Profile of Thoothuvalai (Solanum trilobatum) | Botanical Profile | `public_domain` | **SUCCESS** | *N/A* |
| 110 | National Medicinal Plants Board (NMPB) | Botanical Profile of Tulsi (Ocimum sanctum) | Botanical Profile | `public_domain` | **SUCCESS** | *N/A* |
| 111 | National Medicinal Plants Board (NMPB) | Botanical Profile of Vallarai (Centella asiatica) | Botanical Profile | `public_domain` | **SUCCESS** | *N/A* |
| 112 | National Medicinal Plants Board (NMPB) | Botanical Profile of Vendhayam (Trigonella foenum-graecum) | Botanical Profile | `public_domain` | **SUCCESS** | *N/A* |
| 113 | Tamil Virtual Academy Digital Library | Biographical Profile of Siddhar Agasthiyar | Siddhar Biography | `public_domain` | **SUCCESS** | *N/A* |
| 114 | Tamil Virtual Academy Digital Library | Biographical Profile of Siddhar Thirumoolar | Siddhar Biography | `public_domain` | **SUCCESS** | *N/A* |
| 115 | Tamil Virtual Academy Digital Library | Biographical Profile of Siddhar Bogar | Siddhar Biography | `public_domain` | **SUCCESS** | *N/A* |
| 116 | Tamil Virtual Academy Digital Library | Biographical Profile of Siddhar Pambatti Siddhar | Siddhar Biography | `public_domain` | **SUCCESS** | *N/A* |
| 117 | Tamil Virtual Academy Digital Library | Biographical Profile of Siddhar Korakkar | Siddhar Biography | `public_domain` | **SUCCESS** | *N/A* |
| 118 | Tamil Virtual Academy Digital Library | Biographical Profile of Siddhar Sattaimuni | Siddhar Biography | `public_domain` | **SUCCESS** | *N/A* |
| 119 | Tamil Virtual Academy Digital Library | Biographical Profile of Siddhar Konkanar | Siddhar Biography | `public_domain` | **SUCCESS** | *N/A* |
| 120 | Tamil Virtual Academy Digital Library | Biographical Profile of Siddhar Ramadevar | Siddhar Biography | `public_domain` | **SUCCESS** | *N/A* |
| 121 | Tamil Virtual Academy Digital Library | Biographical Profile of Siddhar Machamuni | Siddhar Biography | `public_domain` | **SUCCESS** | *N/A* |
| 122 | Tamil Virtual Academy Digital Library | Biographical Profile of Siddhar Karuvoorar | Siddhar Biography | `public_domain` | **SUCCESS** | *N/A* |
| 123 | British Library EAP810 | Manuscript Catalog Record: Agasthiyar Nayana Vidhi (Ophthalmology) | Manuscript Metadata | `open_access` | **SUCCESS** | *N/A* |
| 124 | British Library EAP810 | Manuscript Catalog Record: Bogar Karpa Vidhi (Rejuvenation) | Manuscript Metadata | `open_access` | **SUCCESS** | *N/A* |
| 125 | French Institute of Pondicherry | Manuscript Catalog Record: Theriyar Kudineer (Decoctions) | Manuscript Metadata | `open_access` | **SUCCESS** | *N/A* |
| 126 | French Institute of Pondicherry | Manuscript Catalog Record: Agasthiyar Vaidya Parani (General Medicine) | Manuscript Metadata | `open_access` | **SUCCESS** | *N/A* |
| 127 | Government Oriental Manuscripts Library, Chennai | Manuscript Catalog Record: Varma Suthiram (Pressure Points) | Manuscript Metadata | `open_access` | **SUCCESS** | *N/A* |
| 128 | Government Oriental Manuscripts Library, Chennai | Manuscript Catalog Record: Theriyar Yamaga Venba | Manuscript Metadata | `open_access` | **SUCCESS** | *N/A* |
| 129 | Saraswathi Mahal Library, Thanjavur | Manuscript Catalog Record: Sarbendra Vaidya Muraigal | Manuscript Metadata | `open_access` | **SUCCESS** | *N/A* |
| 130 | Saraswathi Mahal Library, Thanjavur | Manuscript Catalog Record: Gunapadam Mooligai (Materia Medica) | Manuscript Metadata | `open_access` | **SUCCESS** | *N/A* |
| 131 | Dr. U. V. Swaminatha Iyer Library | Manuscript Catalog Record: Agasthiyar Soumya Sagaram | Manuscript Metadata | `open_access` | **SUCCESS** | *N/A* |
| 132 | Dr. U. V. Swaminatha Iyer Library | Manuscript Catalog Record: Yugi Chinthamani (Pathology) | Manuscript Metadata | `open_access` | **SUCCESS** | *N/A* |
| 133 | Tamil University Thanjavur EAP1217 | Manuscript Catalog Record: Varma Kannaadi | Manuscript Metadata | `open_access` | **SUCCESS** | *N/A* |
| 134 | Tamil University Thanjavur EAP1217 | Manuscript Catalog Record: Vaidya Chinthamani | Manuscript Metadata | `open_access` | **SUCCESS** | *N/A* |
| 135 | Institute of Asian Studies | Manuscript Catalog Record: Theriyar Karisal (Therapeutic Recipes) | Manuscript Metadata | `open_access` | **SUCCESS** | *N/A* |
| 136 | Institute of Asian Studies | Manuscript Catalog Record: Nandi Suthiram | Manuscript Metadata | `open_access` | **SUCCESS** | *N/A* |
| 137 | British Library EAP1260 | Manuscript Catalog Record: Pathartha Guna Chinthamani | Manuscript Metadata | `open_access` | **SUCCESS** | *N/A* |
| 138 | Tamil Virtual Academy Digital Library | Classical Text Metadata: Thirumandiram | Classical Text | `public_domain` | **SUCCESS** | *N/A* |
| 139 | Tamil Virtual Academy Digital Library | Classical Text Metadata: Bogar 7000 | Classical Text | `public_domain` | **SUCCESS** | *N/A* |
| 140 | Tamil Virtual Academy Digital Library | Classical Text Metadata: Agasthiyar Soumya Sagaram | Classical Text | `public_domain` | **SUCCESS** | *N/A* |
| 141 | Tamil Virtual Academy Digital Library | Classical Text Metadata: Theriyar Yamaga Venba | Classical Text | `public_domain` | **SUCCESS** | *N/A* |
| 142 | Tamil Virtual Academy Digital Library | Classical Text Metadata: Sivavakkiyar Padalgal | Classical Text | `public_domain` | **SUCCESS** | *N/A* |
| 143 | Tamil Virtual Academy Digital Library | Classical Text Metadata: Agasthiyar Vaidya Kaviyam | Classical Text | `public_domain` | **SUCCESS** | *N/A* |
| 144 | Tamil Virtual Academy Digital Library | Classical Text Metadata: Yugi Chinthamani 800 | Classical Text | `public_domain` | **SUCCESS** | *N/A* |
| 145 | Tamil Virtual Academy Digital Library | Classical Text Metadata: Pathartha Guna Chinthamani | Classical Text | `public_domain` | **SUCCESS** | *N/A* |
| 146 | Tamil Virtual Academy Digital Library | Classical Text Metadata: Theriyar Sekarappa | Classical Text | `public_domain` | **SUCCESS** | *N/A* |
| 147 | Tamil Virtual Academy Digital Library | Classical Text Metadata: Karuvoorar Pooja Vidhi | Classical Text | `public_domain` | **SUCCESS** | *N/A* |
| 148 | Pharmacopoeia Commission for Indian Medicine & Homoeopathy (PCIM&H) | Formulation Catalog Record: Nilavembu Kudineer | Formulation Recipe | `public_domain` | **SUCCESS** | *N/A* |
| 149 | Pharmacopoeia Commission for Indian Medicine & Homoeopathy (PCIM&H) | Formulation Catalog Record: Amukkara Choornam | Formulation Recipe | `public_domain` | **SUCCESS** | *N/A* |
| 150 | Pharmacopoeia Commission for Indian Medicine & Homoeopathy (PCIM&H) | Formulation Catalog Record: Kabasura Kudineer | Formulation Recipe | `public_domain` | **SUCCESS** | *N/A* |
| 151 | Pharmacopoeia Commission for Indian Medicine & Homoeopathy (PCIM&H) | Formulation Catalog Record: Triphala Choornam | Formulation Recipe | `public_domain` | **SUCCESS** | *N/A* |
| 152 | Pharmacopoeia Commission for Indian Medicine & Homoeopathy (PCIM&H) | Formulation Catalog Record: Agasthiyar Kuzhambu | Formulation Recipe | `public_domain` | **SUCCESS** | *N/A* |
| 153 | Pharmacopoeia Commission for Indian Medicine & Homoeopathy (PCIM&H) | Formulation Catalog Record: Pinda Thailam | Formulation Recipe | `public_domain` | **SUCCESS** | *N/A* |
| 154 | Pharmacopoeia Commission for Indian Medicine & Homoeopathy (PCIM&H) | Formulation Catalog Record: Kalyana Ghritham | Formulation Recipe | `public_domain` | **SUCCESS** | *N/A* |
| 155 | Pharmacopoeia Commission for Indian Medicine & Homoeopathy (PCIM&H) | Formulation Catalog Record: Parangipattai Chooranam | Formulation Recipe | `public_domain` | **SUCCESS** | *N/A* |
| 156 | Pharmacopoeia Commission for Indian Medicine & Homoeopathy (PCIM&H) | Formulation Catalog Record: Muthu Parpam | Formulation Recipe | `public_domain` | **SUCCESS** | *N/A* |
| 157 | Pharmacopoeia Commission for Indian Medicine & Homoeopathy (PCIM&H) | Formulation Catalog Record: Kandarasa Guligai | Formulation Recipe | `public_domain` | **SUCCESS** | *N/A* |
| 158 | Pharmacopoeia Commission for Indian Medicine & Homoeopathy (PCIM&H) | Formulation Catalog Record: Siddha Makaradhwaja | Formulation Recipe | `public_domain` | **SUCCESS** | *N/A* |
| 159 | Pharmacopoeia Commission for Indian Medicine & Homoeopathy (PCIM&H) | Formulation Catalog Record: Seenthil Chooranam | Formulation Recipe | `public_domain` | **SUCCESS** | *N/A* |
| 160 | Pharmacopoeia Commission for Indian Medicine & Homoeopathy (PCIM&H) | Formulation Catalog Record: Asta Choornam | Formulation Recipe | `public_domain` | **SUCCESS** | *N/A* |
| 161 | Pharmacopoeia Commission for Indian Medicine & Homoeopathy (PCIM&H) | Formulation Catalog Record: Chirattai Thailam | Formulation Recipe | `public_domain` | **SUCCESS** | *N/A* |
| 162 | Pharmacopoeia Commission for Indian Medicine & Homoeopathy (PCIM&H) | Formulation Catalog Record: Kumari Ney | Formulation Recipe | `public_domain` | **SUCCESS** | *N/A* |
