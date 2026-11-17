"""Write tools/bones-rs/configs/upper-limb-muscles.json: the right upper-limb bones (BodyParts3D, as in
upper-limb.json) plus the right upper-limb muscles from Z-Anatomy (sources-local/zanat/z-bp3d.zip, made by export.py).
One part per muscle; a muscle's heads/parts are merged."""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
Z = lambda *names: ['Z_' + n for n in names]
# key, display name, Z files (right side)
MUSCLES = [
 # pectoral region and trunk to limb
 ('pec_major', 'Pectoralis major', Z('clavicular_head_of_pectoralis_major_muscle_r', 'sternocostal_head_of_pectoralis_major_muscle_r', 'abdominal_part_of_pectoralis_major_muscle_r')),
 ('pec_minor', 'Pectoralis minor', Z('pectoralis_minor_muscle_r')),
 ('subclavius', 'Subclavius', Z('subclavius_muscle_r')),
 ('serratus_ant', 'Serratus anterior', Z('serratus_anterior_muscle_r')),
 ('trapezius', 'Trapezius', Z('descending_part_of_trapezius_muscle_r', 'transverse_part_of_trapezius_muscle_r', 'ascending_part_of_trapezius_muscle_r')),
 ('lat_dorsi', 'Latissimus dorsi', Z('latissimus_dorsi_muscle_r')),
 ('lev_scap', 'Levator scapulae', Z('levator_scapulae_r')),
 ('rhomb_major', 'Rhomboid major', Z('rhomboid_major_muscle_r')),
 ('rhomb_minor', 'Rhomboid minor', Z('rhomboid_minor_muscle_r')),
 # scapular region
 ('deltoid', 'Deltoid', Z('clavicular_part_of_deltoid_muscle_r', 'acromial_part_of_deltoid_muscle_r', 'scapular_spinal_part_of_deltoid_muscle_r')),
 ('supraspinatus', 'Supraspinatus', Z('supraspinatus_muscle_r')),
 ('infraspinatus', 'Infraspinatus', Z('infraspinatus_muscle_r')),
 ('teres_minor', 'Teres minor', Z('teres_minor_muscle_r')),
 ('teres_major', 'Teres major', Z('teres_major_muscle_r')),
 ('subscapularis', 'Subscapularis', Z('subscapularis_muscle_r')),
 # arm
 ('biceps', 'Biceps brachii', Z('long_head_of_biceps_brachii_r', 'short_head_of_biceps_brachii_r')),
 ('coracobrachialis', 'Coracobrachialis', Z('coracobrachialis_muscle_r')),
 ('brachialis', 'Brachialis', Z('brachialis_muscle_r')),
 ('triceps', 'Triceps brachii', Z('long_head_of_triceps_brachii_r', 'lateral_head_of_triceps_brachii_r', 'medial_head_of_triceps_brachii_r')),
 ('anconeus', 'Anconeus', Z('anconeus_muscle_r')),
 # front of forearm
 ('pronator_teres', 'Pronator teres', Z('superficial_head_of_pronator_teres_r', 'deep_head_of_pronator_teres_r')),
 ('fcr', 'Flexor carpi radialis', Z('flexor_carpi_radialis_r')),
 ('palmaris_longus', 'Palmaris longus', Z('palmaris_longus_muscle_r')),
 ('fcu', 'Flexor carpi ulnaris', Z('humeral_head_of_flexor_carpi_ulnaris_r', 'ulnar_head_of_flexor_carpi_ulnaris_r')),
 ('fds', 'Flexor digitorum superficialis', Z('humero_ulnar_head_of_flexor_digitorum_superficialis_r', 'radial_head_of_flexor_digitorum_superficialis_r')),
 ('fdp', 'Flexor digitorum profundus', Z('flexor_digitorum_profundus_r')),
 ('fpl', 'Flexor pollicis longus', Z('flexor_pollicis_longus_r')),
 ('pronator_quadratus', 'Pronator quadratus', Z('pronator_quadratus_r')),
 # back of forearm
 ('brachioradialis', 'Brachioradialis', Z('brachioradialis_muscle_r')),
 ('ecrl', 'Extensor carpi radialis longus', Z('extensor_carpi_radialis_longus_r')),
 ('ecrb', 'Extensor carpi radialis brevis', Z('extensor_carpi_radialis_brevis_r')),
 ('ed', 'Extensor digitorum', Z('extensor_digitorum_r')),
 ('edm', 'Extensor digiti minimi', Z('extensor_digiti_minimi_r')),
 ('ecu', 'Extensor carpi ulnaris', Z('humeral_head_of_extensor_carpi_ulnaris_r', 'ulnar_head_of_extensor_carpi_ulnaris_r')),
 ('supinator', 'Supinator', Z('supinator_r')),
 ('apl', 'Abductor pollicis longus', Z('abductor_pollicis_longus_r')),
 ('epb', 'Extensor pollicis brevis', Z('extensor_pollicis_brevis_r')),
 ('epl', 'Extensor pollicis longus', Z('extensor_pollicis_longus_r')),
 ('ei', 'Extensor indicis', Z('extensor_indicis_r')),
 # hand
 ('apb', 'Abductor pollicis brevis', Z('abductor_pollicis_brevis_r')),
 ('fpb', 'Flexor pollicis brevis', Z('superficial_head_of_flexor_pollicis_brevis_r', 'deep_head_of_flexor_pollicis_brevis_r')),
 ('op', 'Opponens pollicis', Z('opponens_pollicis_muscle_r')),
 ('adductor_pollicis', 'Adductor pollicis', Z('oblique_head_of_adductor_pollicis_r', 'transverse_head_of_adductor_pollicis_r')),
 ('adm', 'Abductor digiti minimi', Z('abductor_digiti_minimi_of_hand_r')),
 ('fdm', 'Flexor digiti minimi brevis', Z('flexor_digiti_minimi_of_hand_r')),
 ('odm', 'Opponens digiti minimi', Z('opponens_digiti_minimi_muscle_of_hand_r')),
 ('lumbricals', 'Lumbricals', Z('lumbrical_muscles_of_hand_r')),
 ('palmar_interossei', 'Palmar interossei', Z('palmar_interossei_muscles_r')),
 ('dorsal_interossei', 'Dorsal interossei', Z('dorsal_interossei_muscles_of_hand_r')),
]
# connective tissue of the limb (sheets: drawn double-sided)
CONNECTIVE = [
 ('flexor_ret', 'Flexor retinaculum', Z('flexor_retinaculum_of_wrist_r')),
 ('extensor_ret', 'Extensor retinaculum', Z('extensor_retinaculum_of_wrist_r')),
 ('palmar_apon', 'Palmar aponeurosis', Z('palmar_aponeurosis_r')),
 ('interosseous_membrane', 'Interosseous membrane of forearm', Z('interosseous_membrane_of_forearm_r')),
 ('med_septum', 'Medial intermuscular septum of arm', Z('medial_intermuscular_septum_of_arm_r')),
 ('lat_septum', 'Lateral intermuscular septum of arm', Z('lateral_intermuscular_septum_of_arm_r')),
]
bones = json.load(open(os.path.join(ROOT, 'tools/bones-rs/configs/upper-limb.json')))
# axial bones the trunk-to-limb muscles reach (right side + midline), coarse, for context and attachment areas
axial = []
for g in ('thorax', 'spine'):
    for q in json.load(open(os.path.join(ROOT, 'tools/bones-rs/configs/%s.json' % g)))['parts']:
        if q['key'].endswith('_l') or 'disc' in q['key'] or any(a['key'] == 'ax_' + q['key'] for a in axial): continue
        axial.append(dict(q, key='ax_' + q['key'], group='context', error_mm=0.6))
axial += [{'key': 'ax_occipital', 'name': 'Occipital bone', 'fma': 'FMA52735', 'files': ['FMA52735'], 'group': 'context', 'error_mm': 0.6},
          {'key': 'ax_hip', 'name': 'Right hip bone', 'fma': 'FMA16586', 'files': ['FMA16586'], 'group': 'context', 'error_mm': 0.6}]
names = {l.split('\t')[0] for l in open(os.path.join(HERE, 'z-index.tsv'))}
missing = [f for _, _, fs in MUSCLES + CONNECTIVE for f in fs if f not in names]
assert not missing, missing
cfg = {'name': 'upper-limb-muscles', 'zips': ['../../../sources-local/bp3d/BodyParts3D_3.0_obj_95.zip', '../../../sources-local/zanat/z-bp3d.zip'],
       'out': '../../../anatomy/models/upper-limb-muscles', 'error_mm': 0.2, 'contact_mm': 1.5, 'contacts_across_groups_only': True,
       'source': 'Bones: BodyParts3D, (c) The Database Center for Life Science, CC BY-SA 2.1 Japan. Muscles and connective tissue: Z-Anatomy, CC BY-SA 4.0 (from BodyParts3D), moved into the BodyParts3D frame',
       'parts': [dict(p, group='bone') for p in bones['parts']] + axial +
                [{'key': k, 'name': n, 'fma': '', 'files': fs, 'group': 'muscle', 'error_mm': 0.35} for k, n, fs in MUSCLES] +
                [{'key': k, 'name': n, 'fma': '', 'files': fs, 'group': 'connective', 'error_mm': 0.35} for k, n, fs in CONNECTIVE]}
json.dump(cfg, open(os.path.join(ROOT, 'tools/bones-rs/configs/upper-limb-muscles.json'), 'w'), indent=1)
print(len(cfg['parts']), 'parts')
