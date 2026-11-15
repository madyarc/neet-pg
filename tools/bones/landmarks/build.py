"""Collect the hand-placed landmark points (one JSON per bone, made with tools/test/bone_views.py pick)
into anatomy/models/skull-detail/landmarks.json: {bone type: {landmark key: {p, dir}}}.
`dir` is the direction (body frame) the page turns to face when the landmark is selected."""
import json, glob, os
DIRS = {'ant': [0, -1, 0], 'post': [0, 1, 0], 'left': [1, 0, 0], 'right': [-1, 0, 0], 'sup': [0, -0.35, 1], 'inf': [0, -0.35, -1]}
here = os.path.dirname(os.path.abspath(__file__))
out = {}
for f in sorted(glob.glob(os.path.join(here, '*.json'))):
    bone = os.path.basename(f)[:-5]
    pts = {}
    for it in json.load(open(f)):
        if not it.get('p'): raise SystemExit(f'{bone}.{it["name"]}: no point')
        d = it['dir']; d = DIRS[d] if isinstance(d, str) and d in DIRS else ([float(x) for x in d.split(',')] if isinstance(d, str) else d)
        pts[it['name']] = {'p': it['p'], 'dir': d}
    out[bone] = pts
dst = os.path.join(here, '../../../anatomy/models/skull-detail/landmarks.json')
json.dump(out, open(dst, 'w'), separators=(',', ':'))
print({b: len(p) for b, p in out.items()}, sum(len(p) for p in out.values()))
