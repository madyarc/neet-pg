"""Fit one similarity transform (scale s, rotation R, shift t) taking Z-Anatomy world coordinates (m)
to the BodyParts3D 3.0 body frame (mm), using matched bones; report per-bone residuals.
usage: fit.py blend bp3d_zip out.json"""
import sys, json, os, numpy as np
sys.path.insert(0, os.path.dirname(__file__))
import zblend
from compare import load_obj, nn

PAIRS = [('Frontal bone','FMA52734'),('Occipital bone','FMA52735'),('Mandible','FMA52748'),('Atlas (C1)','FMA12519'),
         ('Axis (C2)','FMA12520'),('Sacrum','FMA16202'),('Manubrium of sternum','FMA7486'),('Body of sternum','FMA7487'),
         ('First rib.r','FMA7857'),('Sixth rib.r','FMA8175'),('Clavicle.r','FMA13322'),('Scapula.r','FMA13395'),
         ('Humerus.r','FMA23130'),('Radius.r','FMA23464'),('Ulna.r','FMA23467'),('Hamate bone.r','FMA24448'),
         ('Hip bone.r','FMA16586'),('Femur.r','FMA24474'),('Tibia.r','FMA24477'),('Talus.r','FMA24482'),
         ('Calcaneus.r','FMA24497'),('Humerus.l','FMA23131'),('Femur.l','FMA24475'),('Clavicle.l','FMA13323')]
bf = zblend.open_blend(sys.argv[1])
obs = {zblend.obname(o): o for o in bf.code_index[b'OB']}
rng = np.random.default_rng(1)
data = []
for zn, fma in PAIRS:
    o = obs[zn]; V, _ = zblend.mesh_arrays(o.get_pointer(b'data'))
    Z = zblend.world(o, V)
    B = load_obj(sys.argv[2], fma)
    data.append((zn, Z[rng.choice(len(Z), min(400, len(Z)), replace=False)], B[rng.choice(len(B), min(4000, len(B)), replace=False)]))

def umeyama(X, Y):
    mx, my = X.mean(0), Y.mean(0); Xc, Yc = X - mx, Y - my
    U, S, Vt = np.linalg.svd(Yc.T @ Xc / len(X))
    D = np.eye(3); D[2, 2] = np.sign(np.linalg.det(U @ Vt))
    R = U @ D @ Vt; s = (S * np.diag(D)).sum() / (Xc ** 2).sum(1).mean()
    return s, R, my - s * R @ mx

# start: scale 1000/1.033, shift from bbox centres
Zall = np.vstack([d[1] for d in data]); Ball = np.vstack([d[2] for d in data])
s, R = 1000 / 1.033, np.eye(3); t = Ball.mean(0) - s * Zall.mean(0)
for it in range(40):
    X, Y = [], []
    for zn, Z, B in data:
        P = s * Z @ R.T + t
        idx = np.empty(len(P), int)
        d2 = ((P[:, None] - B[None]) ** 2).sum(-1); idx = d2.argmin(1)
        X.append(Z); Y.append(B[idx])
    s, R, t = umeyama(np.vstack(X), np.vstack(Y))
ang = np.degrees(np.arccos((np.trace(R) - 1) / 2))
print('scale mm per m %.3f (=> Z is %.4f x BP3D)  rotation %.3f deg  shift %s mm' % (s, 1000 / s, ang, t.round(2)))
for zn, Z, B in data:
    P = s * Z @ R.T + t
    d = nn(P, B)
    print('  %-22s median %.2f  p95 %.2f  max %.2f mm' % (zn, np.median(d), np.percentile(d, 95), d.max()))
json.dump({'scale': s, 'R': R.tolist(), 't': t.tolist(), 'note': 'BP3D_mm = scale * R @ Z_world_m + t'}, open(sys.argv[3], 'w'), indent=1)
