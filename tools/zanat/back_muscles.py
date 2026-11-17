"""Write tools/bones-rs/configs/back-muscles.json: the vertebral column, occipital and right temporal bones, right ribs
and hip bone (BodyParts3D) and the right deep back muscles and thoracolumbar fascia from Z-Anatomy. Heads/parts merged.
(Z-Anatomy has no semispinalis capitis: the page gives it as text only.)"""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(os.path.dirname(HERE))
Z = lambda *n: ['Z_' + x + '_r' for x in n]
MUSCLES = [
 ('serr_post_sup', 'Serratus posterior superior', Z('serratus_posterior_superior_muscle')),
 ('serr_post_inf', 'Serratus posterior inferior', Z('serratus_posterior_inferior_muscle')),
 ('splenius_cap', 'Splenius capitis', Z('splenius_capitis_muscle')),
 ('splenius_cerv', 'Splenius cervicis', Z('splenius_colli_muscle')),
 ('iliocostalis', 'Iliocostalis', Z('iliocostalis_lumborum_muscle', 'iliocostalis_thoracis_muscle', 'iliocostalis_colli_muscle')),
 ('longissimus', 'Longissimus', Z('longissimus_thoracis_muscle', 'longissimus_colli_muscle', 'longissimus_capitis_muscle')),
 ('spinalis', 'Spinalis', Z('spinalis_thoracis_muscle', 'spinalis_colli_muscle', 'spinalis_capitis_muscle')),
 ('semispinalis', 'Semispinalis (thoracis, cervicis)', Z('semispinalis_thoracis_muscle', 'semispinalis_colli_muscle')),
 ('multifidus', 'Multifidus', Z('multifidus_lumborum_muscle', 'multifidus_thoracis_muscle', 'multifidus_colli_muscle')),
 ('rotatores', 'Rotatores', Z('rotatores')),
 ('interspinales', 'Interspinales', Z('interspinales_colli_muscles', 'interspinales_thoracis_muscles', 'interspinales_lumborum_muscles')),
 ('intertransversarii', 'Intertransversarii (lumbar)', Z('dorsal_parts_of_lateral_intertransversarii_lumborum_muscles', 'ventral_parts_of_lateral_intertransversarii_lumborum_muscles')),
 ('rcp_major', 'Rectus capitis posterior major', Z('rectus_posterior_major_capitis_muscle')),
 ('rcp_minor', 'Rectus capitis posterior minor', Z('rectus_posterior_minor_capitis_muscle')),
 ('obl_cap_sup', 'Obliquus capitis superior', Z('obliquus_superior_capitis_muscle')),
 ('obl_cap_inf', 'Obliquus capitis inferior', Z('obliquus_inferior_capitis_muscle')),
 ('quad_lumb', 'Quadratus lumborum', Z('quadratus_lumborum_muscle')),
]
CONNECTIVE = [
 ('tlf_post', 'Thoracolumbar fascia: posterior layer', Z('posterior_layer_of_thoracolumbar_fascia')),
 ('tlf_mid', 'Thoracolumbar fascia: middle layer', Z('middle_layer_of_thoracolumbar_fascia')),
 ('tlf_ant', 'Thoracolumbar fascia: anterior layer', Z('anterior_layer_of_thoracolumbar_fascia')),
]
bones = []
for q in json.load(open(os.path.join(ROOT, 'tools/bones-rs/configs/spine.json')))['parts']:
    if 'disc' not in q['key']: bones.append(dict(q, group='bone', error_mm=0.3))
for q in json.load(open(os.path.join(ROOT, 'tools/bones-rs/configs/thorax.json')))['parts']:
    if q['key'].startswith('rib') and q['key'].endswith('_r'): bones.append(dict(q, group='bone', error_mm=0.4))
bones += [{'key': 'occipital', 'name': 'Occipital bone', 'fma': 'FMA52735', 'files': ['FMA52735'], 'group': 'bone', 'error_mm': 0.3},
          {'key': 'temporal_r', 'name': 'Right temporal bone', 'fma': 'FMA52738', 'files': ['FMA52738'], 'group': 'bone', 'error_mm': 0.3},
          {'key': 'hip', 'name': 'Right hip bone', 'fma': 'FMA16586', 'files': ['FMA16586'], 'group': 'bone', 'error_mm': 0.4}]
names = {l.split('\t')[0] for l in open(os.path.join(HERE, 'z-index.tsv'))}
missing = [f for _, _, fs in MUSCLES + CONNECTIVE for f in fs if f not in names]; assert not missing, missing
cfg = {'name': 'back-muscles', 'zips': ['../../../sources-local/bp3d/BodyParts3D_3.0_obj_95.zip', '../../../sources-local/zanat/z-bp3d.zip'],
       'out': '../../../anatomy/models/back-muscles', 'error_mm': 0.3, 'contact_mm': 1.5, 'contacts_across_groups_only': True,
       'source': 'Bones: BodyParts3D, (c) The Database Center for Life Science, CC BY-SA 2.1 Japan. Muscles and fascia: Z-Anatomy, CC BY-SA 4.0 (from BodyParts3D), moved into the BodyParts3D frame',
       'parts': bones + [{'key': k, 'name': n, 'fma': '', 'files': fs, 'group': 'muscle', 'error_mm': 0.35} for k, n, fs in MUSCLES] +
                [{'key': k, 'name': n, 'fma': '', 'files': fs, 'group': 'connective', 'error_mm': 0.35} for k, n, fs in CONNECTIVE]}
json.dump(cfg, open(os.path.join(ROOT, 'tools/bones-rs/configs/back-muscles.json'), 'w'), indent=1)
print(len(cfg['parts']), 'parts', len(bones), 'bones')
