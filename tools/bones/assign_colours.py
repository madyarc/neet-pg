"""Choose one colour per bone type for an assembled region (e.g. the skull).

Usage: buildenv/bin/python -I neet-pg/tools/bones/assign_colours.py <models dir> <manifest name>

Palette: Paul Tol's "light" qualitative scheme (https://personal.sron.nl/~pault/), designed to stay
distinguishable with colour-vision deficiency and light enough for dark labels on top. Its pale grey is left out
(it reads as "unselected"), leaving 8 colours, so with more bone types than colours some types share:
  1. bones that touch (contact from `bones build`) never share a colour;
  2. among the valid assignments, the one where same-coloured bones are farthest apart is chosen;
  3. left and right members of a pair (e.g. parietal_r / parietal_l) are one type, one colour.
The page names the bones on the model, so identification never depends on matching a colour to the legend.
"""
import sys, json, random, itertools
import numpy as np

TOL_LIGHT = ['#77AADD', '#EE8866', '#EEDD88', '#FFAABB', '#99DDFF', '#44BB99', '#BBCC33', '#AAAA00']

d, name = sys.argv[1], sys.argv[2]
man = json.load(open(f'{d}/{name}.json'))
typ = lambda k: k.rsplit('_', 1)[0] if k.endswith(('_r', '_l')) else k
types = sorted({typ(p['key']) for p in man['parts']})
cen, size = {}, {}
for t in types:
    bb = [p['bbox'] for p in man['parts'] if typ(p['key']) == t]
    cen[t] = np.mean([(np.array(b[0]) + np.array(b[1])) / 2 for b in bb], 0)
    size[t] = max(np.linalg.norm(np.array(b[1]) - np.array(b[0])) for b in bb)
adj = {t: set() for t in types}
for c in man['contacts']:
    a, b = typ(c['a']), typ(c['b'])
    if a != b and min(c['na'], c['nb']) >= 3: adj[a].add(b); adj[b].add(a)

def quality(assign):
    """smallest centre-to-centre distance (mm) between two different types that share a colour"""
    worst = 1e9
    for a, b in itertools.combinations(types, 2):
        if assign[a] == assign[b]: worst = min(worst, float(np.linalg.norm(cen[a] - cen[b])))
    return worst

random.seed(7)
best, bq = None, -1
order = sorted(types, key=lambda t: (-len(adj[t]), -size[t]))
for attempt in range(20000):
    assign, ok = {}, True
    for t in order:
        options = [c for c in TOL_LIGHT if all(assign.get(n) != c for n in adj[t])]
        if not options: ok = False; break
        unused = [c for c in options if c not in assign.values()]
        if unused: assign[t] = random.choice(unused)
        else:
            far = lambda c: min(np.linalg.norm(cen[t] - cen[u]) for u, cu in assign.items() if cu == c)
            options.sort(key=far, reverse=True)
            assign[t] = options[0] if random.random() < .8 else random.choice(options)
    if ok:
        q = quality(assign)
        if q > bq: best, bq = assign, q
print(json.dumps(best, indent=1))
print(f'{len(types)} types, {len(TOL_LIGHT)} colours; neighbours never share; closest same-colour pair {bq:.0f} mm apart:')
for a, b in itertools.combinations(types, 2):
    if best[a] == best[b]: print(f'   {a} + {b}: {np.linalg.norm(cen[a] - cen[b]):.0f} mm')
