"""Config for the page "Mouth, Pharynx, Nose and Larynx" (anatomy/head-neck/mouth-pharynx-nose.html, module 33): one packed
model of the mouth, nasal cavity, paranasal sinuses, pharynx and larynx. Same pattern as tools/head-neck/nv_config.py and
tools/abdomen-pelvis/organs_config.py.

Parts and where they come from (keys, names, files and error_mm of the whole-body configs where the part is already in one):
  bone    configs/skeleton.json        frontal, sphenoid, ethmoid, vomer, occipital, temporal bones, maxillae, palatine bones,
                                       inferior conchae, nasal and lacrimal bones, mandible, hyoid, C1-C6 (skeleton error_mm)
  tooth   BodyParts3D 3.0              the 28 permanent teeth (incisors to second molars; no third molars in BodyParts3D),
                                       joined into two parts (upper teeth, lower teeth)
  cart    configs/head-neck-muscles.json  thyroid, cricoid and arytenoid cartilages, epiglottis (z-bp3d-extra.zip)
          z-bp3d-oro.zip               corniculate cartilage, nasal septal cartilage and its lateral process
  tube    z-bp3d-oro.zip               auditory tube (Solidify, Subsurf applied)
  lig     z-bp3d-oro.zip               quadrangular membrane, median cricothyroid ligament, median and lateral thyrohyoid ligaments
  muscle  configs/body-muscles.json    constrictors, palatopharyngeus, stylopharyngeus, tongue muscles, floor of mouth, buccinator,
                                       orbicularis oris, pterygoids, intrinsic laryngeal muscles
  tongue / palate / gum / phar / nmuc / sinus   z-bp3d-oro.zip (Z-Anatomy meshes; Subsurf, Mirror, Solidify applied by
          sources-local/facts/fill-oro-scripts/export_oro.py): tongue; soft palate and uvula; gingiva; nasopharynx, oropharynx,
          laryngopharynx (mucosal shells); mucosa of the nasal cavity; frontal and sphenoidal sinuses and the anterior, middle
          and posterior ethmoidal cells (Z-Anatomy has no maxillary sinus mesh: the page marks it by hand, approximate)
  airway  z-bp3d-oro.zip               trachea (Z-Anatomy, same mesh as models/lung)
  gut     z-bp3d-oro-clip.zip          the oesophagus above z = 1320 mm (BodyParts3D 3.0 FMA7131, clipped by fill-oro-scripts/clip.py)
  artery / vein / nerve   configs/body-vessels.json, body-nerves.json (curves swept into tubes)
  tonsil / node   configs/body-lymph.json  palatine tonsil; retropharyngeal and jugulodigastric nodes
Z-Anatomy has no levator or tensor veli palatini, palatoglossus, salpingopharyngeus or musculus uvulae, no vocal or
vestibular fold as a separate part (thyro-arytenoid lies in the vocal fold), no lingual, tonsillar, ascending palatine or
superior laryngeal artery, no greater palatine, nasopalatine, internal laryngeal or recurrent laryngeal nerve, no
pterygopalatine ganglion and no adenoid, lingual or tubal tonsil.
Exports (2026-11-21):
  export_oro.py Startup.blend z-to-bp3d.json sources-local/zanat/z-bp3d-oro.zip tools/zanat/z-index-oro.tsv "name:Tongue" ...
  clip.py sources-local/zanat/z-bp3d-oro-clip.zip "BodyParts3D_3.0_obj_95.zip|...FMA7131.obj|1320|BP_oesophagus_upper"
Right-only parts are mirrored on the page with the body layers' reflection (copied into kinds.json). Parts are ordered by
colour (the viewer draws neighbouring parts of one colour with a single call). One group, contacts not needed.

Also writes anatomy/models/oro/kinds.json: {"mirror": {m, t}, "parts": {key: {"kind", "mirror"}}} for the page.

usage: python3 -I tools/head-neck/oro_config.py   ->  tools/bones-rs/configs/oro.json (+ anatomy/models/oro/kinds.json)
then:  cd tools/bones-rs && target/release/bones build configs/oro.json   (through tools/capped)"""
import json, os, re, csv
import numpy as np
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
CFG = os.path.join(ROOT, 'tools', 'bones-rs', 'configs')
MODELS = os.path.join(ROOT, 'anatomy', 'models')
ZAN = os.path.join(ROOT, 'tools', 'zanat')
load = lambda n: json.load(open(os.path.join(CFG, n + '.json')))
meta = lambda g, f: json.load(open(os.path.join(MODELS, g, f + '.json')))
ZIP_ORO = '../../../sources-local/zanat/z-bp3d-oro.zip'
ZIP_CLIP = '../../../sources-local/zanat/z-bp3d-oro-clip.zip'
BP3 = '../../../sources-local/bp3d/BodyParts3D_3.0_obj_95.zip'

BONES = re.compile(r'^(frontal_bone|sphenoid_bone|ethmoid|vomer|occipital_bone|(left|right)_temporal_bone|'
                   r'(left|right)_(maxilla|palatine_bone|inferior_nasal_concha|nasal_bone|lacrimal_bone)|mandible|hyoid_bone|'
                   r'atlas|axis|(third|fourth|fifth|sixth)_cervical_vertebra)$')
UPPER_TEETH = ['FMA55680', 'FMA55681', 'FMA55682', 'FMA55683', 'FMA55688', 'FMA55689', 'FMA55690', 'FMA55691', 'FMA55697', 'FMA55698',
               'FMA55699', 'FMA55700', 'FMA55798', 'FMA55799']
LOWER_TEETH = ['FMA55686', 'FMA55687', 'FMA55692', 'FMA55693', 'FMA55694', 'FMA55695', 'FMA55703', 'FMA55704', 'FMA55705', 'FMA55706',
               'FMA57140', 'FMA57141', 'FMA57142', 'FMA57143']
LARYNX = ['thyroid_cart', 'cricoid_cart', 'aryt_cart_r', 'aryt_cart_l', 'epiglottis']          # from head-neck-muscles.json
# Z-Anatomy exports: (key, file, name, kind, mirror, error_mm)
ZPARTS = [('c_corniculate', 'Z_corniculate_cartilage_r', 'Right corniculate cartilage', 'cart', True, 0.1),
          ('c_septal', 'Z_nasal_septal_cartilage', 'Septal cartilage of the nose', 'cart', False, 0.2),
          ('c_septal_lat', 'Z_lateral_process_of_nasal_septal_cartilage_r', 'Right lateral process of septal cartilage', 'cart', True, 0.2),
          ('z_auditory_tube', 'Z_auditory_tube_r', 'Right auditory (pharyngotympanic) tube', 'tube', True, 0.3),
          ('g_quadrangular', 'Z_quadrangular_membrane_r', 'Right quadrangular membrane', 'lig', True, 0.2),
          ('g_cricothyroid', 'Z_median_cricothyroid_ligament', 'Median cricothyroid ligament', 'lig', False, 0.2),
          ('g_thyrohyoid', 'Z_median_thyrohyoid_ligament', 'Median thyrohyoid ligament', 'lig', False, 0.2),
          ('g_thyrohyoid_lat', 'Z_lateral_thyrohyoid_ligament_r', 'Right lateral thyrohyoid ligament', 'lig', True, 0.2),
          ('z_tongue', 'Z_tongue', 'Tongue', 'tongue', False, 0.3),
          ('z_soft_palate', 'Z_soft_palate', 'Soft palate', 'palate', False, 0.3),
          ('z_uvula', 'Z_uvula_of_palate', 'Uvula', 'palate', False, 0.2),
          ('z_gingiva', 'Z_gingiva', 'Gingiva (gums)', 'gum', False, 0.35),
          ('z_nasopharynx', 'Z_nasopharynx', 'Nasopharynx', 'phar', False, 0.35),
          ('z_oropharynx', 'Z_oropharynx', 'Oropharynx', 'phar', False, 0.35),
          ('z_laryngopharynx', 'Z_laryngopharynx', 'Laryngopharynx', 'phar', False, 0.35),
          ('z_nasal_mucosa', 'Z_mucosa_of_nasal_cavity', 'Mucosa of the nasal cavity', 'nmuc', False, 0.35),
          ('s_frontal', 'Z_sinus_of_frontal_bone', 'Frontal sinus', 'sinus', False, 0.3),
          ('s_sphenoid', 'Z_sinus_of_sphenoid_bone', 'Sphenoidal sinus', 'sinus', False, 0.3),
          ('s_ethmoid_ant', 'Z_anterior_cells_of_ethmoid_bone_r', 'Right anterior ethmoidal cells', 'sinus', True, 0.2),
          ('s_ethmoid_mid', 'Z_middle_cells_of_ethmoid_bone_r', 'Right middle ethmoidal cells', 'sinus', True, 0.2),
          ('s_ethmoid_post', 'Z_posterior_cells_of_ethmoid_bone_r', 'Right posterior ethmoidal cells', 'sinus', True, 0.2),
          ('z_trachea', 'Z_trachea', 'Trachea', 'airway', False, 0.3)]
MUSCLES = ['m_sup_constrictor', 'm_mid_constrictor', 'm_inf_constrictor', 'm_palatopharyngeus', 'm_stylopharyngeus', 'm_genioglossus',
           'm_hyoglossus', 'm_mylohyoid', 'm_geniohyoid', 'm_buccinator', 'm_orb_oris', 'm_med_pterygoid', 'm_lat_pterygoid',
           'm_thyroaryt', 'm_post_cricoaryt', 'm_lat_cricoaryt', 'm_trans_aryt', 'm_obl_aryt', 'm_cricothyroid']
ARTERIES = ['external_carotid_artery_r', 'internal_carotid_artery_r', 'facial_artery_r', 'ascending_pharyngeal_artery_r', 'maxillary_artery_r',
            'descending_palatine_artery_r', 'greater_palatine_artery_r', 'posterior_septal_branches_of_sphenopalatine_artery_r',
            'posterior_lateral_nasal_branches_of_sphenopalatine_artery_r', 'anterior_ethmoidal_artery_r',
            'anterior_septal_branches_of_anterior_ethmoidal_artery_r', 'posterior_ethmoidal_artery_r',
            'septal_branches_of_posterior_ethmoidal_artery_r', 'superior_labial_artery_r', 'inferior_labial_artery_r',
            'infra_orbital_artery_r', 'posterior_superior_alveolar_artery_r']
VEINS = ['internal_jugular_vein_r', 'facial_vein_r', 'lingual_vein_r']
NERVES = ['lingual_nerve_r', 'glossopharyngeal_nerve_ix_r', 'vagus_nerve_x_r', 'vagus_nerve_x_l', 'hypoglossal_nerve_xii_r', 'maxillary_nerve_r',
          'olfactory_nerve_i_r', 'chorda_tympani_r', 'inferior_alveolar_nerve_r', 'sympathetic_trunk_r']
NODES = ['l_palatine_tonsil_r', 'l_retropharyngeal_nodes_r', 'l_jugulodigastric_node_r']
ORDER = ['bone', 'tooth', 'cart', 'tube', 'lig', 'muscle', 'tongue', 'palate', 'gum', 'phar', 'nmuc', 'sinus', 'airway', 'gut',
         'artery', 'vein', 'nerve', 'tonsil', 'node']


def copy(p, default_err, kind, mirror=False):
    return {'key': p['key'], 'name': p['name'], 'fma': p['fma'], 'files': p['files'], 'group': 'oro',
            'error_mm': p.get('error_mm', default_err), '_kind': kind, '_mirror': bool(mirror)}


def part(key, name, files, err, kind, mirror=False, fma=''):
    return {'key': key, 'name': name, 'fma': fma, 'files': files, 'group': 'oro', 'error_mm': err, '_kind': kind, '_mirror': mirror}


def take(cfg, keys, kind, mmeta=None):
    by = {p['key']: p for p in cfg['parts']}
    miss = [k for k in keys if k not in by]; assert not miss, miss
    return [copy(by[k], cfg['error_mm'], kind, mmeta[k]['mirror'] if mmeta else False) for k in keys]


parts, zips = [], []
sk = load('skeleton'); zips += sk['zips']
parts += [copy(p, sk['error_mm'], 'bone') for p in sk['parts'] if BONES.match(p['key'])]
assert len(parts) == 25, len(parts)
zips.append(BP3)
parts += [part('t_upper_teeth', 'Upper teeth', UPPER_TEETH, 0.3, 'tooth'), part('t_lower_teeth', 'Lower teeth', LOWER_TEETH, 0.3, 'tooth')]
hm = load('head-neck-muscles'); zips += hm['zips']
parts += take(hm, LARYNX, 'cart')
idx = {r['file'] for r in csv.DictReader(open(os.path.join(ZAN, 'z-index-oro.tsv')), delimiter='\t')}
for key, f, nm, kind, mir, err in ZPARTS:
    assert f in idx, f
    parts.append(part(key, nm, [f], err, kind, mir))
parts.append(part('z_oesophagus', 'Oesophagus (upper part)', ['BP_oesophagus_upper'], 0.3, 'gut', fma='FMA7131'))
zips += [ZIP_ORO, ZIP_CLIP]
mu = load('body-muscles'); zips += mu['zips']; mmeta = meta('body-muscles', 'muscles')
parts += take(mu, MUSCLES, 'muscle', mmeta['parts'])
ve = load('body-vessels'); zips += ve['zips']; vmeta = meta('body-vessels', 'vessels')
parts += take(ve, ['v_' + k for k in ARTERIES], 'artery', vmeta['parts']) + take(ve, ['v_' + k for k in VEINS], 'vein', vmeta['parts'])
ne = load('body-nerves'); zips += ne['zips']; nmeta = meta('body-nerves', 'nerves')
parts += take(ne, ['n_' + k for k in NERVES], 'nerve', nmeta['parts'])
ly = load('body-lymph'); zips += ly['zips']; lmeta = meta('body-lymph', 'lymph')
parts += take(ly, NODES[:1], 'tonsil', lmeta['parts']) + take(ly, NODES[1:], 'node', lmeta['parts'])
parts.sort(key=lambda p: ORDER.index(p['_kind']))   # stable: keeps the order inside each kind

# finer meshes where the page looks closely (thin nasal bones and shells; the default errors made them coarse)
FINE = {'ethmoid': 0.25, 'vomer': 0.2, 'sphenoid_bone': 0.3, 'hyoid_bone': 0.3, 'right_maxilla': 0.3, 'left_maxilla': 0.3,
        'right_palatine_bone': 0.25, 'left_palatine_bone': 0.25, 'right_inferior_nasal_concha': 0.25, 'left_inferior_nasal_concha': 0.25,
        'right_nasal_bone': 0.25, 'left_nasal_bone': 0.25, 'right_lacrimal_bone': 0.25, 'left_lacrimal_bone': 0.25,
        'thyroid_cart': 0.15, 'cricoid_cart': 0.15, 'aryt_cart_r': 0.1, 'aryt_cart_l': 0.1, 'epiglottis': 0.15,
        'g_quadrangular': 0.12, 'g_cricothyroid': 0.12, 'g_thyrohyoid': 0.12, 'g_thyrohyoid_lat': 0.12,
        'z_nasopharynx': 0.15, 'z_oropharynx': 0.15, 'z_laryngopharynx': 0.15, 'z_soft_palate': 0.12, 'z_uvula': 0.08,
        'z_auditory_tube': 0.12, 'z_tongue': 0.15}
for p in parts:
    if p['key'] in FINE: p['error_mm'] = FINE[p['key']]
assert len({p['key'] for p in parts}) == len(parts)
M = vmeta['mirror']
for other in (nmeta, lmeta, mmeta):
    mo = other['mirror']
    assert np.allclose(mo['m'], M['m'], atol=1e-6) and np.allclose(mo['t'], M['t'], atol=1e-3), 'mirror transforms differ'
kinds = {p['key']: {'kind': p.pop('_kind'), 'mirror': p.pop('_mirror')} for p in parts}
cfg = {'name': 'oro', 'zips': list(dict.fromkeys(zips)), 'out': '../../../anatomy/models/oro',
       'error_mm': 0.3, 'contact_mm': 0.5, 'contacts_across_groups_only': True, 'pack': True,
       'source': 'Bones, teeth and oesophagus: BodyParts3D, (c) The Database Center for Life Science, CC BY-SA 2.1 Japan. Cartilages, '
                 'membranes, tongue, soft palate, gingiva, pharynx, nasal mucosa, sinuses, trachea, muscles, vessels and nerves (curves '
                 'swept into tubes), tonsil and lymph nodes: Z-Anatomy, CC BY-SA 4.0 (from BodyParts3D), moved into the BodyParts3D frame',
       'parts': parts}
out_cfg = os.path.join(CFG, 'oro.json')
assert not os.path.exists(out_cfg) or json.load(open(out_cfg)).get('name') == 'oro'
json.dump(cfg, open(out_cfg, 'w'), indent=1)
os.makedirs(os.path.join(MODELS, 'oro'), exist_ok=True)
json.dump({'note': 'written by tools/head-neck/oro_config.py', 'mirror': M, 'parts': kinds},
          open(os.path.join(MODELS, 'oro', 'kinds.json'), 'w'), indent=0)
from collections import Counter
print(len(parts), 'parts', dict(Counter(k['kind'] for k in kinds.values())), 'mirrored', sum(k['mirror'] for k in kinds.values()))
