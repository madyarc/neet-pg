"""Config for the page "Face and Neck: Regions and Glands" (anatomy/head-neck/regions.html, module 32): one packed model of the
face and neck with the parotid, submandibular, sublingual, thyroid and parathyroid glands, the muscles that bound the
regions, and the vessels and nerves needed for their relations. Same pattern as tools/head-neck/nv_config.py and
tools/thorax/lung_config.py.

Parts and where they come from (keys, names, files and error_mm of the whole-body configs where the part is already in one):
  bone     configs/skeleton.json         skull bones seen from outside, mandible, hyoid, C1-C7, T1-T2, clavicles, scapulae,
                                         ribs 1-2, manubrium (skeleton error_mm)
  cart     configs/skeleton.json         first costal cartilages; thyroid and cricoid cartilages (configs/head-neck-muscles.json)
  airway   z-bp3d-lung.zip               the trachea (as on thorax/lungs.html)
  muscle   configs/body-muscles.json     sternocleidomastoid, trapezius, levator scapulae, splenius capitis, the scalenes,
                                         digastric, stylohyoid, mylohyoid, hyoglossus, the infrahyoid muscles, cricothyroid,
                                         masseter, temporalis, the pterygoids, buccinator (right; mirrored on the page)
  saliv    z-bp3d-hnreg.zip              parotid, accessory parotid, submandibular and sublingual glands (right)
  thyroid  z-bp3d-hnreg.zip              Z-Anatomy's "Thyroid gland" (lobes and isthmus; its right half with a Mirror modifier,
                                         applied by sources-local/facts/fill-hnreg-scripts/export_glands.py)
  parathy  z-bp3d-hnreg.zip              superior and inferior parathyroid glands (right)
  duct     z-bp3d-hnreg-curves.zip       parotid and submandibular ducts (curves swept into tubes, tools/zanat/export_curves.py)
  artery   configs/body-vessels.json     carotids, external carotid branches of the face, maxillary artery and the branches in
                                         the infratemporal fossa, subclavian with thyrocervical trunk, inferior thyroid,
                                         transverse cervical and suprascapular arteries
  vein     configs/body-vessels.json     retromandibular, facial, external and anterior jugular, internal jugular, superior thyroid,
                                         lingual, maxillary and superficial temporal veins, subclavian vein
  nerve    configs/body-nerves.json      facial nerve (with its branches), trigeminal nerve and its divisions with the mandibular
                                         branches (lingual, inferior alveolar, mental, buccal, nerve to mylohyoid), chorda
                                         tympani, accessory, hypoglossal, vagus, brachial plexus roots and trunks
  node     configs/body-lymph.json       parotid, pre- and infra-auricular, submandibular, submental, thyroid, pretracheal,
                                         paratracheal, supraclavicular, superficial lateral cervical and occipital nodes
Exports (2026-11-21):
  fill-hnreg-scripts/export_glands.py Startup.blend z-to-bp3d.json sources-local/zanat/z-bp3d-hnreg.zip tools/zanat/z-index-hnreg.tsv
      "name:Thyroid gland" "name:Parotid gland.r" "name:(Accessory parotid gland).r" "name:Submandibular gland.r"
      "name:Sublingual gland.r" "name:Superior parathyroid gland.r" "name:Inferior parathyroid gland.r"
  export_curves.py Startup.blend z-to-bp3d.json sources-local/zanat/z-bp3d-hnreg-curves.zip tools/zanat/z-index-hnreg-curves.tsv
      "Mouth" --no-left
Z-Anatomy has no submandibular or otic ganglion, no auriculotemporal, great auricular or other cervical plexus nerve, no
recurrent or superior laryngeal nerve as a separate part, no superior thyroid, lingual or posterior auricular artery, no middle
or inferior thyroid vein, no semispinalis capitis and no pretracheal fascia: the page shows these in schematics.
Right-only parts (mirror: true) are mirrored on the page with the body-vessels transform copied into kinds.json.
Parts are ordered by colour: the viewer draws neighbouring parts of one colour with a single call. One group.

Also writes anatomy/models/hn-reg/kinds.json: {"mirror": {m, t}, "parts": {key: {"kind", "mirror"}}} for the page.

usage: python3 -I tools/head-neck/regions_config.py   ->  tools/bones-rs/configs/hn-reg.json (+ anatomy/models/hn-reg/kinds.json)
then:  cd tools/bones-rs && target/release/bones build configs/hn-reg.json   (through tools/capped)"""
import json, os, re, csv
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
CFG = os.path.join(ROOT, 'tools', 'bones-rs', 'configs')
MODELS = os.path.join(ROOT, 'anatomy', 'models')
ZAN = os.path.join(ROOT, 'tools', 'zanat')
load = lambda n: json.load(open(os.path.join(CFG, n + '.json')))
meta = lambda g, f: json.load(open(os.path.join(MODELS, g, f + '.json')))
GLAND_ERR, SMALL_ERR, DUCT_ERR, TRACHEA_ERR = 0.3, 0.1, 0.12, 0.25

BONES = re.compile(r'^(frontal_bone|(left|right)_parietal_bone|occipital_bone|(left|right)_temporal_bone|sphenoid_bone|'
                   r'(left|right)_(maxilla|zygomatic_bone|nasal_bone)|mandible|hyoid_bone|atlas|axis|'
                   r'(third|fourth|fifth|sixth|seventh)_cervical_vertebra|(first|second)_thoracic_vertebra|'
                   r'(left|right)_(clavicle|scapula|first_rib|second_rib)|manubrium)$')
CART = re.compile(r'^(left|right)_first_costal_cartilage$')
MUSCLES = ['m_scm', 'm_trapezius', 'm_lev_scap', 'm_splenius_cap', 'm_scal_ant', 'm_scal_med', 'm_scal_post', 'm_digastric',
           'm_stylohyoid', 'm_mylohyoid', 'm_hyoglossus', 'm_omohyoid', 'm_sternohyoid', 'm_sternothyroid', 'm_thyrohyoid',
           'm_cricothyroid', 'm_masseter', 'm_temporalis', 'm_lat_pterygoid', 'm_med_pterygoid', 'm_buccinator']
ARTERIES = ['v_right_common_carotid_artery', 'v_external_carotid_artery_r', 'v_internal_carotid_artery_r',
            'v_superficial_temporal_artery_r', 'v_frontal_branch_of_superficial_temporal_artery_r', 'v_transverse_facial_artery_r',
            'v_maxillary_artery_r', 'v_middle_meningeal_artery_r', 'v_accessory_branch_of_middle_meningeal_artery_r',
            'v_anterior_deep_temporal_artery_r', 'v_posterior_deep_temporal_artery_r', 'v_inferior_alveolar_artery_r',
            'v_mylohyoid_branch_of_inferior_alveolar_artery_r', 'v_buccal_artery_r', 'v_posterior_superior_alveolar_artery_r',
            'v_facial_artery_r', 'v_submental_artery_r', 'v_occipital_artery_r', 'v_brachiocephalic_trunk', 'v_right_subclavian_artery',
            'v_thyrocervical_trunk_r', 'v_inferior_thyroid_artery_r', 'v_transverse_cervical_artery_r',
            'v_superficial_branch_of_transverse_cervical_artery_r', 'v_deep_branch_of_transverse_cervical_artery_r',
            'v_suprascapular_artery_r']
VEINS = ['v_retromandibular_vein_r', 'v_anterior_division_of_retromandibular_vein_r', 'v_posterior_division_of_retromandibular_vein_r',
         'v_superficial_temporal_veins_r', 'v_maxillary_veins_r', 'v_posterior_auricular_vein_r', 'v_facial_vein_r',
         'v_common_facial_vein_r', 'v_submental_vein_r', 'v_lingual_vein_r', 'v_external_jugular_vein_r', 'v_anterior_jugular_vein_r',
         'v_internal_jugular_vein_r', 'v_superior_thyroid_vein_r', 'v_right_subclavian_vein', 'v_right_brachiocephalic_vein']
NERVES = ['n_facial_nerve_vii_r', 'n_chorda_tympani_r', 'n_trigeminal_nerve_v_r', 'n_ophthalmic_nerve_r', 'n_maxillary_nerve_r',
          'n_anterior_division_of_mandibular_nerve_r', 'n_posterior_division_of_mandibular_nerve_r', 'n_buccal_nerve_r',
          'n_lingual_nerve_r', 'n_inferior_alveolar_nerve_r', 'n_mental_nerve_r', 'n_nerve_to_mylohyoid_muscle_r',
          'n_accessory_nerve_xi_r', 'n_hypoglossal_nerve_xii_r', 'n_vagus_nerve_x_r', 'n_roots_of_brachial_plexus_r',
          'n_superior_trunk_of_brachial_plexus_r', 'n_middle_trunk_of_brachial_plexus_r', 'n_inferior_trunk_of_brachial_plexus_r']
NODES = ['l_intraglandular_parotid_nodes_r', 'l_superficial_parotid_nodes_r', 'l_pre_auricular_nodes_r', 'l_infra_auricular_nodes_r',
         'l_submandibular_nodes_r', 'l_submental_nodes_r', 'l_thyroid_nodes_r', 'l_pretracheal_nodes_r', 'l_paratracheal_cervical_nodes',
         'l_supraclavicular_nodes_r', 'l_superficial_lateral_cervical_nodes_r', 'l_occipital_nodes_r']
# glands: [key, Z-Anatomy file, name, kind, mirror, error_mm]
GLANDS = [['g_parotid', 'Z_parotid_gland_r', 'Parotid gland', 'saliv', True, GLAND_ERR],
          ['g_acc_parotid', 'Z_accessory_parotid_gland_r', 'Accessory parotid gland', 'saliv', True, SMALL_ERR],
          ['g_submandibular', 'Z_submandibular_gland_r', 'Submandibular gland', 'saliv', True, GLAND_ERR],
          ['g_sublingual', 'Z_sublingual_gland_r', 'Sublingual gland', 'saliv', True, GLAND_ERR],
          ['g_thyroid', 'Z_thyroid_gland', 'Thyroid gland', 'thyroid', False, GLAND_ERR],
          ['g_sup_parathyroid', 'Z_superior_parathyroid_gland_r', 'Superior parathyroid gland', 'parathy', True, SMALL_ERR],
          ['g_inf_parathyroid', 'Z_inferior_parathyroid_gland_r', 'Inferior parathyroid gland', 'parathy', True, SMALL_ERR]]
DUCTS = [['d_parotid', 'Z_parotid_duct_r', 'Parotid duct'], ['d_submandibular', 'Z_submandibular_duct_r', 'Submandibular duct']]
ZIP_GL = '../../../sources-local/zanat/z-bp3d-hnreg.zip'
ZIP_DUCT = '../../../sources-local/zanat/z-bp3d-hnreg-curves.zip'
ZIP_LUNG = '../../../sources-local/zanat/z-bp3d-lung.zip'


def copy(p, default_err, kind, mirror=False):
    return {'key': p['key'], 'name': p['name'], 'fma': p['fma'], 'files': p['files'], 'group': 'hnreg',
            'error_mm': p.get('error_mm', default_err), '_kind': kind, '_mirror': bool(mirror)}


def zpart(key, name, file, err, kind, mirror):
    return {'key': key, 'name': name, 'fma': '', 'files': [file], 'group': 'hnreg', 'error_mm': err, '_kind': kind,
            '_mirror': mirror}


parts, zips = [], []
sk = load('skeleton'); zips += sk['zips']
parts += [copy(p, sk['error_mm'], 'bone') for p in sk['parts'] if BONES.match(p['key'])]
parts += [copy(p, sk['error_mm'], 'cart') for p in sk['parts'] if CART.match(p['key'])]
hn = load('head-neck-muscles'); hp = {p['key']: p for p in hn['parts']}
parts += [copy(hp[k], hn['error_mm'], 'cart') for k in ('thyroid_cart', 'cricoid_cart')]
zips += [z for z in hn['zips'] if 'extra' in z]
parts.append(zpart('r_trachea', 'Trachea', 'Z_trachea', TRACHEA_ERR, 'airway', False)); zips.append(ZIP_LUNG)

mu = load('body-muscles'); zips += mu['zips']; mp = {p['key']: p for p in mu['parts']}
mmeta = meta('body-muscles', 'muscles')['parts']
parts += [copy(mp[k], mu['error_mm'], 'muscle', mmeta[k]['mirror']) for k in MUSCLES]

gl = {r['file']: r for r in csv.DictReader(open(os.path.join(ZAN, 'z-index-hnreg.tsv')), delimiter='\t')}
for kind in ('saliv', 'thyroid', 'parathy'):
    parts += [zpart(k, nm, f, e, kd, mi) for k, f, nm, kd, mi, e in GLANDS if kd == kind and f in gl]
du = {r['file']: r for r in csv.DictReader(open(os.path.join(ZAN, 'z-index-hnreg-curves.tsv')), delimiter='\t')}
parts += [zpart(k, nm, f, DUCT_ERR, 'duct', True) for k, f, nm in DUCTS if f in du]
zips += [ZIP_GL, ZIP_DUCT]

ve = load('body-vessels'); zips += ve['zips']; vp = {p['key']: p for p in ve['parts']}
vmeta = meta('body-vessels', 'vessels')
for kind, keys in (('artery', ARTERIES), ('vein', VEINS)):
    for k in keys:
        assert vmeta['parts'][k]['kind'] == kind, k
        parts.append(copy(vp[k], ve['error_mm'], kind, vmeta['parts'][k]['mirror']))
ne = load('body-nerves'); zips += ne['zips']; np_ = {p['key']: p for p in ne['parts']}
nmeta = meta('body-nerves', 'nerves')
parts += [copy(np_[k], ne['error_mm'], 'nerve', nmeta['parts'][k]['mirror']) for k in NERVES]
ly = load('body-lymph'); zips += ly['zips']; lp = {p['key']: p for p in ly['parts']}
lmeta = meta('body-lymph', 'lymph')
parts += [copy(lp[k], ly['error_mm'], 'node', lmeta['parts'][k]['mirror']) for k in NODES]

assert len({p['key'] for p in parts}) == len(parts)
assert vmeta['mirror'] == nmeta['mirror'] == lmeta['mirror']
kinds = {p['key']: {'kind': p.pop('_kind'), 'mirror': p.pop('_mirror')} for p in parts}
cfg = {'name': 'hn-reg', 'zips': list(dict.fromkeys(zips)), 'out': '../../../anatomy/models/hn-reg',
       'error_mm': 0.3, 'contact_mm': 0.5, 'contacts_across_groups_only': True, 'pack': True,
       'source': 'Bones: BodyParts3D, (c) The Database Center for Life Science, CC BY-SA 2.1 Japan. Glands, ducts, trachea, '
                 'laryngeal cartilages, muscles, vessels, nerves and lymph nodes: Z-Anatomy, CC BY-SA 4.0 (from BodyParts3D), moved '
                 'into the BodyParts3D frame; ducts, vessels and nerves are curves swept into tubes',
       'parts': parts}
out_cfg = os.path.join(CFG, 'hn-reg.json')
assert not os.path.exists(out_cfg) or json.load(open(out_cfg)).get('name') == 'hn-reg'
json.dump(cfg, open(out_cfg, 'w'), indent=1)
os.makedirs(os.path.join(MODELS, 'hn-reg'), exist_ok=True)
json.dump({'note': 'written by tools/head-neck/regions_config.py', 'mirror': vmeta['mirror'], 'parts': kinds},
          open(os.path.join(MODELS, 'hn-reg', 'kinds.json'), 'w'), indent=0)
from collections import Counter
print(len(parts), 'parts', dict(Counter(k['kind'] for k in kinds.values())), 'mirrored', sum(k['mirror'] for k in kinds.values()))
