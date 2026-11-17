"""The muscles of the whole body, for the Anatomy home page (assembled from the five regional muscle builds).

  body_muscles.py config      write tools/bones-rs/configs/body-muscles.json (right-side muscles + midline ones,
                              plus the tendons/aponeuroses that join them to bone; coarser than the regional pages)
  body_muscles.py post        after `bones build`: anatomy/models/body-muscles/muscles.json — for each part its
                              region page, side, whether the page mirrors it to the left, and an identity colour
                              (the same on both sides) such that different muscles that touch never share one

Z-Anatomy's left muscles are its right meshes under one mirror matrix (checked: every pair fits one reflection to
0.0001 mm), so the page builds the left side from the right one with MIRROR below instead of downloading it twice.
"""
import sys, os, json, struct, numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, '..', '..'))
CFG = os.path.join(ROOT, 'tools', 'bones-rs', 'configs')
OUT = os.path.join(ROOT, 'anatomy', 'models', 'body-muscles')
# regional build -> (region name, page)
REGIONS = [
    ('upper-limb-muscles', 'Muscles of the upper limb', 'upper-limb/muscles.html'),
    ('lower-limb-muscles', 'Muscles of the lower limb', 'lower-limb/muscles.html'),
    ('back-muscles', 'Muscles of the back', 'back/muscles.html'),
    ('trunk-muscles', 'Muscles of the trunk wall', 'thorax/wall-muscles.html'),
    ('head-neck-muscles', 'Muscles of the head and neck', 'head-neck/muscles.html'),
]
# connective parts kept: bands that join muscle to bone and would leave a visible gap if missing.
# Left out: sheets that would cover the muscles (investing fascia, deep layers of the thoracolumbar fascia),
# the intermuscular septa and the interosseous membrane (inside the limb), the tendinous arch of levator ani.
KEEP_CONNECTIVE = {'flexor_ret', 'extensor_ret', 'palmar_apon', 'it_tract', 'calc_tendon', 'plantar_apon',
                   'sup_ext_ret', 'inf_ext_ret', 'flex_ret_f', 'sup_fib_ret', 'inf_fib_ret', 'tlf_post',
                   'inguinal_lig', 'linea_alba', 'epicranial_apon'}
ERROR_MM = 0.7     # regional pages: 0.2–0.4 mm; the whole body is seen from further away
PAL = ['#CC6677', '#332288', '#DDCC77', '#117733', '#88CCEE', '#882255', '#44AA99', '#999933', '#AA4499']


def mirror():
    """reflection that takes a right-side Z-Anatomy mesh (BodyParts3D frame) to its left twin:
    in Z-Anatomy world coordinates it is x -> -x; z-to-bp3d.json maps that frame to ours"""
    z = json.load(open(os.path.join(HERE, 'z-to-bp3d.json')))
    R, t = np.array(z['R']), np.array(z['t'])
    Q = R @ np.diag([-1.0, 1, 1]) @ R.T
    return Q, t - Q @ t


def config():
    parts, seen = [], set()
    for build, _, _ in REGIONS:
        cf = json.load(open(os.path.join(CFG, build + '.json')))
        for p in cf['parts']:
            g = p.get('group')
            if g == 'muscle' or (g == 'connective' and p['key'] in KEEP_CONNECTIVE):
                f = tuple(p['files'])
                assert f not in seen, f
                seen.add(f)
                parts.append({'key': 'm_' + p['key'], 'name': p['name'], 'fma': p['fma'], 'files': p['files'],
                              'group': 'muscle'})
    cfg = {'name': 'body-muscles',
           'zips': ['../../../sources-local/zanat/z-bp3d.zip', '../../../sources-local/zanat/z-bp3d-extra.zip'],
           'out': '../../../anatomy/models/body-muscles', 'error_mm': ERROR_MM, 'contact_mm': 1.5,
           'contacts_across_groups_only': True, 'pack': True,
           'source': 'Z-Anatomy, CC BY-SA 4.0 (from BodyParts3D), moved into the BodyParts3D frame',
           'parts': parts}
    json.dump(cfg, open(os.path.join(CFG, 'body-muscles.json'), 'w'), indent=1)
    print(len(parts), 'parts')


def decode(b, o0):
    assert b[o0:o0 + 4] == b'NPM1'
    nv, nt = struct.unpack_from('<II', b, o0 + 4)
    lo = np.array(struct.unpack_from('<3f', b, o0 + 12)); span = struct.unpack_from('<f', b, o0 + 24)[0]
    return lo + np.frombuffer(b, np.uint16, nv * 3, o0 + 32).reshape(nv, 3) / 65535 * span


def touching(P, D=2.0):
    keys = list(P)
    box = {k: (v.min(0) - D, v.max(0) + D) for k, v in P.items()}
    cells = {}
    for k, v in P.items():
        g = {}
        for j, c in enumerate(map(tuple, np.floor(v / D).astype(np.int64))): g.setdefault(c, []).append(j)
        cells[k] = g
    adj = {k: set() for k in keys}
    off = [(dx, dy, dz) for dx in (-1, 0, 1) for dy in (-1, 0, 1) for dz in (-1, 0, 1)]
    for i, a in enumerate(keys):
        for b in keys[i + 1:]:
            if np.any(box[a][1] < box[b][0]) or np.any(box[b][1] < box[a][0]): continue
            A, B, g = P[a], P[b], cells[b]
            # only A's vertices inside B's box can touch
            inb = A[np.all((A >= box[b][0]) & (A <= box[b][1]), 1)]
            for p in inb:
                c = np.floor(p / D).astype(np.int64)
                ids = [j for d in off for j in g.get((c[0] + d[0], c[1] + d[1], c[2] + d[2]), ())]
                if ids and ((B[ids] - p) ** 2).sum(1).min() <= D * D:
                    adj[a].add(b); adj[b].add(a); break
    return adj


def post():
    cfg = json.load(open(os.path.join(CFG, 'body-muscles.json')))
    man = json.load(open(os.path.join(OUT, 'body-muscles.json')))
    pack = open(os.path.join(OUT, 'body-muscles.pack'), 'rb').read()
    region = {}
    for build, name, page in REGIONS:
        for p in json.load(open(os.path.join(CFG, build + '.json')))['parts']:
            region.setdefault('m_' + p['key'], (name, page, p.get('group')))
    files = {p['key']: p['files'] for p in cfg['parts']}
    Q, t = mirror()
    P, info = {}, {}
    for p in man['parts']:
        k = p['key']; v = decode(pack, p['offset'])
        paired = all(f.endswith('_r') for f in files[k])
        P[k] = v
        if paired: P[k + '_l'] = v @ Q.T + t
        rn, page, g = region[k]
        info[k] = {'region': rn, 'page': page, 'kind': 'muscle' if g == 'muscle' else 'connective',
                   'side': 'right' if paired else 'midline', 'mirror': paired}
    mus = {k: v for k, v in P.items() if info[k if k in info else k[:-2]]['kind'] == 'muscle'}
    adj = touching(mus, 1.0)   # 2 mm (as on the regional pages) leaves no colour free where left and right meet in the back
    # a muscle and its left twin share a colour (so the body looks symmetric): colour the pair as one node, with the
    # neighbours of both; the twins touching each other across the midline (trapezius, rectus abdominis) is allowed
    node = lambda k: k if k in info else k[:-2]
    nadj = {}
    for k, ns in adj.items():
        nadj.setdefault(node(k), set()).update(node(n) for n in ns if node(n) != node(k))
    # DSATUR: colour next the node whose neighbours already use the most colours
    col = {}
    while len(col) < len(nadj):
        k = max((k for k in nadj if k not in col), key=lambda k: (len({col[n] for n in nadj[k] if n in col}), len(nadj[k]), k))
        used = {col[n] for n in nadj[k] if n in col}
        free = [c for c in PAL if c not in used]
        if not free: print('no free colour for', k, file=sys.stderr)
        col[k] = free[0] if free else PAL[0]
    for k, d in info.items():
        if d['kind'] == 'muscle':
            d['colour'] = col[k]
    out = {'note': 'written by tools/zanat/body_muscles.py post; colours: Paul Tol muted, touching (1 mm) never share',
           'mirror': {'m': Q.tolist(), 't': t.tolist()}, 'parts': info}
    json.dump(out, open(os.path.join(OUT, 'muscles.json'), 'w'), indent=0)
    print(len(info), 'parts,', sum(d['mirror'] for d in info.values()), 'mirrored; max neighbours',
          max(len(v) for v in nadj.values()))


if __name__ == '__main__':
    {'config': config, 'post': post}[sys.argv[1]]()
