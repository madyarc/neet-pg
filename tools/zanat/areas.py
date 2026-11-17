"""Attachment areas of muscles on bones, from the built meshes.

An area = bone vertices that are (1) within `d` mm of the muscle mesh and (2) within `r` mm of the landmark(s) the
textbook names for that attachment (landmarks from anatomy/models/<group>-detail/landmarks.json, same body frame),
or inside an explicit box; then small holes are closed (dilate + erode `close` rings over the mesh edges).
Proximity alone is not enough: muscles that slide over bone (deltoid over the greater tubercle) would mark it.

usage: areas.py spec.json
spec = {"manifest": "...json", "landmarks": "...json", "out": "...json", "d": 3.0,
        "attach": {"<muscle>": [{"bone": "humerus", "kind": "ori"|"ins", "near": ["deltoid_tuberosity"], "r": 25,
                                 "zmin": .., "zmax": .. (optional, mm), "zfrac": [lo, hi] (part of the bone's height, 0 = distal end) or "frac" + "axis",
                                 "mesh": "other part to measure from",
                                 "d": .. (optional), "close": 2}]}}
writes {"<muscle>": [{"bone", "kind", "verts": [ids]}]} and prints the vertex count of each area."""
import sys, os, json, struct
import numpy as np


def decode(path):
    b = open(path, 'rb').read()
    assert b[:4] == b'NPM1'
    nv, nt = struct.unpack_from('<II', b, 4)
    lo = np.array(struct.unpack_from('<3f', b, 12)); span = struct.unpack_from('<f', b, 24)[0]
    ib = struct.unpack_from('<I', b, 28)[0]
    o = 32
    pos = lo + np.frombuffer(b, np.uint16, nv * 3, o).reshape(nv, 3) / 65535 * span
    o += nv * 6 + nv * 3
    o = (o + 3) & ~3
    idx = np.frombuffer(b, np.uint16 if ib == 2 else np.uint32, nt * 3, o).reshape(nt, 3).astype(np.int64)
    return pos, idx


def near_mask(B, M, d):
    """bone vertices within d of any muscle vertex (grid hash)"""
    cell = {}
    for i, c in enumerate(map(tuple, np.floor(M / d).astype(int))): cell.setdefault(c, []).append(i)
    out = np.zeros(len(B), bool)
    for j, p in enumerate(B):
        c = np.floor(p / d).astype(int)
        ids = [i for dx in (-1, 0, 1) for dy in (-1, 0, 1) for dz in (-1, 0, 1) for i in cell.get((c[0] + dx, c[1] + dy, c[2] + dz), ())]
        if ids and ((M[ids] - p) ** 2).sum(1).min() <= d * d: out[j] = True
    return out


def neighbours(nv, idx):
    nb = [set() for _ in range(nv)]
    for a, b, c in idx:
        nb[a].update((b, c)); nb[b].update((a, c)); nb[c].update((a, b))
    return [np.fromiter(s, int) for s in nb]


def grow(mask, nb, k, allowed=None):
    for _ in range(k):
        new = mask.copy()
        for i in np.nonzero(mask)[0]: new[nb[i]] = True
        mask = new if allowed is None else (new & allowed)
    return mask


def shrink(mask, nb, k):
    for _ in range(k):
        new = mask.copy()
        for i in np.nonzero(mask)[0]:
            if not mask[nb[i]].all(): new[i] = False
        mask = new
    return mask


def main():
    spec = json.load(open(sys.argv[1]))
    here = os.path.dirname(os.path.abspath(sys.argv[1]))
    rel = lambda p: p if os.path.isabs(p) else os.path.join(here, p)
    man = json.load(open(rel(spec['manifest']))); base = os.path.dirname(rel(spec['manifest']))
    L = json.load(open(rel(spec['landmarks']))) if spec.get('landmarks') else {}
    files = {p['key']: os.path.join(base, p['file']) for p in man['parts']}
    cache, nbs = {}, {}
    mesh = lambda k: cache.setdefault(k, decode(files[k]))
    out = {}
    for m, lst in spec['attach'].items():
        for a in lst:
            M = mesh(a.get('mesh', m))[0]     # 'mesh': measure from another part (e.g. the calcaneal tendon)
            B, idx = mesh(a['bone'])
            if a['bone'] not in nbs: nbs[a['bone']] = neighbours(len(B), idx)
            nb = nbs[a['bone']]
            d = a.get('d', spec.get('d', 3.0))
            allowed = np.ones(len(B), bool)
            if a.get('near'):
                look = lambda n: (L.get(a['bone'], {}).get(n) or next(g[n] for g in L.values() if n in g))['p']
                pts = np.array([look(n) for n in a['near']])
                allowed &= (((B[:, None, :] - pts[None]) ** 2).sum(-1).min(1) <= a.get('r', 20) ** 2)
            if 'zfrac' in a or 'frac' in a:   # part of the bone along an axis (default z): 0 = low end, 1 = high end
                ax = a.get('axis', 2); fr = a.get('frac', a.get('zfrac'))   # foot bones: axis 1 (+y = back), base of a metatarsal = high y
                z0, z1 = B[:, ax].min(), B[:, ax].max(); f = (B[:, ax] - z0) / (z1 - z0)
                allowed &= (f >= fr[0]) & (f <= fr[1])
            if 'zmin' in a: allowed &= B[:, 2] >= a['zmin']
            if 'zmax' in a: allowed &= B[:, 2] <= a['zmax']
            mask = near_mask(B, M, d) & allowed
            k = a.get('close', 2)
            if k: mask = shrink(grow(mask, nb, k, allowed), nb, k) | mask
            verts = np.nonzero(mask)[0].tolist()
            out.setdefault(m, []).append({'bone': a['bone'], 'kind': a['kind'], 'verts': verts})
            print('%-20s %-10s %-4s %5d verts' % (m, a['bone'], a['kind'], len(verts)))
    json.dump(out, open(rel(spec['out']), 'w'), separators=(',', ':'))


if __name__ == '__main__':
    main()
