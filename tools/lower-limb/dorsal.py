"""Dorsal (top) surface point of each named bone near the middle of its footprint: dorsal.py <manifest> key ..."""
import sys, json, os
import numpy as np
sys.path.insert(0, os.path.dirname(__file__)); from contacts import load
m = json.load(open(sys.argv[1])); d = os.path.dirname(sys.argv[1]); P = {p['key']: p for p in m['parts']}
for k in sys.argv[2:]:
    V = load(os.path.join(d, P[k]['file'])); c = (V.min(0) + V.max(0)) / 2
    near = V[np.hypot(V[:, 0] - c[0], V[:, 1] - c[1]) < 4]
    print(k, np.round(near[near[:, 2].argmax()], 1).tolist())
