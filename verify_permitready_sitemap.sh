#!/usr/bin/env bash
set -euo pipefail

SITEMAP="sitemap.xml"
BASE="https://techsmog.com"

required=(
  "$BASE/permitready/"
  "$BASE/permitready/privacy.html"
  "$BASE/permitready/terms.html"
  "$BASE/permitready/states/massachusetts/"
  "$BASE/permitready/states/california/"
  "$BASE/permitready/states/texas/"
  "$BASE/permitready/states/florida/"
  "$BASE/permitready/states/new-york/"
  "$BASE/permitready/states/pennsylvania/"
  "$BASE/permitready/states/illinois/"
  "$BASE/permitready/states/ohio/"
  "$BASE/permitready/states/north-carolina/"
  "$BASE/permitready/states/michigan/"
  "$BASE/permitready/states/georgia/"
  "$BASE/permitready/states/new-jersey/"
  "$BASE/permitready/states/virginia/"
  "$BASE/permitready/states/maryland/"
  "$BASE/permitready/states/missouri/"
  "$BASE/permitready/states/indiana/"
  "$BASE/permitready/states/tennessee/"
  "$BASE/permitready/states/washington/"
  "$BASE/permitready/states/arizona/"
)

missing=0
for url in "${required[@]}"; do
  if ! grep -Fq "<loc>${url}</loc>" "$SITEMAP"; then
    echo "MISSING: $url"
    missing=1
  fi
done

if ! grep -Fq 'Sitemap: https://techsmog.com/sitemap.xml' robots.txt; then
  echo 'MISSING: robots.txt sitemap declaration'
  missing=1
fi

python - <<'PY'
import xml.etree.ElementTree as ET
ET.parse('sitemap.xml')
print('XML parse: OK')
PY

if [[ "$missing" -ne 0 ]]; then
  echo 'Verification failed.'
  exit 1
fi

echo 'Verification passed: all required PermitReady URLs and robots sitemap declaration are present.'
