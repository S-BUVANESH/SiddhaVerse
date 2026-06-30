"""
Diagnostic: dump 200 lines of raw HTML starting from the first Tamil character
to understand Project Madurai's actual verse markup structure.
"""
import urllib.request, sys, re

URLS = [
    "https://www.projectmadurai.org/pm_etexts/utf8/pmuni0004.html",
    "https://www.projectmadurai.org/pm_etexts/utf8/pmuni0269.html",
]

TAMIL_RE = re.compile(r"[\u0B80-\u0BFF]")

for url in URLS:
    print("\n" + "="*70)
    print("URL:", url)
    print("="*70)
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        raw = resp.read().decode("utf-8", errors="replace")

    lines = raw.splitlines()
    # find first line with Tamil content
    start = 0
    for i, ln in enumerate(lines):
        if TAMIL_RE.search(ln):
            start = max(0, i - 5)
            break

    # print 150 lines from that point
    for ln in lines[start : start + 150]:
        # safe ASCII repr for windows console
        safe = ln.encode("ascii", errors="replace").decode("ascii")
        print(safe)
