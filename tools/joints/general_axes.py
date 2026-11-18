"""Pivot points and axes for the moving examples on the general joints page, computed from the bone surfaces.
usage: python -I general_axes.py  -> anatomy/models/joints-general/motions.json

Each motion: the bones that move, a pivot point (mm, BodyParts3D frame: +x left, +y posterior, +z up) and one or
more movements: {name, axis (unit vector), arc [from, to] in degrees} or {name, slide (unit vector), mm}.
The arcs only show the kind of movement; they are not normal ranges. Pivots are fitted (sphere/circle) to the
joint surfaces, so they are approximate.
"""
import os, sys, json, struct, numpy as np

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
OUT = os.path.join(ROOT, 'anatomy', 'models', 'joints-general')
man = json.load(open(os.path.join(OUT, 'joints-general.json')))
pack = open(os.path.join(OUT, 'joints-general.pack'), 'rb').read()


def decode(o0):
    nv = struct.unpack_from('<I', pack, o0 + 4)[0]
    lo = np.array(struct.unpack_from('<3f', pack, o0 + 12)); span = struct.unpack_from('<f', pack, o0 + 24)[0]
    return lo + np.frombuffer(pack, np.uint16, nv * 3, o0 + 32).reshape(nv, 3) / 65535 * span


P = {p['key']: decode(p['offset']) for p in man['parts']}
HAND = ['scaphoid', 'lunate', 'triquetral', 'pisiform', 'trapezium', 'trapezoid', 'capitate', 'hamate',
        'mc1', 'mc2', 'mc3', 'mc4', 'mc5', 'pp1', 'dp1', 'pp2', 'mp2', 'dp2', 'pp3', 'mp3', 'dp3', 'pp4', 'mp4', 'dp4',
        'pp5', 'mp5', 'dp5']


def near(a, b, d):
    """vertices of part a within d mm of the closest approach of part b (the joint space is empty in the model:
    cartilage is not modelled, so the surfaces facing each other are found relative to the narrowest gap)"""
    A, B = P[a], P[b] if isinstance(b, str) else np.vstack([P[x] for x in b])
    dd = np.empty(len(A))
    for i in range(0, len(A), 512):
        dd[i:i + 512] = np.sqrt(((A[i:i + 512, None, :] - B[None, :, :]) ** 2).sum(-1).min(1))
    return A[dd <= dd.min() + d]


def sphere(X):
    """least-squares sphere: |x|^2 = 2 c.x + k"""
    A = np.c_[2 * X, np.ones(len(X))]; s = np.linalg.lstsq(A, (X ** 2).sum(1), rcond=None)[0]
    c = s[:3]; return c, float(np.sqrt(s[3] + c @ c))


def circle(X, axis):
    """centre of the least-squares circle of X projected on the plane normal to axis (returned in 3D, at X's mean)"""
    axis = np.asarray(axis, float); axis /= np.linalg.norm(axis)
    u = np.cross(axis, [0, 0, 1] if abs(axis[2]) < 0.9 else [1, 0, 0]); u /= np.linalg.norm(u); w = np.cross(axis, u)
    m = X.mean(0); Q = np.c_[(X - m) @ u, (X - m) @ w]
    A = np.c_[2 * Q, np.ones(len(Q))]; s = np.linalg.lstsq(A, (Q ** 2).sum(1), rcond=None)[0]
    return m + s[0] * u + s[1] * w, float(np.sqrt(s[2] + s[0] ** 2 + s[1] ** 2))


def pca(X):
    w, v = np.linalg.eigh(np.cov((X - X.mean(0)).T)); return v[:, ::-1].T   # largest first


unit = lambda v: (np.asarray(v, float) / np.linalg.norm(v)).round(4).tolist()
R = lambda v: np.round(v, 2).tolist()
M, info = {}, {}

# ball and socket: hip
X = near('femur', 'hip', 3.0); c, r = sphere(X)
knee = P['femur'][P['femur'][:, 2] < P['femur'][:, 2].min() + 15].mean(0)
M['hip'] = {'moving': ['femur'], 'pivot': R(c), 'moves': [
    {'name': 'Flexion and extension', 'axis': [1, 0, 0], 'arc': [-60, 15]},
    {'name': 'Abduction and adduction', 'axis': [0, 1, 0], 'arc': [-10, 30]},
    {'name': 'Medial and lateral rotation', 'axis': unit(c - knee), 'arc': [-30, 30]}]}
info['hip'] = f'femoral head sphere r={r:.1f} mm from {len(X)} vertices'

# hinge: elbow (humero-ulnar); the forearm and hand move together
X = near('humerus', ['ulna', 'radius'], 5.0); c, r = circle(X, [1, 0, 0])
M['elbow'] = {'moving': ['ulna', 'radius'] + HAND, 'pivot': R(c), 'moves': [
    {'name': 'Flexion and extension', 'axis': [1, 0, 0], 'arc': [-110, 0]}]}
info['elbow'] = f'trochlea circle r={r:.1f} mm from {len(X)} vertices'

# pivot: median atlanto-axial joint; the atlas turns about the dens
# the dens is too short and round for its own axis to be fitted reliably: a vertical line through its centre
D = P['c2'][P['c2'][:, 2] > P['c2'][:, 2].max() - 12]
dax = np.array([0, 0, 1.0])
M['atlantoaxial'] = {'moving': ['c1'], 'pivot': R(D.mean(0)), 'moves': [
    {'name': 'Rotation (turning the head)', 'axis': unit(dax), 'arc': [-30, 30]}]}
info['atlantoaxial'] = f'dens: {len(D)} vertices in the top 12 mm of the axis'

# pivot: radio-ulnar joints; the radius (and hand) turns about a line from the radial head to the ulnar head
rz = P['radius'][:, 2]
head = near('radius', 'ulna', 2.0); head = head[head[:, 2] > rz.max() - 30]
uz = P['ulna'][:, 2]
uh = near('ulna', 'radius', 2.0); uh = uh[uh[:, 2] < uz.min() + 30]
a, b = head.mean(0), uh.mean(0)
M['radioulnar'] = {'moving': ['radius'] + HAND, 'pivot': R(a), 'moves': [
    {'name': 'Pronation and supination', 'axis': unit(a - b), 'arc': [0, 150]}]}
info['radioulnar'] = f'radial head {len(head)} / ulnar head {len(uh)} contact vertices'

# condylar: knee; the leg moves on the femoral condyles. The joint space is empty in the model, so the flexion
# centre is fitted to the outline of the condyles seen from the side (inferior to posterior arc)
F = P['femur']; zmin = F[:, 2].min(); D = F[F[:, 2] < zmin + 45]; yc, zc = D[:, 1].mean(), zmin + 25
ang = np.degrees(np.arctan2(D[:, 2] - zc, D[:, 1] - yc)); rr = np.hypot(D[:, 2] - zc, D[:, 1] - yc)
X = np.array([D[m][rr[m].argmax()] for a0 in range(-90, 30, 6) for m in [(ang >= a0) & (ang < a0 + 6)] if m.any()])
c, r = circle(X, [1, 0, 0])
M['knee'] = {'moving': ['tibia', 'fibula', 'talus', 'men_med', 'men_lat'], 'pivot': R(c), 'moves': [
    {'name': 'Flexion and extension', 'axis': [1, 0, 0], 'arc': [0, 100]}]}
info['knee'] = f'condyle outline circle r={r:.1f} mm from {len(X)} points, {c[2] - zmin:.1f} mm above the lowest point'

# ellipsoid: radiocarpal (wrist); the hand moves about the head of the capitate
X = near('capitate', ['lunate', 'scaphoid'], 2.0)
cap = X.mean(0)
M['wrist'] = {'moving': HAND, 'pivot': R(cap), 'moves': [
    {'name': 'Flexion and extension', 'axis': [1, 0, 0], 'arc': [-60, 50]},
    {'name': 'Abduction and adduction (radial and ulnar deviation)', 'axis': [0, 1, 0], 'arc': [-30, 15]}]}
info['wrist'] = f'head of capitate: {len(X)} vertices'

# saddle: first carpometacarpal; the thumb metacarpal moves on the trapezium
X = near('trapezium', 'mc1', 1.5); c = X.mean(0)
l = pca(P['mc1'])[0]; l = l if l @ (P['mc1'].mean(0) - c) > 0 else -l
n = np.array([0, -1.0, 0])
abd = np.cross(l, n); abd /= np.linalg.norm(abd); flex = n - (n @ l) * l; flex /= np.linalg.norm(flex)
M['thumb'] = {'moving': ['mc1', 'pp1', 'dp1'], 'pivot': R(c), 'moves': [
    {'name': 'Flexion and extension', 'axis': unit(flex), 'arc': [-20, 35]},
    {'name': 'Abduction and adduction', 'axis': unit(abd), 'arc': [-5, 35]}]}
info['thumb'] = f'trapezium facet {len(X)} vertices'

# plane: acromioclavicular; the clavicle glides on the acromion
X = near('clavicle', 'scapula', 2.0); e = pca(X)
M['acromioclavicular'] = {'moving': ['clavicle'], 'pivot': R(X.mean(0)), 'moves': [
    {'name': 'Gliding', 'slide': unit(e[0]), 'mm': 4}, {'name': 'Gliding', 'slide': unit(e[1]), 'mm': 4}]}
info['acromioclavicular'] = f'facet {len(X)} vertices; normal {unit(e[2])}'

json.dump({'note': 'written by tools/joints/general_axes.py; pivots fitted to the joint surfaces (approximate); '
                   'arcs show the kind of movement only, not normal ranges', 'motions': M},
          open(os.path.join(OUT, 'motions.json'), 'w'), indent=1)
for k, v in info.items(): print(k, v, M[k]['pivot'])
