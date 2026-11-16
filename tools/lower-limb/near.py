"""Centroids of the parts of bone A that lie within D mm of bone B, split into clusters by height:
near.py <manifest.json> A B D [zsplit ...]  -> one centroid per z band (bands cut at the given z values)."""
import sys, json, os
import numpy as np
sys.path.insert(0, os.path.dirname(__file__)); from contacts import load
m = json.load(open(sys.argv[1])); d = os.path.dirname(sys.argv[1]); P = {p['key']: p for p in m['parts']}
A = load(os.path.join(d, P[sys.argv[2]]['file'])); B = load(os.path.join(d, P[sys.argv[3]]['file']))
dist = np.concatenate([np.sqrt(((A[i:i+500, None] - B[None]) ** 2).sum(-1)).min(1) for i in range(0, len(A), 500)]); sel = A[dist < float(sys.argv[4])]
cuts = [-1e9] + [float(z) for z in sys.argv[5:]] + [1e9]
for lo, hi in zip(cuts, cuts[1:]):
    s = sel[(sel[:, 2] >= lo) & (sel[:, 2] < hi)]
    if len(s): print(f'z {lo:.0f}..{hi:.0f}: n={len(s)}', np.round(s.mean(0), 1).tolist(), 'zrange', round(s[:,2].min()), round(s[:,2].max()))
