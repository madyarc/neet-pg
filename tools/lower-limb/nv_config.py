"""Config for the page "Nerves, Vessels and Lymph Nodes of the Lower Limb" (anatomy/lower-limb/nerves-vessels.html):
one packed model of the RIGHT lower limb so the page does not download the whole-body packs.
The lower-limb counterpart of tools/upper-limb/nv_config.py (same pattern, same rules).

Parts are copied from the existing whole-body configs, with the same keys, names, files and per-part error_mm
(a source config's default error_mm is written on each part that had none), so names and colours match the other pages:
  bones      configs/skeleton.json      right lower-limb bones, right hip bone, sacrum, L5
  muscles    configs/body-muscles.json  right lower-limb muscles (psoas major ... fibular retinacula) + inguinal ligament
  vessels    configs/body-vessels.json  every right-side part of region "Lower limb" + the iliac, gluteal, pudendal,
                                        obturator and inferior epigastric vessels, the lower aorta and IVC
                                        (minus the small foot vessels in DROP)
  nerves     configs/body-nerves.json   every right-side part of group "lumbosacral" + the pudendal and iliohypogastric nerves
  lymph      configs/body-lymph.json    inguinal, popliteal and external iliac nodes (right)
Body-vessels / body-nerves label a few right-side parts "midline" (no _r suffix; their x is < 0, i.e. right): those are
kept, the "left" ones dropped. Parts are ordered by colour (bone, muscle, artery, vein, nerve, node): the viewer draws
neighbouring parts of one colour with a single call. Contacts are not needed (one group, contacts_across_groups_only).

Also writes anatomy/models/ll-nv/nv.json: {key: {"kind": bone|muscle|artery|vein|nerve|node}} for the page.

usage: python3 -I tools/lower-limb/nv_config.py   ->  tools/bones-rs/configs/ll-nv.json (+ anatomy/models/ll-nv/nv.json)
then:  cd tools/bones-rs && target/release/bones build configs/ll-nv.json   (through tools/capped)"""
import json, os, re
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
CFG = os.path.join(ROOT, 'tools', 'bones-rs', 'configs')
MODELS = os.path.join(ROOT, 'anatomy', 'models')
load = lambda n: json.load(open(os.path.join(CFG, n + '.json')))

BONES_LL = re.compile(r'^(right_(hip_bone|femur|patella|tibia|fibula|talus|calcaneus|cuboid_bone|\w+_cuneiform_bone|\w+_metatarsal_bone)|'
                      r'navicular_bone_of_right_foot|(distal|middle|proximal)_phalanx_of_right_\w+_toe)$')
BONES_AXIAL = {'sacrum', 'fifth_lumbar_vertebra'}
MUSCLE_EXTRA = {'m_inguinal_lig'}
VESSELS_TRUNK = {
    'v_abdominal_aorta', 'v_inferior_vena_cava_abdominal_part', 'v_common_iliac_artery_r', 'v_common_iliac_vein_r',
    'v_external_iliac_artery_r', 'v_external_iliac_vein_r', 'v_internal_iliac_artery_r', 'v_internal_iliac_vein_r',
    'v_anterior_division_of_internal_iliac_artery_r', 'v_posterior_division_of_internal_iliac_artery_r',
    'v_superior_gluteal_artery_r', 'v_superior_gluteal_veins_r', 'v_inferior_gluteal_artery_r', 'v_inferior_gluteal_veins_r',
    'v_internal_pudendal_artery_r', 'v_internal_pudendal_vein_r', 'v_obturator_artery_r',
    'v_inferior_epigastric_artery_r', 'v_inferior_epigastric_vein_r'}
NERVES_EXTRA = {'n_pudendal_nerve_r', 'n_iliohypogastric_nerve_r'}
# left out to keep the pack near the size of ul-nv (~850 KB): the small veins and arteries of the toes and metatarsals, the
# genicular veins, the obturator nodes, L4 (none is needed by the page)
DROP = {'v_plantar_digital_veins_r', 'v_dorsal_digital_veins_of_foot_r', 'v_intercapitular_veins_of_foot_r', 'v_plantar_metatarsal_veins_r',
        'v_dorsal_metatarsal_veins_r', 'v_genicular_veins_r', 'v_perforating_branches_of_plantar_metatarsal_arteries_r',
        'v_proper_plantar_digital_arteries_r', 'v_dorsal_digital_arteries_of_foot_r'}
NODES = {'l_superolateral_superficial_inguinal_nodes_r', 'l_superomedial_superficial_inguinal_nodes_r',
         'l_inferior_superficial_inguinal_nodes_r', 'l_proximal_deep_inguinal_node_r', 'l_intermediate_deep_inguinal_node_r',
         'l_superficial_popliteal_nodes_r', 'l_deep_popliteal_nodes_r', 'l_medial_external_iliac_nodes_r',
         'l_intermediate_external_iliac_nodes_r'}


def copy(p, default_err, group):
    return {'key': p['key'], 'name': p['name'], 'fma': p['fma'], 'files': p['files'], 'group': 'nv',
            'error_mm': p.get('error_mm', default_err), '_kind': group}


parts, zips = [], []
sk = load('skeleton'); zips += sk['zips']
parts += [copy(p, sk['error_mm'], 'bone') for p in sk['parts'] if BONES_LL.match(p['key']) or p['key'] in BONES_AXIAL]

mu = load('body-muscles'); zips += mu['zips']
keys = [p['key'] for p in mu['parts']]
ll = set(keys[keys.index('m_psoas_major'):keys.index('m_inf_fib_ret') + 1])
parts += [copy(p, mu['error_mm'], 'muscle') for p in mu['parts'] if p['key'] in ll or p['key'] in MUSCLE_EXTRA]

ve = load('body-vessels'); zips += ve['zips']
vmeta = json.load(open(os.path.join(MODELS, 'body-vessels', 'vessels.json')))['parts']
sel = [p for p in ve['parts'] if p['key'] not in DROP and (p['key'] in VESSELS_TRUNK or
       (vmeta[p['key']]['region'] == 'Lower limb' and vmeta[p['key']]['side'] != 'left'))]
for kind in ('artery', 'vein'):
    parts += [copy(p, ve['error_mm'], kind) for p in sel if vmeta[p['key']]['kind'] == kind]

ne = load('body-nerves'); zips += ne['zips']
nmeta = json.load(open(os.path.join(MODELS, 'body-nerves', 'nerves.json')))['parts']
parts += [copy(p, ne['error_mm'], 'nerve') for p in ne['parts'] if p['key'] in NERVES_EXTRA or
          (nmeta[p['key']]['group'] == 'lumbosacral' and nmeta[p['key']]['side'] != 'left')]

ly = load('body-lymph'); zips += ly['zips']
parts += [copy(p, ly['error_mm'], 'node') for p in ly['parts'] if p['key'] in NODES]

missing = (VESSELS_TRUNK | NODES | MUSCLE_EXTRA | BONES_AXIAL | NERVES_EXTRA) - {p['key'] for p in parts}
assert not missing, missing
kinds = {p['key']: {'kind': p.pop('_kind')} for p in parts}
cfg = {'name': 'll-nv', 'zips': list(dict.fromkeys(zips)), 'out': '../../../anatomy/models/ll-nv',
       'error_mm': 0.3, 'contact_mm': 0.5, 'contacts_across_groups_only': True, 'pack': True,
       'source': 'Bones: BodyParts3D, (c) The Database Center for Life Science, CC BY-SA 2.1 Japan. Muscles, vessels (curves '
                 'swept into tubes), nerves (curves swept into tubes) and lymph nodes: Z-Anatomy, CC BY-SA 4.0 (from BodyParts3D), '
                 'moved into the BodyParts3D frame',
       'parts': parts}
json.dump(cfg, open(os.path.join(CFG, 'll-nv.json'), 'w'), indent=1)
os.makedirs(os.path.join(MODELS, 'll-nv'), exist_ok=True)
json.dump({'note': 'written by tools/lower-limb/nv_config.py', 'parts': kinds}, open(os.path.join(MODELS, 'll-nv', 'nv.json'), 'w'), indent=0)
from collections import Counter
print(len(parts), 'parts', dict(Counter(k['kind'] for k in kinds.values())))
