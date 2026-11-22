"""Config for the page "Lungs, Pleura and Trachea" (anatomy/thorax/lungs.html, module 30): one packed model of the lungs,
pleura, airways and the vessels of the lung roots, with the thoracic cage for surface marking.
Same pattern as tools/thorax/nv_config.py and tools/thorax/heart_config.py.

Parts and where they come from (keys, names, files and error_mm of the whole-body configs where the part is already in one):
  bone     configs/skeleton.json      C6, C7, T1-T12, L1, ribs 1-12, sternum, clavicles (skeleton error_mm)
  cart     configs/skeleton.json      costal cartilages 1-7; cricoid cartilage (configs/head-neck-muscles.json)
  muscle   configs/body-muscles.json  diaphragm
  heart    configs/body-vessels.json  the four chambers, as context
  artery   configs/body-vessels.json  pulmonary trunk, right and left pulmonary arteries, their lobar and segmental
                                      branches; aorta (ascending, arch, thoracic) and the arch branches
  vein     configs/body-vessels.json  the four pulmonary veins and their tributaries; SVC, brachiocephalic veins, azygos,
                                      hemiazygos, accessory hemiazygos, thoracic IVC
  nerve    configs/body-nerves.json   both vagus nerves
  node     configs/body-lymph.json    intrapulmonary, superior and inferior tracheobronchial, paratracheal (thoracic) nodes
  gut      z-bp3d-lung-curves.zip     the oesophagus (Z-Anatomy curve swept into a tube by tools/zanat/export_curves.py;
                                      Z-Anatomy shapes it with a profile curve, the tube is round: approximate calibre)
  airway   z-bp3d-lung.zip            the trachea (mesh, tools/zanat/export_mod.py)
           z-bp3d-lung-curves.zip     main, lobar and segmental bronchi (curves swept into tubes)
  lobe     z-bp3d-lung.zip            the five lobes (Subsurf applied)
  pleura   z-bp3d-lung-pleura.zip     Z-Anatomy's single "Pleura" object (both pleural sacs), Subsurf applied but not its
                                      Solidify (the two thin shells poked through each other after simplification)
Exports (2026-11-21):
  export_curves.py Startup.blend z-to-bp3d.json sources-local/zanat/z-bp3d-lung-curves.zip tools/zanat/z-index-lung-curves.tsv Bronchi "Digestive canal"
  export_mod.py    Startup.blend z-to-bp3d.json sources-local/zanat/z-bp3d-lung.zip tools/zanat/z-index-lung.tsv "name:Trachea" and
                   "name:<lobe>" for the five lobes
  sources-local/facts/fill-lung-scripts/export_nosolid.py (same arguments) -> z-bp3d-lung-pleura.zip, z-index-lung-pleura.tsv "name:Pleura"
The lungs are asymmetric and Z-Anatomy models both: nothing is mirrored on this page.
Parts are ordered by colour: the viewer draws neighbouring parts of one colour with a single call. One group.

Also writes anatomy/models/lung/kinds.json: {"parts": {key: {"kind", "mirror": false}}} for the page.

usage: python3 -I tools/thorax/lung_config.py   ->  tools/bones-rs/configs/lung.json (+ anatomy/models/lung/kinds.json)
then:  cd tools/bones-rs && target/release/bones build configs/lung.json   (through tools/capped)"""
import json, os, re, csv
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
CFG = os.path.join(ROOT, 'tools', 'bones-rs', 'configs')
MODELS = os.path.join(ROOT, 'anatomy', 'models')
ZAN = os.path.join(ROOT, 'tools', 'zanat')
load = lambda n: json.load(open(os.path.join(CFG, n + '.json')))
LOBE_ERR, PLEURA_ERR, AIRWAY_ERR, TRACHEA_ERR, GUT_ERR = 0.45, 0.5, 0.15, 0.25, 0.3

BONES = re.compile(r'^(sixth_cervical_vertebra|seventh_cervical_vertebra|\w+_thoracic_vertebra|first_lumbar_vertebra|'
                   r'(left|right)_\w+_rib|(left|right)_clavicle|manubrium|body_of_sternum|xiphoid_process)$')
CART = re.compile(r'^(left|right)_\w+_costal_cartilage$')
CHAMBERS = ['v_right_atrium', 'v_right_ventricle', 'v_left_atrium', 'v_left_ventricle']
SYS_ART = ['v_ascending_aorta', 'v_aortic_arch', 'v_thoracic_aorta', 'v_brachiocephalic_trunk', 'v_right_common_carotid_artery',
           'v_left_common_carotid_artery', 'v_right_subclavian_artery', 'v_left_subclavian_artery']
SYS_VEIN = ['v_superior_vena_cava', 'v_right_brachiocephalic_vein', 'v_left_brachiocephalic_vein', 'v_azygos_vein',
            'v_hemi_azygos_vein', 'v_accessory_hemi_azygos_vein', 'v_inferior_vena_cava_thoracic_part']
NERVES = ['n_vagus_nerve_x_r', 'n_vagus_nerve_x_l']
NODES = ['l_intrapulmonary_nodes', 'l_superior_tracheobronchial_nodes', 'l_inferior_tracheobronchial_nodes',
         'l_paratracheal_thoracic_nodes']
LOBES = ['superior_lobe_of_right_lung', 'middle_lobe_of_right_lung', 'inferior_lobe_of_right_lung',
         'superior_lobe_of_left_lung', 'inferior_lobe_of_left_lung']
ZIP_LUNG = '../../../sources-local/zanat/z-bp3d-lung.zip'
ZIP_CURVES = '../../../sources-local/zanat/z-bp3d-lung-curves.zip'
ZIP_PLEURA = '../../../sources-local/zanat/z-bp3d-lung-pleura.zip'


def copy(p, default_err, kind):
    return {'key': p['key'], 'name': p['name'], 'fma': p['fma'], 'files': p['files'], 'group': 'lung',
            'error_mm': p.get('error_mm', default_err), '_kind': kind}


def zpart(key, name, file, err, kind):
    return {'key': key, 'name': name, 'fma': '', 'files': [file], 'group': 'lung', 'error_mm': err, '_kind': kind}


parts, zips = [], []
sk = load('skeleton'); zips += sk['zips']
parts += [copy(p, sk['error_mm'], 'bone') for p in sk['parts'] if BONES.match(p['key'])]
parts += [copy(p, sk['error_mm'], 'cart') for p in sk['parts'] if CART.match(p['key'])]
hn = load('head-neck-muscles'); hp = {p['key']: p for p in hn['parts']}
parts.append(copy(hp['cricoid_cart'], hn['error_mm'], 'cart')); zips += [z for z in hn['zips'] if 'extra' in z]

mu = load('body-muscles'); zips += mu['zips']; mp = {p['key']: p for p in mu['parts']}
parts.append(copy(mp['m_diaphragm'], mu['error_mm'], 'muscle'))

ve = load('body-vessels'); zips += ve['zips']; vp = {p['key']: p for p in ve['parts']}
vmeta = json.load(open(os.path.join(MODELS, 'body-vessels', 'vessels.json')))['parts']
PULM_A = [k for k in vp if vmeta[k]['kind'] == 'artery' and vmeta[k]['circuit'] == 'pulmonary']
PULM_V = [k for k in vp if vmeta[k]['kind'] == 'vein' and vmeta[k]['circuit'] == 'pulmonary']
for kind, keys in (('heart', CHAMBERS), ('artery', PULM_A + SYS_ART), ('vein', PULM_V + SYS_VEIN)):
    parts += [copy(vp[k], ve['error_mm'], kind) for k in keys]
ne = load('body-nerves'); zips += ne['zips']; np_ = {p['key']: p for p in ne['parts']}
parts += [copy(np_[k], ne['error_mm'], 'nerve') for k in NERVES]
ly = load('body-lymph'); zips += ly['zips']; lp = {p['key']: p for p in ly['parts']}
parts += [copy(lp[k], ly['error_mm'], 'node') for k in NODES]

curves = list(csv.DictReader(open(os.path.join(ZAN, 'z-index-lung-curves.tsv')), delimiter='\t'))
mesh = {r['file']: r for r in csv.DictReader(open(os.path.join(ZAN, 'z-index-lung.tsv')), delimiter='\t')}
parts.append(zpart('g_oesophagus', 'Oesophagus', 'Z_oesophagus', GUT_ERR, 'gut'))
parts.append(zpart('r_trachea', 'Trachea', 'Z_trachea', TRACHEA_ERR, 'airway'))
for r in curves:
    if 'Bronchi' not in r['collections']: continue
    nm = re.sub(r'\.r$', '', r['object'])
    if nm.startswith('(') and nm.endswith(')'): nm = nm[1:-1]
    parts.append(zpart('r_' + r['file'][2:], nm, r['file'], AIRWAY_ERR, 'airway'))
for l in LOBES:
    parts.append(zpart('r_' + l, mesh['Z_' + l]['object'], 'Z_' + l, LOBE_ERR, 'lobe'))
parts.append(zpart('r_pleura', 'Pleura', 'Z_pleura', PLEURA_ERR, 'pleura'))
zips += [ZIP_LUNG, ZIP_CURVES, ZIP_PLEURA]

assert len({p['key'] for p in parts}) == len(parts)
kinds = {p['key']: {'kind': p.pop('_kind'), 'mirror': False} for p in parts}
cfg = {'name': 'lung', 'zips': list(dict.fromkeys(zips)), 'out': '../../../anatomy/models/lung',
       'error_mm': 0.3, 'contact_mm': 0.5, 'contacts_across_groups_only': True, 'pack': True,
       'source': 'Bones: BodyParts3D, (c) The Database Center for Life Science, CC BY-SA 2.1 Japan. Lungs, pleura, trachea, '
                 'bronchi, oesophagus, cricoid cartilage, diaphragm, heart chambers, vessels, nerves and lymph nodes: Z-Anatomy, '
                 'CC BY-SA 4.0 (from BodyParts3D), moved into the BodyParts3D frame; bronchi, oesophagus, vessels and nerves '
                 'are curves swept into tubes',
       'parts': parts}
json.dump(cfg, open(os.path.join(CFG, 'lung.json'), 'w'), indent=1)
os.makedirs(os.path.join(MODELS, 'lung'), exist_ok=True)
json.dump({'note': 'written by tools/thorax/lung_config.py', 'parts': kinds},
          open(os.path.join(MODELS, 'lung', 'kinds.json'), 'w'), indent=0)
from collections import Counter
print(len(parts), 'parts', dict(Counter(k['kind'] for k in kinds.values())))
