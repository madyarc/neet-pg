"""Put a bone's JSON into its page: replaces the body of <script type="application/json" id="mesh">.
Usage: python3 -I embed.py <bone.json> <page.html>"""
import sys, re, json
data = json.load(open(sys.argv[1]))
page = open(sys.argv[2], encoding='utf-8').read()
blob = json.dumps(data, separators=(',', ':'))
new, n = re.subn(r'(<script type="application/json" id="mesh">)(.*?)(</script>)',
                 lambda m: m.group(1) + blob + m.group(3), page, flags=re.S)
assert n == 1, 'mesh script tag not found exactly once'
open(sys.argv[2], 'w', encoding='utf-8').write(new)
print(f'embedded {len(blob)/1024:.1f} KB into {sys.argv[2]}')
