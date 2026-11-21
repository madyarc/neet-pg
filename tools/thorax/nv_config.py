"""Config for the page "Nerves, Vessels and Lymphatics of the Thorax" (anatomy/thorax/nerves-vessels.html, module 27):
one packed model of the thoracic wall and mediastinum so the page does not download the whole-body packs.
Same pattern as tools/upper-limb/nv_config.py, tools/lower-limb/nv_config.py and tools/thorax/heart_config.py.

Parts are copied from the existing whole-body configs with the same keys, names, files and per-part error_mm (a source
config's default error_mm is written on each part that had none), so names and colours match the other pages:
  bone     configs/skeleton.json      T1-T12, L1-L2 (start of the azygos vein and thoracic duct), ribs 1-12, costal
                                      cartilages 1-7, sternum, clavicles (both sides: they are in the skeleton)
  cart     (same)                     the costal cartilages are given their own kind (--cart on the page)
  muscle   configs/body-muscles.json  diaphragm, transversus thoracis (right; mirrored on the page)
  heart    configs/body-vessels.json  the four chambers as context (whole-body error; the detail is on heart.html)
  artery   configs/body-vessels.json  aorta (ascending, arch, thoracic, abdominal), arch branches, subclavian roots,
                                      internal thoracic and its end branches, costocervical / supreme intercostal,
                                      posterior intercostal and subcostal arteries, superior phrenic, pulmonary trunk
  vein     configs/body-vessels.json  SVC, brachiocephalic and subclavian veins, internal jugular, azygos system,
                                      superior intercostal and subcostal veins, ascending lumbar veins, internal
                                      thoracic veins, thoracic IVC, the four pulmonary veins
  nerve    configs/body-nerves.json   intercostal nerves, sympathetic trunk and its nerves, both vagus nerves
  ganglion configs/body-nerves.json   ganglia of the sympathetic trunk
  node     configs/body-lymph.json    the thoracic node groups; organ: the two lobes of the thymus
Z-Anatomy has no phrenic nerve and no thoracic duct: the page draws both as labelled approximate lines.
Right-only parts (body-* "mirror": true) are mirrored on the page with the transform copied into kinds.json.
Parts are ordered by colour (bone, cartilage, muscle, heart, artery, vein, nerve, ganglion, node, organ): the viewer
draws neighbouring parts of one colour with a single call. One group, contacts not needed.

Also writes anatomy/models/thorax-nv/kinds.json: {"mirror": {m, t}, "parts": {key: {"kind", "mirror"}}} for the page.

usage: python3 -I tools/thorax/nv_config.py   ->  tools/bones-rs/configs/thorax-nv.json (+ anatomy/models/thorax-nv/kinds.json)
then:  cd tools/bones-rs && target/release/bones build configs/thorax-nv.json   (through tools/capped)"""
import json, os, re
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
CFG = os.path.join(ROOT, 'tools', 'bones-rs', 'configs')
MODELS = os.path.join(ROOT, 'anatomy', 'models')
load = lambda n: json.load(open(os.path.join(CFG, n + '.json')))
meta = lambda g, f: json.load(open(os.path.join(MODELS, g, f + '.json')))

BONES = re.compile(r'^(\w+_thoracic_vertebra|first_lumbar_vertebra|second_lumbar_vertebra|(left|right)_\w+_rib|'
                   r'(left|right)_clavicle|manubrium|body_of_sternum|xiphoid_process)$')
CART = re.compile(r'^(left|right)_\w+_costal_cartilage$')
MUSCLES = ['m_diaphragm', 'm_transversus_thoracis']
CHAMBERS = ['v_right_atrium', 'v_right_ventricle', 'v_left_atrium', 'v_left_ventricle']
ARTERIES = ['v_ascending_aorta', 'v_aortic_arch', 'v_thoracic_aorta', 'v_abdominal_aorta', 'v_brachiocephalic_trunk',
            'v_right_common_carotid_artery', 'v_left_common_carotid_artery', 'v_right_subclavian_artery', 'v_left_subclavian_artery',
            'v_vertebral_artery_r', 'v_thyrocervical_trunk_r', 'v_costocervical_trunk_r', 'v_supreme_intercostal_artery_r',
            'v_internal_thoracic_artery_r', 'v_musculophrenic_artery_r', 'v_superior_epigastric_artery_r',
            'v_first_posterior_intercostal_artery_r', 'v_first_posterior_intercostal_artery_l',
            'v_second_posterior_intercostal_artery_r', 'v_second_posterior_intercostal_artery_l',
            'v_posterior_intercostal_arteries_r', 'v_posterior_intercostal_arteries_l', 'v_subcostal_artery_r', 'v_subcostal_artery_l',
            'v_superior_phrenic_arteries', 'v_pulmonary_trunk', 'v_bifurcation_of_pulmonary_trunk', 'v_right_pulmonary_artery',
            'v_left_pulmonary_artery']
VEINS = ['v_superior_vena_cava', 'v_right_brachiocephalic_vein', 'v_left_brachiocephalic_vein', 'v_right_subclavian_vein',
         'v_left_subclavian_vein', 'v_internal_jugular_vein_r', 'v_vertebral_vein_r', 'v_azygos_vein', 'v_hemi_azygos_vein',
         'v_accessory_hemi_azygos_vein', 'v_right_superior_intercostal_vein', 'v_left_superior_intercostal_vein',
         'v_right_subcostal_vein', 'v_left_subcostal_vein', 'v_right_ascending_lumbar_vein', 'v_left_ascending_lumbar_vein',
         'v_internal_thoracic_veins_r', 'v_musculophrenic_veins_r', 'v_inferior_vena_cava_thoracic_part',
         'v_right_superior_pulmonary_vein', 'v_right_inferior_pulmonary_vein', 'v_left_superior_pulmonary_vein',
         'v_left_inferior_pulmonary_vein']
NERVES = ['n_intercostal_nerves_r', 'n_sympathetic_trunk_r', 'n_sympathetic_nerves_r', 'n_vagus_nerve_x_r', 'n_vagus_nerve_x_l']
GANGLIA = ['n_ganglia_of_sympathetic_trunk_r']
NODES = ['l_paratracheal_thoracic_nodes', 'l_superior_tracheobronchial_nodes', 'l_inferior_tracheobronchial_nodes',
         'l_brachiocephalic_nodes', 'l_node_of_arch_of_azygos_vein', 'l_node_of_ligamentum_arteriosum', 'l_prepericardial_nodes',
         'l_lateral_pericardial_nodes', 'l_parasternal_nodes_r', 'l_intercostal_nodes_r', 'l_juxta_oesophageal_nodes',
         'l_prevertebral_nodes', 'l_superior_diaphragmatic_nodes']
ORGANS = ['l_right_lobe_of_thymus', 'l_left_lobe_of_thymus']


def copy(p, default_err, kind, mirror=False):
    return {'key': p['key'], 'name': p['name'], 'fma': p['fma'], 'files': p['files'], 'group': 'thnv',
            'error_mm': p.get('error_mm', default_err), '_kind': kind, '_mirror': bool(mirror)}


parts, zips = [], []
sk = load('skeleton'); zips += sk['zips']
parts += [copy(p, sk['error_mm'], 'bone') for p in sk['parts'] if BONES.match(p['key'])]
parts += [copy(p, sk['error_mm'], 'cart') for p in sk['parts'] if CART.match(p['key'])]

mu = load('body-muscles'); zips += mu['zips']; mp = {p['key']: p for p in mu['parts']}
mmeta = meta('body-muscles', 'muscles')['parts']
parts += [copy(mp[k], mu['error_mm'], 'muscle', mmeta.get(k, {}).get('mirror', k != 'm_diaphragm')) for k in MUSCLES]

ve = load('body-vessels'); zips += ve['zips']; vp = {p['key']: p for p in ve['parts']}
vmeta = meta('body-vessels', 'vessels')
for kind, keys in (('heart', CHAMBERS), ('artery', ARTERIES), ('vein', VEINS)):
    parts += [copy(vp[k], ve['error_mm'], kind, vmeta['parts'][k]['mirror']) for k in keys]

ne = load('body-nerves'); zips += ne['zips']; np_ = {p['key']: p for p in ne['parts']}
nmeta = meta('body-nerves', 'nerves')
for kind, keys in (('nerve', NERVES), ('ganglion', GANGLIA)):
    parts += [copy(np_[k], ne['error_mm'], kind, nmeta['parts'][k]['mirror']) for k in keys]

ly = load('body-lymph'); zips += ly['zips']; lp = {p['key']: p for p in ly['parts']}
lmeta = meta('body-lymph', 'lymph')
for kind, keys in (('node', NODES), ('organ', ORGANS)):
    parts += [copy(lp[k], ly['error_mm'], kind, lmeta['parts'][k]['mirror']) for k in keys]

assert len({p['key'] for p in parts}) == len(parts)
assert vmeta['mirror'] == nmeta['mirror'] == lmeta['mirror']
kinds = {p['key']: {'kind': p.pop('_kind'), 'mirror': p.pop('_mirror')} for p in parts}
cfg = {'name': 'thorax-nv', 'zips': list(dict.fromkeys(zips)), 'out': '../../../anatomy/models/thorax-nv',
       'error_mm': 0.3, 'contact_mm': 0.5, 'contacts_across_groups_only': True, 'pack': True,
       'source': 'Bones: BodyParts3D, (c) The Database Center for Life Science, CC BY-SA 2.1 Japan. Muscles, heart chambers, '
                 'vessels (curves swept into tubes), nerves (curves swept into tubes), lymph nodes and thymus: Z-Anatomy, '
                 'CC BY-SA 4.0 (from BodyParts3D), moved into the BodyParts3D frame',
       'parts': parts}
out_cfg = os.path.join(CFG, 'thorax-nv.json')
json.dump(cfg, open(out_cfg, 'w'), indent=1)
os.makedirs(os.path.join(MODELS, 'thorax-nv'), exist_ok=True)
json.dump({'note': 'written by tools/thorax/nv_config.py', 'mirror': vmeta['mirror'], 'parts': kinds},
          open(os.path.join(MODELS, 'thorax-nv', 'kinds.json'), 'w'), indent=0)
from collections import Counter
print(len(parts), 'parts', dict(Counter(k['kind'] for k in kinds.values())), 'mirrored', sum(k['mirror'] for k in kinds.values()))
