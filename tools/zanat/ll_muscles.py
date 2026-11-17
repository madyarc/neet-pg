"""Write tools/bones-rs/configs/lower-limb-muscles.json: the right lower-limb bones (BodyParts3D, as in
lower-limb.json), the lower spine as context, and the right lower-limb muscles and connective tissue from Z-Anatomy
(sources-local/zanat/z-bp3d.zip, made by export.py). One part per muscle; heads/parts are merged."""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
Z = lambda *names: ['Z_' + n + '_r' for n in names]
MUSCLES = [
 # iliac region and gluteal region
 ('psoas_major', 'Psoas major', Z('psoas_major')),
 ('iliacus', 'Iliacus', Z('iliacus_muscle')),
 ('glut_max', 'Gluteus maximus', Z('gluteus_maximus_muscle')),
 ('glut_med', 'Gluteus medius', Z('gluteus_medius_muscle')),
 ('glut_min', 'Gluteus minimus', Z('gluteus_minimus_muscle')),
 ('tfl', 'Tensor fasciae latae', Z('tensor_fasciae_latae')),
 ('piriformis', 'Piriformis', Z('piriformis_muscle')),
 ('sup_gemellus', 'Superior gemellus', Z('superior_gemellus_muscle')),
 ('obt_int', 'Obturator internus', Z('obturator_internus')),
 ('inf_gemellus', 'Inferior gemellus', Z('inferior_gemellus_muscle')),
 ('quad_fem', 'Quadratus femoris', Z('quadratus_femoris_muscle')),
 ('obt_ext', 'Obturator externus', Z('obturator_externus')),
 # front of thigh
 ('sartorius', 'Sartorius', Z('sartorius_muscle')),
 ('rectus_fem', 'Rectus femoris', Z('rectus_femoris_muscle')),
 ('vastus_lat', 'Vastus lateralis', Z('vastus_lateralis_muscle')),
 ('vastus_med', 'Vastus medialis', Z('vastus_medialis_muscle')),
 ('vastus_int', 'Vastus intermedius', Z('vastus_intermedius_muscle')),
 # medial thigh
 ('pectineus', 'Pectineus', Z('pectineus_muscle')),
 ('add_longus', 'Adductor longus', Z('adductor_longus')),
 ('add_brevis', 'Adductor brevis', Z('adductor_brevis')),
 ('add_magnus', 'Adductor magnus', Z('adductor_magnus', 'adductor_minimus')),
 ('gracilis', 'Gracilis', Z('gracilis_muscle')),
 # back of thigh
 ('biceps_fem', 'Biceps femoris', Z('long_head_of_biceps_femoris', 'short_head_of_biceps_femoris')),
 ('semitend', 'Semitendinosus', Z('semitendinosus_muscle')),
 ('semimemb', 'Semimembranosus', Z('semimembranosus_muscle')),
 # front of leg
 ('tib_ant', 'Tibialis anterior', Z('tibialis_anterior_muscle')),
 ('ehl', 'Extensor hallucis longus', Z('extensor_hallucis_longus')),
 ('edl', 'Extensor digitorum longus', Z('extensor_digitorum_longus', 'tendon_of_extensor_digitorum_longus')),
 ('fib_tertius', 'Fibularis tertius', Z('fibularis_tertius_muscle')),
 # lateral leg
 ('fib_longus', 'Fibularis longus', Z('fibularis_longus_muscle')),
 ('fib_brevis', 'Fibularis brevis', Z('fibularis_brevis_muscle')),
 # back of leg
 ('gastrocnemius', 'Gastrocnemius', Z('medial_head_of_gastrocnemius', 'lateral_head_of_gastrocnemius')),
 ('soleus', 'Soleus', Z('soleus_muscle')),
 ('plantaris', 'Plantaris', Z('plantaris_muscle')),
 ('popliteus', 'Popliteus', Z('popliteus_muscle')),
 ('fhl', 'Flexor hallucis longus', Z('flexor_hallucis_longus')),
 ('fdl', 'Flexor digitorum longus', Z('flexor_digitorum_longus')),
 ('tib_post', 'Tibialis posterior', Z('tibialis_posterior_muscle')),
 # foot
 ('edb', 'Extensor digitorum brevis', Z('extensor_digitorum_brevis')),
 ('ehb', 'Extensor hallucis brevis', Z('extensor_hallucis_brevis')),
 ('abd_hal', 'Abductor hallucis', Z('abductor_hallucis')),
 ('fdb', 'Flexor digitorum brevis', Z('flexor_digitorum_brevis')),
 ('abd_dm', 'Abductor digiti minimi', Z('abductor_digiti_minimi_of_foot')),
 ('quad_plantae', 'Quadratus plantae', Z('quadratus_plantae_muscle')),
 ('lumbricals_f', 'Lumbricals', Z('lumbrical_muscles_of_foot')),
 ('fhb', 'Flexor hallucis brevis', Z('medial_head_of_flexor_hallucis_brevis', 'lateral_head_of_flexor_hallucis_brevis')),
 ('add_hal', 'Adductor hallucis', Z('oblique_head_of_adductor_hallucis', 'transverse_head_of_adductor_hallucis')),
 ('fdm_f', 'Flexor digiti minimi brevis', Z('flexor_digiti_minimi_of_foot')),
 ('plantar_int', 'Plantar interossei', Z('plantar_interossei_muscles')),
 ('dorsal_int_f', 'Dorsal interossei', Z('dorsal_interossei_muscles_of_foot')),
]
CONNECTIVE = [
 ('it_tract', 'Iliotibial tract', Z('iliotibial_tract')),
 ('calc_tendon', 'Calcaneal (Achilles) tendon', Z('calcaneal_tendon')),
 ('plantar_apon', 'Plantar aponeurosis', Z('plantar_aponeurosis')),
 ('sup_ext_ret', 'Superior extensor retinaculum', Z('superior_extensor_retinaculum_of_ankle')),
 ('inf_ext_ret', 'Inferior extensor retinaculum', Z('inferior_extensor_retinaculum_of_ankle')),
 ('flex_ret_f', 'Flexor retinaculum (ankle)', Z('flexor_retinaculum_of_ankle')),
 ('sup_fib_ret', 'Superior fibular retinaculum', Z('superior_fibular_retinaculum')),
 ('inf_fib_ret', 'Inferior fibular retinaculum', Z('inferior_fibular_retinaculum')),
]
bones = json.load(open(os.path.join(ROOT, 'tools/bones-rs/configs/lower-limb.json')))
axial = []
for q in json.load(open(os.path.join(ROOT, 'tools/bones-rs/configs/spine.json')))['parts']:
    if q['key'] in ('t12', 'l1', 'l2', 'l3', 'l4', 'l5', 'sacrum', 'coccyx'):
        axial.append(dict(q, key='ax_' + q['key'], group='context', error_mm=0.6))
names = {l.split('\t')[0] for l in open(os.path.join(HERE, 'z-index.tsv'))}
missing = [f for _, _, fs in MUSCLES + CONNECTIVE for f in fs if f not in names]
assert not missing, missing
cfg = {'name': 'lower-limb-muscles', 'zips': ['../../../sources-local/bp3d/BodyParts3D_3.0_obj_95.zip', '../../../sources-local/zanat/z-bp3d.zip'],
       'out': '../../../anatomy/models/lower-limb-muscles', 'error_mm': 0.2, 'contact_mm': 1.5, 'contacts_across_groups_only': True,
       'source': 'Bones: BodyParts3D, (c) The Database Center for Life Science, CC BY-SA 2.1 Japan. Muscles and connective tissue: Z-Anatomy, CC BY-SA 4.0 (from BodyParts3D), moved into the BodyParts3D frame',
       'parts': [dict(p, group='bone') for p in bones['parts']] + axial +
                [{'key': k, 'name': n, 'fma': '', 'files': fs, 'group': 'muscle', 'error_mm': 0.35} for k, n, fs in MUSCLES] +
                [{'key': k, 'name': n, 'fma': '', 'files': fs, 'group': 'connective', 'error_mm': 0.35} for k, n, fs in CONNECTIVE]}
json.dump(cfg, open(os.path.join(ROOT, 'tools/bones-rs/configs/lower-limb-muscles.json'), 'w'), indent=1)
print(len(cfg['parts']), 'parts;', len(axial), 'axial')
