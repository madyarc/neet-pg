"""Build the femur data block for anatomy/bones/femur.html from BodyParts3D.

Usage (from ~/personal):
  buildenv/bin/python -I neet-pg/tools/bones/build_femur.py <FJ3365.obj> <out.json> [check.png]

FJ3365.obj = BodyParts3D 4.0 "right femur" (FMA24474), partof_BP3D_4.0_obj_99 (99 % polygon reduction).
BodyParts3D, (c) The Database Center for Life Science, CC BY-SA 2.1 Japan (licence stated in the OBJ header;
the 2025 README says CC BY 4.0 - we follow the stricter one).

Frame (BodyParts3D): +x = toward the body's left (= MEDIAL for a right femur), +y = POSTERIOR, +z = SUPERIOR, mm.
Output frame: same axes, origin at the bounding-box centre.

Landmarks are found from the shape with simple rules (extreme points in a direction within a height band),
then checked by eye on the rendered check image. They are approximate points on a reduced mesh, not
measured specimen landmarks; the page labels them so.
"""
import sys, json, base64
import numpy as np

src, out = sys.argv[1], sys.argv[2]
V, F = [], []
for line in open(src):
    p = line.split()
    if not p: continue
    if p[0] == 'v': V.append([float(x) for x in p[1:4]])
    elif p[0] == 'f': F.append([int(x.split('/')[0]) - 1 for x in p[1:4]])
V = np.array(V); F = np.array(F, dtype=np.int64)
centre = (V.min(0) + V.max(0)) / 2
V = V - centre
zmin, zmax = V[:, 2].min(), V[:, 2].max()
L = zmax - zmin
MED = np.array([1, 0, 0.]); LAT = -MED; POST = np.array([0, 1, 0.]); ANT = -POST; UP = np.array([0, 0, 1.]); DOWN = -UP

def extreme(direction, zlo=-1e9, zhi=1e9, mask=None):
    """Vertex furthest along `direction` among vertices with zlo <= z <= zhi."""
    m = (V[:, 2] >= zlo) & (V[:, 2] <= zhi)
    if mask is not None: m &= mask
    idx = np.where(m)[0]
    d = np.asarray(direction, float); d /= np.linalg.norm(d)
    return int(idx[np.argmax(V[idx] @ d)])

def nearest(p, mask=None):
    d = np.linalg.norm(V - p, axis=1)
    if mask is not None: d[~mask] = 1e9
    return int(np.argmin(d))

def surface_toward(p, direction, radius=6.0):
    """Among vertices within `radius` of the line through p along `direction` (ignoring that axis),
    the one furthest along `direction`: projects p onto the outer surface on that side."""
    d = np.asarray(direction, float); d /= np.linalg.norm(d)
    rel = V - p
    perp = rel - np.outer(rel @ d, d)
    m = np.linalg.norm(perp, axis=1) < radius
    idx = np.where(m)[0]
    if len(idx) == 0: return nearest(p)
    return int(idx[np.argmax(rel[idx] @ d)])

# --- head: sphere fit to the top-medial cap -------------------------------------------
top = extreme(UP)
cap = np.where(np.linalg.norm(V - V[top], axis=1) < 38)[0]
A = np.c_[2 * V[cap], np.ones(len(cap))]
b = (V[cap] ** 2).sum(1)
sol = np.linalg.lstsq(A, b, rcond=None)[0]
head_c = sol[:3]; head_r = float(np.sqrt(sol[3] + head_c @ head_c))

# --- shaft axis (PCA of the middle half) ---------------------------------------------------
mid = V[(V[:, 2] > zmin + 0.3 * L) & (V[:, 2] < zmax - 0.3 * L)]
mc = mid.mean(0)
axis = np.linalg.svd(mid - mc)[2][0]
if axis[2] < 0: axis = -axis

lm = {}
lm['head'] = top
# fovea: "a little below and behind the center of the head" (Gray). Direction from the head centre:
# medial, slightly posterior and inferior.
fdir = np.array([1.0, 0.30, -0.25]); fdir /= np.linalg.norm(fdir)
lm['fovea'] = nearest(head_c + head_r * fdir)
lat_mask = V[:, 0] < head_c[0] - 45
lm['greater_trochanter'] = extreme(UP, mask=lat_mask)
gt = V[lm['greater_trochanter']]
# neck: anterior surface, 40 % of the way from head centre to the trochanter summit, a little lower
neck_p = head_c + 0.45 * (gt - head_c) + np.array([0, 0, -8])
lm['neck'] = surface_toward(neck_p, ANT)
# lesser trochanter: posteromedial projection below the neck
band_lo, band_hi = head_c[2] - 95, head_c[2] - 45
lm['lesser_trochanter'] = extreme(POST + 0.9 * MED, band_lo, band_hi)
lt = V[lm['lesser_trochanter']]
# intertrochanteric crest (posterior, between the trochanters) and line (anterior)
crest_p = (gt + lt) / 2 + np.array([0, 0, 0])
lm['intertrochanteric_crest'] = surface_toward(crest_p, POST)
line_p = (gt + np.array([0, 0, -30])) * 0.45 + lt * 0.55   # runs down and medially, tubercle -> below LT
lm['intertrochanteric_line'] = surface_toward(line_p, ANT)
# trochanteric fossa: medial surface of the trochanter at its base, toward the back
fossa_p = gt + np.array([14, 8, -16])
lm['trochanteric_fossa'] = nearest(fossa_p)
# gluteal tuberosity: posterolateral, below the lesser trochanter
lm['gluteal_tuberosity'] = extreme(POST + 0.6 * LAT, lt[2] - 55, lt[2] - 35)
# linea aspera: posterior, middle third
lm['linea_aspera'] = extreme(POST, zmin + 0.47 * L, zmin + 0.53 * L)
# lower end
distal = V[:, 2] < zmin + 70
lm['medial_epicondyle'] = extreme(MED, zmin + 25, zmin + 75)
me = V[lm['medial_epicondyle']]
lm['adductor_tubercle'] = extreme(MED, me[2] + 12, me[2] + 32)
lm['lateral_epicondyle'] = extreme(LAT, zmin + 25, zmin + 75)
xmid = (V[lm['medial_epicondyle']][0] + V[lm['lateral_epicondyle']][0]) / 2
lm['medial_condyle'] = extreme(DOWN + 0.6 * POST, mask=distal & (V[:, 0] > xmid + 8))
lm['lateral_condyle'] = extreme(DOWN + 0.6 * POST, mask=distal & (V[:, 0] < xmid - 8))
mc_, lc_ = V[lm['medial_condyle']], V[lm['lateral_condyle']]
fossa_target = np.array([(mc_[0] + lc_[0]) / 2, max(mc_[1], lc_[1]) - 6, zmin + 28])
lm['intercondylar_fossa'] = nearest(fossa_target)
lm['patellar_surface'] = surface_toward(np.array([xmid, 0, zmin + 38]), ANT)
lm['popliteal_surface'] = extreme(POST, zmin + 0.17 * L, zmin + 0.20 * L)

# --- quantise mesh -----------------------------------------------------------------------
lo = V.min(0); span = (V.max(0) - lo).max()
q = np.round((V - lo) / span * 65535).astype('<u2')
assert len(V) < 65536
data = {
    'source': 'BodyParts3D FJ3365 (right femur, FMA24474)',
    'nverts': int(len(V)), 'ntris': int(len(F)),
    'lo': [round(float(x), 3) for x in lo], 'span': round(float(span), 3),
    'pos': base64.b64encode(q.tobytes()).decode(),
    'idx': base64.b64encode(F.astype('<u2').tobytes()).decode(),
    'head_centre': [round(float(x), 1) for x in head_c], 'head_radius': round(head_r, 1),
    'shaft_axis': [round(float(x), 4) for x in axis],
    'landmarks': {k: {'v': v, 'p': [round(float(x), 1) for x in V[v]]} for k, v in lm.items()},
    'length_mm': round(float(L), 1),
}
json.dump(data, open(out, 'w'))
print(f'verts {len(V)} tris {len(F)} length {L:.1f} mm head r {head_r:.1f} mm; json {len(json.dumps(data))/1024:.1f} KB')

if len(sys.argv) > 3:   # check image: 4 views with landmark dots
    from PIL import Image, ImageDraw
    H, W = 760, 330
    views = [('anterior', 0), ('medial', 90), ('posterior', 180), ('lateral', 270)]
    img = Image.new('RGB', (W * 4, H + 30), 'white'); dr = ImageDraw.Draw(img)
    s = H / (L * 1.08)
    names = list(lm)
    pal = [(220, 50, 50), (40, 110, 220), (30, 150, 70), (200, 120, 0), (150, 60, 200), (0, 150, 160)]
    for k, (vn, ang) in enumerate(views):
        # rotate about z so that the viewed side faces the camera (camera at -y looking +y)
        a = np.radians(ang); R = np.array([[np.cos(a), -np.sin(a), 0], [np.sin(a), np.cos(a), 0], [0, 0, 1]])
        if vn == 'medial': R = np.array([[0, 1, 0], [-1, 0, 0], [0, 0, 1.]])     # medial (+x) toward -y
        if vn == 'lateral': R = np.array([[0, -1, 0], [1, 0, 0], [0, 0, 1.]])
        P = V @ R.T
        zb = np.full((H, W), -1e9); col = np.full((H, W, 3), 255, np.uint8)
        light = np.array([0.4, -0.7, 0.6]); light /= np.linalg.norm(light)
        for f in F:
            a_, b_, c_ = P[f]
            n = np.cross(b_ - a_, c_ - a_); nn = np.linalg.norm(n)
            if nn == 0: continue
            n /= nn
            if n[1] > 0: continue
            sh = abs(n @ light)
            pts = np.array([[W / 2 + p[0] * s, H / 2 - p[2] * s, -p[1]] for p in (a_, b_, c_)])
            x0, x1 = int(max(0, pts[:, 0].min())), int(min(W - 1, pts[:, 0].max() + 1))
            y0, y1 = int(max(0, pts[:, 1].min())), int(min(H - 1, pts[:, 1].max() + 1))
            (ax, ay, az), (bx, by, bz), (cx, cy, cz) = pts
            den = (by - cy) * (ax - cx) + (cx - bx) * (ay - cy)
            if abs(den) < 1e-9: continue
            ys, xs = np.mgrid[y0:y1 + 1, x0:x1 + 1]
            w1 = ((by - cy) * (xs - cx) + (cx - bx) * (ys - cy)) / den
            w2 = ((cy - ay) * (xs - cx) + (ax - cx) * (ys - cy)) / den
            w3 = 1 - w1 - w2
            inside = (w1 >= 0) & (w2 >= 0) & (w3 >= 0)
            zz = w1 * az + w2 * bz + w3 * cz
            sub = zb[y0:y1 + 1, x0:x1 + 1]
            upd = inside & (zz > sub)
            sub[upd] = zz[upd]
            c = np.array([235, 228, 210]) * (0.35 + 0.65 * sh)
            col[y0:y1 + 1, x0:x1 + 1][upd] = c.astype(np.uint8)
        img.paste(Image.fromarray(col), (k * W, 0))
        dr.text((k * W + 8, H + 8), vn, fill='black')
        for i, nm in enumerate(names):
            p = P[lm[nm]]
            X, Y = W / 2 + p[0] * s + k * W, H / 2 - p[2] * s
            vis = -p[1] >= zb[int(min(H - 1, max(0, Y))), int(min(W - 1, max(0, X - k * W)))] - 3
            if not vis: continue
            c = pal[i % len(pal)]
            dr.ellipse([X - 4, Y - 4, X + 4, Y + 4], fill=c)
            dr.text((X + 6, Y - 6), nm.replace('_', ' '), fill=c)
    img.save(sys.argv[3])
