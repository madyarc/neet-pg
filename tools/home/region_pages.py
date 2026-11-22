"""Which detailed page a tap on a Trunk part of the home page's vessel, nerve and lymph layers opens.

Z-Anatomy files many parts under "Trunk" (thorax, abdomen, pelvis, and also the axillary and inguinal nodes).
A part opens the regional page whose packed model contains it; parts in both the thorax and the abdomen models are
settled by PREFER. Parts in no regional model keep their region (no page).

usage: python3 -I tools/home/region_pages.py  ->  anatomy/models/region-pages.json  {key: page region name}
The page region names are the keys of REGION_PAGES in anatomy/index.html."""
import json, os
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
M = os.path.join(ROOT, 'anatomy', 'models')
MODELS = [('Thorax', 'thorax-nv/thorax-nv.json'), ('Abdomen and pelvis', 'abd-nv/abd-nv.json'),
          ('Upper limb', 'ul-nv/ul-nv.json'), ('Lower limb', 'll-nv/ll-nv.json'),
          ('Head and neck', 'hn-nv/hn-nv.json'), ('Lungs', 'lung/lung.json'),
          ('Abdominal organs', 'abdo/abdo.json')]
PREFER = {'v_abdominal_aorta': 'Abdomen and pelvis', 'v_inferior_vena_cava_thoracic_part': 'Abdomen and pelvis',
          'v_left_ascending_lumbar_vein': 'Abdomen and pelvis', 'v_right_ascending_lumbar_vein': 'Abdomen and pelvis',
          'v_common_facial_vein_r': 'Head and neck'}
info = {}
for f in ('body-vessels/vessels.json', 'body-nerves/nerves.json', 'body-lymph/lymph.json'):
    info.update(json.load(open(os.path.join(M, f)))['parts'])
out = {}
for region, f in MODELS:
    for p in json.load(open(os.path.join(M, f)))['parts']:
        k = p['key']
        if k in info and info[k]['region'] == 'Trunk' and k not in out: out[k] = PREFER.get(k, region)
json.dump(dict(sorted(out.items())), open(os.path.join(M, 'region-pages.json'), 'w'), separators=(',', ':'))
from collections import Counter
print(len(out), Counter(out.values()))
