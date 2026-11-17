"""Write tools/bones-rs/configs/head-neck-muscles.json: skull, hyoid, cervical spine, clavicles, manubrium, first ribs,
right scapula (BodyParts3D), laryngeal cartilages and the right eyeball (Z-Anatomy, extra zip) as context, and the
head and neck muscles from Z-Anatomy (right side; midline muscles whole). Not in Z-Anatomy (text only on the page):
tensor and levator veli palatini, styloglossus, palatoglossus, intrinsic tongue muscles, salpingopharyngeus."""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(os.path.dirname(HERE))
names = {l.split('\t')[0] for l in open(os.path.join(HERE, 'z-index.tsv'))} | {l.split('\t')[0] for l in open(os.path.join(HERE, 'z-index-extra.tsv'))}
def Z(*slugs):
    out = []
    for s in slugs:
        f = next((c for c in ('Z_' + s + '_r', 'Z_' + s) if c in names), None)
        assert f, s
        out.append(f)
    return out
MUSCLES = [
 ('occipitofrontalis', 'Occipitofrontalis', Z('frontalis_muscle', 'occipitalis_muscle')),
 ('orb_oculi', 'Orbicularis oculi', Z('orbital_part_of_orbicularis_oculi', 'palpebral_part_of_orbicularis_oculi')),
 ('corrugator', 'Corrugator supercilii', Z('corrugator_supercilii')),
 ('procerus', 'Procerus', Z('procerus_muscle')),
 ('nasalis', 'Nasalis', Z('nasalis_muscle')),
 ('orb_oris', 'Orbicularis oris', Z('orbicularis_oris_muscle')),
 ('buccinator', 'Buccinator', Z('bucinator')),
 ('zyg_major', 'Zygomaticus major', Z('zygomaticus_major_muscle')),
 ('zyg_minor', 'Zygomaticus minor', Z('zygomaticus_minor_muscle')),
 ('lev_lab_sup', 'Levator labii superioris', Z('levator_labii_superioris')),
 ('lev_lab_alae', 'Levator labii superioris alaeque nasi', Z('levator_nasolabialis')),
 ('lev_ang_oris', 'Levator anguli oris', Z('levator_anguli_oris')),
 ('dep_ang_oris', 'Depressor anguli oris', Z('depressor_anguli_oris')),
 ('dep_lab_inf', 'Depressor labii inferioris', Z('depressor_labii_inferioris')),
 ('mentalis', 'Mentalis', Z('mentalis_muscle')),
 ('risorius', 'Risorius', Z('risorius_muscle')),
 ('platysma', 'Platysma', Z('platysma')),
 ('masseter', 'Masseter', Z('superficial_part_of_masseter', 'deep_part_of_masseter')),
 ('temporalis', 'Temporalis', Z('temporalis_muscle')),
 ('lat_pterygoid', 'Lateral pterygoid', Z('superior_head_of_lateral_pterygoid_muscle', 'inferior_head_of_lateral_pterygoid_muscle')),
 ('med_pterygoid', 'Medial pterygoid', Z('medial_pterygoid_muscle')),
 ('scm', 'Sternocleidomastoid', Z('sternocleidomastoid_muscle')),
 ('digastric', 'Digastric', Z('anterior_belly_of_digastric_muscle', 'posterior_belly_of_digastric_muscle', 'intermediate_tendon_of_digastric_muscle')),
 ('stylohyoid', 'Stylohyoid', Z('stylohyoid_muscle')),
 ('mylohyoid', 'Mylohyoid', Z('mylohyoid_muscle')),
 ('geniohyoid', 'Geniohyoid', Z('geniohyoid_muscle')),
 ('sternohyoid', 'Sternohyoid', Z('sternohyoid_muscle')),
 ('sternothyroid', 'Sternothyroid', Z('sternothyroid_muscle')),
 ('thyrohyoid', 'Thyrohyoid', Z('thyrohyoid_muscle')),
 ('omohyoid', 'Omohyoid', Z('omohyoid_muscle')),
 ('scal_ant', 'Scalenus anterior', Z('scalenus_anterior_muscle')),
 ('scal_med', 'Scalenus medius', Z('scalenus_medius_muscle')),
 ('scal_post', 'Scalenus posterior', Z('scalenus_posterior_muscle')),
 ('longus_colli', 'Longus colli', Z('longus_colli_muscle')),
 ('longus_capitis', 'Longus capitis', Z('longus_capitis_muscle')),
 ('rect_cap_ant', 'Rectus capitis anterior', Z('rectus_anterior_capitis_muscle')),
 ('rect_cap_lat', 'Rectus capitis lateralis', Z('rectus_lateralis_capitis_muscle')),
 ('sup_rectus', 'Superior rectus', Z('superior_rectus_muscle')),
 ('inf_rectus', 'Inferior rectus', Z('inferior_rectus_muscle')),
 ('med_rectus', 'Medial rectus', Z('medial_rectus_muscle')),
 ('lat_rectus', 'Lateral rectus', Z('lateral_rectus_muscle')),
 ('sup_oblique', 'Superior oblique', Z('superior_oblique_muscle')),
 ('inf_oblique', 'Inferior oblique', Z('inferior_oblique_muscle')),
 ('lps', 'Levator palpebrae superioris', Z('levator_palpebrae_superioris')),
 ('genioglossus', 'Genioglossus', Z('genioglossus_muscle')),
 ('hyoglossus', 'Hyoglossus', Z('hyoglossus_muscle')),
 ('sup_constrictor', 'Superior constrictor', Z('superior_pharyngeal_constrictor')),
 ('mid_constrictor', 'Middle constrictor', Z('middle_pharyngeal_constrictor')),
 ('inf_constrictor', 'Inferior constrictor', Z('inferior_pharyngeal_constrictor')),
 ('stylopharyngeus', 'Stylopharyngeus', Z('stylopharyngeus_muscle')),
 ('palatopharyngeus', 'Palatopharyngeus', Z('palatopharyngeus_muscle')),
 ('post_cricoaryt', 'Posterior cricoarytenoid', Z('posterior_crico_arytenoid_muscle')),
 ('lat_cricoaryt', 'Lateral cricoarytenoid', Z('lateral_crico_arytenoid_muscle')),
 ('trans_aryt', 'Transverse arytenoid', Z('transverse_arytenoid_muscle')),
 ('obl_aryt', 'Oblique arytenoid', Z('ary_epiglottic_part_of_oblique_arytenoid_muscle')),
 ('thyroaryt', 'Thyroarytenoid', Z('external_part_of_thyro_arytenoid_muscle', 'thyro_epiglottic_part_of_thyro_arytenoid_muscle')),
 ('cricothyroid', 'Cricothyroid', Z('straight_part_of_cricothyroid_muscle', 'oblique_part_of_cricothyroid_muscle')),
]
CONNECTIVE = [
 ('epicranial_apon', 'Epicranial aponeurosis', Z('epicranial_aponeurosis')),
 ('investing_fascia', 'Investing layer of deep cervical fascia', Z('superficial_investing_cervical_fascia')),
]
CONTEXT = [
 ('thyroid_cart', 'Thyroid cartilage', ['Z_thyroid_cartilage']), ('cricoid_cart', 'Cricoid cartilage', ['Z_cricoid_cartilage']),
 ('aryt_cart_r', 'Right arytenoid cartilage', ['Z_arytenoid_cartilage_r']), ('aryt_cart_l', 'Left arytenoid cartilage', ['Z_arytenoid_cartilage_l']),
 ('epiglottis', 'Epiglottis', ['Z_epiglottis']), ('eyeball', 'Right eyeball', ['Z_sclera_r', 'Z_cornea_r']),
]
bones = [dict(q, group='bone', error_mm=0.3) for q in json.load(open(os.path.join(ROOT, 'tools/bones-rs/configs/skull-detail.json')))['parts']]
for q in json.load(open(os.path.join(ROOT, 'tools/bones-rs/configs/spine.json')))['parts']:
    if q['key'] in ('c1', 'c2', 'c3', 'c4', 'c5', 'c6', 'c7', 't1', 't2'): bones.append(dict(q, group='bone', error_mm=0.3))
for q in json.load(open(os.path.join(ROOT, 'tools/bones-rs/configs/thorax.json')))['parts']:
    if q['key'] in ('manubrium', 'rib1_r', 'rib1_l', 'rib2_r', 'rib2_l', 'cc1_r', 'cc1_l'): bones.append(dict(q, group='bone', error_mm=0.4))
bones += [{'key': 'clavicle', 'name': 'Right clavicle', 'fma': 'FMA13322', 'files': ['FMA13322'], 'group': 'bone', 'error_mm': 0.3},
          {'key': 'clavicle_l', 'name': 'Left clavicle', 'fma': 'FMA13323', 'files': ['FMA13323'], 'group': 'bone', 'error_mm': 0.3},
          {'key': 'scapula', 'name': 'Right scapula', 'fma': 'FMA13395', 'files': ['FMA13395'], 'group': 'bone', 'error_mm': 0.4}]
cfg = {'name': 'head-neck-muscles', 'zips': ['../../../sources-local/bp3d/BodyParts3D_3.0_obj_95.zip', '../../../sources-local/zanat/z-bp3d.zip', '../../../sources-local/zanat/z-bp3d-extra.zip'],
       'out': '../../../anatomy/models/head-neck-muscles', 'error_mm': 0.3, 'contact_mm': 1.5, 'contacts_across_groups_only': True,
       'source': 'Bones: BodyParts3D, (c) The Database Center for Life Science, CC BY-SA 2.1 Japan. Muscles, cartilages, eyeball and fascia: Z-Anatomy, CC BY-SA 4.0 (from BodyParts3D), moved into the BodyParts3D frame',
       'parts': bones + [{'key': k, 'name': n, 'fma': '', 'files': fs, 'group': 'bone', 'error_mm': 0.3} for k, n, fs in CONTEXT] +
                [{'key': k, 'name': n, 'fma': '', 'files': fs, 'group': 'muscle', 'error_mm': 0.3} for k, n, fs in MUSCLES] +
                [{'key': k, 'name': n, 'fma': '', 'files': fs, 'group': 'connective', 'error_mm': 0.3} for k, n, fs in CONNECTIVE]}
json.dump(cfg, open(os.path.join(ROOT, 'tools/bones-rs/configs/head-neck-muscles.json'), 'w'), indent=1)
print(len(cfg['parts']), 'parts;', len(MUSCLES), 'muscles')
