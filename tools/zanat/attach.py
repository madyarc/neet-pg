"""Distance from Z-Anatomy objects (moved into the BP3D frame) to the nearest BP3D bone surface vertex.
usage: attach.py blend zip transform.json "Z name=FMA,FMA" ...   (each Z object checked against the union of its bones)"""
import sys, os, json, numpy as np
sys.path.insert(0, os.path.dirname(__file__))
import zblend
from compare import load_obj, nn
bf = zblend.open_blend(sys.argv[1]); T = json.load(open(sys.argv[3]))
obs = {zblend.obname(o): o for o in bf.code_index[b'OB']}
cache = {}
for arg in sys.argv[4:]:
    zn, fm = arg.split('=')
    o = obs.get(zn)
    if o is None: print('missing', zn); continue
    V, _ = zblend.mesh_arrays(o.get_pointer(b'data'))
    Z = T['scale'] * zblend.world(o, V) @ np.array(T['R']).T + np.array(T['t'])
    B = np.vstack([cache.setdefault(f, load_obj(sys.argv[2], f)) for f in fm.split(',')])
    d = nn(Z, B)
    print('%-44s n=%-5d median %.2f  p90 %.2f  max %.2f mm' % (zn, len(Z), np.median(d), np.percentile(d, 90), d.max()))
