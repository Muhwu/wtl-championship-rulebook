#!/usr/bin/env python3
"""Checks src/page.html against a rulebook text export.

- every [x.y.z] rule ID in the doc has a matching <span class="rid">x.y.z</span> on the page
- every rule ID on the page still exists in the doc
- lists the doc's hyperlinks (from the HTML export) so they can be checked against the page

Usage: python3 -I scripts/check-rules.py [sources/rulebook.latest.txt]
"""
import html
import os
import re
import sys

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
txt = sys.argv[1] if len(sys.argv) > 1 else os.path.join(root, "sources", "rulebook.latest.txt")
doc = open(txt, encoding="utf-8-sig").read()
page = open(os.path.join(root, "src", "page.html"), encoding="utf-8").read()

doc_ids = set(re.findall(r"\[(\d+(?:\.\d+)+)\]", doc))
page_ids = set(re.findall(r'<span class="rid">([\d.]+)</span>', page))
missing = sorted(i for i in doc_ids if i not in page_ids)
stale = sorted(i for i in page_ids if f"[{i}]" not in doc)
print(f"Rule IDs: {len(doc_ids)} in doc, {len(page_ids)} on page")
print("Missing from page:", missing or "none")
print("On page but not in doc:", stale or "none")

html_path = os.path.splitext(txt)[0] + ".html"
if os.path.exists(html_path):
    src = open(html_path, encoding="utf-8").read()
    print("\nDoc hyperlinks:")
    for m in re.finditer(r'<a [^>]*href="([^"]+)"[^>]*>(.*?)</a>', src):
        text = html.unescape(re.sub("<[^>]+>", "", m.group(2)))
        url = html.unescape(m.group(1))
        url = re.sub(r"^https://www\.google\.com/url\?q=([^&]+)&.*", r"\1", url).replace("%3D", "=")
        on_page = "on page" if url.split("?")[0].rstrip("/") in page else "NOT ON PAGE"
        print(f"  {text!r:24} {url}  [{on_page}]")

sys.exit(1 if missing or stale else 0)
