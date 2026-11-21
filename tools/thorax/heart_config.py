"""Config for the page "The Heart" (anatomy/thorax/heart.html, module 26): one packed model of the heart, its own
vessels, the roots of the great vessels and (for surface marking) the sternum, ribs 1-7 and costal cartilages 1-7.
Same pattern as tools/upper-limb/nv_config.py and tools/lower-limb/nv_config.py.

Parts and where they come from (same keys, names and files as the whole-body configs, so names match the other pages):
  bone     configs/skeleton.json      sternum (manubrium, body, xiphoid), ribs 1-7 and costal cartilages 1-7, both sides
                                      (skeleton error_mm, 0.6 mm: they are only landmarks here)
  chamber  configs/body-vessels.json  the four chambers (Z-Anatomy meshes in z-bp3d-heart.zip), rebuilt here at a finer
                                      error (CHAMBER_ERR) than the whole-body layer (0.3 mm), so the inside can be shown
  papillary, valve  z-index-heart.tsv the papillary muscles and the valve leaflets (cusps), which the whole-body layer
                                      does not include (VALVE_ERR)
  artery   configs/body-vessels.json  coronary arteries and branches; ascending aorta, arch, thoracic aorta; pulmonary
                                      trunk, its bifurcation, right and left pulmonary arteries; brachiocephalic trunk
  vein     configs/body-vessels.json  coronary sinus and cardiac veins; SVC, thoracic IVC; the four pulmonary veins
Parts are ordered by colour (bone, chamber + papillary (both --heart), valve, artery, vein): the viewer draws
neighbouring parts of one colour with a single call. One group, contacts not needed.

Also writes anatomy/models/heart/kinds.json: {key: {"kind": ...}} for the page.

usage: python3 -I tools/thorax/heart_config.py   ->  tools/bones-rs/configs/heart.json (+ anatomy/models/heart/kinds.json)
then:  cd tools/bones-rs && target/release/bones build configs/heart.json   (through tools/capped)"""
import json, os, csv
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
CFG = os.path.join(ROOT, 'tools', 'bones-rs', 'configs')
MODELS = os.path.join(ROOT, 'anatomy', 'models')
load = lambda n: json.load(open(os.path.join(CFG, n + '.json')))
CHAMBER_ERR, VALVE_ERR = 0.12, 0.08

ORD = ['first', 'second', 'third', 'fourth', 'fifth', 'sixth', 'seventh']
BONES = {'manubrium', 'body_of_sternum', 'xiphoid_process'} | {f'{s}_{o}_rib' for s in ('left', 'right') for o in ORD} | \
        {f'{s}_{o}_costal_cartilage' for s in ('left', 'right') for o in ORD}
CHAMBERS = ['v_right_atrium', 'v_right_ventricle', 'v_left_atrium', 'v_left_ventricle']
ARTERIES = ['v_ascending_aorta', 'v_aortic_arch', 'v_thoracic_aorta', 'v_brachiocephalic_trunk', 'v_pulmonary_trunk',
            'v_bifurcation_of_pulmonary_trunk', 'v_right_pulmonary_artery', 'v_left_pulmonary_artery',
            'v_right_coronary_artery', 'v_right_inferolateral_branch_of_right_coronary_artery', 'v_left_coronary_artery',
            'v_anterior_interventricular_artery', 'v_septal_branches_of_anterior_interventricular_artery',
            'v_circumflex_artery_of_heart']
VEINS = ['v_coronary_sinus', 'v_great_cardiac_vein', 'v_middle_cardiac_vein', 'v_inferior_vein_of_left_ventricle',
         'v_inferior_vein_of_left_ventricle_posterior', 'v_superior_vena_cava', 'v_inferior_vena_cava_thoracic_part',
         'v_right_superior_pulmonary_vein', 'v_right_inferior_pulmonary_vein', 'v_left_superior_pulmonary_vein',
         'v_left_inferior_pulmonary_vein']


def copy(p, err, kind):
    return {'key': p['key'], 'name': p['name'], 'fma': p['fma'], 'files': p['files'], 'group': 'heart',
            'error_mm': err, '_kind': kind}


parts, zips = [], []
sk = load('skeleton'); zips += sk['zips']
parts += [copy(p, p.get('error_mm', sk['error_mm']), 'bone') for p in sk['parts'] if p['key'] in BONES]

ve = load('body-vessels'); zips += ve['zips']
vp = {p['key']: p for p in ve['parts']}
parts += [copy(vp[k], CHAMBER_ERR, 'chamber') for k in CHAMBERS]
rows = list(csv.DictReader(open(os.path.join(ROOT, 'tools', 'zanat', 'z-index-heart.tsv')), delimiter='\t'))
for kind, test in (('papillary', lambda o: 'papillary muscle' in o), ('valve', lambda o: 'leaflet' in o)):
    for r in rows:
        if 'Heart' in r['collections'] and test(r['object']):
            parts.append({'key': 'h_' + r['file'][2:], 'name': r['object'], 'fma': '', 'files': [r['file']], 'group': 'heart',
                          'error_mm': VALVE_ERR, '_kind': kind})
parts += [copy(vp[k], vp[k].get('error_mm', ve['error_mm']), 'artery') for k in ARTERIES]
parts += [copy(vp[k], vp[k].get('error_mm', ve['error_mm']), 'vein') for k in VEINS]

missing = (BONES | set(CHAMBERS) | set(ARTERIES) | set(VEINS)) - {p['key'] for p in parts}
assert not missing, missing
kinds = {p['key']: {'kind': p.pop('_kind')} for p in parts}
cfg = {'name': 'heart', 'zips': list(dict.fromkeys(zips)), 'out': '../../../anatomy/models/heart',
       'error_mm': 0.3, 'contact_mm': 0.5, 'contacts_across_groups_only': True, 'pack': True,
       'source': 'Bones: BodyParts3D, (c) The Database Center for Life Science, CC BY-SA 2.1 Japan. Heart chambers, valve '
                 'leaflets, papillary muscles and vessels (curves swept into tubes): Z-Anatomy, CC BY-SA 4.0 (from '
                 'BodyParts3D), moved into the BodyParts3D frame',
       'parts': parts}
json.dump(cfg, open(os.path.join(CFG, 'heart.json'), 'w'), indent=1)
os.makedirs(os.path.join(MODELS, 'heart'), exist_ok=True)
json.dump({'note': 'written by tools/thorax/heart_config.py', 'parts': kinds}, open(os.path.join(MODELS, 'heart', 'kinds.json'), 'w'), indent=0)
from collections import Counter
print(len(parts), 'parts', dict(Counter(k['kind'] for k in kinds.values())))
