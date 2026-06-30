import os
import sqlite3
import json

BASE_DIR = r"d:\Siddha_Wisdom"
NORM_DIR = os.path.join(BASE_DIR, "normalized_corpus")
DB_PATH = os.path.join(BASE_DIR, "siddhaverse.db")
ENTITY_REFINED_PATH = os.path.join(BASE_DIR, "entity_registry", "entity_index_refined.json")
ENTITY_XREF_PATH = os.path.join(BASE_DIR, "entity_cross_reference.json")
SEARCH_INDEX_PATH = os.path.join(BASE_DIR, "search_index.json")

def dict_to_json(d):
    return json.dumps(d, ensure_ascii=False)

def sanitize_str(val):
    if val is None:
        return None
    if isinstance(val, (list, dict)):
        return json.dumps(val, ensure_ascii=False)
    return str(val)

def main():
    print("--- Database Seeder Starting (Enriched with search_index.json) ---")
    if os.path.exists(DB_PATH):
        try:
            os.remove(DB_PATH)
            print(f"Removed existing database at {DB_PATH}")
        except Exception as e:
            print(f"Warning: Could not remove existing database: {e}")

    # Load search_index.json for keywords and search_text enrichment
    index_records = {}
    if os.path.exists(SEARCH_INDEX_PATH):
        print(f"Loading search index from {SEARCH_INDEX_PATH}...")
        with open(SEARCH_INDEX_PATH, "r", encoding="utf-8") as f:
            search_idx = json.load(f)
        for r in search_idx.get("records", []):
            doc_id = r.get("document_id") or r.get("text_id")
            if doc_id:
                index_records[doc_id] = r
        print(f"Loaded {len(index_records)} index records for enrichment.")
    else:
        print(f"Warning: {SEARCH_INDEX_PATH} not found. Keywords enrichment will be skipped.")

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # 1. Create tables
    print("Creating tables...")
    cursor.execute("""
    CREATE TABLE documents (
        document_id TEXT PRIMARY KEY,
        title TEXT,
        source_work TEXT,
        collection TEXT,
        verse_number TEXT,
        author TEXT,
        language TEXT,
        script TEXT,
        tamil_text TEXT,
        transliteration TEXT,
        english_translation TEXT,
        content_hash TEXT,
        copyright_status TEXT,
        source_repository TEXT,
        source_url TEXT,
        acquisition_timestamp TEXT,
        provenance_metadata TEXT,
        normalization TEXT,
        entity_ids TEXT,
        search_text TEXT,
        doc_type TEXT,
        custom_fields TEXT
    );
    """)

    cursor.execute("""
    CREATE VIRTUAL TABLE documents_fts USING fts5(
        document_id UNINDEXED,
        title,
        author,
        source_work,
        collection,
        search_text,
        tamil_text,
        transliteration
    );
    """)

    cursor.execute("""
    CREATE TABLE entities (
        entity_id TEXT PRIMARY KEY,
        entity_category TEXT,
        entity_name TEXT,
        description TEXT,
        occurrence_count INTEGER,
        dominant_tier TEXT,
        false_positive_risk TEXT,
        fp_annotation TEXT,
        tier_breakdown TEXT,
        max_confidence REAL,
        avg_confidence REAL,
        work_distribution TEXT,
        co_occurring_entities TEXT,
        sample_verse_ids TEXT
    );
    """)

    # 2. Seed documents
    print("Seeding documents...")
    doc_count = 0
    for fname in sorted(os.listdir(NORM_DIR)):
        if not fname.endswith(".json"):
            continue
        fpath = os.path.join(NORM_DIR, fname)
        with open(fpath, encoding="utf-8") as f:
            doc = json.load(f)

        doc_id = doc.get("document_id") or doc.get("text_id")
        if not doc_id:
            continue
        
        # Determine doc_type
        if fname.startswith("text_") or doc_id.startswith("text_"):
            doc_type = "verse"
        elif doc_id.startswith("siddhar_"):
            doc_type = "biography"
        elif doc_id.startswith("formulation_"):
            doc_type = "formulation"
        elif doc_id.startswith("plant_"):
            doc_type = "plant"
        elif doc_id.startswith("manuscript_"):
            doc_type = "manuscript"
        elif doc_id.startswith("classic_"):
            doc_type = "classical_text"
        elif doc_id.startswith("pubmed_"):
            doc_type = "research"
        else:
            doc_type = "other"

        # Separate custom fields (all fields not in base schema)
        base_schema_fields = {
            "document_id", "text_id", "title", "source_work", "collection", 
            "verse_number", "author", "language", "script", "tamil_text", 
            "transliteration", "english_translation", "content_hash", 
            "copyright_status", "source_repository", "source_url", 
            "acquisition_timestamp", "provenance_metadata", "normalization", 
            "entity_ids", "search_text", "translation_status"
        }
        custom = {k: v for k, v in doc.items() if k not in base_schema_fields}

        # Enrich search_text with index keywords and search text
        idx_rec = index_records.get(doc_id, {})
        keywords = idx_rec.get("keywords", [])
        
        raw_search_text = doc.get("search_text") or idx_rec.get("search_text") or ""
        enriched_search_text = raw_search_text
        if keywords:
            enriched_search_text = enriched_search_text + " " + " ".join(keywords)

        cursor.execute("""
        INSERT INTO documents (
            document_id, title, source_work, collection, verse_number, author,
            language, script, tamil_text, transliteration, english_translation,
            content_hash, copyright_status, source_repository, source_url,
            acquisition_timestamp, provenance_metadata, normalization,
            entity_ids, search_text, doc_type, custom_fields
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        """, (
            doc_id,
            sanitize_str(doc.get("title")),
            sanitize_str(doc.get("source_work")),
            sanitize_str(doc.get("collection")),
            sanitize_str(doc.get("verse_number")),
            sanitize_str(doc.get("author")),
            sanitize_str(doc.get("language")),
            sanitize_str(doc.get("script")),
            sanitize_str(doc.get("tamil_text")),
            sanitize_str(doc.get("transliteration")),
            sanitize_str(doc.get("english_translation")),
            sanitize_str(doc.get("content_hash")),
            sanitize_str(doc.get("copyright_status")),
            sanitize_str(doc.get("source_repository")),
            sanitize_str(doc.get("source_url")),
            sanitize_str(doc.get("acquisition_timestamp")),
            dict_to_json(doc.get("provenance_metadata") or {}),
            dict_to_json(doc.get("normalization") or {}),
            dict_to_json(doc.get("entity_ids") or []),
            enriched_search_text,
            doc_type,
            dict_to_json(custom)
        ))

        # Insert FTS index record
        cursor.execute("""
        INSERT INTO documents_fts (
            document_id, title, author, source_work, collection, search_text, tamil_text, transliteration
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?);
        """, (
            doc_id,
            sanitize_str(doc.get("title")) or "",
            sanitize_str(doc.get("author")) or "",
            sanitize_str(doc.get("source_work")) or "",
            sanitize_str(doc.get("collection")) or "",
            enriched_search_text,
            sanitize_str(doc.get("tamil_text")) or "",
            sanitize_str(doc.get("transliteration")) or ""
        ))
        
        doc_count += 1

    print(f"Seeded {doc_count} documents into SQL and FTS tables.")

    # 3. Seed entities
    print("Seeding entities...")
    with open(ENTITY_REFINED_PATH, encoding="utf-8") as f:
        refined = json.load(f)

    with open(ENTITY_XREF_PATH, encoding="utf-8") as f:
        xref = json.load(f).get("cross_references", {})

    entity_count = 0
    for ent in refined.get("entities", []):
        ent_id = ent["entity_id"]
        xref_data = xref.get(ent_id, {})
        
        cursor.execute("""
        INSERT INTO entities (
            entity_id, entity_category, entity_name, description, occurrence_count,
            dominant_tier, false_positive_risk, fp_annotation, tier_breakdown,
            max_confidence, avg_confidence, work_distribution, co_occurring_entities, sample_verse_ids
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        """, (
            ent_id,
            ent.get("entity_category"),
            ent.get("entity_name"),
            ent.get("description"),
            ent.get("occurrence_count"),
            ent.get("dominant_tier"),
            ent.get("false_positive_risk"),
            ent.get("fp_annotation"),
            dict_to_json(ent.get("tier_breakdown") or {}),
            ent.get("max_confidence"),
            ent.get("avg_confidence"),
            dict_to_json(xref_data.get("work_distribution") or {}),
            dict_to_json(xref_data.get("co_occurring_entities") or []),
            dict_to_json(xref_data.get("verse_ids") or [])
        ))
        entity_count += 1

    print(f"Seeded {entity_count} entities.")

    conn.commit()
    conn.close()
    print("--- Database Seeder Finished ---")

if __name__ == "__main__":
    main()
