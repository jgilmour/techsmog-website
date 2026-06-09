#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT_DIR"

python3 - <<'PY'
import json
import xml.etree.ElementTree as ET
from pathlib import Path

base = "https://techsmog.com"
states = json.loads(Path("permitready/data/states.json").read_text())
required = [
    f"{base}/permitready/",
    f"{base}/permitready/privacy.html",
    f"{base}/permitready/terms.html",
]
required.extend(f"{base}/permitready/states/{state['slug']}/" for state in states)

tree = ET.parse("sitemap.xml")
ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
locs = {elem.text for elem in tree.findall(".//sm:loc", ns)}

missing = [url for url in required if url not in locs]
if missing:
    for url in missing:
        print(f"MISSING: {url}")
    raise SystemExit("Verification failed.")

robots = Path("robots.txt").read_text()
for expected in (
    "Sitemap: https://techsmog.com/sitemap.xml",
    "Sitemap: https://techsmog.com/llms.txt",
):
    if expected not in robots:
        raise SystemExit(f"Verification failed: missing robots.txt reference: {expected}")

print("XML parse: OK")
print("Verification passed: all required PermitReady URLs and robots sitemap declarations are present.")
PY
