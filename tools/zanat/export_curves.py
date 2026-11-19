"""Export Z-Anatomy vessels (Blender Bezier curves with a round bevel) as tube meshes in the BodyParts3D 3.0 frame (mm),
OBJ files in one zip, like export.py, so tools/bones-rs builds them as parts.
usage: export_curves.py blend transform.json out.zip index.tsv "collection substring" [...] [--no-left]

Blender draws each curve as a tube of radius  bevel depth (Curve.ext2) x point radius  swept along the Bezier spline
(Curve.resolu samples per span, minimum-twist frames). Here: the same spline and radius (interpolated as Blender's
Nurb.radius_interp says: linear or ease), sampled every 1 mm and thinned where the path is straight (thin()), with 6 sides (8 over 1.5 mm radius, 12 over
4 mm) and closed ends. Each spline of an object becomes one tube of that object's OBJ.
--no-left skips the .l objects that are the .r curve mirrored (the page mirrors the .r ones, as for the muscles);
the index's mirror column marks the .r objects whose left twin was skipped."""
import sys, os, re, json, zipfile, io, struct, numpy as np
sys.path.insert(0, os.path.dirname(__file__))
import zblend

args = [a for a in sys.argv[1:] if not a.startswith('--')]
NOLEFT = '--no-left' in sys.argv
bf = zblend.open_blend(args[0]); T = json.load(open(args[1]))
R, t, s = np.array(T['R']), np.array(T['t']), T['scale']
wanted = args[4:]
PS = bf.header.pointer_size
coll = {}
def listbase(blk, field):
    p = blk.get_pointer((field, b'first'))
    while p is not None:
        yield p; p = p.get_pointer(b'next')
for g in bf.code_index[b'GR']:
    for co in listbase(g, b'gobject'):
        ob = co.get_pointer(b'ob')
        if ob is not None: coll.setdefault(ob.addr_old, []).append(g.id_name[2:].decode('utf-8', 'replace'))

def bezier_points(nu):
    """[(knot, handle_left, handle_right, radius)] of one Bezier spline, object space"""
    bz = nu.get_pointer(b'bezt'); Td = bz.dna_type; raw = bz.raw_data()
    ov = Td.field_from_path(PS, b'vec')[1]; orad = Td.field_from_path(PS, b'radius')[1]
    out = []
    for i in range(nu.get(b'pntsu')):
        o = i * Td.size
        v = np.frombuffer(raw[o + ov:o + ov + 36], np.float32).reshape(3, 3).astype(np.float64)
        out.append((v[1], v[0], v[2], struct.unpack_from('<f', raw, o + orad)[0]))
    return out

def poly_points(nu):
    bp = nu.get_pointer(b'bp'); Td = bp.dna_type; raw = bp.raw_data()
    ov = Td.field_from_path(PS, b'vec')[1]; orad = Td.field_from_path(PS, b'radius')[1]
    P, r = [], []
    for i in range(nu.get(b'pntsu')):
        o = i * Td.size
        P.append(np.frombuffer(raw[o + ov:o + ov + 12], np.float32).astype(np.float64))
        r.append(struct.unpack_from('<f', raw, o + orad)[0])
    return np.array(P), np.array(r)

def sample(nu, step):
    """centreline points and radius factors along one spline (object space, step in object units)"""
    typ, cyc = nu.get(b'type'), nu.get(b'flagu') & 1
    try: ease = nu.get(b'radius_interp') == 3
    except Exception: ease = False
    if typ != 1:                       # poly / NURBS: use the control polygon (Z-Anatomy vessels are Bezier)
        return poly_points(nu)
    K = bezier_points(nu)
    spans = list(zip(K, K[1:] + K[:1])) if cyc else list(zip(K, K[1:]))
    P, r = [], []
    for a, b in spans:
        c = [a[0], a[2], b[1], b[0]]
        L = sum(np.linalg.norm(c[i + 1] - c[i]) for i in range(3))
        n = max(2, int(np.ceil(L / step)))
        for u in np.linspace(0, 1, n, endpoint=False):
            m = 1 - u
            P.append(m**3 * c[0] + 3 * m * m * u * c[1] + 3 * m * u * u * c[2] + u**3 * c[3])
            w = u * u * (3 - 2 * u) if ease else u
            r.append(a[3] * (1 - w) + b[3] * w)
    if not cyc: P.append(K[-1][0]); r.append(K[-1][3])
    return np.array(P), np.array(r)

def tube(P, rad):
    """P (n,3) mm, rad (n,) mm -> V, F; minimum-twist (parallel transport) frames, closed ends"""
    keep = np.r_[True, np.linalg.norm(np.diff(P, axis=0), axis=1) > 1e-6]
    P, rad = P[keep], rad[keep]
    if len(P) < 2: return None, None
    P, rad = thin(P, rad)
    k = 12 if rad.max() > 4 else 8 if rad.max() > 1.5 else 6
    Tn = np.gradient(P, axis=0); nl = np.linalg.norm(Tn, axis=1)
    for i in np.where(nl < 1e-9)[0]: Tn[i] = P[min(i + 1, len(P) - 1)] - P[max(i - 1, 0)] if i else P[1] - P[0]   # a hairpin
    Tn /= np.maximum(np.linalg.norm(Tn, axis=1), 1e-12)[:, None]
    a = np.array([1.0, 0, 0]) if abs(Tn[0][0]) < 0.9 else np.array([0, 1.0, 0])
    N = np.cross(Tn[0], a); N /= np.linalg.norm(N)
    ang = np.linspace(0, 2 * np.pi, k, endpoint=False)
    V = []
    for i in range(len(P)):
        if i:
            N = N - Tn[i] * (N @ Tn[i])
            if np.linalg.norm(N) < 1e-9: N = np.cross(Tn[i], a)
            N /= np.linalg.norm(N)
        B = np.cross(Tn[i], N)
        V.extend(P[i] + rad[i] * (np.cos(q) * N + np.sin(q) * B) for q in ang)
    F = []
    for i in range(len(P) - 1):
        for j in range(k):
            a0, a1 = i * k + j, i * k + (j + 1) % k
            b0, b1 = a0 + k, a1 + k
            F += [(a0, a1, b1), (a0, b1, b0)]
    c0, c1 = len(V), len(V) + 1; V += [P[0], P[-1]]
    last = (len(P) - 1) * k
    for j in range(k):
        F.append((c0, (j + 1) % k, j)); F.append((c1, last + j, last + (j + 1) % k))
    return np.array(V), np.array(F)

def thin(P, rad):
    """drop centreline points the tube does not need (Douglas-Peucker): the path stays within 0.2 mm + 15 % of the
    radius and the radius within 10 % of the line between the kept points"""
    keep = np.zeros(len(P), bool); keep[[0, -1]] = True
    stack = [(0, len(P) - 1)]
    while stack:
        i, j = stack.pop()
        if j <= i + 1: continue
        a, b = P[i], P[j]; d = b - a; L2 = d @ d
        u = np.clip(((P[i + 1:j] - a) @ d) / L2, 0, 1) if L2 > 0 else np.zeros(j - i - 1)
        dev = np.linalg.norm(P[i + 1:j] - (a + u[:, None] * d), axis=1)
        rl = rad[i] + u * (rad[j] - rad[i])
        bad = np.maximum(dev / (0.2 + 0.15 * rad[i + 1:j]), np.abs(rad[i + 1:j] - rl) / (0.1 * rad[i + 1:j]))
        m = int(bad.argmax())
        if bad[m] > 1: keep[i + 1 + m] = True; stack += [(i, i + 1 + m), (i + 1 + m, j)]
    return P[keep], rad[keep]

def slug(n): return 'Z_' + re.sub(r'[^a-z0-9]+', '_', n.lower()).strip('_')
seen = {}; n_obj = 0
CURVES = {zblend.obname(o): o for o in bf.code_index[b'OB'] if o.get(b'type') == 2}
def twin_is_mirror(name):
    """the .l object is the .r curve under the x -> -x reflection of Z-Anatomy world space (to 0.5 mm)"""
    r, l = CURVES.get(name[:-2] + '.r'), CURVES.get(name[:-2] + '.l')
    if r is None or l is None or r.get_pointer(b'data').addr_old != l.get_pointer(b'data').addr_old: return False
    Mr = np.array(r.get(b'obmat')).reshape(4, 4); Ml = np.array(l.get(b'obmat')).reshape(4, 4)
    return np.abs(Mr @ np.diag([-1.0, 1, 1, 1]) - Ml).max() < 5e-4
with zipfile.ZipFile(args[2], 'w', zipfile.ZIP_DEFLATED) as zf, open(args[3], 'w') as idx:
    idx.write('file\tobject\tverts\ttris\tsplines\tradius_mm\tmirror\tcollections\n')
    for ob in bf.code_index[b'OB']:
        name = zblend.obname(ob)
        if re.search(r'\.(j|i|g|t|s)$', name) or not re.search(r'[A-Za-z]', name): continue
        if NOLEFT and name.endswith('.l') and twin_is_mirror(name): continue
        cs = coll.get(ob.addr_old, [])
        if not any(w in c for w in wanted for c in cs): continue
        cu = ob.get_pointer(b'data')
        if cu is None or cu.code != b'CU' or ob.get(b'type') != 2: continue
        depth = cu.get(b'ext2')
        if depth <= 0: continue
        M = np.array(ob.get(b'obmat'), np.float64).reshape(4, 4)
        sc = np.cbrt(abs(np.linalg.det(M[:3, :3])))       # object scale (uniform here)
        Vs, Fs, base, radii, nspl = [], [], 0, [], 0
        for nu in listbase(cu, b'nurb'):
            P, r = sample(nu, 0.001 / sc)                   # ~1 mm, thinned in tube()
            Pw = s * (P @ M[:3, :3] + M[3, :3]) @ R.T + t
            r = np.maximum(np.abs(r), 0.05 / (s * sc * depth))   # a point radius can be <= 0 (central retinal artery)
            V, F = tube(Pw, s * sc * depth * r)
            if V is None: continue
            Vs.append(V); Fs.append(F + base); base += len(V); radii.extend(s * sc * depth * r); nspl += 1
        if not Vs: continue
        V, F = np.vstack(Vs), np.vstack(Fs)
        fn = slug(name.strip('()'))
        if fn in seen: seen[fn] += 1; fn += '_%d' % seen[fn]
        else: seen[fn] = 0
        buf = io.StringIO()
        buf.write('# %s (Z-Anatomy, CC BY-SA 4.0), tube swept along its curve, BodyParts3D 3.0 frame, mm\n' % name)
        for v in V: buf.write('v %.4f %.4f %.4f\n' % tuple(v))
        for f in F + 1: buf.write('f %d %d %d\n' % tuple(f))
        zf.writestr(fn + '.obj', buf.getvalue())
        idx.write('\t'.join([fn, name, str(len(V)), str(len(F)), str(nspl), '%.2f-%.2f' % (min(radii), max(radii)),
                             str(int(NOLEFT and name.endswith('.r') and twin_is_mirror(name))),
                             '|'.join(cs)]) + '\n')
        n_obj += 1
print(n_obj, 'curves')
