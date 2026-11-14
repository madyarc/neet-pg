"""Fill NMC domain (K/S/A/C) for rows where it is printed on a line next to the code."""
import json, re
d = json.load(open('cbme.json'))
raw = open(__import__('sys').argv[2] if len(__import__('sys').argv)>2 else 'cbme.txt').read().split('\n')
start = next(i for i, l in enumerate(raw) if re.match(r'^\s*AN1\.1\b', l))
def dom_in(line):
    for tok in re.split(r'\s{2,}', line.strip())[1:] if line.strip() else []:
        t = re.sub(r'\s*and\s*', '/', tok).replace(' ', '').upper()
        if re.fullmatch(r'[KSAC](?:[/,][KSAC])*', t): return t.replace(',', '/')
    m = re.match(r'^\s{20,}([KSAC](?:\s?[/,]\s?[KSAC])*)(\s{2,}|$)', line)
    return m.group(1).replace(' ', '').replace(',', '/') if m else None
left = 0
for s, ts in d.items():
    for t in ts:
        for it in t['items']:
            if it.get('domain'): continue
            pre, rest = re.match(r'([A-Z]+)(.*)', it['code']).groups()
            pat = re.compile(r'^\s*' + pre + r'\s?' + re.escape(rest) + r'\b')
            k = next((j for j in range(start, len(raw)) if pat.match(raw[j])), None)
            if k is None: left += 1; continue
            body = pat.sub('', raw[k], count=1).lstrip('*').strip()
            chunk = re.split(r'\s{2,}', body)[0] if body else ''
            g = re.search(r'\s([KSAC](?:\s?(?:/|,|and)\s?[KSAC])*)$', chunk)
            if g:
                dm = re.sub(r'\s*(?:and|,)\s*', '/', g.group(1)).replace(' ', '')
                it['domain'] = dm
                it['desc'] = it['desc'].replace(chunk, chunk[:g.start()].rstrip(), 1)
                continue
            for j in (k, k - 1, k + 1, k - 2, k + 2):
                dm = dom_in(raw[j])
                if dm: it['domain'] = dm; break
            else: left += 1; print('no domain', it['code'])
json.dump(d, open('cbme.json', 'w'), indent=1, ensure_ascii=False)
print('still missing', left)
