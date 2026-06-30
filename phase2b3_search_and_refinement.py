"""
Phase 2B-3: Search Infrastructure, Entity Refinement & Cross-References
=======================================================================
Objectives:
  1. Build search_index.json  (all 1,150 documents, search-ready fields)
  2. Entity Refinement        (confirmed / probable / candidate tiers, FP analysis)
  3. Entity Cross-References  (evidence-based co-occurrence relationships)
  4. Corpus Navigation Layer  (statistics for website nav design)

No embeddings, vectorization, LLM, or knowledge-graph operations.
All relationships derived exclusively from corpus evidence.

Run: python phase2b3_search_and_refinement.py
"""

import os, re, json, datetime
from collections import defaultdict

BASE_DIR    = r"d:\Siddha_Wisdom"
NORM_DIR    = os.path.join(BASE_DIR, "normalized_corpus")
ENT_DIR     = os.path.join(BASE_DIR, "entity_registry")
LOG_FILE    = os.path.join(BASE_DIR, "phase2b3_run.log")
RUN_TS      = datetime.datetime.now(datetime.timezone.utc).isoformat()

# ── Logger ────────────────────────────────────────────────────────────────────
def log(msg):
    safe = msg.encode("ascii", errors="replace").decode("ascii")
    stamp = datetime.datetime.now(datetime.timezone.utc).strftime("%H:%M:%S")
    print(f"[{stamp}] {safe}")
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{stamp}] {msg}\n")

# ══════════════════════════════════════════════════════════════════════════════
# HIGH-FALSE-POSITIVE ROOTS — roots that match too many unrelated Tamil words
# ══════════════════════════════════════════════════════════════════════════════
# Entities flagged here have their root_match confidence tier lowered to
# "candidate" with a false_positive_risk annotation.

HIGH_FP_RISK_ENTITIES = {
    # Root "திரு" is an honorific prefix used throughout Tamil for places,
    # names, texts (திருக்குறள், திருவாசகம், திருவண்ணாமலை, etc.)
    "siddhar_thirumoolar":   {"root": "திரு", "reason": "Honorific prefix ubiquitous in Tamil"},
    "place_tiruvannamalai":  {"root": "திரு", "reason": "Honorific prefix ubiquitous in Tamil"},

    # Root "சிவ" matches Shiva derivatives but also unrelated compound words
    # like சிவப்பு (red), சிவக்க (to redden)
    "siddhar_sivavakkiyar":  {"root": "சிவ", "reason": "Also root of color-term sivappu (red)"},
    "concept_shiva_shakti":  {"root": "சிவ", "reason": "Compound root; difficult to isolate from Shiva references"},

    # Root "கரு" appears in கருவூரார் but also in கருப்பு (black), கருத்து (opinion)
    "siddhar_karuvoorar":    {"root": "கரு", "reason": "Common root: karu = dark/seed/opinion"},

    # Root "கும்" appears in கும்பகம் but also in கும்மி, குமரன் etc.
    "practice_kumbhaka":     {"root": "கும்", "reason": "Root shared with unrelated words"},

    # Root "குத" appears in குதம்பை but also in குதிரை (horse) and குதிக்க (jump)
    "siddhar_kudambai":      {"root": "குத", "reason": "Root shared with kutirai (horse) etc."},

    # Root "வர்" appears in வர்மம் but also in வர (to come), வரி (tax/line)
    "practice_varma":        {"root": "வர்", "reason": "Common Tamil verb root: vara (to come)"},

    # Root "தவ" appears in தவம் but also in தவறு (mistake)
    "concept_tapas":         {"root": "தவ", "reason": "Root shared with thavaru (mistake)"},

    # Roots for various practices that use common syllables
    "practice_pranayama":    {"root": "பிரா", "reason": "Root pira- appears in many Tamil loanwords"},
    "concept_dhyana":        {"root": "தியா", "reason": "Root appears in limited contexts but less specific"},
    "place_potigai":         {"root": "பொதி", "reason": "Root appears in pothigai but also pothi (bundle)"},
    "symbol_eighteen":       {"root": "பதின", "reason": "Numeric root; matches many number constructs"},
    "practice_kayakalpa":    {"root": "காய", "reason": "Root kaaya appears in kaayam (matter/body) broadly"},
    "siddhar_pambatti":      {"root": "பாம்", "reason": "Root paam appears in paambu (snake) variants"},
    "siddhar_ramadevar":     {"root": "இரா", "reason": "Root iraa- is common prefix (night, Rama, etc.)"},
    "siddhar_yugi":          {"root": "யோகி", "reason": "Yogi is generic for any spiritual practitioner"},
    "concept_kundalini":     {"root": "குண்", "reason": "Root kund- matches quality (guna) derivatives"},
    "plant_vallarai":        {"root": "வல்", "reason": "Val- root appears in many strength-related words"},
    "plant_tulsi":           {"root": "துள", "reason": "Root tula- used in multiple contexts"},
    "plant_thippili":        {"root": "திப்", "reason": "Root is fairly specific but short"},
    "siddhar_theriyar":      {"root": "தேரை", "reason": "Root terai appears in toad (terai) and other words"},
    "siddhar_idaikkadar":    {"root": "இடை", "reason": "Root idai- is very common (middle, shepherd, etc.)"},
    "siddhar_korakkar":      {"root": "கோர", "reason": "Root kora appears in goraku and in frightful (kora)"},
    "practice_bandha":       {"root": "பந்த", "reason": "Root bandha appears in bond/family contexts too"},
    "practice_ashta_siddhi": {"root": "அட்ட", "reason": "Atta prefix common in Sanskrit loanwords broadly"},
    "symbol_five":           {"root": "ஐந்த", "reason": "Numeric root matches all five-related constructs"},
    "symbol_eight":          {"root": "எட்ட", "reason": "Numeric root matches eight-related constructs"},
}

# Low false-positive entities (specific roots / exact matches dominate)
LOW_FP_RISK_ENTITIES = {
    "practice_moolamantra",  # நமசிவாய is highly specific
    "concept_pranava",       # ஓம்/பிரணவம் quite specific
    "concept_mantra",        # மந்திரம் distinct
    "body_eye",              # கண் very common but intentional — high precision
    "body_light",            # சோதி/ஒளி — specific imagery terms
    "body_sound",            # நாதம் — specific term
    "body_seed",             # விந்து — specific esoteric term
    "body_heart",            # இதயம்/மனம் — common but intentional
    "concept_nadi",          # நாடி — quite specific in this context
    "siddhar_nandidevar",    # நந்தி — specific when exact match
    "concept_jnana",         # ஞானம் — specific philosophical term
    "concept_mukti",         # முக்தி — specific liberation term
    "concept_samadhi",       # சமாதி — specific
    "concept_atman",         # ஆத்மா — specific
    "concept_guru",          # குரு — contextually specific
    "deity_shiva",           # சிவம்/சிவன் — when exact match, high precision
    "deity_shakti",          # சக்தி — distinct
    "deity_brahma",          # பிரமன் — distinct
    "deity_murugan",         # முருகன் — distinct
    "deity_ganesha",         # விநாயகன் — distinct
    "deity_kali",            # காளி — distinct
    "deity_vishnu",          # திருமால் — distinct
    "place_chidambaram",     # தில்லை/சிதம்பரம் — distinct
    "place_kailash",         # கயிலை — distinct
    "place_madurai",         # மதுரை — distinct
    "place_kashi",           # காசி — distinct
    "place_himalaya",        # இமயம் — distinct
    "concept_yoga",          # யோகம் — specific
    "concept_tantra",        # தந்திரம் — specific
    "concept_karma",         # கர்மம்/வினை — specific
    "concept_maya",          # மாயை — specific
    "concept_bhakti",        # பக்தி — specific
    "concept_chakra",        # சக்கரம் — specific
    "concept_pancha_bootham",# பஞ்சபூதம் — specific
    "concept_agama",         # ஆகமம் — specific
    "practice_mudra",        # முத்திரை — specific
    "practice_deekshai",     # தீட்சை — specific
    "practice_japa",         # ஜபம் — specific
    "plant_lotus",           # தாமரை/கமலம் — distinct
    "plant_nelli",           # நெல்லி — distinct
    "plant_neem",            # வேம்பு — distinct
    "plant_ginger",          # இஞ்சி/சுக்கு — distinct
    "plant_manjal",          # மஞ்சள் — distinct
    "plant_milagu",          # மிளகு — distinct
    "plant_kadukkai",        # கடுக்காய் — distinct
    "plant_keezhanelli",     # கீழாநெல்லி — distinct
    "plant_ashwagandha",     # அஷ்வகந்தா — distinct loanword
    "siddhar_agasthiyar",    # அகத்தியர் — distinct
    "siddhar_bogar",         # போகர் — distinct
    "siddhar_machamuni",     # மச்சமுனி — distinct
    "siddhar_konkanar",      # கொங்கணர் — distinct
    "siddhar_sattaimuni",    # சட்டைமுனி — distinct
    "symbol_three",          # மும்மலம் — specific
    "body_udal",             # உடம்பு — common but specific
    "body_uyir",             # உயிர் — specific
    "body_moolam",           # மூலம் — specific
    "body_breath",           # சுவாசம்/மூச்சு — specific
    "body_head",             # தலை — common but intentional
    "body_fire",             # அக்னி/தீ — specific
    "concept_prana",         # பிராணன் — specific
    "concept_brahman",       # பரம்பொருள் — distinct
    "concept_shishya",       # சீடன் — specific
    "practice_rasayana",     # இரசாயனம் — specific
    "practice_kumbhaka",     # கும்பகம் — specific (overriding above risk)
}


def assign_confidence_tier(entity_id: str, match_type: str, confidence: float) -> dict:
    """
    Map raw confidence score + match type to a human-readable confidence tier.
    Apply false-positive risk annotation where applicable.
    """
    is_high_fp = entity_id in HIGH_FP_RISK_ENTITIES
    fp_info    = HIGH_FP_RISK_ENTITIES.get(entity_id, {})

    if confidence == 1.0:
        tier = "confirmed"
        fp_risk = "low"
    elif confidence == 0.85:
        tier = "probable"
        fp_risk = "low"
    else:  # 0.60 root_match
        if is_high_fp:
            tier    = "candidate"
            fp_risk = "high"
        else:
            tier    = "candidate"
            fp_risk = "medium"

    return {
        "tier":          tier,
        "fp_risk":       fp_risk,
        "fp_reason":     fp_info.get("reason", ""),
        "original_conf": confidence,
        "match_type":    match_type,
    }


# ══════════════════════════════════════════════════════════════════════════════
# STEP 1 — LOAD ALL NORMALIZED DOCUMENTS
# ══════════════════════════════════════════════════════════════════════════════

def load_corpus():
    docs = []
    for fname in sorted(os.listdir(NORM_DIR)):
        if not fname.endswith(".json"):
            continue
        with open(os.path.join(NORM_DIR, fname), encoding="utf-8") as f:
            try:
                docs.append(json.load(f))
            except Exception as e:
                log(f"  WARN: {fname}: {e}")
    return docs


# ══════════════════════════════════════════════════════════════════════════════
# STEP 2 — BUILD SEARCH INDEX
# ══════════════════════════════════════════════════════════════════════════════

def extract_keywords(doc: dict) -> list:
    """Build keyword list from document metadata and entity names."""
    kw = set()

    # Author / work / collection
    for field in ["author", "source_work", "collection", "language",
                  "copyright_status", "source_repository"]:
        val = doc.get(field)
        if val and isinstance(val, str):
            kw.add(val.strip())

    # Category tag from document type
    doc_id = doc.get("document_id") or ""
    if doc_id.startswith("text_thirumandiram"):
        kw.update(["Thirumandiram", "Tamil verse", "Shaiva Siddhanta", "yoga", "tantra"])
    elif doc_id.startswith("text_sivavakkiyar"):
        kw.update(["Sivavakkiyam", "Tamil verse", "Siddhar poetry", "iconoclasm"])
    elif doc_id.startswith("siddhar_"):
        kw.update(["Siddhar", "biography", "Tamil sage"])
    elif doc_id.startswith("formulation_"):
        kw.update(["Siddha medicine", "formulation", "herbal remedy"])
    elif doc_id.startswith("plant_"):
        kw.update(["medicinal plant", "materia medica", "Siddha herb"])
    elif doc_id.startswith("manuscript_"):
        kw.update(["manuscript", "palm leaf", "Tamil script"])
    elif doc_id.startswith("classic_"):
        kw.update(["classical text", "Siddha literature"])
    elif doc_id.startswith("pubmed_"):
        kw.update(["research", "scientific", "clinical"])

    # Entity names (English) for keyword search
    for eid in doc.get("entity_ids", []):
        # convert entity_id to readable keyword
        kw.add(eid.replace("_", " ").replace("siddhar ", "").replace(
               "deity ", "").replace("concept ", "").replace(
               "practice ", "").replace("plant ", "").replace(
               "place ", "").replace("body ", "").replace("symbol ", "").strip())

    return sorted(kw)


def build_search_text(doc: dict) -> str:
    """Combine all searchable text into a single string."""
    parts = []
    for field in ["title", "source_work", "collection", "author", "verse_number"]:
        v = doc.get(field)
        if v:
            parts.append(str(v))
    if doc.get("tamil_text"):
        parts.append(doc["tamil_text"])
    if doc.get("transliteration"):
        parts.append(doc["transliteration"])
    if doc.get("abstract"):
        parts.append(doc["abstract"])
    if doc.get("description"):
        parts.append(doc["description"])
    return " ".join(parts)


def build_search_index(docs: list) -> list:
    """Build search index records for all documents."""
    index = []
    for doc in docs:
        record = {
            "document_id":   doc.get("document_id"),
            "title":         doc.get("title"),
            "source_work":   doc.get("source_work"),
            "author":        doc.get("author"),
            "collection":    doc.get("collection"),
            "verse_number":  doc.get("verse_number"),
            "language":      doc.get("language"),
            "doc_type":      _doc_type(doc.get("document_id", "")),
            "entity_ids":    doc.get("entity_ids", []),
            "keywords":      extract_keywords(doc),
            "search_text":   build_search_text(doc),
            "source_url":    doc.get("source_url"),
            "copyright_status": doc.get("copyright_status"),
        }
        index.append(record)
    return index


def _doc_type(doc_id) -> str:
    if not doc_id:
        return "other"
    if doc_id.startswith("text_"):       return "verse"
    if doc_id.startswith("siddhar_"):    return "biography"
    if doc_id.startswith("formulation_"):return "formulation"
    if doc_id.startswith("plant_"):      return "plant"
    if doc_id.startswith("manuscript_"): return "manuscript"
    if doc_id.startswith("classic_"):    return "classical_text"
    if doc_id.startswith("pubmed_"):     return "research"
    return "other"


# ══════════════════════════════════════════════════════════════════════════════
# STEP 3 — ENTITY REFINEMENT (confidence tier assignment)
# ══════════════════════════════════════════════════════════════════════════════

def load_entity_registry() -> dict:
    """Load all entity registry files, keyed by entity_id."""
    all_entities = {}
    for fname in os.listdir(ENT_DIR):
        if fname == "entity_index.json" or not fname.endswith(".json"):
            continue
        with open(os.path.join(ENT_DIR, fname), encoding="utf-8") as f:
            data = json.load(f)
            for ent in data.get("entities", []):
                all_entities[ent["entity_id"]] = ent
    return all_entities


def build_refined_entity_map(entity_map: dict) -> dict:
    """
    Add confidence tier (confirmed/probable/candidate) to every entity
    and compute tier breakdown from source_documents.
    """
    refined = {}
    for eid, ent in entity_map.items():
        tier_counts = {"confirmed": 0, "probable": 0, "candidate": 0}
        refined_docs = []

        for src in ent.get("source_documents", []):
            conf = src.get("confidence", 0.60)
            mt   = src.get("match_type", "root_match")
            tier_info = assign_confidence_tier(eid, mt, conf)
            refined_docs.append({**src, **tier_info})
            tier_counts[tier_info["tier"]] += 1

        fp_risk = "low"
        if eid in HIGH_FP_RISK_ENTITIES:
            fp_risk = "high"

        dominant_tier = max(tier_counts, key=lambda k: tier_counts[k])

        refined[eid] = {
            **ent,
            "dominant_tier":    dominant_tier,
            "false_positive_risk": fp_risk,
            "fp_annotation":    HIGH_FP_RISK_ENTITIES.get(eid, {}).get("reason", ""),
            "tier_breakdown": tier_counts,
            "source_documents_total_stored": len(refined_docs),
            "refined_source_documents": refined_docs[:50],
        }
    return refined


# ══════════════════════════════════════════════════════════════════════════════
# STEP 4 — ENTITY CROSS-REFERENCES (evidence-based co-occurrence)
# ══════════════════════════════════════════════════════════════════════════════

def build_cross_references(docs: list, entity_map: dict) -> dict:
    """
    For each entity, compute:
      - related_verses:    list of doc_ids where entity appears
      - co_occurring_entities: entities that appear in the same docs
        (sorted by co-occurrence frequency)
      - work_distribution: {Thirumandiram: N, Sivavakkiyam: N, ...}

    All relationships derived from corpus co-occurrence only.
    """
    # Build doc → entity_ids map
    doc_entities: dict[str, set] = {}
    for doc in docs:
        doc_id  = doc.get("document_id", "")
        ent_ids = set(doc.get("entity_ids", []))
        if ent_ids:
            doc_entities[doc_id] = ent_ids

    # Build entity → doc_ids map
    ent_docs: dict[str, set] = defaultdict(set)
    for doc_id, ent_ids in doc_entities.items():
        for eid in ent_ids:
            ent_docs[eid].add(doc_id)

    # For each entity, find co-occurring entities
    cross_refs = {}
    for eid in entity_map:
        my_docs = ent_docs.get(eid, set())
        if not my_docs:
            continue

        # Co-occurrence count
        co_count: dict[str, int] = defaultdict(int)
        work_dist: dict[str, int] = defaultdict(int)

        for doc_id in my_docs:
            # Work distribution
            if "thirumandiram" in doc_id:
                work_dist["Thirumandiram"] += 1
            elif "sivavakkiyar" in doc_id:
                work_dist["Sivavakkiyam"] += 1
            else:
                work_dist["other"] += 1

            # Co-occurring entities
            for other_eid in doc_entities.get(doc_id, set()):
                if other_eid != eid:
                    co_count[other_eid] += 1

        # Top co-occurring entities (by frequency)
        top_co = sorted(co_count.items(), key=lambda x: -x[1])[:20]

        cross_refs[eid] = {
            "entity_id":     eid,
            "entity_name":   entity_map[eid].get("entity_name", eid),
            "entity_category": entity_map[eid].get("entity_category", ""),
            "occurrence_count": len(my_docs),
            "verse_ids":     sorted(my_docs)[:100],     # cap at 100 for size
            "verse_ids_total": len(my_docs),
            "work_distribution": dict(work_dist),
            "co_occurring_entities": [
                {
                    "entity_id":      co_eid,
                    "entity_name":    entity_map.get(co_eid, {}).get("entity_name", co_eid),
                    "entity_category": entity_map.get(co_eid, {}).get("entity_category", ""),
                    "co_occurrence_count": cnt,
                    "evidence": "corpus_co_occurrence",
                }
                for co_eid, cnt in top_co
            ],
        }

    return cross_refs


# ══════════════════════════════════════════════════════════════════════════════
# STEP 5 — COMPUTE NAVIGATION STATISTICS
# ══════════════════════════════════════════════════════════════════════════════

def compute_nav_stats(docs: list, entity_map: dict, cross_refs: dict) -> dict:
    """Compute statistics for corpus navigation layer."""
    doc_type_counts: dict = defaultdict(int)
    work_counts:     dict = defaultdict(int)
    lang_counts:     dict = defaultdict(int)

    for doc in docs:
        doc_type_counts[_doc_type(doc.get("document_id", ""))] += 1
        sw = doc.get("source_work") or _doc_type(doc.get("document_id", ""))
        work_counts[sw] += 1
        lang_counts[doc.get("language", "Unknown")] += 1

    # Top entities per category
    by_cat: dict = defaultdict(list)
    for eid, ent in entity_map.items():
        by_cat[ent.get("entity_category", "other")].append({
            "entity_id":      eid,
            "entity_name":    ent.get("entity_name", eid),
            "occurrence_count": ent.get("occurrence_count", 0),
            "avg_confidence": ent.get("avg_confidence", 0),
        })
    for cat in by_cat:
        by_cat[cat].sort(key=lambda x: -x["occurrence_count"])

    return {
        "total_documents":    len(docs),
        "document_types":     dict(doc_type_counts),
        "work_distribution":  dict(work_counts),
        "language_distribution": dict(lang_counts),
        "top_entities_by_category": {k: v[:10] for k, v in by_cat.items()},
        "total_unique_entities": len(entity_map),
        "entity_categories":  list(by_cat.keys()),
    }


# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════

def main():
    open(LOG_FILE, "w", encoding="utf-8").close()
    log("=" * 60)
    log("Phase 2B-3: Search Infrastructure & Entity Refinement")
    log("=" * 60)

    # Step 1: Load corpus
    log("\nStep 1: Loading normalized corpus...")
    docs = load_corpus()
    log(f"  Loaded {len(docs)} documents")

    # Step 2: Build search index
    log("\nStep 2: Building search index...")
    search_index = build_search_index(docs)
    out_path = os.path.join(BASE_DIR, "search_index.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump({
            "index_version":  "2B-3",
            "generated_at":   RUN_TS,
            "total_documents": len(search_index),
            "searchable_fields": ["search_text", "keywords", "title",
                                  "source_work", "author", "entity_ids"],
            "records":        search_index,
        }, f, ensure_ascii=False, indent=2)
    log(f"  search_index.json written ({len(search_index)} records)")

    # Step 3: Load entity registry
    log("\nStep 3: Loading entity registry for refinement...")
    entity_map = load_entity_registry()
    log(f"  Loaded {len(entity_map)} entities")

    # Step 4: Entity refinement
    log("\nStep 4: Applying confidence tier refinement...")
    refined_map = build_refined_entity_map(entity_map)

    # Compute refinement statistics
    tier_counts = {"confirmed": 0, "probable": 0, "candidate": 0}
    fp_counts   = {"high": 0, "medium": 0, "low": 0}
    for eid, ent in refined_map.items():
        tier_counts[ent["dominant_tier"]] += 1
        fp_counts[ent["false_positive_risk"]] += 1

    log(f"  Confirmed: {tier_counts['confirmed']} | Probable: {tier_counts['probable']} | Candidate: {tier_counts['candidate']}")
    log(f"  FP Risk — High: {fp_counts['high']} | Medium: {fp_counts['medium']} | Low: {fp_counts['low']}")

    # Save refined entity index
    refined_index = []
    for eid, ent in refined_map.items():
        refined_index.append({
            "entity_id":            eid,
            "entity_category":      ent.get("entity_category"),
            "entity_name":          ent.get("entity_name"),
            "description":          ent.get("description"),
            "occurrence_count":     ent.get("occurrence_count"),
            "dominant_tier":        ent["dominant_tier"],
            "false_positive_risk":  ent["false_positive_risk"],
            "fp_annotation":        ent["fp_annotation"],
            "tier_breakdown":       ent["tier_breakdown"],
            "max_confidence":       ent.get("max_confidence"),
            "avg_confidence":       ent.get("avg_confidence"),
        })
    refined_index.sort(key=lambda x: -x["occurrence_count"])

    refined_path = os.path.join(ENT_DIR, "entity_index_refined.json")
    with open(refined_path, "w", encoding="utf-8") as f:
        json.dump({
            "version":       "2B-3",
            "generated_at":  RUN_TS,
            "total_entities": len(refined_index),
            "tier_summary":  tier_counts,
            "fp_risk_summary": fp_counts,
            "entities":      refined_index,
        }, f, ensure_ascii=False, indent=2)
    log(f"  entity_index_refined.json written")

    # Step 5: Cross-references
    log("\nStep 5: Building entity cross-references...")
    cross_refs = build_cross_references(docs, refined_map)
    xref_path  = os.path.join(BASE_DIR, "entity_cross_reference.json")
    with open(xref_path, "w", encoding="utf-8") as f:
        json.dump({
            "version":      "2B-3",
            "generated_at": RUN_TS,
            "methodology":  "corpus_co_occurrence",
            "note":         "All relationships derived from actual corpus evidence only. No AI-inferred links.",
            "total_entities": len(cross_refs),
            "cross_references": cross_refs,
        }, f, ensure_ascii=False, indent=2)
    log(f"  entity_cross_reference.json written ({len(cross_refs)} entities)")

    # Step 6: Navigation statistics
    log("\nStep 6: Computing corpus navigation statistics...")
    nav_stats = compute_nav_stats(docs, refined_map, cross_refs)

    stats_path = os.path.join(BASE_DIR, "phase2b3_stats.json")
    with open(stats_path, "w", encoding="utf-8") as f:
        json.dump({
            "run_ts":       RUN_TS,
            "navigation":   nav_stats,
            "refinement":   {"tier_counts": tier_counts, "fp_counts": fp_counts},
            "search_index": {"total_records": len(search_index)},
        }, f, ensure_ascii=False, indent=2)

    log("\n" + "=" * 60)
    log("Phase 2B-3 pipeline complete.")
    log(f"  Search index:          {len(search_index)} records")
    log(f"  Refined entities:      {len(refined_index)}")
    log(f"  Cross-references:      {len(cross_refs)} entities")
    log("=" * 60)

    return nav_stats, tier_counts, fp_counts, search_index


if __name__ == "__main__":
    main()
