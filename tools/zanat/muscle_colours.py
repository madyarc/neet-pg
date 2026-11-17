"""Give each muscle of a built group a colour from Paul Tol's "muted" palette so that muscles that touch
(any vertices within D mm) never share one. usage: muscle_colours.py manifest.json out.json [D=2]"""
import sys, os, json, numpy as np
sys.path.insert(0, os.path.dirname(__file__))
from areas import decode
PAL = ['#CC6677', '#332288', '#DDCC77', '#117733', '#88CCEE', '#882255', '#44AA99', '#999933', '#AA4499']
man = json.load(open(sys.argv[1])); base = os.path.dirname(sys.argv[1]); D = float(sys.argv[3]) if len(sys.argv) > 3 else 2.0
cfgp = [p for p in man['parts']]
mus = [p for p in cfgp if p.get('group', 'muscle') == 'muscle'] if 'group' in cfgp[0] else None
keys = [p['key'] for p in (mus or cfgp)]
only = set(json.load(open(os.environ['KEYS']))) if os.environ.get('KEYS') else None
if only: keys = [k for k in keys if k in only]
P = {k: decode(os.path.join(base, k + '.bin'))[0] for k in keys}
box = {k: (v.min(0) - D, v.max(0) + D) for k, v in P.items()}
adj = {k: set() for k in keys}
for i, a in enumerate(keys):
    for b in keys[i + 1:]:
        if np.any(box[a][1] < box[b][0]) or np.any(box[b][1] < box[a][0]): continue
        A, B = P[a], P[b]
        # sample A against grid of B
        cell = {}
        for j, c in enumerate(map(tuple, np.floor(B / D).astype(int))): cell.setdefault(c, []).append(j)
        hit = False
        for p in A:
            c = np.floor(p / D).astype(int)
            ids = [j for dx in (-1, 0, 1) for dy in (-1, 0, 1) for dz in (-1, 0, 1) for j in cell.get((c[0]+dx, c[1]+dy, c[2]+dz), ())]
            if ids and ((B[ids] - p) ** 2).sum(1).min() <= D * D: hit = True; break
        if hit: adj[a].add(b); adj[b].add(a)
col = {}
for k in sorted(keys, key=lambda k: -len(adj[k])):
    used = {col[n] for n in adj[k] if n in col}
    free = [c for c in PAL if c not in used]
    col[k] = free[0] if free else PAL[0]
    if not free: print('no free colour for', k, file=sys.stderr)
json.dump({'palette': 'Paul Tol muted', 'touch_mm': D, 'colours': col, 'touching': {k: sorted(v) for k, v in adj.items()}}, open(sys.argv[2], 'w'), indent=0)
print(len(keys), 'muscles; max neighbours', max(len(v) for v in adj.values()))
