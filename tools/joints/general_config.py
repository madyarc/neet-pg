"""Config for the general joints page (anatomy/general/joints.html): the bones of one example joint per type.
usage: python3 -I general_config.py   -> tools/bones-rs/configs/joints-general.json"""
import json, os
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
CFG = os.path.join(ROOT, 'tools', 'bones-rs', 'configs')
src = {}
for f in ['upper-limb', 'lower-limb', 'skull', 'spine', 'thorax']:
    for p in json.load(open(os.path.join(CFG, f + '.json')))['parts']:
        src.setdefault(p['key'], p)
src['hip_l'] = {'key': 'hip_l', 'name': 'Left hip bone', 'fma': 'FMA16587', 'files': ['FMA16587']}
HAND = ['scaphoid', 'lunate', 'triquetral', 'pisiform', 'trapezium', 'trapezoid', 'capitate', 'hamate',
        'mc1', 'mc2', 'mc3', 'mc4', 'mc5', 'pp1', 'dp1', 'pp2', 'mp2', 'dp2', 'pp3', 'mp3', 'dp3', 'pp4', 'mp4', 'dp4',
        'pp5', 'mp5', 'dp5']
BONES = ['hip', 'hip_l', 'femur', 'tibia', 'fibula', 'talus', 'humerus', 'radius', 'ulna', 'clavicle', 'scapula'] + HAND + \
        ['c1', 'c2', 'l4', 'l5', 'disc_l4', 'frontal', 'parietal_r', 'parietal_l', 'occipital', 'mandible',
         'manubrium', 'sternum_body', 'rib1_r', 'cc1_r', 'rib2_r', 'cc2_r']
# lower right teeth (BodyParts3D 3.0 element ids, from parts_list_e.txt)
TEETH = [('t_li1', 'Lower right central incisor', 'FMA57142'), ('t_li2', 'Lower right lateral incisor', 'FMA57140'),
         ('t_lc', 'Lower right canine', 'FMA55686'), ('t_lp1', 'Lower right first premolar', 'FMA55694'),
         ('t_lp2', 'Lower right second premolar', 'FMA55695'), ('t_lm1', 'Lower right first molar', 'FMA55705'),
         ('t_lm2', 'Lower right second molar', 'FMA55706')]
# soft parts from Z-Anatomy (moved into the BodyParts3D frame, see tools/zanat)
SOFT = [('interpubic_disc', 'Interpubic disc', 'Z_interpubic_disc'),
        ('men_med', 'Medial meniscus', 'Z_medial_meniscus_r'), ('men_lat', 'Lateral meniscus', 'Z_lateral_meniscus_r')]
parts = []
for k in BONES:
    p = src[k]; parts.append({'key': k, 'name': p['name'], 'fma': p['fma'], 'files': p['files'], 'group': 'bone'})
for k, n, f in TEETH: parts.append({'key': k, 'name': n, 'fma': f, 'files': [f], 'group': 'bone'})
for k, n, f in SOFT: parts.append({'key': k, 'name': n, 'fma': '', 'files': [f], 'group': 'soft'})
cfg = {'name': 'joints-general',
       'zips': ['../../../sources-local/bp3d/BodyParts3D_3.0_obj_95.zip', '../../../sources-local/zanat/z-bp3d.zip'],
       'out': '../../../anatomy/models/joints-general', 'error_mm': 0.25, 'contact_mm': 1.5, 'pack': True,
       'source': 'Bones and teeth: BodyParts3D, (c) The Database Center for Life Science, CC BY-SA 2.1 Japan. '
                 'Menisci and interpubic disc: Z-Anatomy, CC BY-SA 4.0 (from BodyParts3D)',
       'parts': parts}
json.dump(cfg, open(os.path.join(CFG, 'joints-general.json'), 'w'), indent=1)
print(len(parts), 'parts')
