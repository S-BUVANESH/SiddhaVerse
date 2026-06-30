"""
Phase 2B-3.5: Search Index Integrity Audit, Metadata Validation & Search Quality Testing
=========================================================================================
Objectives:
  1. Audit and repair search_index.json  (null fields, invalid doc_type, empty search_text)
  2. Validate every normalized_corpus document against production schema
  3. Run automated search quality tests across 9 query categories

Outputs:
  - search_index.json (repaired in-place)
  - phase2b35_audit_results.json (raw data for reports)

Run:  python phase2b35_audit.py
"""

import os, re, json, datetime
from collections import defaultdict

BASE_DIR   = r"d:\Siddha_Wisdom"
NORM_DIR   = os.path.join(BASE_DIR, "normalized_corpus")
IDX_PATH   = os.path.join(BASE_DIR, "search_index.json")
LOG_FILE   = os.path.join(BASE_DIR, "phase2b35_run.log")
RUN_TS     = datetime.datetime.now(datetime.timezone.utc).isoformat()

VALID_DOC_TYPES = {"verse", "biography", "formulation", "plant",
                   "manuscript", "classical_text", "research", "other"}

def log(msg):
    safe = msg.encode("ascii", errors="replace").decode("ascii")
    ts   = datetime.datetime.now(datetime.timezone.utc).strftime("%H:%M:%S")
    print(f"[{ts}] {safe}")
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{ts}] {msg}\n")

def _doc_type_from_id(doc_id):
    if not doc_id:
        return "other"
    doc_id = str(doc_id)
    if doc_id.startswith("text_"):         return "verse"
    if doc_id.startswith("siddhar_"):      return "biography"
    if doc_id.startswith("formulation_"):  return "formulation"
    if doc_id.startswith("plant_"):        return "plant"
    if doc_id.startswith("manuscript_"):   return "manuscript"
    if doc_id.startswith("classic_"):      return "classical_text"
    if doc_id.startswith("pubmed_"):       return "research"
    return "other"

# ══════════════════════════════════════════════════════════════════════════════
# OBJECTIVE 1 — SEARCH INDEX INTEGRITY AUDIT
# ══════════════════════════════════════════════════════════════════════════════

REQUIRED_FIELDS = ["document_id", "title", "author", "source_work",
                   "collection", "source_url", "search_text", "doc_type"]
# source_url is exempt for certain non-verse doc types
SOURCE_URL_EXEMPT_TYPES = {"biography", "research", "manuscript",
                           "classical_text", "formulation", "plant"}

def audit_and_repair_index(index_data: list) -> dict:
    """
    Audit each record. Repair what can be inferred. Return audit statistics.
    """
    stats = {
        "total":          len(index_data),
        "repaired":       0,
        "warnings":       [],
        "null_field_counts": defaultdict(int),
        "invalid_doc_type": 0,
        "empty_search_text": 0,
        "duplicate_ids":  [],
        "repairs_detail": [],
    }

    seen_ids = {}
    for i, rec in enumerate(index_data):
        repairs = []
        doc_id  = rec.get("document_id") or ""

        # --- Duplicate ID check ---
        if doc_id:
            if doc_id in seen_ids:
                stats["duplicate_ids"].append({"doc_id": doc_id, "indices": [seen_ids[doc_id], i]})
            else:
                seen_ids[doc_id] = i

        # --- doc_type: repair if invalid or missing ---
        dt = rec.get("doc_type")
        if not dt or dt not in VALID_DOC_TYPES:
            inferred = _doc_type_from_id(doc_id)
            if inferred != dt:
                repairs.append(f"doc_type: '{dt}' -> '{inferred}'")
                rec["doc_type"] = inferred
            stats["invalid_doc_type"] += 1 if (not dt or dt not in VALID_DOC_TYPES) else 0

        doc_type = rec.get("doc_type", "other")

        # --- null / missing field checks ---
        for field in REQUIRED_FIELDS:
            val = rec.get(field)
            if field == "source_url" and doc_type in SOURCE_URL_EXEMPT_TYPES:
                continue  # exempt
            if val is None or val == "" or val == []:
                stats["null_field_counts"][field] += 1
                # Attempt repairs
                if field == "title" and doc_id:
                    rec["title"] = doc_id.replace("_", " ").title()
                    repairs.append(f"title: synthesized from doc_id")
                elif field == "author" and doc_type == "verse":
                    if "thirumandiram" in doc_id:
                        rec["author"] = "Thirumoolar"
                        repairs.append("author: set to Thirumoolar (verse)")
                    elif "sivavakkiyar" in doc_id:
                        rec["author"] = "Sivavakkiyar"
                        repairs.append("author: set to Sivavakkiyar (verse)")
                elif field == "source_work" and doc_type == "verse":
                    if "thirumandiram" in doc_id:
                        rec["source_work"] = "Thirumandiram"
                        repairs.append("source_work: set to Thirumandiram")
                    elif "sivavakkiyar" in doc_id:
                        rec["source_work"] = "Sivavakkiyam"
                        repairs.append("source_work: set to Sivavakkiyam")
                elif field == "collection":
                    if doc_type in {"biography", "research", "plant", "formulation"}:
                        rec["collection"] = doc_type.capitalize()
                        repairs.append(f"collection: set to '{rec['collection']}'")
                elif field == "search_text":
                    # Build minimal search_text from available fields
                    parts = [str(rec.get(f, "")) for f in ["title", "source_work", "author"]
                             if rec.get(f)]
                    rec["search_text"] = " ".join(parts)
                    repairs.append("search_text: synthesized from title/work/author")

        # --- empty search_text check (after repair attempt) ---
        st = rec.get("search_text", "")
        if not st or len(st.strip()) < 5:
            stats["empty_search_text"] += 1

        if repairs:
            stats["repaired"] += 1
            stats["repairs_detail"].append({"doc_id": doc_id, "repairs": repairs})

    stats["null_field_counts"] = dict(stats["null_field_counts"])
    return stats


# ══════════════════════════════════════════════════════════════════════════════
# OBJECTIVE 2 — METADATA VALIDATION
# ══════════════════════════════════════════════════════════════════════════════

SCHEMA = {
    "verse": {
        "required": ["document_id", "title", "author", "language", "source_work",
                     "collection", "verse_number", "tamil_text", "transliteration",
                     "content_hash", "copyright_status", "source_repository",
                     "source_url", "acquisition_timestamp", "provenance_metadata"],
        "optional": ["english_translation", "entity_ids", "normalization"],
    },
    "biography": {
        "required": ["document_id", "title", "language", "copyright_status"],
        "optional": ["author", "source_work", "entity_ids"],
    },
    "plant": {
        "required": ["document_id", "title", "language", "copyright_status"],
        "optional": ["author", "source_work", "entity_ids"],
    },
    "formulation": {
        "required": ["document_id", "title", "language", "copyright_status"],
        "optional": [],
    },
    "manuscript": {
        "required": ["document_id", "title", "language", "copyright_status"],
        "optional": [],
    },
    "classical_text": {
        "required": ["document_id", "title", "language", "copyright_status"],
        "optional": [],
    },
    "research": {
        "required": ["document_id", "title", "language"],
        "optional": ["author"],
    },
    "other": {
        "required": ["document_id"],
        "optional": [],
    }
}

def validate_documents(docs: list) -> dict:
    """Validate all normalized corpus documents against production schema."""
    results = {
        "total":         len(docs),
        "fully_valid":   0,
        "warnings":      0,
        "errors":        0,
        "field_issues":  defaultdict(list),  # field -> list of doc_ids with issue
        "doc_type_breakdown": defaultdict(lambda: {"total": 0, "valid": 0, "warnings": 0}),
        "compliance_per_doc": [],
    }

    for doc in docs:
        doc_id   = doc.get("document_id", "UNKNOWN")
        doc_type = _doc_type_from_id(doc_id)
        schema   = SCHEMA.get(doc_type, SCHEMA["other"])
        required = schema["required"]

        missing  = [f for f in required if not doc.get(f)]
        is_valid = len(missing) == 0

        results["doc_type_breakdown"][doc_type]["total"]   += 1
        if is_valid:
            results["fully_valid"] += 1
            results["doc_type_breakdown"][doc_type]["valid"] += 1
        else:
            results["warnings"] += 1
            results["doc_type_breakdown"][doc_type]["warnings"] += 1
            for f in missing:
                results["field_issues"][f].append(doc_id)

        results["compliance_per_doc"].append({
            "doc_id":  doc_id,
            "type":    doc_type,
            "valid":   is_valid,
            "missing": missing,
        })

    results["field_issues"]          = dict(results["field_issues"])
    results["doc_type_breakdown"]    = dict(results["doc_type_breakdown"])
    results["compliance_percentage"] = round(results["fully_valid"] / max(results["total"], 1) * 100, 2)
    return results


# ══════════════════════════════════════════════════════════════════════════════
# OBJECTIVE 3 — SEARCH QUALITY TESTING
# ══════════════════════════════════════════════════════════════════════════════

def simple_search(records: list, query: str) -> list:
    """Simple token-based search matching query tokens against searchable fields."""
    tokens = query.lower().split()
    results = []
    for rec in records:
        # Searchable fields
        haystack = " ".join(filter(None, [
            str(rec.get("search_text", "") or ""),
            " ".join(rec.get("keywords", []) or []),
            str(rec.get("title", "") or ""),
            str(rec.get("author", "") or ""),
            str(rec.get("source_work", "") or ""),
            " ".join(rec.get("entity_ids", []) or []),
        ])).lower()
        if all(t in haystack for t in tokens):
            results.append(rec)
    return results


# Test suite: (query, category, relevant_entity_id, min_expected_results)
TEST_SUITE = [
    # Siddhar names
    ("Thirumoolar",   "siddhars",  "siddhar_thirumoolar",  10),
    ("Sivavakkiyar",  "siddhars",  "siddhar_sivavakkiyar", 10),
    ("Agasthiyar",    "siddhars",  "siddhar_agasthiyar",    1),
    ("Bogar",         "siddhars",  "siddhar_bogar",          1),
    ("Nandidevar",    "siddhars",  "siddhar_nandidevar",     5),

    # Plants
    ("Tulsi",         "plants",    "plant_tulsi",            1),
    ("Vallarai",      "plants",    "plant_vallarai",         1),
    ("Lotus",         "plants",    "plant_lotus",            1),
    ("Thippili",      "plants",    "plant_thippili",         1),
    ("Nelli",         "plants",    "plant_nelli",            1),

    # Deities
    ("Shiva",         "deities",   "deity_shiva",           10),
    ("Shakti",        "deities",   "deity_shakti",           5),
    ("Murugan",       "deities",   "deity_murugan",          5),
    ("Vishnu",        "deities",   "deity_vishnu",           5),
    ("Ganesha",       "deities",   "deity_ganesha",          1),

    # Concepts
    ("Yoga",          "concepts",  "concept_yoga",            5),
    ("Maya",          "concepts",  "concept_maya",            5),
    ("Pranava",       "concepts",  "concept_pranava",         5),
    ("Kundalini",     "concepts",  "concept_kundalini",       1),
    ("Jnana",         "concepts",  "concept_jnana",           5),

    # Practices
    ("Pranayama",     "practices", "practice_pranayama",     10),
    ("Mudra",         "practices", "practice_mudra",          5),
    ("Kumbhaka",      "practices", "practice_kumbhaka",       5),
    ("Kayakalpa",     "practices", "practice_kayakalpa",      1),

    # Places
    ("Chidambaram",   "places",    "place_chidambaram",       5),
    ("Kailash",       "places",    "place_kailash",           1),
    ("Madurai",       "places",    "place_madurai",           1),
    ("Kashi",         "places",    "place_kashi",             1),

    # Tamil text searches
    ("Thirumandiram", "tamil_text", None,                    100),
    ("Sivavakkiyam",  "tamil_text", None,                    100),

    # Romanized text
    ("pranayamam",    "romanized",  None,                      1),
    ("siva",          "romanized",  None,                      5),

    # English keywords
    ("meditation",    "english",    None,                      1),
    ("liberation",    "english",    None,                      1),
    ("breath",        "english",    None,                      1),
    ("public domain", "english",    None,                     10),
]


def run_search_tests(records: list) -> dict:
    """Run all test suite queries, compute precision and recall."""
    # Pre-build entity -> relevant doc_ids map
    entity_docs: dict = defaultdict(set)
    for rec in records:
        for eid in rec.get("entity_ids", []):
            entity_docs[eid].add(rec["document_id"])

    test_results = []
    category_stats: dict = defaultdict(lambda: {"queries": 0, "passed": 0,
                                                  "total_precision": 0.0,
                                                  "total_recall": 0.0})
    for query, category, entity_id, min_expected in TEST_SUITE:
        retrieved = simple_search(records, query)
        retrieved_ids = {r["document_id"] for r in retrieved}
        retrieved_count = len(retrieved)

        # Relevant = docs that have the entity_id in entity_ids
        relevant_ids = entity_docs.get(entity_id, set()) if entity_id else set()
        relevant_count = len(relevant_ids)

        if entity_id and relevant_count > 0:
            true_positives = len(retrieved_ids & relevant_ids)
            precision = true_positives / max(retrieved_count, 1)
            recall    = true_positives / max(relevant_count, 1)
        else:
            # For open queries (Tamil text, romanized, English), just check count
            precision = 1.0 if retrieved_count >= min_expected else retrieved_count / max(min_expected, 1)
            recall    = 1.0 if retrieved_count >= min_expected else 0.0
            true_positives = retrieved_count

        passed = retrieved_count >= min_expected

        cat_stat = category_stats[category]
        cat_stat["queries"] += 1
        cat_stat["passed"]  += 1 if passed else 0
        cat_stat["total_precision"] += precision
        cat_stat["total_recall"]    += recall

        test_results.append({
            "query":         query,
            "category":      category,
            "entity_id":     entity_id,
            "min_expected":  min_expected,
            "retrieved":     retrieved_count,
            "relevant":      relevant_count if entity_id else "n/a",
            "true_positives": true_positives,
            "precision":     round(precision, 3),
            "recall":        round(recall, 3),
            "passed":        passed,
            "sample_docs":   [r["document_id"] for r in retrieved[:3]],
        })

    # Compute per-category averages
    category_summary = {}
    for cat, s in category_stats.items():
        n = s["queries"]
        category_summary[cat] = {
            "total_queries":  n,
            "passed":         s["passed"],
            "pass_rate":      round(s["passed"] / max(n, 1) * 100, 1),
            "avg_precision":  round(s["total_precision"] / max(n, 1), 3),
            "avg_recall":     round(s["total_recall"] / max(n, 1), 3),
        }

    total_q  = len(test_results)
    total_ok = sum(1 for t in test_results if t["passed"])
    avg_prec = sum(t["precision"] for t in test_results) / max(total_q, 1)
    avg_rec  = sum(t["recall"]    for t in test_results) / max(total_q, 1)

    return {
        "total_queries":    total_q,
        "passed":           total_ok,
        "overall_pass_rate": round(total_ok / max(total_q, 1) * 100, 1),
        "avg_precision":    round(avg_prec, 3),
        "avg_recall":       round(avg_rec, 3),
        "category_summary": category_summary,
        "test_results":     test_results,
    }


# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════

def main():
    open(LOG_FILE, "w", encoding="utf-8").close()
    log("=" * 60)
    log("Phase 2B-3.5: Index Integrity, Metadata Validation & Search QA")
    log("=" * 60)

    # ── Load search index ─────────────────────────────────────────────────────
    log("\nStep 1: Loading search_index.json...")
    with open(IDX_PATH, encoding="utf-8") as f:
        idx_wrapper = json.load(f)
    records = idx_wrapper.get("records", [])
    log(f"  Loaded {len(records)} records")

    # ── Audit and repair ──────────────────────────────────────────────────────
    log("\nStep 2: Auditing and repairing search index...")
    audit_stats = audit_and_repair_index(records)
    log(f"  Repaired: {audit_stats['repaired']} records")
    log(f"  Invalid doc_type: {audit_stats['invalid_doc_type']}")
    log(f"  Empty search_text (remaining): {audit_stats['empty_search_text']}")
    log(f"  Duplicate IDs: {len(audit_stats['duplicate_ids'])}")

    # Save repaired index
    idx_wrapper["records"] = records
    idx_wrapper["repaired_at"] = RUN_TS
    with open(IDX_PATH, "w", encoding="utf-8") as f:
        json.dump(idx_wrapper, f, ensure_ascii=False, indent=2)
    log("  search_index.json saved (repaired)")

    # ── Metadata validation ───────────────────────────────────────────────────
    log("\nStep 3: Validating normalized corpus documents...")
    docs = []
    for fname in sorted(os.listdir(NORM_DIR)):
        if not fname.endswith(".json"):
            continue
        with open(os.path.join(NORM_DIR, fname), encoding="utf-8") as f:
            try:
                docs.append(json.load(f))
            except Exception as e:
                log(f"  WARN: {fname}: {e}")

    val_results = validate_documents(docs)
    log(f"  Total docs: {val_results['total']}")
    log(f"  Fully valid: {val_results['fully_valid']} ({val_results['compliance_percentage']}%)")
    log(f"  With warnings: {val_results['warnings']}")

    # ── Search quality tests ──────────────────────────────────────────────────
    log("\nStep 4: Running search quality tests...")
    sq_results = run_search_tests(records)
    log(f"  Total queries: {sq_results['total_queries']}")
    log(f"  Passed: {sq_results['passed']} ({sq_results['overall_pass_rate']}%)")
    log(f"  Avg precision: {sq_results['avg_precision']}")
    log(f"  Avg recall: {sq_results['avg_recall']}")

    # ── Save all results ──────────────────────────────────────────────────────
    output = {
        "run_ts":              RUN_TS,
        "index_integrity":     audit_stats,
        "metadata_validation": val_results,
        "search_quality":      sq_results,
    }
    # Remove large per-doc compliance list before saving (to keep file manageable)
    output["metadata_validation"] = {k: v for k, v in val_results.items()
                                     if k != "compliance_per_doc"}
    out_path = os.path.join(BASE_DIR, "phase2b35_audit_results.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    log(f"\nAudit results saved to phase2b35_audit_results.json")
    log("=" * 60)
    log("Phase 2B-3.5 audit pipeline complete.")
    log("=" * 60)
    return output


if __name__ == "__main__":
    main()
