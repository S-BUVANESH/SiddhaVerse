"""
Phase 2B-2: Corpus Normalization, Metadata Standardization & Entity Discovery
==============================================================================
Objectives:
  1. Corpus Normalization  – Unicode NFC, HTML artifact removal, whitespace
  2. Metadata Standardization – consistent schema across all 1,150 active docs
  3. Entity Discovery – dictionary-based extraction with confidence scores
  4. Entity Registry – structured JSON registry with source traceability

No embeddings, vectorization, LLM, or knowledge-graph operations.

Run from workspace root:  python phase2b2_pipeline.py
"""

import os
import re
import json
import unicodedata
import hashlib
import datetime
from collections import defaultdict

# ── Paths ─────────────────────────────────────────────────────────────────────
BASE_DIR      = r"d:\Siddha_Wisdom"
RAW_DIR       = os.path.join(BASE_DIR, "raw_documents")
META_DIR      = os.path.join(BASE_DIR, "metadata_registry")
NORM_DIR      = os.path.join(BASE_DIR, "normalized_corpus")
ENTITY_DIR    = os.path.join(BASE_DIR, "entity_registry")
LOG_FILE      = os.path.join(BASE_DIR, "phase2b2_run.log")
RUN_TS        = datetime.datetime.now(datetime.timezone.utc).isoformat()

os.makedirs(NORM_DIR,   exist_ok=True)
os.makedirs(ENTITY_DIR, exist_ok=True)

# ── Logger ─────────────────────────────────────────────────────────────────────
def log(msg: str):
    safe = msg.encode("ascii", errors="replace").decode("ascii")
    line = f"[{datetime.datetime.now(datetime.timezone.utc).strftime('%H:%M:%S')}] {safe}"
    print(line)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{datetime.datetime.now(datetime.timezone.utc).strftime('%H:%M:%S')}] {msg}\n")


# ══════════════════════════════════════════════════════════════════════════════
# SECTION 1 — ENTITY LEXICON
# ══════════════════════════════════════════════════════════════════════════════

# Each entry: { "tamil": str|list, "transliteration": str, "description": str, "type": str }
# Confidence levels:
#   1.0 = exact standalone token match
#   0.85 = exact substring match
#   0.65 = root/partial match

ENTITY_LEXICON = {

    # ── Siddhars ──────────────────────────────────────────────────────────────
    "siddhars": [
        {"id": "siddhar_thirumoolar",   "tamil": ["திருமூலர்", "திருமூல"],          "roman": "Thirumoolar",   "desc": "Author of Thirumandiram; foremost Siddhar-Nayanar"},
        {"id": "siddhar_sivavakkiyar",  "tamil": ["சிவவாக்கியர்", "சிவவாக்கியம்"], "roman": "Sivavakkiyar",  "desc": "Iconoclastic Siddhar poet; author of Sivavakkiyam"},
        {"id": "siddhar_agasthiyar",    "tamil": ["அகத்தியர்", "அகத்திய"],          "roman": "Agasthiyar",    "desc": "Primordial Siddhar; father of Tamil language and medicine"},
        {"id": "siddhar_bogar",         "tamil": ["போகர்", "போக"],                  "roman": "Bogar",         "desc": "Siddhar alchemist and author of Bogar 7000"},
        {"id": "siddhar_pambatti",      "tamil": ["பாம்பட்டி", "பாம்பட்"],          "roman": "Pambatti",      "desc": "Snake Siddhar; poet of Pambatti Siddhar songs"},
        {"id": "siddhar_konkanar",      "tamil": ["கொங்கணர்", "கொங்கண"],            "roman": "Konkanar",      "desc": "Siddhar from Konkan region"},
        {"id": "siddhar_korakkar",      "tamil": ["கோரக்கர்", "கோரக்க"],             "roman": "Gorakkar",      "desc": "Siddhar and alchemist; disciple of Machamuni"},
        {"id": "siddhar_machamuni",     "tamil": ["மச்சமுனி", "மச்சேந்திர"],        "roman": "Machamuni",     "desc": "Fish Siddhar; Matsyendranath in North Indian tradition"},
        {"id": "siddhar_theriyar",      "tamil": ["தேரையர்", "தேரைய"],               "roman": "Theriyar",      "desc": "Siddhar physician and poet"},
        {"id": "siddhar_karuvoorar",    "tamil": ["கருவூரார்", "கருவூர"],             "roman": "Karuvoorar",    "desc": "Siddhar alchemist associated with Karur"},
        {"id": "siddhar_ramadevar",     "tamil": ["இராமதேவர்", "ராமதேவர்"],         "roman": "Ramadevar",     "desc": "Siddhar; also known as Yakob in some traditions"},
        {"id": "siddhar_sattaimuni",    "tamil": ["சட்டைமுனி", "சட்டை"],             "roman": "Sattaimuni",    "desc": "Siddhar of Tirunelveli; coat-wearing ascetic"},
        {"id": "siddhar_kudambai",      "tamil": ["குதம்பை", "குடம்பை"],             "roman": "Kudambai",      "desc": "Siddhar poet; known for enigmatic verse style"},
        {"id": "siddhar_idaikkadar",    "tamil": ["இடைக்காடர்", "இடைக்காட"],        "roman": "Idaikkadar",    "desc": "Shepherd Siddhar poet"},
        {"id": "siddhar_nandidevar",    "tamil": ["நந்தி", "நந்தீசர்"],              "roman": "Nandidevar",    "desc": "Nandi — divine Siddhar guru of Thirumoolar"},
        {"id": "siddhar_yugi",          "tamil": ["யூகி", "யோகி"],                  "roman": "Yugi Muni",     "desc": "Siddhar physician; author of Yugi Chinthamani"},
    ],

    # ── Deities & Divine Concepts ─────────────────────────────────────────────
    "deities": [
        {"id": "deity_shiva",          "tamil": ["சிவன்", "சிவம்", "சிவ", "ஈசன்", "ஈசுவரன்", "மகேசன்", "பரமன்", "பரமேசுவரன்", "சம்பு"], "roman": "Shiva",    "desc": "Supreme deity of Shaiva Siddhanta; the Absolute"},
        {"id": "deity_shakti",         "tamil": ["சக்தி", "பராசக்தி", "அம்பாள்", "ஆதிசக்தி", "பார்வதி", "உமை"], "roman": "Shakti", "desc": "Divine feminine energy; consort of Shiva"},
        {"id": "deity_murugan",        "tamil": ["முருகன்", "குமரன்", "கார்த்திகேயன்", "வேலன்"], "roman": "Murugan", "desc": "Son of Shiva; Tamil deity of war and wisdom"},
        {"id": "deity_vishnu",         "tamil": ["விஷ்ணு", "திருமால்", "மாயோன்", "நாராயணன்"],  "roman": "Vishnu",  "desc": "Preserver deity; Vaishnava tradition"},
        {"id": "deity_ganesha",        "tamil": ["கணேசன்", "விநாயகன்", "பிள்ளையார்", "கணபதி"], "roman": "Ganesha", "desc": "Elephant-headed deity; remover of obstacles"},
        {"id": "deity_brahma",         "tamil": ["பிரமன்", "பிரம்மா", "நான்முகன்"],             "roman": "Brahma",  "desc": "Creator deity of the Hindu Trimurti"},
        {"id": "deity_kali",           "tamil": ["காளி", "துர்கை", "சண்டி"],                   "roman": "Kali",    "desc": "Fierce form of Shakti"},
    ],

    # ── Sacred Places ─────────────────────────────────────────────────────────
    "places": [
        {"id": "place_kailash",        "tamil": ["கயிலை", "கயிலாயம்"],              "roman": "Kailash",         "desc": "Sacred mountain; abode of Shiva"},
        {"id": "place_chidambaram",    "tamil": ["சிதம்பரம்", "தில்லை"],             "roman": "Chidambaram",     "desc": "Temple city; site of Nataraja shrine"},
        {"id": "place_tiruvannamalai", "tamil": ["திருவண்ணாமலை", "அண்ணாமலை"],      "roman": "Tiruvannamalai",  "desc": "Sacred hill; Arunachala; associated with Shiva"},
        {"id": "place_madurai",        "tamil": ["மதுரை"],                           "roman": "Madurai",         "desc": "Ancient Tamil capital; Meenakshi temple city"},
        {"id": "place_kashi",          "tamil": ["காசி", "வாரணாசி", "பேணாரசி"],     "roman": "Kashi",           "desc": "Holy city of Varanasi/Benares"},
        {"id": "place_potigai",        "tamil": ["பொதியை", "பொதிகை"],               "roman": "Potigai",         "desc": "Potigai hill; abode of Sage Agasthiyar"},
        {"id": "place_himalaya",       "tamil": ["இமயம்", "இமையம்", "இமாலயம்"],    "roman": "Himalaya",        "desc": "Himalayan mountains; abode of sages"},
    ],

    # ── Philosophical & Yogic Concepts ────────────────────────────────────────
    "concepts": [
        {"id": "concept_yoga",          "tamil": ["யோகம்", "யோக"],                   "roman": "Yoga",          "desc": "Spiritual discipline; union with the Divine"},
        {"id": "concept_tantra",        "tamil": ["தந்திரம்", "தந்திர"],              "roman": "Tantra",        "desc": "Esoteric system of ritual and yoga"},
        {"id": "concept_mantra",        "tamil": ["மந்திரம்", "மந்திர"],              "roman": "Mantra",        "desc": "Sacred sound formula for meditation"},
        {"id": "concept_mukti",         "tamil": ["முக்தி", "வீடு", "வீடுபேறு", "மோட்சம்", "கைவல்யம்"], "roman": "Mukti/Liberation", "desc": "Liberation from cycle of birth and death"},
        {"id": "concept_atman",         "tamil": ["ஆத்மா", "ஆன்மா", "உயிர்"],        "roman": "Atman",         "desc": "The individual soul/self"},
        {"id": "concept_pranava",       "tamil": ["பிரணவம்", "ஓம்", "ஓங்கார"],       "roman": "Pranava/OM",    "desc": "Sacred syllable OM; primordial sound"},
        {"id": "concept_kundalini",     "tamil": ["குண்டலினி", "குண்டலி"],            "roman": "Kundalini",     "desc": "Dormant spiritual energy coiled at spine base"},
        {"id": "concept_chakra",        "tamil": ["சக்கரம்", "சக்ர"],                 "roman": "Chakra",        "desc": "Energy centers in the subtle body"},
        {"id": "concept_nadi",          "tamil": ["நாடி"],                            "roman": "Nadi",          "desc": "Energy channels in subtle body; also pulse diagnosis"},
        {"id": "concept_prana",         "tamil": ["பிராணன்", "பிராண", "வாயு", "ஐந்து வாயு"], "roman": "Prana", "desc": "Life force / vital breath"},
        {"id": "concept_karma",         "tamil": ["கர்மம்", "வினை"],                  "roman": "Karma",         "desc": "Law of action and consequence"},
        {"id": "concept_maya",          "tamil": ["மாயை", "மாய"],                     "roman": "Maya",          "desc": "Cosmic illusion; the veil over reality"},
        {"id": "concept_jnana",         "tamil": ["ஞானம்", "மெய்ஞ்ஞானம்"],           "roman": "Jnana",         "desc": "Wisdom; direct knowledge of Brahman"},
        {"id": "concept_bhakti",        "tamil": ["பக்தி"],                           "roman": "Bhakti",        "desc": "Devotional love toward the Divine"},
        {"id": "concept_tapas",         "tamil": ["தவம்", "தபம்"],                    "roman": "Tapas",         "desc": "Austerity; spiritual discipline through heat/effort"},
        {"id": "concept_dhyana",        "tamil": ["தியானம்", "தியான"],                "roman": "Dhyana",        "desc": "Meditation; deep contemplative practice"},
        {"id": "concept_samadhi",       "tamil": ["சமாதி"],                           "roman": "Samadhi",       "desc": "State of meditative absorption"},
        {"id": "concept_pancha_bootham","tamil": ["பஞ்சபூதம்", "பஞ்ச பூதம்", "ஐம்பூதம்"], "roman": "Pancha Bhuta", "desc": "Five elements: earth, water, fire, air, space"},
        {"id": "concept_shiva_shakti",  "tamil": ["சிவசக்தி"],                        "roman": "Shiva-Shakti",  "desc": "Union of Shiva and Shakti; non-dual ultimate reality"},
        {"id": "concept_siddhi",        "tamil": ["சித்தி", "சித்து"],                "roman": "Siddhi",        "desc": "Supernormal power attained through spiritual practice"},
        {"id": "concept_guru",          "tamil": ["குரு", "ஆசான்", "ஆச்சார்யன்"],    "roman": "Guru",          "desc": "Spiritual teacher; dispeller of ignorance"},
        {"id": "concept_shishya",       "tamil": ["சீடன்", "சிஷ்யன்"],               "roman": "Shishya",       "desc": "Disciple; student of the Guru"},
        {"id": "concept_brahman",       "tamil": ["பரம்பொருள்", "பரப்பிரம்மம்"],     "roman": "Brahman",       "desc": "The Absolute; ultimate reality in Vedanta"},
        {"id": "concept_agama",         "tamil": ["ஆகமம்", "ஆகம"],                   "roman": "Agama",         "desc": "Scriptural canon of Shaiva Siddhanta"},
    ],

    # ── Body & Physiology Terms ───────────────────────────────────────────────
    "body_terms": [
        {"id": "body_udal",     "tamil": ["உடம்பு", "உடல்"],                    "roman": "Udal (Body)",   "desc": "Physical body"},
        {"id": "body_uyir",     "tamil": ["உயிர்"],                              "roman": "Uyir (Life)",   "desc": "Life/soul; the animating principle"},
        {"id": "body_moolam",   "tamil": ["மூலம்", "மூலாதாரம்"],                "roman": "Moolam",        "desc": "Root; base chakra (Muladhara)"},
        {"id": "body_head",     "tamil": ["தலை", "சிரசு", "மூர்த்தி"],          "roman": "Head",          "desc": "Head; seat of consciousness in some traditions"},
        {"id": "body_heart",    "tamil": ["இதயம்", "நெஞ்சு", "மனம்"],           "roman": "Heart/Mind",    "desc": "Heart/mind; seat of consciousness"},
        {"id": "body_breath",   "tamil": ["சுவாசம்", "மூச்சு", "மூச்சுக்காற்று"], "roman": "Breath",     "desc": "Breath; vehicle of prana"},
        {"id": "body_seed",     "tamil": ["விந்து"],                              "roman": "Vindu",         "desc": "Bindu; seed; drop of vital essence"},
        {"id": "body_sound",    "tamil": ["நாதம்"],                               "roman": "Nadam",         "desc": "Inner sound; cosmic vibration"},
        {"id": "body_eye",      "tamil": ["கண்", "கண்ணி"],                       "roman": "Eye",           "desc": "Eye; often symbolic of divine perception"},
        {"id": "body_light",    "tamil": ["சோதி", "ஒளி", "தீபம்"],              "roman": "Light/Flame",   "desc": "Inner light; divine illumination"},
        {"id": "body_fire",     "tamil": ["அக்னி", "தீ"],                        "roman": "Agni/Fire",     "desc": "Sacred fire; digestive fire; transformative energy"},
    ],

    # ── Medicinal Plants (cross-ref with Phase 2A) ────────────────────────────
    "plants": [
        {"id": "plant_tulsi",     "tamil": ["துளசி", "துலசி"],                "roman": "Tulsi",         "desc": "Holy Basil; sacred and medicinal plant"},
        {"id": "plant_neem",      "tamil": ["வேம்பு", "வேப்பு", "வேப்பம்"],    "roman": "Neem (Vembu)", "desc": "Azadirachta indica; antimicrobial herb"},
        {"id": "plant_nelli",     "tamil": ["நெல்லி"],                         "roman": "Nelli",         "desc": "Indian Gooseberry (Amla); rejuvenative herb"},
        {"id": "plant_manjal",    "tamil": ["மஞ்சள்"],                         "roman": "Turmeric",      "desc": "Curcuma longa; anti-inflammatory"},
        {"id": "plant_milagu",    "tamil": ["மிளகு"],                           "roman": "Black Pepper",  "desc": "Piper nigrum; Trikatu component"},
        {"id": "plant_ginger",    "tamil": ["இஞ்சி", "சுக்கு"],                "roman": "Ginger/Sukku", "desc": "Zingiber officinale; digestive herb"},
        {"id": "plant_ashwagandha",  "tamil": ["அஷ்வகந்தா", "அமுக்கிரா"],     "roman": "Ashwagandha",   "desc": "Withania somnifera; adaptogenic root"},
        {"id": "plant_vallarai",  "tamil": ["வல்லாரை"],                        "roman": "Vallarai",      "desc": "Centella asiatica; brain tonic"},
        {"id": "plant_thippili",  "tamil": ["திப்பிலி"],                        "roman": "Thippili",      "desc": "Long Pepper (Piper longum)"},
        {"id": "plant_lotus",     "tamil": ["தாமரை", "கமலம்"],                 "roman": "Lotus",         "desc": "Sacred lotus; Nelumbo nucifera; symbol of purity"},
        {"id": "plant_kadukkai",  "tamil": ["கடுக்காய்"],                       "roman": "Haritaki",      "desc": "Terminalia chebula; triphala component"},
        {"id": "plant_vembu",     "tamil": ["வேம்பு"],                          "roman": "Neem",          "desc": "Azadirachta indica; used in Siddha medicine"},
        {"id": "plant_keezhanelli","tamil": ["கீழாநெல்லி"],                    "roman": "Keezhanelli",   "desc": "Phyllanthus niruri; liver tonic"},
    ],

    # ── Siddha Medical / Alchemical Terms ────────────────────────────────────
    "practices": [
        {"id": "practice_kayakalpa",   "tamil": ["காயகல்பம்", "காயகல்ப"],       "roman": "Kayakalpa",    "desc": "Rejuvenation therapy for bodily immortality"},
        {"id": "practice_rasayana",    "tamil": ["இரசாயனம்", "ரசவாதம்"],         "roman": "Rasayana",     "desc": "Alchemical rejuvenation; elixir preparation"},
        {"id": "practice_varma",       "tamil": ["வர்மம்", "வர்ம"],               "roman": "Varma",        "desc": "Vital points therapy; Siddha body energy points"},
        {"id": "practice_pranayama",   "tamil": ["பிராணாயாமம்", "கும்பகம்"],     "roman": "Pranayama",    "desc": "Breath control practice"},
        {"id": "practice_mudra",       "tamil": ["முத்திரை"],                    "roman": "Mudra",        "desc": "Ritual hand gesture; energy seal"},
        {"id": "practice_bandha",      "tamil": ["பந்தம்", "பந்த"],               "roman": "Bandha",       "desc": "Energy lock in yoga"},
        {"id": "practice_deekshai",    "tamil": ["தீட்சை"],                      "roman": "Diksha",       "desc": "Spiritual initiation by a Guru"},
        {"id": "practice_japa",        "tamil": ["ஜபம்", "ஜப"],                   "roman": "Japa",         "desc": "Repetitive chanting of mantra/name"},
        {"id": "practice_puja",        "tamil": ["பூஜை"],                         "roman": "Puja",         "desc": "Ritual worship"},
        {"id": "practice_kumbhaka",    "tamil": ["கும்பகம்"],                     "roman": "Kumbhaka",     "desc": "Breath retention in pranayama"},
        {"id": "practice_moolamantra", "tamil": ["நமசிவாய", "நமச்சிவாய", "பஞ்சாட்சரம்"], "roman": "Namashivaya", "desc": "Five-syllable mantra of Shiva; Panchakshara"},
        {"id": "practice_ashta_siddhi","tamil": ["அட்டசித்தி", "எட்டுச்சித்தி"], "roman": "Ashta Siddhi", "desc": "Eight supernatural powers attained by Siddhars"},
    ],

    # ── Numbers & Symbolic Groups ─────────────────────────────────────────────
    "symbolic": [
        {"id": "symbol_three",    "tamil": ["மும்மலம்", "முத்தொழில்", "முத்தி"],    "roman": "Three/Trinity",  "desc": "Triple impurities (anava, kanma, maya)"},
        {"id": "symbol_five",     "tamil": ["ஐந்தெழுத்து", "பஞ்சாட்சரம்"],         "roman": "Five Letters",   "desc": "Five sacred syllables Na-Ma-Si-Va-Ya"},
        {"id": "symbol_six",      "tamil": ["ஆறாதாரம்"],                             "roman": "Six Supports",   "desc": "Six chakras / energy centers"},
        {"id": "symbol_eight",    "tamil": ["எட்டு", "அட்ட"],                         "roman": "Eight",          "desc": "Symbolic eight; Ashta-siddhi"},
        {"id": "symbol_eighteen", "tamil": ["பதினெட்டு சித்தர்", "பதினெட்டு"],       "roman": "Eighteen Siddhars","desc": "The eighteen Siddhars of Tamil tradition"},
    ],
}

# Flat list of all entities for quick lookup
ALL_ENTITIES = []
for cat, entries in ENTITY_LEXICON.items():
    for ent in entries:
        ent["category"] = cat
        ALL_ENTITIES.append(ent)


# ══════════════════════════════════════════════════════════════════════════════
# SECTION 2 — NORMALIZATION
# ══════════════════════════════════════════════════════════════════════════════

HTML_ENT_RE  = re.compile(r"&(?:nbsp|amp|lt|gt|quot|apos|#\d+|#x[0-9a-fA-F]+);", re.IGNORECASE)
MULTI_SP_RE  = re.compile(r"[ \t]{2,}")
TRAIL_NUM_RE = re.compile(r"\s+\d+\s*$")           # trailing verse number on last line
BRACKET_NUM  = re.compile(r"\(\d+\)\s*$")           # trailing (N)
SECTION_HDR  = re.compile(r"^[^\u0B80-\u0BFF\n]{0,40}$")  # lines with no Tamil chars (section headers)


def normalize_tamil_text(raw: str) -> dict:
    """
    Apply normalization to a Tamil verse text string.
    Returns dict with normalized text and change log.
    """
    changes = []
    text = raw

    # 1. Unicode NFC normalization
    nfc = unicodedata.normalize("NFC", text)
    if nfc != text:
        changes.append("unicode_nfc")
        text = nfc

    # 2. Remove HTML entities
    cleaned = HTML_ENT_RE.sub(" ", text)
    if cleaned != text:
        changes.append("html_entities_removed")
        text = cleaned

    # 3. Remove stray section header lines (lines with no Tamil content and short)
    lines = text.splitlines()
    filtered = []
    for line in lines:
        has_tamil = bool(re.search(r"[\u0B80-\u0BFF]", line))
        is_short_ascii = not has_tamil and len(line.strip()) < 60
        if is_short_ascii and line.strip():
            changes.append(f"section_header_removed:{repr(line.strip()[:30])}")
        else:
            filtered.append(line)

    if len(filtered) != len(lines):
        text = "\n".join(filtered)

    # 4. Strip trailing verse numbers from last line
    lines2 = text.splitlines()
    if lines2:
        last = lines2[-1]
        cleaned_last = TRAIL_NUM_RE.sub("", last).rstrip()
        cleaned_last = BRACKET_NUM.sub("", cleaned_last).rstrip()
        if cleaned_last != last:
            changes.append("trailing_verse_number_stripped")
            lines2[-1] = cleaned_last
        text = "\n".join(lines2)

    # 5. Normalize whitespace within lines (collapse multiple spaces)
    new_lines = []
    for line in text.splitlines():
        norm_line = MULTI_SP_RE.sub(" ", line).strip()
        new_lines.append(norm_line)
    normalized = "\n".join(l for l in new_lines if l or True)  # keep blank separators
    if normalized != text:
        if "whitespace_normalized" not in changes:
            changes.append("whitespace_normalized")
        text = normalized

    # 6. Strip leading/trailing whitespace
    text = text.strip()

    return {"text": text, "changes": changes, "changed": bool(changes)}


STANDARD_SCHEMA = {
    # Core identity
    "document_id":           None,
    "text_id":               None,
    "title":                 None,
    # Source classification
    "source_work":           None,
    "collection":            None,
    "verse_number":          None,
    "author":                None,
    # Content
    "language":              "Tamil",
    "script":                "Tamil script",
    "tamil_text":            None,
    "transliteration":       None,
    "english_translation":   None,
    # Integrity
    "content_hash":          None,
    "normalization": {
        "applied":           False,
        "changes":           [],
        "normalized_by":     "SiddhaVerse Phase 2B-2",
        "normalized_at":     RUN_TS,
    },
    # Provenance
    "copyright_status":      None,
    "source_repository":     None,
    "source_url":            None,
    "acquisition_timestamp": None,
    "provenance_metadata":   {},
    # Entity links (filled later)
    "entity_ids":            [],
}


def standardize_doc(raw_doc: dict) -> dict:
    """Merge raw document into standard schema; normalize Tamil text."""
    doc = dict(STANDARD_SCHEMA)
    doc["normalization"] = {
        "applied":       False,
        "changes":       [],
        "normalized_by": "SiddhaVerse Phase 2B-2",
        "normalized_at": RUN_TS,
    }

    # Copy all existing fields
    for k, v in raw_doc.items():
        doc[k] = v

    # Normalize Tamil text if present
    if doc.get("tamil_text"):
        result = normalize_tamil_text(doc["tamil_text"])
        if result["changed"]:
            doc["tamil_text"] = result["text"]
            doc["normalization"]["applied"]  = True
            doc["normalization"]["changes"]  = result["changes"]
            # Recompute content hash
            norm = re.sub(r"\s+", " ", result["text"]).strip()
            doc["content_hash"] = hashlib.sha256(norm.encode("utf-8")).hexdigest()

    # Ensure language / script fields
    if not doc.get("language"):
        doc["language"] = "Tamil"
    if not doc.get("script"):
        doc["script"] = "Tamil script"

    return doc


# ══════════════════════════════════════════════════════════════════════════════
# SECTION 3 — ENTITY EXTRACTION
# ══════════════════════════════════════════════════════════════════════════════

TAMIL_TOKEN_RE = re.compile(r"[\u0B80-\u0BFF]+")


def compute_confidence(tamil_text: str, entity_terms: list[str]) -> tuple[float, str, str]:
    """
    Returns (confidence, match_type, matched_term).
    match_type: 'exact_token' | 'exact_substring' | 'root_match'
    """
    # Tokenise text
    tokens = set(TAMIL_TOKEN_RE.findall(tamil_text))

    for term in entity_terms:
        if not re.search(r"[\u0B80-\u0BFF]", term):
            continue  # skip non-Tamil terms

        # Exact token match (highest)
        if term in tokens:
            return (1.0, "exact_token", term)

        # Exact substring match
        if term in tamil_text:
            return (0.85, "exact_substring", term)

        # Root match: check if any token starts with first 3 chars of term
        if len(term) >= 3:
            root = term[:3]
            if root in tamil_text:
                return (0.60, "root_match", term)

    return (0.0, "no_match", "")


def extract_entities_from_doc(doc: dict) -> list[dict]:
    """
    Run all entity lexicon entries against doc's Tamil text.
    Returns list of entity match records.
    """
    text = doc.get("tamil_text", "")
    if not text:
        return []

    doc_id = doc["document_id"]
    matches = []

    for ent in ALL_ENTITIES:
        terms = ent["tamil"] if isinstance(ent["tamil"], list) else [ent["tamil"]]
        conf, match_type, matched = compute_confidence(text, terms)
        if conf > 0:
            matches.append({
                "entity_id":      ent["id"],
                "entity_category": ent["category"],
                "entity_name_roman": ent["roman"],
                "description":    ent["desc"],
                "matched_term":   matched,
                "match_type":     match_type,
                "confidence":     conf,
                "source_doc_id":  doc_id,
                "source_work":    doc.get("source_work"),
                "verse_number":   doc.get("verse_number"),
            })

    return matches


# ══════════════════════════════════════════════════════════════════════════════
# SECTION 4 — REGISTRY BUILDER
# ══════════════════════════════════════════════════════════════════════════════

def build_entity_registry(all_matches: list[dict]):
    """
    Aggregate entity matches into a structured registry.
    Writes per-category JSON files + master index.
    """
    # Group by entity_id
    entity_map: dict = {}  # entity_id → entity record

    for m in all_matches:
        eid = m["entity_id"]
        if eid not in entity_map:
            entity_map[eid] = {
                "entity_id":       eid,
                "entity_category": m["entity_category"],
                "entity_name":     m["entity_name_roman"],
                "description":     m["description"],
                "occurrence_count": 0,
                "max_confidence":  0.0,
                "min_confidence":  1.0,
                "avg_confidence":  0.0,
                "confidence_sum":  0.0,
                "source_documents": [],  # list of {doc_id, verse_number, source_work, confidence, match_type, matched_term}
            }

        rec = entity_map[eid]
        rec["occurrence_count"] += 1
        rec["confidence_sum"]   += m["confidence"]
        rec["max_confidence"]   = max(rec["max_confidence"], m["confidence"])
        rec["min_confidence"]   = min(rec["min_confidence"], m["confidence"])
        rec["source_documents"].append({
            "document_id":  m["source_doc_id"],
            "verse_number": m["verse_number"],
            "source_work":  m["source_work"],
            "confidence":   m["confidence"],
            "match_type":   m["match_type"],
            "matched_term": m["matched_term"],
        })

    # Compute avg confidence and sort source_documents by confidence desc
    for rec in entity_map.values():
        n = rec["occurrence_count"]
        rec["avg_confidence"] = round(rec["confidence_sum"] / n, 4) if n else 0.0
        del rec["confidence_sum"]
        rec["source_documents"].sort(key=lambda x: -x["confidence"])
        # Cap stored source docs to 50 (keep highest confidence)
        rec["source_documents_total"] = len(rec["source_documents"])
        rec["source_documents"] = rec["source_documents"][:50]

    # Write per-category files
    by_category: dict = defaultdict(list)
    for rec in entity_map.values():
        by_category[rec["entity_category"]].append(rec)

    for cat, records in by_category.items():
        records.sort(key=lambda r: -r["occurrence_count"])
        path = os.path.join(ENTITY_DIR, f"{cat}.json")
        out = {
            "category":       cat,
            "entity_count":   len(records),
            "generated_at":   RUN_TS,
            "entities":       records,
        }
        with open(path, "w", encoding="utf-8") as f:
            json.dump(out, f, ensure_ascii=False, indent=2)
        log(f"  Registry: {cat}.json — {len(records)} entities")

    # Master entity index
    index_records = []
    for rec in entity_map.values():
        index_records.append({
            "entity_id":        rec["entity_id"],
            "entity_category":  rec["entity_category"],
            "entity_name":      rec["entity_name"],
            "description":      rec["description"],
            "occurrence_count": rec["occurrence_count"],
            "max_confidence":   rec["max_confidence"],
            "avg_confidence":   rec["avg_confidence"],
        })
    index_records.sort(key=lambda r: -r["occurrence_count"])

    index_path = os.path.join(ENTITY_DIR, "entity_index.json")
    with open(index_path, "w", encoding="utf-8") as f:
        json.dump({
            "total_entities":    len(index_records),
            "generated_at":      RUN_TS,
            "categories":        list(by_category.keys()),
            "entities":          index_records,
        }, f, ensure_ascii=False, indent=2)

    log(f"  Master index: {len(index_records)} entities")
    return entity_map, by_category


# ══════════════════════════════════════════════════════════════════════════════
# SECTION 5 — MAIN PIPELINE
# ══════════════════════════════════════════════════════════════════════════════

def main():
    open(LOG_FILE, "w", encoding="utf-8").close()
    log("=" * 60)
    log("Phase 2B-2: Normalization, Standardization & Entity Discovery")
    log("=" * 60)

    # ── Load all active raw documents ─────────────────────────────────────────
    log("\nStep 1: Loading raw documents...")
    docs = []
    for fname in sorted(os.listdir(RAW_DIR)):
        if not fname.endswith(".json"):
            continue
        fpath = os.path.join(RAW_DIR, fname)
        with open(fpath, "r", encoding="utf-8") as f:
            try:
                docs.append((fname, json.load(f)))
            except json.JSONDecodeError as e:
                log(f"  WARN: Could not parse {fname}: {e}")
    log(f"  Loaded {len(docs)} documents")

    # ── Normalization & Standardization ───────────────────────────────────────
    log("\nStep 2: Normalizing and standardizing corpus...")
    norm_stats = {
        "total_docs":           len(docs),
        "docs_with_tamil_text": 0,
        "docs_normalized":      0,
        "change_types":         defaultdict(int),
        "schema_fields_added":  defaultdict(int),
    }

    normalized_docs = []
    all_entity_matches = []

    for fname, raw_doc in docs:
        norm_doc = standardize_doc(raw_doc)

        if norm_doc.get("tamil_text"):
            norm_stats["docs_with_tamil_text"] += 1

        if norm_doc["normalization"]["applied"]:
            norm_stats["docs_normalized"] += 1
            for ch in norm_doc["normalization"]["changes"]:
                ch_key = ch.split(":")[0]
                norm_stats["change_types"][ch_key] += 1

        normalized_docs.append((fname, norm_doc))

    log(f"  Documents with Tamil text: {norm_stats['docs_with_tamil_text']}")
    log(f"  Documents with changes:    {norm_stats['docs_normalized']}")

    # ── Save normalized corpus ────────────────────────────────────────────────
    log("\nStep 3: Saving normalized corpus...")
    for fname, norm_doc in normalized_docs:
        out_path = os.path.join(NORM_DIR, fname)
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(norm_doc, f, ensure_ascii=False, indent=2)
    log(f"  Saved {len(normalized_docs)} normalized documents to normalized_corpus/")

    # ── Entity Extraction ─────────────────────────────────────────────────────
    log("\nStep 4: Extracting entities...")
    entity_hit_docs = 0

    for fname, norm_doc in normalized_docs:
        matches = extract_entities_from_doc(norm_doc)
        if matches:
            entity_hit_docs += 1
            all_entity_matches.extend(matches)
            # Attach entity_ids back to the normalized doc
            ent_ids = list({m["entity_id"] for m in matches})
            norm_doc["entity_ids"] = ent_ids
            # Re-save with entity links
            out_path = os.path.join(NORM_DIR, fname)
            with open(out_path, "w", encoding="utf-8") as f:
                json.dump(norm_doc, f, ensure_ascii=False, indent=2)

    log(f"  Total entity mentions found: {len(all_entity_matches)}")
    log(f"  Documents with >=1 entity:   {entity_hit_docs}")

    # ── Build Entity Registry ─────────────────────────────────────────────────
    log("\nStep 5: Building entity registry...")
    entity_map, by_category = build_entity_registry(all_entity_matches)

    # ── Compile Statistics for Reports ────────────────────────────────────────
    log("\nStep 6: Compiling statistics...")

    # Entity stats per category
    cat_stats = {}
    for cat, recs in by_category.items():
        cat_stats[cat] = {
            "entity_count":      len(recs),
            "total_occurrences": sum(r["occurrence_count"] for r in recs),
            "avg_confidence":    round(sum(r["avg_confidence"] for r in recs) / len(recs), 3) if recs else 0,
            "top_entities":      [{"id": r["entity_id"], "name": r["entity_name"], "count": r["occurrence_count"]} for r in recs[:5]],
        }

    # Entity confidence distribution
    conf_dist = {"high_1.0": 0, "high_0.85": 0, "medium_0.60": 0}
    for m in all_entity_matches:
        if m["confidence"] == 1.0:
            conf_dist["high_1.0"] += 1
        elif m["confidence"] == 0.85:
            conf_dist["high_0.85"] += 1
        else:
            conf_dist["medium_0.60"] += 1

    # Save aggregated stats
    stats_obj = {
        "run_ts":             RUN_TS,
        "normalization":      dict(norm_stats),
        "entity_extraction": {
            "total_mentions":      len(all_entity_matches),
            "unique_entities":     len(entity_map),
            "documents_with_entities": entity_hit_docs,
            "confidence_distribution": conf_dist,
            "categories":          cat_stats,
        },
    }
    stats_obj["normalization"]["change_types"] = dict(norm_stats["change_types"])
    stats_obj["normalization"]["schema_fields_added"] = dict(norm_stats["schema_fields_added"])

    stats_path = os.path.join(BASE_DIR, "phase2b2_stats.json")
    with open(stats_path, "w", encoding="utf-8") as f:
        json.dump(stats_obj, f, ensure_ascii=False, indent=2)

    log(f"\nAll pipeline steps complete.")
    log(f"  Unique entities discovered: {len(entity_map)}")
    log(f"  Total entity mentions:      {len(all_entity_matches)}")
    return stats_obj, entity_map, by_category


if __name__ == "__main__":
    main()
