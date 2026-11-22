"""Which 3D parts are bones (and costal/laryngeal cartilage of the skeleton), for the viewer's Bones on/off button.

A part is a bone if its key is in a bone model (skeleton and the regional bone and detail models), or kinds.json of a
packed model gives it kind bone or cart. Mirrored left copies (key + '_l') are matched by the viewer.

usage: python3 -I tools/home/bone_keys.py  ->  anatomy/models/bone-keys.json  ["key", ...]"""
import json, os
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
M = os.path.join(ROOT, 'anatomy', 'models')
BONE_MODELS = ['skeleton', 'skull', 'skull-detail', 'spine', 'spine-detail', 'thorax', 'thorax-detail', 'upper-limb',
               'upper-limb-detail', 'lower-limb', 'lower-limb-detail']
keys = set()
for d in BONE_MODELS:
    f = os.path.join(M, d, d + '.json')
    if os.path.exists(f): keys.update(p['key'] for p in json.load(open(f))['parts'])
for d in sorted(os.listdir(M)):
    f = os.path.join(M, d, 'kinds.json')
    if os.path.exists(f):
        for k, v in json.load(open(f))['parts'].items():
            if v.get('kind') in ('bone', 'cart', 'cartilage'): keys.add(k)
# the limb muscle models carry the axial bones under an 'ax_' prefix
for d in sorted(os.listdir(M)):
    f = os.path.join(M, d, d + '.json')
    if os.path.exists(f): keys.update(p['key'] for p in json.load(open(f))['parts'] if p['key'].startswith('ax_'))
json.dump(sorted(keys), open(os.path.join(M, 'bone-keys.json'), 'w'), separators=(',', ':'))
print(len(keys), 'bone keys')
