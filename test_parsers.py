"""
Quick parse test: fetch one Thirumandiram and one Sivavakkiyam page,
run through the new parsers, and print the first 5 verses.
"""
import sys, os
sys.path.insert(0, r"d:\Siddha_Wisdom")
from execute_real_acquisition import (
    fetch_url, extract_thirumandiram_verses, extract_sivavakkiyam_verses
)

TM_URL = "https://www.projectmadurai.org/pm_etexts/utf8/pmuni0004.html"
SV_URL = "https://www.projectmadurai.org/pm_etexts/utf8/pmuni0269.html"

TM_SRC = {"url": TM_URL, "work": "Thirumandiram", "collection": "Tantirams 1-2"}
SV_SRC = {"url": SV_URL, "work": "Sivavakkiyam",  "collection": "Sivavakkiyam (Complete)"}

print("=== THIRUMANDIRAM ===")
html = fetch_url(TM_URL)
if html:
    verses = extract_thirumandiram_verses(html, TM_SRC)
    print(f"Total parsed: {len(verses)}")
    for v in verses[:5]:
        print(f"\n--- Verse {v['verse_number']} ---")
        print(v['verse_text'][:200].encode("ascii","replace").decode())
else:
    print("FAILED to fetch")

print("\n\n=== SIVAVAKKIYAM ===")
html = fetch_url(SV_URL)
if html:
    verses = extract_sivavakkiyam_verses(html, SV_SRC)
    print(f"Total parsed: {len(verses)}")
    for v in verses[:5]:
        print(f"\n--- Verse {v['verse_number']} ---")
        print(v['verse_text'][:200].encode("ascii","replace").decode())
else:
    print("FAILED to fetch")
