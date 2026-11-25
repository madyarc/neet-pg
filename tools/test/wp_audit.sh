#!/bin/sh
# Audit every Wikipedia article quoted in the fact sheets (WP-<Title> keys) for OpenStax / Boundless / Lumen citations.
# Fetches raw wikitext (paced, follows one redirect) into OUT, then lists articles that cite a banned source.
# usage: tools/test/wp_audit.sh OUTDIR   (run from the repo root; takes ~20 min for ~2700 articles; skips already-fetched)
OUT=${1:?outdir}; mkdir -p "$OUT"; UA="neet-pg-source-audit/1.0 (study notes; contact via GitHub repo)"
grep -oh "\*\*WP-[^*]*\*\*" sources-local/facts/*.md | sed 's/\*\*WP-\(.*\)\*\*/\1/' | sort -u > "$OUT/titles.txt"
enc() { python3 -I -c "import sys,urllib.parse;print(urllib.parse.quote(sys.argv[1].replace(' ','_')))" "$1"; }
while read a; do
  f="$OUT/$a.txt"; [ -s "$f" ] && continue
  curl -s -L --max-time 30 -A "$UA" "https://en.wikipedia.org/w/index.php?title=$(enc "$a")&action=raw" -o "$f"; sleep 2
  t=$(grep -o -i -m1 "^#redirect *\[\[[^]|#]*" "$f" | sed 's/^#[Rr][Ee][Dd][Ii][Rr][Ee][Cc][Tt] *\[\[//')
  [ -n "$t" ] && { curl -s -L --max-time 30 -A "$UA" "https://en.wikipedia.org/w/index.php?title=$(enc "$t")&action=raw" -o "$OUT/$a.target.txt"; sleep 2; }
done < "$OUT/titles.txt"
echo "empty (retry later): $(find "$OUT" -name '*.txt' ! -name titles.txt -size 0 | wc -l)"
grep -l -i "openstax\|cnx\.org\|boundless\.com\|lumenlearning\|courses\.lumen" "$OUT"/*.txt | sed 's#.*/##; s#\.target\.txt$##; s#\.txt$##' | sort -u | while read a; do
  echo "$a -> $(grep -c -F "**WP-$a**" sources-local/facts/*.md | awk -F: '$2>0{printf "%s(%s) ",$1,$2}' | sed 's#sources-local/facts/##g')"; done
