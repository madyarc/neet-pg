"""Config for the page on the joints of the jaw, spine and pelvis: BodyParts3D skull bones (temporomandibular joint),
vertebrae, discs, sacrum and both hip bones, and the Z-Anatomy joint parts exported with their modifiers applied
(tools/zanat/export_mod.py -> sources-local/zanat/z-bp3d-joints-ax.zip, index tools/zanat/z-index-joints-ax.tsv).
usage: python3 -I ax_config.py -> tools/bones-rs/configs/ax-joints.json"""
import json, os, csv
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
CFG = os.path.join(ROOT, 'tools', 'bones-rs', 'configs')
parts = []
def add(cfgname, keys=None):
    for p in json.load(open(os.path.join(CFG, cfgname)))['parts']:
        if keys is None or p['key'] in keys:
            parts.append({'key': p['key'], 'name': p['name'], 'fma': p['fma'], 'files': p['files'], 'group': 'bone'})
add('skull.json', ['temporal_r', 'temporal_l', 'occipital', 'mandible', 'sphenoid'])
add('spine.json')
add('lower-limb.json', ['hip'])
parts.append({'key': 'hip_l', 'name': 'Left hip bone', 'fma': 'FMA16587', 'files': ['FMA16587'], 'group': 'bone'})
for r in csv.DictReader(open(os.path.join(ROOT, 'tools', 'zanat', 'z-index-joints-ax.tsv')), delimiter='\t'):
    # Z-Anatomy's lateral temporomandibular ligament '.l' is the one on the right side (its '.r' is on the left): exported '.l'
    f = r['file']; key = f[2:].removesuffix('_r').removesuffix('_l')
    parts.append({'key': key, 'name': r['object'].removesuffix('.r').removesuffix('.l'), 'fma': '', 'files': [f], 'group': 'joint',
                  'error_mm': 0.1 if 'Solidify' in r['modifiers'] else 0.15})
cfg = {'name': 'ax-joints',
       'zips': ['../../../sources-local/bp3d/BodyParts3D_3.0_obj_95.zip', '../../../sources-local/zanat/z-bp3d-joints-ax.zip'],
       'out': '../../../anatomy/models/ax-joints', 'error_mm': 0.25, 'contact_mm': 1.5, 'contacts_across_groups_only': True,
       'pack': True,
       'source': 'Bones and discs: BodyParts3D, (c) The Database Center for Life Science, CC BY-SA 2.1 Japan. Ligaments, '
                 'capsule, discs, nucleus pulposus: Z-Anatomy, CC BY-SA 4.0 (from BodyParts3D), modifiers applied, moved into the BodyParts3D frame',
       'parts': parts}
json.dump(cfg, open(os.path.join(CFG, 'ax-joints.json'), 'w'), indent=1)
print(len(parts), 'parts')
