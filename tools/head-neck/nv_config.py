"""Config for the page "Nerves, Vessels and Lymph Nodes of the Head and Neck" (anatomy/head-neck/nerves-vessels.html,
module 29): one packed model of the head and neck so the page does not download the whole-body packs.
Same pattern as tools/thorax/nv_config.py and tools/upper-limb/nv_config.py.

Parts are copied from the existing whole-body configs with the same keys, names, files and per-part error_mm (a source
config's default error_mm is written on each part that had none), so names and colours match the other pages:
  bone     configs/skeleton.json      skull bones, mandible, hyoid, C1-C7, T1-T2, clavicles, ribs 1-2, manubrium (context)
  cart     (same)                     first costal cartilages
  muscle   configs/body-muscles.json  sternocleidomastoid, scalenus anterior / medius, digastric, omohyoid (right;
                                      mirrored on the page): glass context for the carotid sheath and subclavian parts
  artery   configs/body-vessels.json  arch of the aorta and its branches, subclavian and its branches, carotids and the
                                      external carotid branches, the vertebral / basilar system and the circle of Willis
                                      (the cortical branches of the cerebral arteries are left out), orbital arteries
  vein     configs/body-vessels.json  dural venous sinuses, ophthalmic veins, veins of the face and neck, jugular,
                                      subclavian and brachiocephalic veins, SVC
  nerve    configs/body-nerves.json   cranial nerves I-XII (the cochlear / vestibular parts left out: the ear is a later
                                      module), sympathetic trunk and its nerves, roots and trunks of the brachial plexus
  ganglion configs/body-nerves.json   ganglia of the sympathetic trunk
  node     configs/body-lymph.json    the head and neck node groups (the palatine tonsil is left out: a later module)
Z-Anatomy has no cervical plexus, no phrenic nerve, no lingual, superior thyroid or posterior auricular artery, no
recurrent laryngeal nerve as a separate part and no lymph vessels.
Right-only parts (body-* "mirror": true) are mirrored on the page with the transform copied into kinds.json.
Parts are ordered by colour (bone, cartilage, muscle, artery, vein, nerve, ganglion, node): the viewer draws neighbouring
parts of one colour with a single call. One group, contacts not needed.

Also writes anatomy/models/hn-nv/kinds.json: {"mirror": {m, t}, "parts": {key: {"kind", "mirror"}}} for the page.

usage: python3 -I tools/head-neck/nv_config.py   ->  tools/bones-rs/configs/hn-nv.json (+ anatomy/models/hn-nv/kinds.json)
then:  cd tools/bones-rs && target/release/bones build configs/hn-nv.json   (through tools/capped)"""
import json, os, re
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
CFG = os.path.join(ROOT, 'tools', 'bones-rs', 'configs')
MODELS = os.path.join(ROOT, 'anatomy', 'models')
load = lambda n: json.load(open(os.path.join(CFG, n + '.json')))
meta = lambda g, f: json.load(open(os.path.join(MODELS, g, f + '.json')))

BONES = re.compile(r'^(frontal_bone|(left|right)_parietal_bone|occipital_bone|(left|right)_temporal_bone|sphenoid_bone|ethmoid|'
                   r'(left|right)_(maxilla|zygomatic_bone|nasal_bone|lacrimal_bone|palatine_bone|inferior_nasal_concha)|vomer|'
                   r'mandible|hyoid_bone|atlas|axis|(third|fourth|fifth|sixth|seventh)_cervical_vertebra|'
                   r'(first|second)_thoracic_vertebra|(left|right)_clavicle|(left|right)_(first|second)_rib|manubrium)$')
CART = re.compile(r'^(left|right)_first_costal_cartilage$')
MUSCLES = ['m_scm', 'm_scal_ant', 'm_scal_med', 'm_digastric', 'm_omohyoid']
# arteries outside the "Head and neck" region of body-vessels (Trunk): the roots of the neck
TRUNK_ART = ['v_aortic_arch', 'v_brachiocephalic_trunk', 'v_right_subclavian_artery', 'v_left_subclavian_artery',
             'v_thyrocervical_trunk_r', 'v_costocervical_trunk_r', 'v_supreme_intercostal_artery_r', 'v_internal_thoracic_artery_r',
             'v_suprascapular_artery_r', 'v_superficial_branch_of_transverse_cervical_artery_r',
             'v_deep_branch_of_transverse_cervical_artery_r']
TRUNK_VEIN = ['v_superior_vena_cava', 'v_right_brachiocephalic_vein', 'v_left_brachiocephalic_vein', 'v_right_subclavian_vein',
              'v_left_subclavian_vein', 'v_common_facial_vein_r']
# head-and-neck parts left out: cortical branches of the cerebral arteries (the circle of Willis and the main trunks stay),
# the unnamed part "v_x_r", the inner-ear nerves, the palatine tonsil
SKIP = re.compile(r'^v_(x_r|artery_of_(central|precentral)_sulcus_r|branch_to_angular_gyrus_r|callosomarginal_artery_r|'
                  r'distal_lateral_striate|proximal_lateral_striate|frontal_branches_of_callosomarginal|insular_branches|'
                  r'lateral_frontobasal|lateral_occipital|medial_occipital|middle_cerebral_artery_m3|orbitofrontal_branches|'
                  r'parietal_branches|parieto_occipital|pericallosal|postcentral|posterior_parietal|prefrontal|'
                  r'temporal_branches_of_middle|temporo_occipital|anterior_temporal_branch|posterior_temporal_branch|'
                  r'lateral_pontine|medial_pontine)|^n_(cochlear_nerve|vestibular_nerve)|^l_palatine_tonsil')
NERVES_UL = ['n_roots_of_brachial_plexus_r', 'n_superior_trunk_of_brachial_plexus_r', 'n_middle_trunk_of_brachial_plexus_r',
             'n_inferior_trunk_of_brachial_plexus_r']


def copy(p, default_err, kind, mirror=False):
    return {'key': p['key'], 'name': p['name'], 'fma': p['fma'], 'files': p['files'], 'group': 'hnnv',
            'error_mm': p.get('error_mm', default_err), '_kind': kind, '_mirror': bool(mirror)}


parts, zips = [], []
sk = load('skeleton'); zips += sk['zips']
parts += [copy(p, sk['error_mm'], 'bone') for p in sk['parts'] if BONES.match(p['key'])]
parts += [copy(p, sk['error_mm'], 'cart') for p in sk['parts'] if CART.match(p['key'])]

mu = load('body-muscles'); zips += mu['zips']; mp = {p['key']: p for p in mu['parts']}
mmeta = meta('body-muscles', 'muscles')['parts']
parts += [copy(mp[k], mu['error_mm'], 'muscle', mmeta[k]['mirror']) for k in MUSCLES]

ve = load('body-vessels'); zips += ve['zips']
vmeta = meta('body-vessels', 'vessels')
hn = lambda m, k: m['parts'].get(k, {}).get('region') == 'Head and neck' and not SKIP.search(k)
vparts = [p for p in ve['parts'] if p['key'] in TRUNK_ART + TRUNK_VEIN or hn(vmeta, p['key'])]
for kind in ('artery', 'vein'):
    parts += [copy(p, ve['error_mm'], kind, vmeta['parts'][p['key']]['mirror']) for p in vparts
              if vmeta['parts'][p['key']]['kind'] == kind]

ne = load('body-nerves'); zips += ne['zips']
nmeta = meta('body-nerves', 'nerves')
nparts = [p for p in ne['parts'] if p['key'] in NERVES_UL or hn(nmeta, p['key'])]
for kind in ('nerve', 'ganglion'):
    parts += [copy(p, ne['error_mm'], kind, nmeta['parts'][p['key']]['mirror']) for p in nparts
              if nmeta['parts'][p['key']]['kind'] == kind]

ly = load('body-lymph'); zips += ly['zips']
lmeta = meta('body-lymph', 'lymph')
parts += [copy(p, ly['error_mm'], 'node', lmeta['parts'][p['key']]['mirror']) for p in ly['parts']
          if hn(lmeta, p['key']) and lmeta['parts'][p['key']]['kind'] == 'node']

assert len({p['key'] for p in parts}) == len(parts)
assert vmeta['mirror'] == nmeta['mirror'] == lmeta['mirror']
kinds = {p['key']: {'kind': p.pop('_kind'), 'mirror': p.pop('_mirror')} for p in parts}
cfg = {'name': 'hn-nv', 'zips': list(dict.fromkeys(zips)), 'out': '../../../anatomy/models/hn-nv',
       'error_mm': 0.3, 'contact_mm': 0.5, 'contacts_across_groups_only': True, 'pack': True,
       'source': 'Bones: BodyParts3D, (c) The Database Center for Life Science, CC BY-SA 2.1 Japan. Muscles, vessels (curves '
                 'swept into tubes), nerves (curves swept into tubes) and lymph nodes: Z-Anatomy, CC BY-SA 4.0 (from '
                 'BodyParts3D), moved into the BodyParts3D frame',
       'parts': parts}
out_cfg = os.path.join(CFG, 'hn-nv.json')
assert not os.path.exists(out_cfg) or json.load(open(out_cfg)).get('name') == 'hn-nv'
json.dump(cfg, open(out_cfg, 'w'), indent=1)
os.makedirs(os.path.join(MODELS, 'hn-nv'), exist_ok=True)
json.dump({'note': 'written by tools/head-neck/nv_config.py', 'mirror': vmeta['mirror'], 'parts': kinds},
          open(os.path.join(MODELS, 'hn-nv', 'kinds.json'), 'w'), indent=0)
from collections import Counter
print(len(parts), 'parts', dict(Counter(k['kind'] for k in kinds.values())), 'mirrored', sum(k['mirror'] for k in kinds.values()))
