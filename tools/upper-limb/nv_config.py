"""Config for the page "Nerves, Vessels and Lymph Nodes of the Upper Limb" (anatomy/upper-limb/nerves-vessels.html):
one packed model of the RIGHT upper limb so the page does not download the whole-body packs.

Parts are copied from the existing whole-body configs, with the same keys, names, files and per-part error_mm
(a source config's default error_mm is written on each part that had none), so names and colours match the other pages:
  bones      configs/skeleton.json      right upper-limb bones, clavicle, scapula, ribs 1-5, manubrium, C4-T2
  muscles    configs/body-muscles.json  right upper-limb muscles (+ the neck/axilla muscles: scalenes, SCM, omohyoid)
  vessels    configs/body-vessels.json  every part of region "Upper limb" + subclavian / axillary / neck-root vessels
  nerves     configs/body-nerves.json   every part of group "brachial" (brachial plexus and its branches)
  lymph      configs/body-lymph.json    axillary, interpectoral, infraclavicular, brachial, cubital, supratrochlear,
                                        supraclavicular nodes
Parts are ordered by colour (bone, muscle, artery, vein, nerve, node): the viewer draws neighbouring parts of one
colour with a single call. Contacts are not needed (one group, contacts_across_groups_only), which keeps the manifest small.

Also writes anatomy/models/ul-nv/nv.json: {key: {"kind": bone|muscle|artery|vein|nerve|node}} for the page.

usage: python3 -I tools/upper-limb/nv_config.py   ->  tools/bones-rs/configs/ul-nv.json (+ anatomy/models/ul-nv/nv.json)
then:  cd tools/bones-rs && target/release/bones build configs/ul-nv.json"""
import json, os, re
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
CFG = os.path.join(ROOT, 'tools', 'bones-rs', 'configs')
MODELS = os.path.join(ROOT, 'anatomy', 'models')
load = lambda n: json.load(open(os.path.join(CFG, n + '.json')))

BONES_UL = re.compile(r'^(right_(clavicle|scapula|humerus|radius|ulna|scaphoid|lunate|triquetral|pisiform|trapezium|trapezoid|'
                      r'capitate|hamate|\w+_metacarpal_bone|first_rib|second_rib|third_rib|fourth_rib|fifth_rib)|'
                      r'(distal|middle|proximal)_phalanx_of_right_(thumb|\w+_finger))$')
BONES_AXIAL = {'manubrium', 'fourth_cervical_vertebra', 'fifth_cervical_vertebra', 'sixth_cervical_vertebra',
               'seventh_cervical_vertebra', 'first_thoracic_vertebra', 'second_thoracic_vertebra'}
# body-muscles.json: the upper-limb block runs from pectoralis major to the palmar aponeurosis; plus the neck muscles
# that bound the posterior triangle / scalene gap the plexus and subclavian artery pass through
MUSCLE_NECK = {'m_scal_ant', 'm_scal_med', 'm_scal_post', 'm_scm', 'm_omohyoid'}
VESSELS_NECK = {
    'v_right_subclavian_artery', 'v_brachiocephalic_trunk', 'v_vertebral_artery_r', 'v_thyrocervical_trunk_r',
    'v_suprascapular_artery_r', 'v_transverse_cervical_artery_r', 'v_deep_branch_of_transverse_cervical_artery_r',
    'v_superficial_branch_of_transverse_cervical_artery_r', 'v_internal_thoracic_artery_r', 'v_costocervical_trunk_r',
    'v_axillary_artery_r', 'v_thoraco_acromial_artery_r', 'v_pectoral_branches_of_thoraco_acromial_artery_r',
    'v_lateral_thoracic_artery_r', 'v_subscapular_artery_r', 'v_circumflex_scapular_artery_r', 'v_thoracodorsal_artery_r',
    'v_right_subclavian_vein', 'v_right_brachiocephalic_vein', 'v_internal_jugular_vein_r', 'v_external_jugular_vein_r',
    'v_lateral_thoracic_vein_r', 'v_thoracodorsal_vein_r', 'v_subscapular_vein_r', 'v_suprascapular_vein_r'}
NODES = {'l_anterior_axillary_nodes_r', 'l_posterior_axillary_nodes_r', 'l_lateral_axillary_nodes_r', 'l_central_axillary_nodes_r',
         'l_apical_axillary_nodes_r', 'l_interpectoral_nodes_r', 'l_infraclavicular_nodes_r', 'l_brachial_nodes_r',
         'l_cubital_nodes_r', 'l_supratrochlear_nodes_r', 'l_supraclavicular_nodes_r'}


def copy(p, default_err, group):
    return {'key': p['key'], 'name': p['name'], 'fma': p['fma'], 'files': p['files'], 'group': 'nv',
            'error_mm': p.get('error_mm', default_err), '_kind': group}


parts, zips = [], []
sk = load('skeleton'); zips += sk['zips']
parts += [copy(p, sk['error_mm'], 'bone') for p in sk['parts'] if BONES_UL.match(p['key']) or p['key'] in BONES_AXIAL]

mu = load('body-muscles'); zips += mu['zips']
keys = [p['key'] for p in mu['parts']]
ul = set(keys[keys.index('m_pec_major'):keys.index('m_palmar_apon') + 1])
parts += [copy(p, mu['error_mm'], 'muscle') for p in mu['parts'] if p['key'] in ul or p['key'] in MUSCLE_NECK]

ve = load('body-vessels'); zips += ve['zips']
vmeta = json.load(open(os.path.join(MODELS, 'body-vessels', 'vessels.json')))['parts']
sel = [p for p in ve['parts'] if p['key'] in VESSELS_NECK or vmeta[p['key']]['region'] == 'Upper limb']
for kind in ('artery', 'vein'):
    parts += [copy(p, ve['error_mm'], kind) for p in sel if vmeta[p['key']]['kind'] == kind]

ne = load('body-nerves'); zips += ne['zips']
nmeta = json.load(open(os.path.join(MODELS, 'body-nerves', 'nerves.json')))['parts']
parts += [copy(p, ne['error_mm'], 'nerve') for p in ne['parts'] if nmeta[p['key']]['group'] == 'brachial']

ly = load('body-lymph'); zips += ly['zips']
parts += [copy(p, ly['error_mm'], 'node') for p in ly['parts'] if p['key'] in NODES]

missing = (VESSELS_NECK | NODES | MUSCLE_NECK | BONES_AXIAL) - {p['key'] for p in parts}
assert not missing, missing
kinds = {p['key']: {'kind': p.pop('_kind')} for p in parts}
cfg = {'name': 'ul-nv', 'zips': list(dict.fromkeys(zips)), 'out': '../../../anatomy/models/ul-nv',
       'error_mm': 0.3, 'contact_mm': 0.5, 'contacts_across_groups_only': True, 'pack': True,
       'source': 'Bones: BodyParts3D, (c) The Database Center for Life Science, CC BY-SA 2.1 Japan. Muscles, vessels (curves '
                 'swept into tubes), nerves (curves swept into tubes) and lymph nodes: Z-Anatomy, CC BY-SA 4.0 (from BodyParts3D), '
                 'moved into the BodyParts3D frame',
       'parts': parts}
json.dump(cfg, open(os.path.join(CFG, 'ul-nv.json'), 'w'), indent=1)
os.makedirs(os.path.join(MODELS, 'ul-nv'), exist_ok=True)
json.dump({'note': 'written by tools/upper-limb/nv_config.py', 'parts': kinds}, open(os.path.join(MODELS, 'ul-nv', 'nv.json'), 'w'), indent=0)
from collections import Counter
print(len(parts), 'parts', dict(Counter(k['kind'] for k in kinds.values())))
