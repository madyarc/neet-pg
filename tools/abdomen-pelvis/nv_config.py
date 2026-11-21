"""Config for the page "Nerves and Vessels of the Abdomen and Pelvis" (anatomy/abdomen-pelvis/nerves-vessels.html):
one packed model of the posterior abdominal wall and pelvis so the page does not download the whole-body packs.
Same pattern and rules as tools/lower-limb/nv_config.py and tools/upper-limb/nv_config.py.

Parts are copied from the existing whole-body configs, with the same keys, names, files and per-part error_mm
(a source config's default error_mm is written on each part that had none), so names and colours match the other pages:
  bones      configs/skeleton.json      T11-L5, sacrum, both hip bones, ribs 10-12 of both sides (context)
  muscles    configs/body-muscles.json  psoas major, iliacus, quadratus lumborum, piriformis (right; mirrored in the page)
  vessels    configs/body-vessels.json  the abdominal aorta and its branches, the iliac vessels and the internal iliac
                                        branches, the IVC and its tributaries, the portal vein and its tributaries
  nerves     configs/body-nerves.json   lumbar plexus branches, the pelvic branches of the sacral plexus, the pudendal
                                        nerve, the cauda equina and the lowest part of the sympathetic trunk
  lymph      configs/body-lymph.json    the abdominal and pelvic node groups
Right-side Z-Anatomy parts marked "mirror" in the whole-body metadata (vessels.json, nerves.json, lymph.json,
muscles.json) are mirrored to the left in the page (all four files carry the same mirror transform, copied into nv.json),
so the pack holds only one copy. Parts are ordered by colour (bone, muscle, artery, vein, nerve, node): the viewer draws
neighbouring parts of one colour with a single call. Contacts are not needed (one group, contacts_across_groups_only).

Also writes anatomy/models/abd-nv/nv.json: {"mirror": {m, t}, "parts": {key: {"kind", "mirror"[, "portal"]}}}.

usage: python3 -I tools/abdomen-pelvis/nv_config.py   ->  tools/bones-rs/configs/abd-nv.json (+ anatomy/models/abd-nv/nv.json)
then:  cd tools/bones-rs && target/release/bones build configs/abd-nv.json   (through tools/capped)"""
import json, os
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
CFG = os.path.join(ROOT, 'tools', 'bones-rs', 'configs')
MODELS = os.path.join(ROOT, 'anatomy', 'models')
load = lambda n: json.load(open(os.path.join(CFG, n + '.json')))
meta = lambda g, f: json.load(open(os.path.join(MODELS, g, f)))

BONES = ['eleventh_thoracic_vertebra', 'twelfth_thoracic_vertebra'] + \
        [n + '_lumbar_vertebra' for n in ('first', 'second', 'third', 'fourth', 'fifth')] + \
        ['sacrum', 'right_hip_bone', 'left_hip_bone'] + [s + '_' + r + '_rib' for s in ('right', 'left') for r in ('tenth', 'eleventh', 'twelfth')]
MUSCLES = ['m_psoas_major', 'm_iliacus', 'm_quad_lumb', 'm_piriformis']
ARTERIES = ['abdominal_aorta', 'inferior_phrenic_artery', 'coeliac_trunk', 'left_gastric_artery', 'splenic_artery', 'common_hepatic_artery',
            'proper_hepatic_artery', 'gastroduodenal_artery', 'superior_mesenteric_artery', 'inferior_pancreaticoduodenal_artery',
            'anterior_inferior_pancreaticoduodenal_artery', 'middle_colic_artery', 'right_colic_artery', 'ileocolic_artery',
            'colic_branch_of_ileocolic_artery', 'ileal_branch_of_ileocolic_artery', 'appendicular_artery', 'marginal_artery',
            'inferior_mesenteric_artery', 'left_colic_artery', 'ascending_branch_of_left_colic_artery', 'descending_branch_of_left_colic_artery',
            'sigmoid_arteries', 'superior_anorectal_artery', 'inferior_suprarenal_artery_r', 'inferior_suprarenal_artery_l',
            'right_renal_artery', 'left_renal_artery', 'anterior_branch_of_renal_artery_r', 'posterior_branch_of_renal_artery_r',
            'anterior_branch_of_renal_artery_l', 'posterior_branch_of_renal_artery_l', 'right_testicular_artery_r', 'left_testicular_artery',
            'lumbar_arteries_r', 'lumbar_arteries_l', 'subcostal_artery_r', 'subcostal_artery_l', 'median_sacral_artery',
            'common_iliac_artery_r', 'common_iliac_artery_l', 'external_iliac_artery_r', 'inferior_epigastric_artery_r',
            'internal_iliac_artery_r', 'anterior_division_of_internal_iliac_artery_r', 'posterior_division_of_internal_iliac_artery_r',
            'iliolumbar_artery_r', 'iliacus_branch_of_iliolumbar_artery_r', 'lumbar_branch_of_iliolumbar_artery_r', 'spinal_branch_of_iliolumbar_artery_r',
            'superior_gluteal_artery_r', 'inferior_gluteal_artery_r', 'internal_pudendal_artery_r', 'obturator_artery_r']
VEINS = ['inferior_vena_cava_abdominal_part', 'inferior_vena_cava_thoracic_part', 'hepatic_veins', 'right_renal_vein', 'left_renal_vein',
         'right_testicular_vein', 'left_testicular_vein', 'lumbar_veins_r', 'lumbar_veins_l', 'right_ascending_lumbar_vein', 'left_ascending_lumbar_vein',
         'right_subcostal_vein', 'left_subcostal_vein', 'azygos_vein', 'hemi_azygos_vein', 'common_iliac_vein_r', 'common_iliac_vein_l',
         'external_iliac_vein_r', 'inferior_epigastric_vein_r', 'internal_iliac_vein_r', 'iliolumbar_vein_r', 'lateral_sacral_veins_r',
         'superior_gluteal_veins_r', 'inferior_gluteal_veins_r', 'internal_pudendal_vein_r',
         'hepatic_portal_vein', 'splenic_vein', 'superior_mesenteric_vein', 'inferior_mesenteric_vein', 'right_gastro_omental_vein',
         'left_gastro_omental_vein', 'middle_colic_vein', 'right_colic_vein', 'sigmoid_veins']
VESSELS = ['v_' + k for k in ARTERIES + VEINS]
NERVES = ['n_' + k for k in (
    'iliohypogastric_nerve_r', 'ilio_inguinal_nerve_r', 'genitofemoral_nerve_r', 'femoral_branch_of_genitofemoral_nerve_r',
    'genital_branch_of_genitofemoral_nerve_r', 'lateral_femoral_cutaneous_nerve_r', 'femoral_nerve_r', 'obturator_nerve_r',
    'sciatic_nerve_r', 'superior_gluteal_nerve_r', 'posterior_femoral_cutaneous_nerve_r', 'anterior_root_of_posterior_femoral_cutaneous_nerve_r',
    'posterior_root_of_posterior_femoral_cutaneous_nerve_r', 'nerve_to_piriformis_muscle_r', 'nerve_to_quadratus_femoris_muscle_r',
    'pudendal_nerve_r', 'cauda_equina', 'sympathetic_trunk_r', 'ganglia_of_sympathetic_trunk_r')]
NODES = ['l_' + k for k in (
    'coeliac_nodes', 'splenic_nodes', 'superior_pancreatic_nodes', 'inferior_pancreatic_nodes', 'right_gastric_nodes',
    'right_gastro_omental_nodes', 'suprapyloric_node', 'subpyloric_nodes', 'retropyloric_nodes', 'superior_pancreaticoduodenal_nodes',
    'cystic_node', 'inferior_diaphragmatic_nodes', 'central_superior_mesenteric_nodes', 'juxta_intestinal_mesenteric_nodes',
    'paracolic_superior_mesenteric_nodes', 'ileocolic_nodes', 'precaecal_nodes', 'retrocaecal_nodes', 'appendicular_nodes',
    'right_colic_nodes', 'middle_colic_nodes', 'left_colic_nodes', 'sigmoid_nodes', 'pararectal_nodes',
    'lateral_aortic_nodes', 'pre_aortic_nodes', 'retro_aortic_nodes', 'lateral_caval_nodes', 'precaval_nodes', 'retrocaval_nodes',
    'intermediate_lumbar_nodes', 'lateral_common_iliac_nodes', 'medial_common_iliac_nodes', 'intermediate_common_iliac_nodes',
    'medial_external_iliac_nodes_r', 'intermediate_external_iliac_nodes_r', 'inferior_epigastric_nodes_r', 'obturator_nodes_r',
    'lateral_sacral_nodes_r', 'superior_gluteal_nodes_r', 'inferior_gluteal_nodes_r', 'lateral_vesical_nodes_r',
    'prevesical_nodes', 'postvesical_nodes')]


def copy(p, default_err, kind, info):
    return {'key': p['key'], 'name': p['name'], 'fma': p['fma'], 'files': p['files'], 'group': 'nv',
            'error_mm': p.get('error_mm', default_err), '_kind': kind, '_mirror': bool(info.get('mirror')),
            '_portal': info.get('circuit') == 'portal'}


def take(cfg, keys, kind_of, mf):
    by = {p['key']: p for p in cfg['parts']}
    missing = [k for k in keys if k not in by]
    assert not missing, missing
    return [copy(by[k], cfg['error_mm'], kind_of(k), mf.get(k, {})) for k in keys]


parts, zips = [], []
sk = load('skeleton'); zips += sk['zips']
parts += take(sk, BONES, lambda k: 'bone', {})
mu = load('body-muscles'); zips += mu['zips']; mmeta = meta('body-muscles', 'muscles.json')
parts += take(mu, MUSCLES, lambda k: 'muscle', mmeta['parts'])
ve = load('body-vessels'); zips += ve['zips']; vmeta = meta('body-vessels', 'vessels.json')
vs = take(ve, VESSELS, lambda k: vmeta['parts'][k]['kind'], vmeta['parts'])
parts += [p for p in vs if p['_kind'] == 'artery'] + [p for p in vs if p['_kind'] == 'vein']
ne = load('body-nerves'); zips += ne['zips']; nmeta = meta('body-nerves', 'nerves.json')
parts += take(ne, NERVES, lambda k: 'nerve', nmeta['parts'])
ly = load('body-lymph'); zips += ly['zips']; lmeta = meta('body-lymph', 'lymph.json')
parts += take(ly, NODES, lambda k: 'node', lmeta['parts'])

M = vmeta['mirror']
assert nmeta['mirror'] == M and lmeta['mirror'] == M and mmeta['mirror'] == M, 'mirror transforms differ'
kinds = {}
for p in parts:
    d = {'kind': p.pop('_kind'), 'mirror': p.pop('_mirror')}
    if p.pop('_portal'): d['portal'] = True
    kinds[p['key']] = d
cfg = {'name': 'abd-nv', 'zips': list(dict.fromkeys(zips)), 'out': '../../../anatomy/models/abd-nv',
       'error_mm': 0.3, 'contact_mm': 0.5, 'contacts_across_groups_only': True, 'pack': True,
       'source': 'Bones: BodyParts3D, (c) The Database Center for Life Science, CC BY-SA 2.1 Japan. Muscles, vessels (curves '
                 'swept into tubes), nerves (curves swept into tubes) and lymph nodes: Z-Anatomy, CC BY-SA 4.0 (from BodyParts3D), '
                 'moved into the BodyParts3D frame',
       'parts': parts}
out = os.path.join(CFG, 'abd-nv.json')
assert not os.path.exists(out) or json.load(open(out)).get('name') == 'abd-nv'
json.dump(cfg, open(out, 'w'), indent=1)
os.makedirs(os.path.join(MODELS, 'abd-nv'), exist_ok=True)
json.dump({'note': 'written by tools/abdomen-pelvis/nv_config.py; mirror: the transform that makes a left part from a right one',
           'mirror': M, 'parts': kinds}, open(os.path.join(MODELS, 'abd-nv', 'nv.json'), 'w'), indent=0)
from collections import Counter
print(len(parts), 'parts', dict(Counter(k['kind'] for k in kinds.values())), 'mirrored in page:', sum(k['mirror'] for k in kinds.values()))
