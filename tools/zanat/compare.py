"""Compare a Z-Anatomy object with a BodyParts3D OBJ in the same body frame.
usage: compare.py blend zip "Z object name" FMAid [FMAid...]   (env ZT=transform.json maps Z into the BP3D frame first)
Prints bounding boxes (mm), centroid offset and nearest-surface-point distances both ways."""
import sys, os, json, zipfile, numpy as np
sys.path.insert(0, __import__('os').path.dirname(__file__))
import zblend

def load_obj(z, fma):
    zf = zipfile.ZipFile(z)
    name = [n for n in zf.namelist() if n.replace('\\', '/').split('/')[-1] == fma + '.obj'][0]
    V = [l.split()[1:4] for l in zf.read(name).decode('latin1').splitlines() if l.startswith('v ')]
    return np.array(V, float)

def nn(A, B):
    d = np.empty(len(A))
    for i in range(0, len(A), 2000):
        a = A[i:i + 2000]
        d[i:i + 2000] = np.sqrt(((a[:, None, :] - B[None, :, :]) ** 2).sum(-1).min(1))
    return d

def stats(d): return 'median %.2f  p95 %.2f  max %.2f mm' % (np.median(d), np.percentile(d, 95), d.max())

if __name__ == '__main__':
    bf = zblend.open_blend(sys.argv[1])
    ob = [o for o in bf.code_index[b'OB'] if zblend.obname(o) == sys.argv[3]][0]
    V, F = zblend.mesh_arrays(ob.get_pointer(b'data'))
    Z = zblend.world(ob, V) * 1000.0
    if os.environ.get('ZT'):
        T = json.load(open(os.environ['ZT'])); Z = T['scale'] * (Z / 1000.0) @ np.array(T['R']).T + np.array(T['t'])
    B = np.vstack([load_obj(sys.argv[2], f) for f in sys.argv[4:]])
    print(sys.argv[3], 'Z verts', len(Z), ' BP3D verts', len(B))
    print(' Z bbox', Z.min(0).round(1), Z.max(0).round(1))
    print(' B bbox', B.min(0).round(1), B.max(0).round(1))
    print(' centroid offset Z-B', (Z.mean(0) - B.mean(0)).round(2), ' bbox-centre offset', ((Z.min(0)+Z.max(0))/2 - (B.min(0)+B.max(0))/2).round(2))
    print(' Z->B', stats(nn(Z, B)))
    Bs = B[np.random.default_rng(0).choice(len(B), min(len(B), 20000), replace=False)]
    print(' B->Z', stats(nn(Bs, Z)))
