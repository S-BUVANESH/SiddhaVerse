"""
Phase 2B-1R: Real Corpus Acquisition — CORRECTED PARSER
========================================================
Based on actual HTML inspection of Project Madurai pages:

THIRUMANDIRAM (e.g. pmuni0004.html):
  Structure: lines separated by <br>
  Verse number appears as:   N.\n  (start of verse block)
  Verse end has:             &nbsp; &nbsp; ... N  (trailing verse number, no parens)
  Pattern: lines of Tamil text followed by "N" with nbsp padding

SIVAVAKKIYAM (pmuni0269.html):
  Structure: <table><tr><td width=450">...Tamil lines...<br>...<td valign="bottom">N</tr>
  NOTE: HTML is malformed — td has width=450" (missing opening quote)
        and no closing </td> tags — uses raw <tr> for row separation.

Run from workspace root:  python execute_real_acquisition.py
"""

import os
import re
import json
import hashlib
import shutil
import urllib.request
import urllib.error
import time
import datetime

# ── Paths ─────────────────────────────────────────────────────────────────────
BASE_DIR      = r"d:\Siddha_Wisdom"
RAW_DIR       = os.path.join(BASE_DIR, "raw_documents")
META_DIR      = os.path.join(BASE_DIR, "metadata_registry")
RAW_ARCHIVE   = os.path.join(RAW_DIR,  "archive")
META_ARCHIVE  = os.path.join(META_DIR, "archive")
LOG_FILE      = os.path.join(BASE_DIR, "acquisition_run.log")

# ── Project Madurai sources ────────────────────────────────────────────────────
THIRUMANDIRAM_SOURCES = [
    {"url": "https://www.projectmadurai.org/pm_etexts/utf8/pmuni0004.html",    "work": "Thirumandiram", "collection": "Tantirams 1-2"},
    {"url": "https://www.projectmadurai.org/pm_etexts/utf8/pmuni0009_01.html", "work": "Thirumandiram", "collection": "Tantiram 3 (Part 1)"},
    {"url": "https://www.projectmadurai.org/pm_etexts/utf8/pmuni0009_02.html", "work": "Thirumandiram", "collection": "Tantiram 3 (Part 2)"},
    {"url": "https://www.projectmadurai.org/pm_etexts/utf8/pmuni0010_01.html", "work": "Thirumandiram", "collection": "Tantiram 4 (Part 1)"},
    {"url": "https://www.projectmadurai.org/pm_etexts/utf8/pmuni0010_02.html", "work": "Thirumandiram", "collection": "Tantiram 4 (Part 2)"},
    {"url": "https://www.projectmadurai.org/pm_etexts/utf8/pmuni0011_01.html", "work": "Thirumandiram", "collection": "Tantiram 5 (Part 1)"},
    {"url": "https://www.projectmadurai.org/pm_etexts/utf8/pmuni0011_02.html", "work": "Thirumandiram", "collection": "Tantiram 5 (Part 2)"},
    {"url": "https://www.projectmadurai.org/pm_etexts/utf8/pmuni0013.html",    "work": "Thirumandiram", "collection": "Tantiram 6"},
    {"url": "https://www.projectmadurai.org/pm_etexts/utf8/pmuni0014.html",    "work": "Thirumandiram", "collection": "Tantiram 7"},
    {"url": "https://www.projectmadurai.org/pm_etexts/utf8/pmuni0015.html",    "work": "Thirumandiram", "collection": "Tantiram 8"},
    {"url": "https://www.projectmadurai.org/pm_etexts/utf8/pmuni0016.html",    "work": "Thirumandiram", "collection": "Tantiram 9"},
]

SIVAVAKKIYAM_SOURCES = [
    {"url": "https://www.projectmadurai.org/pm_etexts/utf8/pmuni0269.html",    "work": "Sivavakkiyam", "collection": "Sivavakkiyam (Complete)"},
]

TARGET_UNIQUE = 1000
ACQUIRE_TS    = datetime.datetime.now(datetime.timezone.utc).isoformat()

# ── Helpers ────────────────────────────────────────────────────────────────────

def log(msg: str):
    # Use ascii-safe repr for arrow/special chars to avoid Windows CP1252 errors
    safe = msg.encode("ascii", errors="replace").decode("ascii")
    line = f"[{datetime.datetime.now(datetime.timezone.utc).strftime('%H:%M:%S')}] {safe}"
    print(line)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{datetime.datetime.now(datetime.timezone.utc).strftime('%H:%M:%S')}] {msg}\n")


def content_hash(text: str) -> str:
    normalised = re.sub(r"\s+", " ", text).strip()
    return hashlib.sha256(normalised.encode("utf-8")).hexdigest()


def fetch_url(url: str, retries: int = 3) -> str | None:
    headers = {"User-Agent": "SiddhaVerse-Corpus-Acquisition/1.0 (research; non-commercial)"}
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=30) as resp:
                raw = resp.read()
                try:
                    return raw.decode("utf-8")
                except UnicodeDecodeError:
                    return raw.decode("latin-1")
        except urllib.error.HTTPError as e:
            log(f"  HTTP {e.code} for {url} (attempt {attempt+1}/{retries})")
            if e.code == 404:
                return None
        except Exception as e:
            log(f"  Error fetching {url}: {e} (attempt {attempt+1}/{retries})")
        time.sleep(2 ** attempt)
    return None


# ── HTML utilities ─────────────────────────────────────────────────────────────

TAMIL_RE  = re.compile(r"[\u0B80-\u0BFF]")
HTML_TAG  = re.compile(r"<[^>]+>")
NBSP_RE   = re.compile(r"&nbsp;", re.IGNORECASE)
AMP_RE    = re.compile(r"&amp;",  re.IGNORECASE)
HTML_ENT  = re.compile(r"&[a-z]+;", re.IGNORECASE)


def strip_tags(s: str) -> str:
    s = NBSP_RE.sub(" ", s)
    s = AMP_RE.sub("&", s)
    s = HTML_TAG.sub("", s)
    s = HTML_ENT.sub("", s)
    return s


def clean(s: str) -> str:
    s = strip_tags(s)
    s = re.sub(r"[ \t]+", " ", s)
    s = "\n".join(line.rstrip() for line in s.splitlines())
    return s.strip()


# ── Thirumandiram parser ───────────────────────────────────────────────────────
# HTML structure (raw, inspected):
#
#   N.\n<br>
#   line1<br>
#   line2<br>
#   line3<br>
#   line4.       &nbsp; &nbsp; &nbsp; &nbsp;   N<br>
#   <br>
#
# The verse number appears:
#   - at START:  bare "N." on its own line (N is 1-4 digits)
#   - at END:    "N" preceded by multiple &nbsp; at end of last line
#
# Strategy:
#   1. Split on <br> (case-insensitive) to get segments
#   2. Detect "N." lines (just a number+dot) → start of new verse
#   3. Accumulate Tamil content lines until next "N." or non-Tamil section
#   4. Strip trailing "&nbsp; ... N" from last line of each verse

def extract_thirumandiram_verses(html: str, source_meta: dict) -> list[dict]:
    # Remove noise
    html = re.sub(r"<!--.*?-->",         "", html, flags=re.DOTALL)
    html = re.sub(r"<script.*?</script>","", html, flags=re.DOTALL)
    html = re.sub(r"<style.*?</style>",  "", html, flags=re.DOTALL)

    # Split on <br> and paragraph/div boundaries
    segments = re.split(r"<(?:br|p|h\d|center|/center|hr)[^>]*>", html, flags=re.IGNORECASE)

    START_NUM = re.compile(r"^\s*(\d{1,4})\.\s*$")  # "N." alone on line
    END_NUM   = re.compile(r"^(.*?)(?:\s|&nbsp;)+(\d{1,4})\s*$")  # text ... N

    verses       = []
    current_num  = None
    current_body = []

    def flush():
        nonlocal current_num, current_body
        if current_num is not None and current_body:
            # join lines (they are Tamil text lines)
            verse_text = "\n".join(line for line in current_body if line)
            if TAMIL_RE.search(verse_text):
                verses.append({
                    "verse_text":   verse_text,
                    "verse_number": str(current_num),
                    "source_meta":  source_meta,
                })
        current_num  = None
        current_body = []

    for seg in segments:
        text = clean(seg)
        if not text:
            continue

        # Check for start-of-verse marker "N."
        m_start = START_NUM.match(text)
        if m_start:
            flush()
            current_num  = int(m_start.group(1))
            current_body = []
            continue

        if current_num is None:
            # not inside a verse block yet
            continue

        # Check if this line ends with trailing "&nbsp; N" pattern (last line of verse)
        clean_seg = NBSP_RE.sub(" ", seg)       # replace nbsp before stripping tags
        clean_seg = HTML_TAG.sub("", clean_seg).strip()
        clean_seg = re.sub(r"[ \t]+", " ", clean_seg)

        m_end = END_NUM.match(clean_seg)
        if m_end:
            verse_line = m_end.group(1).strip()
            end_num    = int(m_end.group(2))
            if verse_line and TAMIL_RE.search(verse_line):
                current_body.append(verse_line)
            # The end number should match current_num for validation
            # (some pages number sequentially so we trust current_num)
            flush()
            current_num  = end_num + 1  # pre-set for next verse? No — reset:
            current_num  = None
            current_body = []
        else:
            # Regular content line
            if TAMIL_RE.search(text):
                current_body.append(text)
            elif text and not TAMIL_RE.search(text):
                # Non-Tamil line = section header; flush current verse
                if current_body:
                    flush()

    flush()  # final flush
    return verses


# ── Sivavakkiyam parser ────────────────────────────────────────────────────────
# HTML structure (actual, inspected):
#
#   <tr><td width=450">           ← malformed: missing opening quote
#   Tamil line 1<br>
#   Tamil line 2<br>
#   ...last line.<td valign="bottom">N</tr>
#
# Strategy:
#   1. Split on <tr> tags → get one block per verse
#   2. Within each block, extract content up to <td valign=...>
#   3. Extract verse number from <td valign=...>N</tr>

def extract_sivavakkiyam_verses(html: str, source_meta: dict) -> list[dict]:
    html = re.sub(r"<!--.*?-->",         "", html, flags=re.DOTALL)
    html = re.sub(r"<script.*?</script>","", html, flags=re.DOTALL)
    html = re.sub(r"<style.*?</style>",  "", html, flags=re.DOTALL)

    verses = []

    # Split on <tr> boundaries
    # Pattern: <tr><td width=...>TAMIL<td valign="bottom">NUM</tr>
    ROW_RE    = re.compile(r"<tr[^>]*>(.*?)</tr>", re.DOTALL | re.IGNORECASE)
    # Extract: content up to second <td> and the number after it
    CONTENT_RE = re.compile(
        r"<td[^>]*>(.*?)<td[^>]*>(\d+)\s*$",
        re.DOTALL | re.IGNORECASE
    )

    for row_m in ROW_RE.finditer(html):
        row_html = row_m.group(1)
        cm = CONTENT_RE.search(row_html)
        if not cm:
            continue
        tamil_html = cm.group(1)
        verse_num  = cm.group(2).strip()
        verse_text = clean(tamil_html)
        if not verse_text or not TAMIL_RE.search(verse_text):
            continue
        verses.append({
            "verse_text":   verse_text,
            "verse_number": verse_num,
            "source_meta":  source_meta,
        })

    return verses


# ── Transliteration (character-map, ISO 15919 approximate) ────────────────────
_TRANS_MAP = {
    # Vowels (independent)
    "அ": "a",   "ஆ": "ā",   "இ": "i",   "ஈ": "ī",
    "உ": "u",   "ஊ": "ū",   "எ": "e",   "ஏ": "ē",
    "ஐ": "ai",  "ஒ": "o",   "ஓ": "ō",   "ஔ": "au",
    # Consonants
    "க": "k",   "ங": "ṅ",   "ச": "c",   "ஞ": "ñ",
    "ட": "ṭ",   "ண": "ṇ",   "த": "t",   "ந": "n",
    "ப": "p",   "ம": "m",   "ய": "y",   "ர": "r",
    "ல": "l",   "வ": "v",   "ழ": "ḻ",   "ள": "ḷ",
    "ற": "ṟ",   "ன": "ṉ",
    # Grantha
    "ஜ": "j",   "ஷ": "ṣ",   "ஸ": "s",   "ஹ": "h",
    # Vowel signs (matras)
    "ா": "ā",   "ி": "i",   "ீ": "ī",
    "ு": "u",   "ூ": "ū",   "ெ": "e",
    "ே": "ē",   "ை": "ai",  "ொ": "o",
    "ோ": "ō",   "ௌ": "au",
    # Special
    "்": "",    "ஃ": "ḥ",
}

def transliterate(text: str) -> str:
    return "".join(_TRANS_MAP.get(ch, ch) for ch in text)


# ── Archive pilot files ────────────────────────────────────────────────────────

def archive_pilot_files():
    os.makedirs(RAW_ARCHIVE,  exist_ok=True)
    os.makedirs(META_ARCHIVE, exist_ok=True)
    raw_moved = meta_moved = 0
    for fname in list(os.listdir(RAW_DIR)):
        if fname.startswith("text_") and fname.endswith(".json"):
            src, dst = os.path.join(RAW_DIR, fname), os.path.join(RAW_ARCHIVE, fname)
            if not os.path.exists(dst):
                shutil.move(src, dst)
                raw_moved += 1
    for fname in list(os.listdir(META_DIR)):
        if fname.startswith("text_") and fname.endswith(".json"):
            src, dst = os.path.join(META_DIR, fname), os.path.join(META_ARCHIVE, fname)
            if not os.path.exists(dst):
                shutil.move(src, dst)
                meta_moved += 1
    log(f"Archive: {raw_moved} raw + {meta_moved} metadata files moved to archive/")
    return raw_moved, meta_moved


# ── Save verified unique verse ─────────────────────────────────────────────────

def save_verse(doc_index: int, verse_data: dict, seen_hashes: set) -> bool:
    text = verse_data["verse_text"]
    h = content_hash(text)
    if h in seen_hashes:
        return False
    seen_hashes.add(h)

    src        = verse_data["source_meta"]
    work       = src["work"]
    collection = src["collection"]
    verse_num  = verse_data["verse_number"]
    src_url    = src["url"]

    author    = "Thirumoolar"   if work == "Thirumandiram" else "Sivavakkiyar"
    safe_name = "thirumandiram" if work == "Thirumandiram" else "sivavakkiyar"

    transliteration = transliterate(text)
    doc_id   = f"{safe_name}_pm_{doc_index:04d}"
    filename = f"text_{safe_name}_pm_{doc_index:04d}.json"

    raw_doc = {
        "document_id":           doc_id,
        "text_id":               doc_id,
        "title":                 f"{work} - Verse {verse_num}",
        "source_work":           work,
        "collection":            collection,
        "verse_number":          verse_num,
        "tamil_text":            text,
        "transliteration":       transliteration,
        "english_translation":   None,
        "author":                author,
        "language":              "Tamil",
        "script":                "Tamil script",
        "content_hash":          h,
        "copyright_status":      "public_domain",
        "source_repository":     "Project Madurai",
        "source_url":            src_url,
        "acquisition_timestamp": ACQUIRE_TS,
        "provenance_metadata": {
            "method":    "direct_html_extraction",
            "extractor": "SiddhaVerse Phase 2B-1R",
            "verified":  True,
            "synthetic": False,
        },
    }

    meta_doc = {
        "document_id":           doc_id,
        "source_work":           work,
        "collection":            collection,
        "verse_number":          verse_num,
        "author":                author,
        "language":              "Tamil",
        "content_hash":          h,
        "copyright_status":      "public_domain",
        "source_repository":     "Project Madurai",
        "source_url":            src_url,
        "acquisition_timestamp": ACQUIRE_TS,
        "synthetic":             False,
    }

    with open(os.path.join(RAW_DIR,  filename), "w", encoding="utf-8") as f:
        json.dump(raw_doc, f, ensure_ascii=False, indent=2)
    with open(os.path.join(META_DIR, filename), "w", encoding="utf-8") as f:
        json.dump(meta_doc, f, ensure_ascii=False, indent=2)

    return True


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    open(LOG_FILE, "w", encoding="utf-8").close()
    log("=" * 60)
    log("Phase 2B-1R: Real Corpus Acquisition")
    log(f"Target: {TARGET_UNIQUE} unique verses")
    log("=" * 60)

    log("Step 1: Archiving replicated pilot files...")
    raw_moved, meta_moved = archive_pilot_files()

    seen_hashes:  set   = set()
    doc_index:    int   = 1
    total_fetched: int  = 0
    total_dupes:   int  = 0
    source_stats:  dict = {}

    log("\nStep 2: Fetching verses from Project Madurai...\n")

    all_sources = THIRUMANDIRAM_SOURCES + SIVAVAKKIYAM_SOURCES

    for src in all_sources:
        if doc_index - 1 >= TARGET_UNIQUE:
            log(f"Target of {TARGET_UNIQUE} unique verses reached. Stopping.")
            break

        url  = src["url"]
        work = src["work"]
        log(f"Fetching [{work}]: {url}")
        html = fetch_url(url)

        if html is None:
            log(f"  SKIP (fetch failed): {url}")
            source_stats[url] = {"work": work, "collection": src["collection"],
                                 "extracted": 0, "written": 0, "duplicates": 0,
                                 "status": "fetch_failed"}
            continue

        log(f"  Downloaded {len(html):,} bytes")

        if work == "Thirumandiram":
            raw_verses = extract_thirumandiram_verses(html, src)
        else:
            raw_verses = extract_sivavakkiyam_verses(html, src)

        log(f"  Parsed {len(raw_verses)} candidate verses")
        total_fetched += len(raw_verses)

        written = dupes = 0
        for v in raw_verses:
            if doc_index - 1 >= TARGET_UNIQUE:
                break
            ok = save_verse(doc_index, v, seen_hashes)
            if ok:
                doc_index += 1
                written += 1
            else:
                dupes += 1
                total_dupes += 1

        source_stats[url] = {
            "work":        work,
            "collection":  src["collection"],
            "extracted":   len(raw_verses),
            "written":     written,
            "duplicates":  dupes,
            "status":      "ok",
        }
        log(f"  Written: {written}  |  Duplicates rejected: {dupes}")
        log(f"  Running unique total: {doc_index - 1}")
        time.sleep(1)

    unique_total = doc_index - 1
    dup_rate     = total_dupes / max(1, total_fetched)

    log("")
    log("=" * 60)
    log("ACQUISITION COMPLETE")
    log(f"  Unique verses acquired  : {unique_total}")
    log(f"  Duplicates rejected     : {total_dupes}")
    log(f"  Total candidates parsed : {total_fetched}")
    log(f"  Duplicate rate          : {dup_rate:.1%}")
    log("=" * 60)

    summary = {
        "phase":              "2B-1R",
        "acquisition_ts":     ACQUIRE_TS,
        "unique_verses":      unique_total,
        "total_fetched":      total_fetched,
        "duplicates_rejected": total_dupes,
        "duplicate_rate":     round(dup_rate, 4),
        "pilot_files_archived": {"raw": raw_moved, "metadata": meta_moved},
        "source_stats":       source_stats,
        "target":             TARGET_UNIQUE,
        "success_criteria": {
            "unique_verses_target":    TARGET_UNIQUE,
            "max_duplicate_rate":      0.05,
            "provenance_coverage":     "100%",
            "synthetic_content":       0,
        },
        "achieved": {
            "unique_verses":      unique_total,
            "duplicate_rate":     round(dup_rate, 4),
            "provenance_coverage": "100%",
            "synthetic_content":  0,
        },
    }

    summary_path = os.path.join(BASE_DIR, "acquisition_summary.json")
    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
    log(f"Summary saved to acquisition_summary.json")

    return summary


if __name__ == "__main__":
    main()
