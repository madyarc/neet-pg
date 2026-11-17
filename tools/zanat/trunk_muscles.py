"""Write tools/bones-rs/configs/trunk-muscles.json: the thoracic cage, lumbar spine, sacrum and both hip bones
(BodyParts3D), the right thoracic- and abdominal-wall muscles, the diaphragm, the right pelvic diaphragm and the
inguinal ligament / linea alba from Z-Anatomy."""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(os.path.dirname(HERE))
Z = lambda *n: ['Z_' + x + '_r' for x in n]
MUSCLES = [
 ('ext_intercostal', 'External intercostals', Z('external_intercostal_muscles')),
 ('int_intercostal', 'Internal intercostals', Z('internal_intercostal_muscles')),
 ('innermost_intercostal', 'Innermost intercostals', Z('innermost_intercostal_muscles')),
 ('transversus_thoracis', 'Transversus thoracis', Z('transversus_thoracis_muscle')),
 ('diaphragm', 'Diaphragm', ['Z_diaphragm']),
 ('ext_oblique', 'External oblique', Z('external_abdominal_oblique_muscle')),
 ('int_oblique', 'Internal oblique', Z('internal_abdominal_oblique_muscle')),
 ('transversus_abd', 'Transversus abdominis', Z('transversus_abdominis_muscle')),
 ('rectus_abd', 'Rectus abdominis', Z('rectus_abdominis_muscle')),
 ('pyramidalis', 'Pyramidalis', Z('pyramidalis_muscle')),
 ('pubococcygeus', 'Pubococcygeus (levator ani)', Z('pubococcygeus_muscle')),
 ('iliococcygeus', 'Iliococcygeus (levator ani)', Z('iliococcygeus_muscle')),
 ('coccygeus', 'Coccygeus', Z('coccygeus_muscle')),
]
CONNECTIVE = [
 ('inguinal_lig', 'Inguinal ligament', Z('inguinal_ligament')),
 ('linea_alba', 'Linea alba', ['Z_linea_alba']),
 ('tendinous_arch', 'Tendinous arch of levator ani', Z('tendinous_arch_of_levator_ani')),
]
bones = []
for q in json.load(open(os.path.join(ROOT, 'tools/bones-rs/configs/thorax.json')))['parts']:
    bones.append(dict(q, group='bone', error_mm=0.4))
have = {b['key'] for b in bones}
for q in json.load(open(os.path.join(ROOT, 'tools/bones-rs/configs/spine.json')))['parts']:
    if 'disc' not in q['key'] and q['key'] not in have and (q['key'].startswith('l') or q['key'] in ('sacrum', 't12', 't11')):
        bones.append(dict(q, group='bone', error_mm=0.4))
bones += [{'key': 'hip', 'name': 'Right hip bone', 'fma': 'FMA16586', 'files': ['FMA16586'], 'group': 'bone', 'error_mm': 0.4},
          {'key': 'hip_l', 'name': 'Left hip bone', 'fma': 'FMA16587', 'files': ['FMA16587'], 'group': 'bone', 'error_mm': 0.4}]
names = {l.split('\t')[0] for l in open(os.path.join(HERE, 'z-index.tsv'))}
missing = [f for _, _, fs in MUSCLES + CONNECTIVE for f in fs if f not in names]; assert not missing, missing
cfg = {'name': 'trunk-muscles', 'zips': ['../../../sources-local/bp3d/BodyParts3D_3.0_obj_95.zip', '../../../sources-local/zanat/z-bp3d.zip'],
       'out': '../../../anatomy/models/trunk-muscles', 'error_mm': 0.4, 'contact_mm': 1.5, 'contacts_across_groups_only': True,
       'source': 'Bones: BodyParts3D, (c) The Database Center for Life Science, CC BY-SA 2.1 Japan. Muscles and connective tissue: Z-Anatomy, CC BY-SA 4.0 (from BodyParts3D), moved into the BodyParts3D frame',
       'parts': bones + [{'key': k, 'name': n, 'fma': '', 'files': fs, 'group': 'muscle', 'error_mm': 0.4} for k, n, fs in MUSCLES] +
                [{'key': k, 'name': n, 'fma': '', 'files': fs, 'group': 'connective', 'error_mm': 0.4} for k, n, fs in CONNECTIVE]}
json.dump(cfg, open(os.path.join(ROOT, 'tools/bones-rs/configs/trunk-muscles.json'), 'w'), indent=1)
print(len(cfg['parts']), 'parts', len(bones), 'bones')
