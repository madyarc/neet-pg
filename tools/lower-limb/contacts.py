"""Print the centroid of each contact patch in a bones-rs manifest: contacts.py <manifest.json> [part ...]
(the 'va' centroid lies on part a, 'vb' on part b) -- used to place joint facets."""
import sys, json, struct, base64, os
import numpy as np
def load(path):
    b = open(path, 'rb').read(); nv, nt = struct.unpack_from('<II', b, 4)
    lo = np.array(struct.unpack_from('<3f', b, 12)); span = struct.unpack_from('<f', b, 24)[0]
    q = np.frombuffer(b, '<u2', nv * 3, 32).reshape(-1, 3)
    return lo + q / 65535 * span
def main():
  m = json.load(open(sys.argv[1])); d = os.path.dirname(sys.argv[1]); want = set(sys.argv[2:])
  V = {p['key']: load(os.path.join(d, p['file'])) for p in m['parts']}
  for c in m['contacts']:
    if want and not (c['a'] in want or c['b'] in want): continue
    for side in 'ab':
        ids = np.frombuffer(base64.b64decode(c['v' + side]), '<u4')
        print(f"{c[side]:10s} (with {c['b' if side == 'a' else 'a']:10s}) n={len(ids):4d}", np.round(V[c[side]][ids].mean(0), 1).tolist())
if __name__ == '__main__': main()
