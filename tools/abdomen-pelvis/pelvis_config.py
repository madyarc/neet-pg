"""Config for the pages "Pelvic Viscera" (anatomy/abdomen-pelvis/pelvis.html) and "Perineum and Male External Genitalia"
(anatomy/abdomen-pelvis/perineum.html), module 35: one packed model of the male pelvis and perineum, used by both pages.
Same pattern as tools/abdomen-pelvis/organs_config.py (organs) and nv_config.py (right-side parts mirrored in the page).

Both sources are male (BodyParts3D and Z-Anatomy have no uterus, uterine tubes, ovaries or vagina), so the female organs
are drawn as schematics on the pages.

Parts and where they come from (keys, names, files and error_mm of the whole-body configs where the part is already in one):
  bone    configs/skeleton.json       L5, sacrum, hip bones (skeleton error_mm). BodyParts3D's sacrum mesh includes the coccyx:
                                      Z-Anatomy's separate coccyx (exported to z-bp3d-pelv.zip for the check) lies on it, median 1.8 mm
  lig     configs/ax-joints.json      sacrotuberous and sacrospinous ligaments (right; mirrored in the page)
  floor   configs/trunk-muscles.json  pubococcygeus, iliococcygeus, coccygeus, tendinous arch of levator ani (right; mirrored)
          z-bp3d-pelv.zip             pubo-analis (Z-Anatomy's name for the puborectal part of levator ani; right; mirrored)
          BodyParts3D 3.0             external anal sphincter (FMA21930, one midline mesh)
  wall    configs/lower-limb-muscles.json  piriformis (right; mirrored); z-bp3d-pelv.zip: obturator internus (right; mirrored)
  artery, vein  configs/body-vessels.json  internal iliac artery and its divisions and named branches in Z-Anatomy, the
          testicular arteries and veins, the left renal vein, IVC, aorta, iliac vessels, penile vessels (right ones mirrored)
  nerve   configs/body-nerves.json    pudendal, obturator, genital branch of genitofemoral, ilio-inguinal (right; mirrored)
  node    configs/body-lymph.json     lateral aortic (lumbar) nodes, superficial inguinal nodes, nodes of the pelvic wall and viscera
  BodyParts3D 3.0 organ meshes (closed, already in the frame; the Z-Anatomy copies of the same organs, exported for comparison
          to z-bp3d-pelv.zip, lie within 1-2 mm of them: same meshes, Z-Anatomy re-topologised and smoothed; the
          BodyParts3D ones are kept, as for the stomach on the abdominal organs page): ureters FMA15571/15572 (as on the abdominal
          organs page), urinary bladder FMA15900, urethra FMA19667
          (with the prostatic and spongy parts), prostate FMA9600, seminal vesicles FMA19387/19388, testes FMA7211/7212,
          epididymides FMA18256/18257, corpus cavernosum FMA19618 (both crura and bodies), corpus spongiosum FMA19617nsn,
          glans FMA18247, rectum FMA14544 (down to the anal canal; no separate anal canal)
  Z-Anatomy curves swept into tubes (tools/zanat/export_curves.py -> z-bp3d-pelv-curves.zip): ductus deferens (both),
          ejaculatory ducts (both)
Not in either source: scrotum (BodyParts3D lists it, no mesh), the female organs, perineal membrane, perineal body,
bulbospongiosus, ischiocavernosus, transverse perineal muscles, external urethral sphincter, internal anal sphincter,
ischio-anal fat, peritoneum, fasciae, tunica vaginalis, bulbourethral glands: drawn as schematics on the pages.
Exports (2026-11-22):
  export_mod.py    Startup.blend z-to-bp3d.json sources-local/zanat/z-bp3d-pelv.zip tools/zanat/z-index-pelv.tsv "name:<object>" ...
  export_curves.py Startup.blend z-to-bp3d.json sources-local/zanat/z-bp3d-pelv-curves.zip tools/zanat/z-index-pelv-curves.tsv
                   "Urinary system" "Genital systems'"   (only the ductus deferens and ejaculatory ducts are used)
Parts are ordered by colour (the viewer draws neighbouring parts of one colour with a single call).

Also writes anatomy/models/pelv/kinds.json: {"mirror": {m, t}, "parts": {key: {"kind", "mirror"}}} for the pages.

usage: python3 -I tools/abdomen-pelvis/pelvis_config.py   ->  tools/bones-rs/configs/pelv.json (+ anatomy/models/pelv/kinds.json)
then:  cd tools/bones-rs && target/release/bones build configs/pelv.json   (through tools/capped)"""
import json, os, csv
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
CFG = os.path.join(ROOT, 'tools', 'bones-rs', 'configs')
MODELS = os.path.join(ROOT, 'anatomy', 'models')
ZAN = os.path.join(ROOT, 'tools', 'zanat')
load = lambda n: json.load(open(os.path.join(CFG, n + '.json')))
meta = lambda g, f: json.load(open(os.path.join(MODELS, g, f)))
ORGAN_ERR, DUCT_ERR, MUSCLE_ERR = 0.3, 0.15, 0.4
ZIP_PELV = '../../../sources-local/zanat/z-bp3d-pelv.zip'
ZIP_CURVES = '../../../sources-local/zanat/z-bp3d-pelv-curves.zip'

BONES = ['fifth_lumbar_vertebra', 'sacrum', 'right_hip_bone', 'left_hip_bone']
ARTERIES = ['abdominal_aorta', 'right_testicular_artery_r', 'left_testicular_artery', 'median_sacral_artery', 'common_iliac_artery_r', 'common_iliac_artery_l',
            'external_iliac_artery_r', 'inferior_epigastric_artery_r', 'internal_iliac_artery_r', 'anterior_division_of_internal_iliac_artery_r',
            'posterior_division_of_internal_iliac_artery_r', 'superior_gluteal_artery_r', 'inferior_gluteal_artery_r', 'internal_pudendal_artery_r',
            'obturator_artery_r', 'superior_anorectal_artery', 'deep_artery_of_penis_r', 'dorsal_artery_of_penis_r']
VEINS = ['inferior_vena_cava_abdominal_part', 'left_renal_vein', 'right_testicular_vein', 'left_testicular_vein', 'common_iliac_vein_r', 'common_iliac_vein_l',
         'external_iliac_vein_r', 'internal_iliac_vein_r', 'internal_pudendal_vein_r', 'deep_dorsal_vein_of_penis', 'superficial_dorsal_veins_of_penis']
NERVES = ['pudendal_nerve_r', 'obturator_nerve_r', 'genital_branch_of_genitofemoral_nerve_r', 'ilio_inguinal_nerve_r']
NODES = ['lateral_aortic_nodes', 'pre_aortic_nodes', 'superomedial_superficial_inguinal_nodes_r', 'superolateral_superficial_inguinal_nodes_r',
         'inferior_superficial_inguinal_nodes_r', 'obturator_nodes_r', 'lateral_sacral_nodes_r', 'lateral_vesical_nodes_r', 'pararectal_nodes',
         'prevesical_nodes', 'postvesical_nodes']
# BodyParts3D 3.0 organs: (key, FMA file, name, kind)
BP = [('o_ureter_r', 'FMA15571', 'Right ureter', 'urinary'), ('o_ureter_l', 'FMA15572', 'Left ureter', 'urinary'),
      ('o_bladder', 'FMA15900', 'Urinary bladder', 'urinary'), ('o_urethra', 'FMA19667', 'Urethra', 'urinary'),
      ('o_prostate', 'FMA9600', 'Prostate', 'prostate'),
      ('o_seminal_vesicle_r', 'FMA19387', 'Right seminal vesicle', 'sv'), ('o_seminal_vesicle_l', 'FMA19388', 'Left seminal vesicle', 'sv'),
      ('o_testis_r', 'FMA7211', 'Right testis', 'testis'), ('o_testis_l', 'FMA7212', 'Left testis', 'testis'),
      ('o_epididymis_r', 'FMA18256', 'Right epididymis', 'duct'), ('o_epididymis_l', 'FMA18257', 'Left epididymis', 'duct'),
      ('o_corpus_cavernosum', 'FMA19618', 'Corpora cavernosa (crura and body)', 'erect'),
      ('o_corpus_spongiosum', 'FMA19617nsn', 'Corpus spongiosum (with the bulb)', 'spong'), ('o_glans', 'FMA18247', 'Glans penis', 'spong'),
      ('o_rectum', 'FMA14544', 'Rectum and anal canal', 'large'), ('m_external_anal_sphincter', 'FMA21930', 'External anal sphincter', 'floor')]
# Z-Anatomy curves: (key, Z file, name, kind)
ZDUCT = [('o_ductus_deferens_r', 'ductus_deferens_r', 'Right ductus deferens', 'duct'), ('o_ductus_deferens_l', 'ductus_deferens_l', 'Left ductus deferens', 'duct'),
         ('o_ejaculatory_duct_r', 'ejaculatory_duct_r', 'Right ejaculatory duct', 'duct'), ('o_ejaculatory_duct_l', 'ejaculatory_duct_l', 'Left ejaculatory duct', 'duct')]
ORDER = ['bone', 'lig', 'wall', 'floor', 'artery', 'vein', 'nerve', 'node', 'urinary', 'large', 'prostate', 'sv', 'duct', 'testis', 'erect', 'spong']


def part(key, name, fma, file, err, kind, mirror=False):
    return {'key': key, 'name': name, 'fma': fma, 'files': [file], 'group': 'pelv', 'error_mm': err, '_kind': kind, '_mirror': mirror}


def take(cfg, keys, kind, mf=None, newkey=None, err=None):
    by = {p['key']: p for p in cfg['parts']}
    miss = [k for k in keys if k not in by]; assert not miss, miss
    out = []
    for k in keys:
        p = by[k]
        out.append({'key': newkey(k) if newkey else k, 'name': p['name'], 'fma': p['fma'], 'files': p['files'], 'group': 'pelv',
                    'error_mm': err or p.get('error_mm', cfg['error_mm']), '_kind': kind,
                    '_mirror': bool((mf or {}).get(k, {}).get('mirror')) if mf is not None else False})
    return out


parts, zips = [], []
sk = load('skeleton'); zips += sk['zips']
parts += take(sk, BONES, 'bone')
ax = load('ax-joints'); zips += ax['zips']
for p in take(ax, ['sacrotuberous_ligament', 'sacrospinous_ligament'], 'lig', newkey=lambda k: 'g_' + k + '_r'):
    p['_mirror'] = True; parts.append(p)
tm = load('trunk-muscles'); zips += tm['zips']
for p in take(tm, ['pubococcygeus', 'iliococcygeus', 'coccygeus', 'tendinous_arch'], 'floor', newkey=lambda k: 'm_' + k + '_r'):
    p['_mirror'] = True
    if p['key'] == 'm_tendinous_arch_r': p['_kind'] = 'lig'
    parts.append(p)
idx = {r['file'] for r in csv.DictReader(open(os.path.join(ZAN, 'z-index-pelv.tsv')), delimiter='\t')}
for key, f, nm, kind in [('m_puborectalis_r', 'pubo_analis_muscle_r', 'Puborectal part of levator ani (pubo-analis)', 'floor'),
                         ('m_obturator_internus_r', 'obturator_internus_r', 'Obturator internus', 'wall')]:
    assert 'Z_' + f in idx, f
    parts.append(part(key, nm, '', 'Z_' + f, MUSCLE_ERR, kind, True))
lm = load('lower-limb-muscles'); zips += lm['zips']
for p in take(lm, ['piriformis'], 'wall', newkey=lambda k: 'm_piriformis_r'):
    p['_mirror'] = True; parts.append(p)
ve = load('body-vessels'); zips += ve['zips']; vmeta = meta('body-vessels', 'vessels.json')
parts += take(ve, ['v_' + k for k in ARTERIES], 'artery', vmeta['parts']) + take(ve, ['v_' + k for k in VEINS], 'vein', vmeta['parts'])
ne = load('body-nerves'); zips += ne['zips']; nmeta = meta('body-nerves', 'nerves.json')
parts += take(ne, ['n_' + k for k in NERVES], 'nerve', nmeta['parts'])
ly = load('body-lymph'); zips += ly['zips']; lmeta = meta('body-lymph', 'lymph.json')
parts += take(ly, ['l_' + k for k in NODES], 'node', lmeta['parts'])
for key, fma, nm, kind in BP:
    parts.append(part(key, nm, fma, fma, ORGAN_ERR, kind))
cidx = {r['file'] for r in csv.DictReader(open(os.path.join(ZAN, 'z-index-pelv-curves.tsv')), delimiter='\t')}
for key, f, nm, kind in ZDUCT:
    assert 'Z_' + f in cidx, f
    parts.append(part(key, nm, '', 'Z_' + f, DUCT_ERR, kind))
zips += [ZIP_PELV, ZIP_CURVES]
parts.sort(key=lambda p: ORDER.index(p['_kind']))   # stable: keeps the order inside each kind

M = vmeta['mirror']
assert nmeta['mirror'] == M and lmeta['mirror'] == M, 'mirror transforms differ'
assert len({p['key'] for p in parts}) == len(parts)
kinds = {p['key']: {'kind': p.pop('_kind'), 'mirror': p.pop('_mirror')} for p in parts}
cfg = {'name': 'pelv', 'zips': list(dict.fromkeys(zips)), 'out': '../../../anatomy/models/pelv',
       'error_mm': 0.4, 'contact_mm': 0.5, 'contacts_across_groups_only': True, 'pack': True,
       'source': 'Bones, bladder, urethra, prostate, seminal vesicles, testes, epididymides, penis, rectum and external anal sphincter: '
                 'BodyParts3D, (c) The Database Center for Life Science, CC BY-SA 2.1 Japan. Pelvic floor and wall muscles, ligaments, '
                 'ductus deferens, ejaculatory ducts, vessels, nerves and lymph nodes: Z-Anatomy, CC BY-SA 4.0 (from BodyParts3D), '
                 'moved into the BodyParts3D frame; ducts, vessels and nerves are curves swept into tubes',
       'parts': parts}
out = os.path.join(CFG, 'pelv.json')
assert not os.path.exists(out) or json.load(open(out)).get('name') == 'pelv'
json.dump(cfg, open(out, 'w'), indent=1)
os.makedirs(os.path.join(MODELS, 'pelv'), exist_ok=True)
json.dump({'note': 'written by tools/abdomen-pelvis/pelvis_config.py; mirror: the transform that makes a left part from a right one',
           'mirror': M, 'parts': kinds}, open(os.path.join(MODELS, 'pelv', 'kinds.json'), 'w'), indent=0)
from collections import Counter
print(len(parts), 'parts', dict(Counter(k['kind'] for k in kinds.values())), 'mirrored in page:', sum(k['mirror'] for k in kinds.values()))
