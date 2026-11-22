"""Config for the neuroanatomy II page (module 37): anatomy/neuro/cerebrum.html. One packed model: the cerebral hemispheres
(BodyParts3D gyri and lobes), corpus callosum and other commissures, basal ganglia, internal capsule (one BodyParts3D mesh, see below),
thalamus, hypothalamus and the rest of the diencephalon, ventricles (casts), optic nerves, chiasm and tracts, the
brainstem and cerebellum for context, the circle of Willis and the cerebral arteries, and the skull for context.
Same pattern as tools/neuro/neuro1_config.py (module 36; its files are not changed).

Parts and where they come from (licences checked 2026-11-22, sources-local/facts/fill-neuro2.md "Models"):
  bone     configs/skeleton.json      skull bones round the brain (BodyParts3D 3.0, 0.6 mm as on the home)
  gyrus    BodyParts3D 3.0            the gyri and lobes BodyParts3D 3.0 has as meshes (both sides): superior and middle frontal,
                                      precentral, postcentral, supramarginal, angular, superior (anterior and posterior parts),
                                      middle and inferior temporal, fusiform, parahippocampal, cingulate gyri, the precuneus
                                      ("superior parietal lobule precuneus"), the straight (orbital) gyrus, the occipital lobe,
                                      the insula, the hippocampus, and a mesh it names "accessory short gyrus" (FMA72701/2) that lies, by position, exactly where the inferior frontal gyrus is (below the middle frontal gyrus, in front of the precentral gyrus, above the lateral sulcus): used as the inferior frontal gyrus. BodyParts3D 3.0 has NO
                                      transverse temporal gyrus, superior parietal lobule (lateral part), cuneus or lingual gyrus as
                                      separate meshes: the page says so and marks those areas on the schematics.
  wm / bg / dien / csf / chp / optic   BodyParts3D 3.0   corpus callosum, septum pellucidum, fornix, anterior and posterior
                                      commissures; caudate, putamen, globus pallidus, amygdala, anterior limb of the internal
                                      capsule (BodyParts3D names the mesh "anterior limb", FMA72908/9, but it runs the whole length of the capsule: lateral to the caudate head in front and to the thalamus behind, checked with fill-neuro2-scripts/geo.py); thalami, lateral and medial geniculate bodies, hypothalamus, mammillary bodies,
                                      pineal body; lateral, third and fourth ventricles, interventricular foramen, aqueduct; choroid
                                      plexus; optic nerves, chiasm and tracts; pituitary gland.
  stem / cblm   BodyParts3D 3.0       midbrain, pons, medulla, cerebellum (context; detail on brainstem.html).
  Z-Anatomy's brain surface, gyri and white matter are NOT used: Z-Anatomy lists the unlicensed "Brainder" and "White matter"
  models among those it adapted.
  artery   configs/body-vessels.json  (Z-Anatomy curves swept into tubes, CC BY-SA 4.0): internal carotid, anterior, middle and
                                      posterior cerebral arteries and their named cortical branches, communicating arteries, lateral
                                      striate (lenticulostriate) branches, basilar and vertebral arteries. Right-side keys mirrored
                                      on the page where body-vessels mirrors them.
Parts are ordered by kind/colour (the viewer draws neighbouring parts of one colour with one call). One group.
Also writes anatomy/models/neuro2/kinds.json: {"mirror": {m, t}, "parts": {key: {"kind", "mirror", "lobe"?}}}.

usage: python3 -I tools/neuro/neuro2_config.py  ->  tools/bones-rs/configs/neuro2.json (+ anatomy/models/neuro2/kinds.json)
then:  cd tools/bones-rs && ../capped target/release/bones build configs/neuro2.json"""
import json, os
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
CFG = os.path.join(ROOT, 'tools', 'bones-rs', 'configs')
MODELS = os.path.join(ROOT, 'anatomy', 'models')
load = lambda n: json.load(open(os.path.join(CFG, n + '.json')))
meta = lambda g, f: json.load(open(os.path.join(MODELS, g, f + '.json')))
BP3 = '../../../sources-local/bp3d/BodyParts3D_3.0_obj_95.zip'
GROUP = 'neuro2'
GE = 0.45          # gyri: absolute simplification error (mm)

SKULL = ['frontal_bone', 'right_parietal_bone', 'left_parietal_bone', 'occipital_bone', 'right_temporal_bone', 'left_temporal_bone',
         'sphenoid_bone', 'ethmoid']
# BodyParts3D 3.0 paired meshes: (key stem, right FMA, left FMA, name, kind, lobe, error)
PAIRED = [
    ('g_sfg', 'FMA72653', 'FMA72654', 'superior frontal gyrus', 'gyrus', 'frontal', GE),
    ('g_mfg', 'FMA72655', 'FMA72656', 'middle frontal gyrus', 'gyrus', 'frontal', GE),
    ('g_prec', 'FMA72661', 'FMA72662', 'precentral gyrus', 'gyrus', 'motor', GE),
    ('g_postc', 'FMA72665', 'FMA72666', 'postcentral gyrus', 'gyrus', 'sensory', GE),
    ('g_smg', 'FMA72667', 'FMA72668', 'supramarginal gyrus', 'gyrus', 'parietal', GE),
    ('g_ang', 'FMA72669', 'FMA72670', 'angular gyrus', 'gyrus', 'parietal', GE),
    ('g_pcun', 'BP50', 'BP49', 'superior parietal lobule and precuneus', 'gyrus', 'parietal', GE),
    ('g_stga', 'FMA72800', 'FMA72801', 'superior temporal gyrus (anterior part)', 'gyrus', 'temporal', GE),
    ('g_stgp', 'FMA72804', 'FMA72805', 'superior temporal gyrus (posterior part)', 'gyrus', 'temporal', GE),
    ('g_mtg', 'FMA72685', 'FMA72686', 'middle temporal gyrus', 'gyrus', 'temporal', GE),
    ('g_itg', 'FMA72687', 'FMA72688', 'inferior temporal gyrus', 'gyrus', 'temporal', GE),
    ('g_fus', 'FMA72689', 'FMA72690', 'fusiform gyrus', 'gyrus', 'temporal', GE),
    ('g_occ', 'FMA72975', 'FMA72976', 'occipital lobe', 'gyrus', 'occipital', GE),
    ('g_ins', 'FMA72977', 'FMA72978', 'insula', 'gyrus', 'insula', GE),
    ('g_ifg', 'FMA72701', 'FMA72702', 'inferior frontal gyrus (BodyParts3D mesh named "accessory short gyrus")', 'gyrus', 'frontal', GE),
    ('g_cing', 'FMA72717', 'FMA72718', 'cingulate gyrus', 'gyrus', 'limbic', GE),
    ('g_phg', 'FMA72705', 'FMA72706', 'parahippocampal gyrus', 'gyrus', 'limbic', GE),
    ('l_hipp', 'FMA72713', 'FMA72714', 'hippocampus', 'limbic', None, 0.15),
    ('l_amyg', 'FMA72832', 'FMA72833', 'amygdala', 'limbic', None, 0.12),
    ('w_fornix', 'FMA72924', 'FMA72925', 'fornix', 'wm', None, 0.1),
    ('w_ic', 'FMA72908', 'FMA72909', 'internal capsule (BodyParts3D mesh named "anterior limb")', 'capsule', None, 0.2),
    ('w_strt', 'FMA72939', 'FMA72940', 'stria terminalis', 'wm', None, 0.08),
    ('bg_caud', 'FMA72826', 'FMA72827', 'caudate nucleus', 'caud', None, 0.12),
    ('bg_put', 'FMA72828', 'FMA72829', 'putamen', 'put', None, 0.12),
    ('bg_gp', 'FMA72830', 'FMA72831', 'globus pallidus', 'gp', None, 0.12),
    ('d_thal', 'FMA258714', 'FMA258716', 'thalamus', 'thal', None, 0.15),
    ('d_lgb', 'FMA73303', 'FMA73304', 'lateral geniculate body', 'meta', None, 0.06),
    ('d_mgb', 'FMA73309', 'FMA73310', 'medial geniculate body', 'meta', None, 0.06),
    ('d_smt', 'FMA73413', 'FMA73414', 'stria medullaris of the thalamus', 'epi', None, 0.06),
    ('c_lat', 'FMA78449', 'FMA78450', 'lateral ventricle', 'csf', None, 0.15),
    ('p_chp', 'FMA274027', 'FMA274029', 'choroid plexus of the lateral ventricle', 'chp', None, 0.35),
    ('o_nerve', 'FMA50875', 'FMA50878', 'optic nerve', 'optic', None, 0.08),
    ('o_tract', 'FMA62382', 'FMA67936', 'optic tract', 'optic', None, 0.08),
]
# BodyParts3D 3.0 single meshes: (key, FMA, name, kind, error)
SINGLE = [
    ('g_rect', 'BP51', 'Straight and orbital gyri (orbital surface, both sides)', 'gyrus', 0.45),
    ('w_cc', 'FMA86464', 'Corpus callosum', 'wm', 0.3), ('w_sp', 'FMA61844', 'Septum pellucidum', 'wm', 0.25),
    ('w_ac', 'FMA61961', 'Anterior commissure', 'wm', 0.06), ('w_pc', 'FMA62072', 'Posterior commissure', 'wm', 0.05),
    ('w_fcom', 'FMA61970', 'Commissure and body of the fornix', 'wm', 0.2),
    ('d_hypo', 'FMA62008nsn', 'Hypothalamus', 'hypo', 0.1), ('d_mam', 'FMA74877', 'Mammillary bodies', 'hypo', 0.06),
    ('d_pineal', 'FMA62033', 'Pineal body', 'epi', 0.06), ('o_chiasm', 'FMA62045', 'Optic chiasm', 'optic', 0.06),
    ('d_pit', 'FMA13889', 'Pituitary gland', 'pit', 0.08),
    ('c_third', 'FMA78454', 'Third ventricle', 'csf', 0.1), ('c_ivf', 'FMA75351', 'Interventricular foramen', 'csf', 0.05),
    ('c_aq', 'FMA78467', 'Cerebral aqueduct', 'csf', 0.06), ('c_fourth', 'FMA78469', 'Fourth ventricle', 'csf', 0.15),
    ('s_mid', 'FMA61993nsn', 'Midbrain', 'stem', 0.3), ('s_ped', 'FMA62394', 'Cerebral peduncles (crura)', 'stem', 0.3),
    ('s_pons', 'FMA67943', 'Pons', 'stem', 0.3), ('s_med', 'FMA62004', 'Medulla oblongata', 'stem', 0.3),
    ('s_cblm', 'FMA67944', 'Cerebellum', 'cblm', 0.5),
]
ARTERIES = ['v_internal_carotid_artery_r', 'v_anterior_cerebral_artery_r', 'v_anterior_communicating_artery', 'v_middle_cerebral_artery_m1_segment_r',
            'v_insular_branches_of_middle_cerebral_artery_m2_r', 'v_insular_branches_of_middle_cerebral_artery_m2_segment_l',
            'v_middle_cerebral_artery_m3_segment_r', 'v_middle_cerebral_artery_m3_segment_l',
            'v_temporal_branches_of_middle_cerebral_artery_r', 'v_parietal_branches_of_middle_cerebral_artery_r',
            'v_prefrontal_artery_r', 'v_posterior_parietal_artery_r', 'v_anterior_temporal_branch_r', 'v_posterior_temporal_branch_r',
            'v_temporo_occipital_branch_r',
            'v_proximal_lateral_striate_branches_r', 'v_distal_lateral_striate_branches_r',
            'v_pericallosal_artery_r', 'v_callosomarginal_artery_r', 'v_frontal_branches_of_callosomarginal_artery_r',
            'v_orbitofrontal_branches_of_anterior_cerebral_artery_r',
            'v_posterior_communicating_artery_r', 'v_posterior_cerebral_artery_r', 'v_lateral_occipital_artery_r', 'v_medial_occipital_artery_r',
            'v_parieto_occipital_artery_r', 'v_basilar_artery', 'v_vertebral_artery_r', 'v_ophthalmic_artery_r']
NV_ERR = 0.06

ORDER = ['bone', 'gyrus', 'limbic', 'wm', 'capsule', 'caud', 'put', 'gp', 'thal', 'meta', 'epi', 'hypo', 'pit', 'optic', 'stem', 'cblm',
         'csf', 'chp', 'artery']


def zpart(key, name, files, err, kind, mirror, fma='', **extra):
    d = {'key': key, 'name': name, 'fma': fma, 'files': files, 'group': GROUP, 'error_mm': err, '_kind': kind, '_mirror': mirror}
    d.update({'_' + k: v for k, v in extra.items() if v is not None})
    return d


parts, zips = [], []
sk = load('skeleton'); zips += sk['zips']; skp = {p['key']: p for p in sk['parts']}
for k in SKULL:
    p = skp[k]
    parts.append(zpart(k, p['name'], p['files'], p.get('error_mm', sk['error_mm']), 'bone', False, p['fma']))
for k, fr, fl, nm, kd, lobe, e in PAIRED:
    for s, side, f in (('r', 'Right', fr), ('l', 'Left', fl)):
        parts.append(zpart(f'{k}_{s}', f'{side} {nm}', [f], e, kd, False, f, lobe=lobe))
for k, f, nm, kd, e in SINGLE:
    parts.append(zpart(k, nm, [f], e, kd, False, f))
zips.append(BP3)
ve = load('body-vessels'); zips += ve['zips']; vp = {p['key']: p for p in ve['parts']}
vmeta = meta('body-vessels', 'vessels')
for k in ARTERIES:
    assert vmeta['parts'][k]['kind'] == 'artery', k
    p = vp[k]
    parts.append({'key': k, 'name': p['name'], 'fma': p['fma'], 'files': p['files'], 'group': GROUP, 'error_mm': NV_ERR,
                  '_kind': 'artery', '_mirror': bool(vmeta['parts'][k]['mirror'])})
parts.sort(key=lambda p: ORDER.index(p['_kind']))          # stable: keeps the order above within a kind

assert len({p['key'] for p in parts}) == len(parts)
kinds = {}
for p in parts:
    d = {'kind': p.pop('_kind'), 'mirror': p.pop('_mirror')}
    if '_lobe' in p: d['lobe'] = p.pop('_lobe')
    kinds[p['key']] = d
cfg = {'name': 'neuro2', 'zips': list(dict.fromkeys(zips)), 'out': '../../../anatomy/models/neuro2',
       'error_mm': 0.3, 'contact_mm': 0.0, 'contacts_across_groups_only': True, 'pack': True,
       'source': 'Skull, gyri and lobes of the cerebral hemispheres, commissures, basal ganglia, internal capsule, '
                 'diencephalon, ventricles, choroid plexus, optic pathway, pituitary, brainstem and cerebellum: BodyParts3D, '
                 '(c) The Database Center for Life Science, CC BY-SA 2.1 Japan. Arteries: Z-Anatomy, CC BY-SA 4.0 (from BodyParts3D), '
                 'curves swept into tubes, moved into the BodyParts3D frame',
       'parts': parts}
out_cfg = os.path.join(CFG, 'neuro2.json')
assert not os.path.exists(out_cfg) or json.load(open(out_cfg)).get('name') == 'neuro2'
json.dump(cfg, open(out_cfg, 'w'), indent=1)
os.makedirs(os.path.join(MODELS, 'neuro2'), exist_ok=True)
json.dump({'note': 'written by tools/neuro/neuro2_config.py', 'mirror': vmeta['mirror'], 'parts': kinds},
          open(os.path.join(MODELS, 'neuro2', 'kinds.json'), 'w'), indent=0)
from collections import Counter
print(len(parts), 'parts', dict(Counter(k['kind'] for k in kinds.values())), 'mirrored', sum(k['mirror'] for k in kinds.values()))
