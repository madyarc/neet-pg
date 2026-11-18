"""Shared helpers for fitting joint pivots and axes (general_axes.py, ul_axes.py…). Set MODEL before importing via exec.

Pivot points and axes for the moving examples, computed from the bone surfaces.
usage: python -I general_axes.py  -> anatomy/models/joints-general/motions.json

Each motion: the bones that move, a pivot point (mm, BodyParts3D frame: +x left, +y posterior, +z up) and one or
more movements: {name, axis (unit vector), arc [from, to] in degrees} or {name, slide (unit vector), mm}.
The arcs only show the kind of movement; they are not normal ranges. Pivots are fitted (sphere/circle) to the
joint surfaces, so they are approximate.
"""
import os, sys, json, struct, numpy as np

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
OUT = os.path.join(ROOT, 'anatomy', 'models', MODEL)
man = json.load(open(os.path.join(OUT, MODEL + '.json')))
pack = open(os.path.join(OUT, MODEL + '.pack'), 'rb').read()


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


