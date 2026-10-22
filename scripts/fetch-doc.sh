#!/usr/bin/env bash
# Downloads the latest WTL rulebook Google Doc and diffs it against the last-synced snapshot.
#   sources/rulebook.txt         last version the page was synced to (committed)
#   sources/rulebook.latest.txt  freshly downloaded text (gitignored)
#   sources/rulebook.latest.html freshly downloaded HTML, used for hyperlinks (gitignored)
# Exit code: 0 = no changes, 1 = doc changed, 2 = download failed.
set -uo pipefail
cd "$(dirname "$0")/.."
DOC_ID="1Qu6pscRUl_iEMHQSeYPh40HkourK8NhKNg7LbW2ugCQ"
BASE="https://docs.google.com/document/d/$DOC_ID/export"

curl -sfL -o sources/rulebook.latest.raw "$BASE?format=txt" || { echo "Download failed (is the doc still shared publicly?)"; exit 2; }
curl -sfL -o sources/rulebook.latest.html "$BASE?format=html" || { echo "HTML download failed"; exit 2; }
# Normalise: strip BOM and CRLF so diffs are clean
tr -d '\r' < sources/rulebook.latest.raw | sed '1s/^\xEF\xBB\xBF//' > sources/rulebook.latest.txt
rm -f sources/rulebook.latest.raw

if diff -q sources/rulebook.txt sources/rulebook.latest.txt >/dev/null; then
  echo "No changes since last sync."
  exit 0
fi
echo "Doc changed since last sync:"
diff -u sources/rulebook.txt sources/rulebook.latest.txt
exit 1
