"""Config for the lower-limb joints page: BodyParts3D bones of the right lower limb
its cartilage for the sternoclavicular joint) and the Z-Anatomy joint parts exported with their modifiers applied
(tools/zanat/export_mod.py -> sources-local/zanat/z-bp3d-joints-ll.zip, index tools/zanat/z-index-joints-ll.tsv).
usage: python3 -I ul_config.py -> tools/bones-rs/configs/ll-joints.json"""
import json, os, csv
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
CFG = os.path.join(ROOT, 'tools', 'bones-rs', 'configs')
parts = []
for p in json.load(open(os.path.join(CFG, 'lower-limb.json')))['parts']:
    if p['key'] == 'sesamoid': continue
    parts.append({'key': p['key'], 'name': p['name'], 'fma': p['fma'], 'files': p['files'], 'group': 'bone'})
# not about the limb joints: pelvic ligaments (sacro-iliac page later), the child's triradiate cartilage, hip retinacula
SKIP = ('sacro_iliac', 'sacrospinous', 'sacrotuberous', 'iliolumbar', 'obturator_membrane', 'triradiate', 'frenula')
rows = list(csv.DictReader(open(os.path.join(ROOT, 'tools', 'zanat', 'z-index-joints-ll.tsv')), delimiter='\t'))
for r in rows:
    f = r['file']; key = f[2:].removesuffix('_r')
    if any(x in key for x in SKIP): continue
    name = r['object'].removesuffix('.r')
    grp = 'bursa' if 'Bursae' in r['collections'] else 'joint'
    # thin shells (0.5 mm Solidify): keep them nearly unsimplified so the two faces do not collapse
    parts.append({'key': key, 'name': name, 'fma': '', 'files': [f], 'group': grp, 'error_mm': 0.05 if 'Solidify' in r['modifiers'] else 0.15})
cfg = {'name': 'll-joints',
       'zips': ['../../../sources-local/bp3d/BodyParts3D_3.0_obj_95.zip', '../../../sources-local/zanat/z-bp3d-joints-ll.zip'],
       'out': '../../../anatomy/models/ll-joints', 'error_mm': 0.2, 'contact_mm': 1.5, 'contacts_across_groups_only': True,
       'pack': True,
       'source': 'Bones: BodyParts3D, (c) The Database Center for Life Science, CC BY-SA 2.1 Japan. Ligaments, capsules, '
                 'discs, labrum, bursae: Z-Anatomy, CC BY-SA 4.0 (from BodyParts3D), modifiers applied, moved into the BodyParts3D frame',
       'parts': parts}
json.dump(cfg, open(os.path.join(CFG, 'll-joints.json'), 'w'), indent=1)
print(len(parts), 'parts')
