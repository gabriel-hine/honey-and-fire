#!/usr/bin/env python3
"""Stamp ?v=<version> onto local asset URLs in HTML files.

GitHub Pages serves with Cache-Control: max-age=600 and we can't override
the response header. Query-string versioning works around it: each deploy's
asset URLs become unique, so the browser treats them as fresh resources
instead of using its 10-minute-old cached copy.

Run this before every commit. It is idempotent — any existing ?v=… is
replaced with the current value.

Version source: git short hash of HEAD, falling back to a unix timestamp
if we're not in a repo.
"""
import re
import subprocess
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

try:
    version = subprocess.check_output(
        ["git", "rev-parse", "--short", "HEAD"],
        cwd=ROOT, text=True, stderr=subprocess.DEVNULL,
    ).strip()
except (subprocess.CalledProcessError, FileNotFoundError):
    version = str(int(time.time()))

# href="…" or src="…" pointing at any local asset (under assets/, images/, or
# root-level files like logo-dark.svg). External http(s) URLs are skipped via
# negative lookahead. An optional existing ?v=… is replaced.
pattern = re.compile(
    r'((?:href|src)=")'
    r'(?!https?://|//|mailto:|tel:|#)'
    r'((?:\./)?[^"?\s]+\.(?:css|js|svg|png|jpg|jpeg|webp|gif|ico|woff2?))'
    r'(?:\?v=[^"]*)?'
    r'"'
)

def stamp(text: str) -> str:
    return pattern.sub(lambda m: f'{m.group(1)}{m.group(2)}?v={version}"', text)

changed = []
# Walk root + every subdirectory so /en/index.html (and any future locale
# pages) stay in lockstep with the IT pages.
for path in sorted(ROOT.rglob("*.html")):
    # Skip vendor / build / .git assets if they ever appear
    if any(part in path.parts for part in (".git", "node_modules")):
        continue
    text = path.read_text()
    new = stamp(text)
    if new != text:
        path.write_text(new)
        changed.append(str(path.relative_to(ROOT)))

print(f"version: {version}")
print("updated: " + (", ".join(changed) if changed else "none"))
