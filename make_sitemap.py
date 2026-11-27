#!/usr/bin/env python3
"""
Sitemap generator for https://mr-avedia.github.io/Abdul-Qadir/

HOW TO USE
1. Put this file in your repo folder (the same folder as index.html).
2. Run:  python make_sitemap.py      (on Windows you can also try:  py make_sitemap.py)
3. It writes sitemap.xml next to it, listing every .html page (and PDFs).
4. Commit + push sitemap.xml, then submit it in Google Search Console as:  sitemap.xml

Re-run it whenever you add a new project page.
"""
import os, subprocess, datetime, urllib.parse
from xml.sax.saxutils import escape

BASE = "https://mr-avedia.github.io/Abdul-Qadir/"
INCLUDE_PDF = True                       # set False to leave PDFs (CVs) out
EXTRA_URLS = [BASE + "?mode=design"]     # the Design profile of the home page
SKIP_FILES = {"404.html"}                # pages that should not be in search
here = os.path.dirname(os.path.abspath(__file__))

def lastmod(path):
    try:                                  # real "last changed" date from git
        out = subprocess.run(["git", "log", "-1", "--format=%cs", "--", path],
                             cwd=here, capture_output=True, text=True).stdout.strip()
        if out:
            return out
    except Exception:
        pass
    return datetime.date.fromtimestamp(os.path.getmtime(path)).isoformat()

entries = []
for root, dirs, files in os.walk(here):
    dirs[:] = [d for d in dirs if not d.startswith((".", "_")) and d != "node_modules"]
    for f in sorted(files):
        low = f.lower()
        if low in SKIP_FILES or low.startswith(("google", "bingsiteauth")):
            continue
        if not (low.endswith(".html") or (INCLUDE_PDF and low.endswith(".pdf"))):
            continue
        full = os.path.join(root, f)
        rel = os.path.relpath(full, here).replace(os.sep, "/")
        url = BASE if rel == "index.html" else BASE + urllib.parse.quote(rel)
        entries.append((url, lastmod(full)))
        if rel == "index.html":
            entries.extend((u, lastmod(full)) for u in EXTRA_URLS)

entries.sort(key=lambda e: (e[0] != BASE, e[0]))      # home page first
xml = ['<?xml version="1.0" encoding="UTF-8"?>',
       '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
for url, lm in entries:
    xml.append("  <url>\n    <loc>%s</loc>\n    <lastmod>%s</lastmod>\n  </url>" % (escape(url), lm))
xml.append("</urlset>\n")
with open(os.path.join(here, "sitemap.xml"), "w", encoding="utf-8") as fh:
    fh.write("\n".join(xml))
print("Done: %d URLs written to sitemap.xml" % len(entries))
for u, _ in entries:
    print("  ", u)
