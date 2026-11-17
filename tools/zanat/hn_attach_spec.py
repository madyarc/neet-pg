"""Writes tools/zanat/hn-attach.json (attachment areas for the head and neck page), following
sources-local/facts/hn-face-mastication.md, hn-neck.md and hn-eye-tongue-pharynx-larynx.md. Check each in a screenshot."""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
def A(bone, kind, near=None, r=20, **kw):
    a = {'bone': bone, 'kind': kind}
    if near: a['near'] = near if isinstance(near, list) else [near]; a['r'] = r
    a.update(kw); return a
O, I = 'ori', 'ins'
attach = {
 # face (bony origins only; most insert into skin)
 'occipitofrontalis': [A('occipital', O, 'superior_nuchal_line', 45), A('temporal_r', O, 'mastoid_process', 20)],
 'corrugator': [A('frontal', O, 'superciliary_arch', 18)],
 'procerus': [A('nasal_r', O, 'inferior_border', 14)],
 'orb_oculi': [A('frontal', O, 'nasion', 14), A('maxilla_r', O, 'frontal_process', 14)],
 'zyg_major': [A('zygomatic_r', O, ['zygomaticofacial_foramen', 'temporal_process'], 18)],
 'zyg_minor': [A('zygomatic_r', O, 'maxillary_process', 16)],
 'lev_lab_sup': [A('maxilla_r', O, 'infraorbital_foramen', 14)],
 'lev_lab_alae': [A('maxilla_r', O, 'frontal_process', 16)],
 'lev_ang_oris': [A('maxilla_r', O, 'infraorbital_foramen', 20)],
 'dep_ang_oris': [A('mandible', O, 'mental_foramen', 25)],
 'dep_lab_inf': [A('mandible', O, 'mental_foramen', 22)],
 'mentalis': [A('mandible', O, 'mental_protuberance', 16)],
 'buccinator': [A('maxilla_r', O, 'alveolar_process', 30), A('mandible', O, ['body', 'ramus'], 30)],
 'platysma': [A('mandible', I, 'body', 40)],
 # mastication
 'masseter': [A('zygomatic_r', O, 'temporal_process', 30), A('maxilla_r', O, 'zygomatic_process', 18), A('temporal_r', O, 'zygomatic_process', 25),
              A('mandible', I, ['angle', 'ramus', 'coronoid_process'], 30)],
 'temporalis': [A('temporal_r', O, 'squama', 60), A('parietal_r', O), A('frontal', O, 'zygomatic_process', 40), A('sphenoid', O, 'greater_wing', 35),
                A('mandible', I, 'coronoid_process', 25)],
 'lat_pterygoid': [A('sphenoid', O, ['greater_wing', 'lateral_pterygoid_plate'], 25), A('mandible', I, 'condyle', 16)],
 'med_pterygoid': [A('sphenoid', O, 'lateral_pterygoid_plate', 20), A('palatine_r', O, 'pyramidal_process', 12), A('maxilla_r', O, 'alveolar_process', 30),
                   A('mandible', I, ['angle', 'mandibular_foramen'], 30)],
 # neck
 'scm': [A('manubrium', O), A('clavicle', O, 'sternal_end', 40), A('temporal_r', I, 'mastoid_process', 22), A('occipital', I, 'superior_nuchal_line', 60, d=6)],
 'digastric': [A('temporal_r', O, 'mastoid_process', 22), A('mandible', O, ['mental_protuberance', 'mental_spines'], 25)],
 'stylohyoid': [A('temporal_r', O, 'styloid_process', 14), A('hyoid', I)],
 'mylohyoid': [A('mandible', O, ['body', 'mental_spines'], 45), A('hyoid', I, 'body', 15)],
 'geniohyoid': [A('mandible', O, 'mental_spines', 12), A('hyoid', I, 'body', 15)],
 'sternohyoid': [A('manubrium', O), A('clavicle', O, 'sternal_end', 25), A('hyoid', I, 'body', 15)],
 'sternothyroid': [A('manubrium', O), A('thyroid_cart', I)],
 'thyrohyoid': [A('thyroid_cart', O, d=1.5), A('hyoid', I, 'greater_cornu', 25)],
 'omohyoid': [A('scapula', O, 'suprascapular_notch', 25), A('hyoid', I, 'body', 15)],
 'scal_ant': [A(c, O, 'transverse_process', 25) for c in ('c3', 'c4', 'c5', 'c6')] + [A('rib1_r', I, 'scalene_tubercle', 20, d=5)],
 'scal_med': [A('rib1_r', I, ['tubercle', 'subclavian_artery_groove'], 30)],
 'scal_post': [A('rib2_r', I)],
 'longus_capitis': [A('occipital', I, 'basilar_part', 20)],
 'longus_colli': [A('c1', I, 'anterior_tubercle', 12)],
 'rect_cap_ant': [A('c1', O, 'lateral_mass', 14), A('occipital', I, ['basilar_part', 'foramen_magnum'], 20)],
 'rect_cap_lat': [A('c1', O, 'transverse_process', 14), A('occipital', I, 'jugular_process', 16)],
 # orbit
 'sup_rectus': [A('eyeball', I)], 'inf_rectus': [A('eyeball', I)], 'med_rectus': [A('eyeball', I)], 'lat_rectus': [A('eyeball', I)],
 'sup_oblique': [A('sphenoid', O, 'optic_canal', 14), A('eyeball', I)],
 'inf_oblique': [A('maxilla_r', O, 'infraorbital_groove', 18), A('eyeball', I)],
 'lps': [A('sphenoid', O, ['lesser_wing', 'optic_canal'], 14)],
 # tongue, pharynx
 'genioglossus': [A('mandible', O, 'mental_spines', 12), A('hyoid', I, 'body', 15)],
 'hyoglossus': [A('hyoid', O)],
 'sup_constrictor': [A('sphenoid', O, ['pterygoid_hamulus', 'medial_pterygoid_plate'], 16)],
 'mid_constrictor': [A('hyoid', O, ['greater_cornu', 'lesser_cornu'], 25)],
 'inf_constrictor': [A('thyroid_cart', O), A('cricoid_cart', O)],
 'stylopharyngeus': [A('temporal_r', O, 'styloid_process', 14), A('thyroid_cart', I)],
 'palatopharyngeus': [A('thyroid_cart', I)],
 # larynx
 'post_cricoaryt': [A('cricoid_cart', O, d=5), A('aryt_cart_r', I, d=5)],
 'lat_cricoaryt': [A('cricoid_cart', O), A('aryt_cart_r', I)],
 'trans_aryt': [A('aryt_cart_r', O), A('aryt_cart_l', I)],
 'thyroaryt': [A('thyroid_cart', O), A('aryt_cart_r', I)],
 'cricothyroid': [A('cricoid_cart', O), A('thyroid_cart', I)],
}
DROP = {'occipitofrontalis': 'occipital belly: 6 vertices; mastoid empty', 'procerus': 'empty', 'zyg_major': 'muscle does not reach the zygomatic bone in the model (8 vertices)', 'lev_lab_alae': '4 vertices', 'lev_ang_oris': 'patches beside the muscle, not under it', 'geniohyoid': 'mental spine 3 vertices; hyoid area hidden', 'longus_capitis': '2 vertices', 'longus_colli': 'atlas tubercle hidden', 'genioglossus': 'mental spine and hyoid slivers', 'sup_constrictor': 'sliver', 'lat_cricoaryt': '4-5 vertices', 'thyroaryt': 'inside the thyroid cartilage, cannot be checked', 'sup_rectus': 'eyeball: the recti and obliques wrap the globe, so proximity marks far more than the insertion; orbit origins hidden', 'inf_rectus': 'as superior rectus', 'med_rectus': 'as superior rectus', 'lat_rectus': 'as superior rectus', 'sup_oblique': 'as superior rectus', 'inf_oblique': 'as superior rectus', 'lps': 'origin hidden in the orbit'}
PART = {'scm': 'insertion: the occipital (superior nuchal line) part is empty, so the mastoid part is dropped too; origins kept', 'omohyoid': 'scapula: 3 vertices (insertion kept)', 'stylopharyngeus': 'thyroid cartilage: 2 vertices', 'digastric': 'anterior belly (digastric fossa): not visible', 'sternohyoid': 'manubrium: 5 vertices (clavicle origin kept)', 'sternothyroid': 'origin (manubrium, 1st costal cartilage): 5 vertices', 'inf_constrictor': 'cricoid part not checkable'}
DROP.update({'scal_ant': 'C4 only of C3-C6; scalene tubercle 7 vertices', 'post_cricoaryt': 'muscle sits off the cricoid lamina in the model (0 vertices)'})
for k in DROP: attach.pop(k)
attach['scm'] = [a for a in attach['scm'] if a['kind'] == 'ori']
attach['omohyoid'] = [a for a in attach['omohyoid'] if a['bone'] != 'scapula']
attach['stylopharyngeus'] = attach['stylopharyngeus'][:1]
attach['digastric'] = attach['digastric'][:1]
attach['sternohyoid'] = [a for a in attach['sternohyoid'] if a['bone'] != 'manubrium']
attach['sternothyroid'] = [a for a in attach['sternothyroid'] if a['bone'] != 'manubrium']
attach['inf_constrictor'] = attach['inf_constrictor'][:1]
spec = {'manifest': '../../anatomy/models/head-neck-muscles/head-neck-muscles.json',
        'landmarks': ['../../anatomy/models/skull-detail/landmarks.json', '../../anatomy/models/spine-detail/landmarks.json',
                      '../../anatomy/models/thorax-detail/landmarks.json', '../../anatomy/models/upper-limb-detail/landmarks.json'],
        'out': '../../anatomy/models/head-neck-muscles/attachments.json', 'd': 3.0,
        '_note': 'Generated by hn_attach_spec.py. Check every area in a screenshot before it ships.', '_dropped': dict(DROP, **{k + ' (part)': v for k, v in PART.items()}), 'attach': attach}
json.dump(spec, open(os.path.join(HERE, 'hn-attach.json'), 'w'), indent=1)
