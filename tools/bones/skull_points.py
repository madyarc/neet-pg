"""Named sutures and craniometric points for the assembled skull, from the contacts found by `bones build`.

Usage (from ~/personal): buildenv/bin/python -I neet-pg/tools/bones/skull_points.py neet-pg/anatomy/models/skull [check.png]
Writes <dir>/skull-points.json:
  sutures: {key: {name, bones, parts: {partKey: [vertex ids]}}}   (outer-surface vertices only)
  points:  {key: {name, p: [x,y,z], part}}

Definitions (Gray's Anatomy 1918, "The Exterior of the Skull"; checked against Wikipedia):
  coronal = frontal-parietals; sagittal = between the parietals; lambdoid = parietals-occipital;
  squamosal + parietomastoid = temporal-parietal (the model does not separate the two, so they are drawn together);
  occipitomastoid = occipital-mastoid part of temporal; sphenoparietal = greater wing of sphenoid-parietal;
  sphenofrontal = sphenoid-frontal (outer part); sphenosquamosal = sphenoid-temporal squama (outer part);
  frontonasal = frontal-nasals; internasal = between the nasal bones.
  bregma = junction of sagittal and coronal; lambda = junction of sagittal and lambdoid;
  asterion = meeting of parietomastoid, occipitomastoid and lambdoid; pterion = posterior end of the
  sphenoparietal suture; nasion = mid-point of the frontonasal suture; inion = external occipital protuberance.
"""
import sys, json, base64, struct
import numpy as np

d = sys.argv[1]
man = json.load(open(f'{d}/skull.json'))

def load(fn):
    b = open(f'{d}/{fn}', 'rb').read()
    assert b[:4] == b'NPM1'
    nv, nt = struct.unpack_from('<II', b, 4)
    lo = np.array(struct.unpack_from('<3f', b, 12)); span = struct.unpack_from('<f', b, 24)[0]
    ib = struct.unpack_from('<I', b, 28)[0]
    o = 32
    q = np.frombuffer(b, '<u2', nv * 3, o).reshape(-1, 3); o += nv * 6
    nrm = np.frombuffer(b, 'i1', nv * 3, o).reshape(-1, 3) / 127.0; o += nv * 3
    o = (o + 3) & ~3
    idx = np.frombuffer(b, '<u2' if ib == 2 else '<u4', nt * 3, o).reshape(-1, 3)
    return lo + q / 65535.0 * span, nrm, idx

P, N = {}, {}
for p in man['parts']:
    P[p['key']], N[p['key']], _ = load(p['file'])
C = {}
for c in man['contacts']:
    va = np.frombuffer(base64.b64decode(c['va']), '<u4'); vb = np.frombuffer(base64.b64decode(c['vb']), '<u4')
    C[(c['a'], c['b'])] = (va, vb); C[(c['b'], c['a'])] = (vb, va)

cranial = ['frontal', 'parietal_r', 'parietal_l', 'occipital', 'temporal_r', 'temporal_l', 'sphenoid', 'ethmoid']
centre = np.vstack([P[k] for k in cranial]).mean(0)
mid_x = (np.vstack([P['parietal_r'], P['parietal_l']])[:, 0]).mean()

def outer(key, verts):
    """keep vertices on the outside of the skull: normal pointing away from the cranial centre"""
    if len(verts) == 0: return verts
    p = P[key][verts]; n = N[key][verts]
    return verts[((p - centre) * n).sum(1) > 0]

def contact(a, b, outside=True):
    if (a, b) not in C: return {}
    va, vb = C[(a, b)]
    if outside: va, vb = outer(a, va), outer(b, vb)
    return {a: va, b: vb}

def merge(*dicts):
    out = {}
    for dd in dicts:
        for k, v in dd.items(): out[k] = np.union1d(out.get(k, np.array([], int)), v)
    return out

SUT = {
  'coronal':        ('Coronal suture', 'frontal and parietals', merge(contact('frontal', 'parietal_r'), contact('frontal', 'parietal_l'))),
  'sagittal':       ('Sagittal suture', 'between the two parietals', contact('parietal_r', 'parietal_l')),
  'lambdoid':       ('Lambdoid suture', 'parietals and occipital', merge(contact('parietal_r', 'occipital'), contact('parietal_l', 'occipital'))),
  'squamosal':      ('Squamosal and parietomastoid sutures', 'temporal and parietal', merge(contact('temporal_r', 'parietal_r'), contact('temporal_l', 'parietal_l'))),
  'occipitomastoid':('Occipitomastoid suture', 'occipital and mastoid part of the temporal', merge(contact('occipital', 'temporal_r'), contact('occipital', 'temporal_l'))),
  'sphenoparietal': ('Sphenoparietal suture', 'greater wing of the sphenoid and parietal', merge(contact('sphenoid', 'parietal_r'), contact('sphenoid', 'parietal_l'))),
  'sphenofrontal':  ('Sphenofrontal suture', 'sphenoid and frontal', contact('sphenoid', 'frontal')),
  'sphenosquamosal':('Sphenosquamosal suture', 'greater wing of the sphenoid and temporal squama', merge(contact('sphenoid', 'temporal_r'), contact('sphenoid', 'temporal_l'))),
  'frontonasal':    ('Frontonasal suture', 'frontal and nasals', merge(contact('frontal', 'nasal_r'), contact('frontal', 'nasal_l'))),
  'internasal':     ('Internasal suture', 'between the two nasal bones', contact('nasal_r', 'nasal_l')),
}

def near_all(key, others, r=4.0, outside=True):
    """vertices of `key` within r mm of every part in `others`"""
    pts = P[key]; ok = np.ones(len(pts), bool)
    for o in others:
        # distance from each vertex of key to nearest vertex of o (chunked)
        q = P[o]; best = np.full(len(pts), np.inf)
        for i in range(0, len(q), 4000):
            dd = np.linalg.norm(pts[:, None, :] - q[None, i:i + 4000, :], axis=2).min(1)
            best = np.minimum(best, dd)
        ok &= best < r
    idx = np.where(ok)[0]
    return outer(key, idx) if outside else idx

def point(key, verts, how='mean'):
    if len(verts) == 0: return None
    m = P[key][verts].mean(0)
    v = verts[np.argmin(np.linalg.norm(P[key][verts] - m, axis=1))]
    return {'p': [round(float(x), 2) for x in P[key][v]], 'part': key, 'v': int(v)}

PTS = {}
PTS['bregma'] = ('Bregma', point('frontal', near_all('frontal', ['parietal_r', 'parietal_l'])))
PTS['lambda'] = ('Lambda', point('occipital', near_all('occipital', ['parietal_r', 'parietal_l'])))
PTS['nasion'] = ('Nasion', point('frontal', near_all('frontal', ['nasal_r', 'nasal_l'])))
for s in ('r', 'l'):
    side = 'right' if s == 'r' else 'left'
    PTS[f'asterion_{s}'] = (f'Asterion ({side})', point('occipital', near_all('occipital', [f'parietal_{s}', f'temporal_{s}'], 5)))
    # posterior end of the sphenoparietal suture = where sphenoid, parietal and temporal meet
    PTS[f'pterion_{s}'] = (f'Pterion ({side})', point('sphenoid', near_all('sphenoid', [f'parietal_{s}', f'temporal_{s}'], 5)))
# inion: external occipital protuberance — most posterior outer point of the occipital near the midline
occ = P['occipital']; mid = np.where(np.abs(occ[:, 0] - mid_x) < 4)[0]
mid = outer('occipital', mid)
PTS['inion'] = ('Inion (external occipital protuberance)', point('occipital', np.array([mid[np.argmax(occ[mid, 1])]])))

# label anchors: for each part, an outward-facing vertex on its main surface — the one closest to the ray from
# the skull centre through the part's centroid (and farthest out along it). Avoids processes that stick out.
ANCH = {}
for k in P:
    v, n = P[k], N[k]; c = v.mean(0); dvec = c - centre; dvec /= (np.linalg.norm(dvec) + 1e-9)
    rel = v - centre; along = rel @ dvec; perp = np.linalg.norm(rel - np.outer(along, dvec), axis=1)
    facing = (n @ dvec) > 0.3
    cand = np.where(facing)[0] if facing.any() else np.arange(len(v))
    score = perp[cand] - 0.15 * along[cand]
    ANCH[k] = [round(float(x), 2) for x in v[cand[np.argmin(score)]]]

# cranial fossae: a point on the floor of each, right side (upward-facing inner surface below the skull centre)
def floor_point(keys, xoff, yrange):
    best = None
    for k in keys:
        v, n = P[k], N[k]
        m = (n[:, 2] > 0.75) & (v[:, 2] < centre[2]) & (np.abs(v[:, 0] - (mid_x - xoff)) < 6) & (v[:, 1] > yrange[0]) & (v[:, 1] < yrange[1])
        m &= ((v - centre) * n).sum(1) < 0          # inner surface (normal toward the centre)
        idx = np.where(m)[0]
        if len(idx) == 0: continue
        i = idx[np.argmax(v[idx, 2])]                 # the upper surface of the floor there
        if best is None: best = (k, int(i))
    return best and {'part': best[0], 'v': best[1], 'p': [round(float(x), 2) for x in P[best[0]][best[1]]]}
ycen = centre[1]
FOS = {
  'anterior':  ('Anterior cranial fossa', floor_point(['frontal'], 25, (-1e9, ycen - 25))),
  'middle':    ('Middle cranial fossa', floor_point(['temporal_r', 'sphenoid'], 38, (ycen - 30, ycen + 5))),
  'posterior': ('Posterior cranial fossa', floor_point(['occipital'], 30, (ycen + 10, 1e9))),
}

out = {'centre': [round(float(x), 2) for x in centre], 'mid_x': round(float(mid_x), 2),
       'sutures': {k: {'name': n, 'bones': b, 'parts': {pk: [int(x) for x in v] for pk, v in parts.items() if len(v)}}
                   for k, (n, b, parts) in SUT.items()},
       'points': {k: dict(name=n, **v) for k, (n, v) in PTS.items() if v},
       'anchors': ANCH,
       'fossae': {k: dict(name=n, **v) for k, (n, v) in FOS.items() if v}}
json.dump(out, open(f'{d}/skull-points.json', 'w'))
for k, (n, b, parts) in SUT.items(): print(f'{k:16s}', {pk: len(v) for pk, v in parts.items()})
for k, (n, v) in PTS.items(): print(f'{k:12s}', v and (v['part'], v['p']))
for k, (n, v) in FOS.items(): print(f'fossa {k:10s}', v and (v['part'], v['p']))
