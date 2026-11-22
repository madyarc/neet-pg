"""Config for the page "The Abdominal Cavity: Peritoneum and Abdominal Organs" (anatomy/abdomen-pelvis/organs.html,
module 31): one packed model of the abdominal organs, the omenta and mesocolon, the main vessels that give the relations,
and the bones round them for the planes and regions. Same pattern as tools/thorax/lung_config.py.

Parts and where they come from (keys, names, files and error_mm of the whole-body configs where the part is already in one):
  bone    configs/skeleton.json      T10-T12, L1-L5, sacrum, hip bones, ribs 5-12, sternum, clavicles (skeleton error_mm)
  cart    configs/skeleton.json      costal cartilages 5-7; z-bp3d-abdo.zip: costal cartilages 8-10 (Z-Anatomy; BodyParts3D
                                     3.0 has no separate 8th-10th cartilages), Subsurf applied
  muscle  configs/body-muscles.json  diaphragm
  artery  configs/body-vessels.json  abdominal aorta, coeliac trunk and its three branches, gastroduodenal, SMA, IMA, renal
  vein    configs/body-vessels.json  IVC, hepatic veins, renal veins, portal, splenic, superior and inferior mesenteric veins
  spleen  configs/body-lymph.json    the spleen (same key as the home page's lymph layer)
  Z-Anatomy organ meshes, Subsurf/Solidify applied (tools/zanat/export_mod.py -> z-bp3d-abdo.zip, z-index-abdo.tsv):
          the eight liver segments (Couinaud I-VIII; the whole "Liver" object is not used), gallbladder,
          pancreas, ascending, transverse, descending and sigmoid colon, vermiform appendix, meso-appendix, greater and
          lesser omentum, transverse mesocolon ("Mesocolon"), both suprarenal glands
  Z-Anatomy curves swept into tubes (tools/zanat/export_curves.py -> z-bp3d-abdo-curves.zip): bile duct, main and
          accessory pancreatic ducts
  BodyParts3D 3.0 meshes: stomach and duodenum (Z-Anatomy's are open at their ends; the BodyParts3D ones are closed and lie
          on them), jejunum, ileum, rectum (Z-Anatomy has none), right and left ureter.
  Kidneys and renal pelves: Z-Anatomy's (its licence credits "Kidney - by Lissie Cowley - CC-BY-NC 4.0"; allowed since the
          project went non-commercial, 2026-11-21). Chosen over BodyParts3D's: a separate renal pelvis that meets the ureter
          (1.4 mm), the renal vessels end 5-12 mm from it on the right (BodyParts3D kidney: 24 mm), suprarenals sit on it (0.8 mm);
          packed size about the same (+3 KB per side)
Not in either source: caecum as a separate part (it is the lower end of Z-Anatomy's ascending colon), hepatic and cystic
ducts, the peritoneum itself (parietal peritoneum, mesentery of the small intestine, sigmoid mesocolon, ligaments of the
liver and spleen), the lesser sac: these are drawn as schematics on the page.
Exports (2026-11-21):
  export_mod.py    Startup.blend z-to-bp3d.json sources-local/zanat/z-bp3d-abdo.zip tools/zanat/z-index-abdo.tsv "name:<object>" ...
  export_curves.py Startup.blend z-to-bp3d.json sources-local/zanat/z-bp3d-abdo-curves.zip tools/zanat/z-index-abdo-curves.tsv
                   "Digestive system" "Urinary system"   (only the three ducts are used)
Nothing is mirrored. Parts are ordered by colour (the viewer draws neighbouring parts of one colour with a single call).

Also writes anatomy/models/abdo/kinds.json: {"parts": {key: {"kind", "mirror": false}}} for the page.

usage: python3 -I tools/abdomen-pelvis/organs_config.py   ->  tools/bones-rs/configs/abdo.json (+ anatomy/models/abdo/kinds.json)
then:  cd tools/bones-rs && target/release/bones build configs/abdo.json   (through tools/capped)"""
import json, os, re, csv
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
CFG = os.path.join(ROOT, 'tools', 'bones-rs', 'configs')
MODELS = os.path.join(ROOT, 'anatomy', 'models')
ZAN = os.path.join(ROOT, 'tools', 'zanat')
load = lambda n: json.load(open(os.path.join(CFG, n + '.json')))
ORGAN_ERR, SHEET_ERR, DUCT_ERR, CART_ERR = 0.6, 0.6, 0.2, 0.5
ORD = ['first', 'second', 'third', 'fourth', 'fifth', 'sixth', 'seventh', 'eighth', 'ninth', 'tenth', 'eleventh', 'twelfth']
BONES = (['tenth_thoracic_vertebra', 'eleventh_thoracic_vertebra', 'twelfth_thoracic_vertebra'] +
         [o + '_lumbar_vertebra' for o in ORD[:5]] + ['sacrum', 'right_hip_bone', 'left_hip_bone'] +
         [s + '_' + o + '_rib' for o in ORD[4:] for s in ('right', 'left')] + ['manubrium', 'body_of_sternum', 'xiphoid_process', 'right_clavicle', 'left_clavicle'])
CART = [s + '_' + o + '_costal_cartilage' for o in ORD[4:7] for s in ('right', 'left')]
ARTERIES = ['abdominal_aorta', 'coeliac_trunk', 'left_gastric_artery', 'splenic_artery', 'common_hepatic_artery', 'proper_hepatic_artery',
            'gastroduodenal_artery', 'superior_mesenteric_artery', 'inferior_mesenteric_artery', 'right_renal_artery', 'left_renal_artery']
VEINS = ['inferior_vena_cava_abdominal_part', 'hepatic_veins', 'right_renal_vein', 'left_renal_vein', 'hepatic_portal_vein', 'splenic_vein',
         'superior_mesenteric_vein', 'inferior_mesenteric_vein']
ZIP_ABDO = '../../../sources-local/zanat/z-bp3d-abdo.zip'
ZIP_CURVES = '../../../sources-local/zanat/z-bp3d-abdo-curves.zip'
# Z-Anatomy organs: (key, Z file, name, kind, error_mm)
LIVER = [('I', 'posterior_segment_of_liver_i', 'Segment I (caudate lobe)'), ('II', 'left_posterior_lateral_segment_of_liver_ii', 'Segment II'),
         ('III', 'left_anterior_lateral_segment_of_liver_iii', 'Segment III'), ('IV', 'left_medial_segment_of_liver_iv', 'Segment IV'),
         ('V', 'anterior_medial_segment_of_liver_v', 'Segment V'), ('VI', 'anterior_lateral_segment_of_liver_vi', 'Segment VI'),
         ('VII', 'posterior_lateral_segment_of_liver_vii', 'Segment VII'), ('VIII', 'posterior_medial_segment_of_liver_viii', 'Segment VIII')]
ZORG = ([('o_liver_' + n.lower(), f, nm, 'liver', ORGAN_ERR) for n, f, nm in LIVER] +
        [('o_gallbladder', 'gallbladder', 'Gallbladder', 'bile', ORGAN_ERR), ('o_pancreas', 'pancreas', 'Pancreas', 'pancreas', ORGAN_ERR),
         ('o_ascending_colon', 'ascending_colon', 'Caecum and ascending colon', 'large', ORGAN_ERR),
         ('o_transverse_colon', 'transverse_colon', 'Transverse colon', 'large', ORGAN_ERR),
         ('o_descending_colon', 'descending_colon', 'Descending colon', 'large', ORGAN_ERR),
         ('o_sigmoid_colon', 'sigmoid_colon', 'Sigmoid colon', 'large', ORGAN_ERR),
         ('o_appendix', 'vermiform_appendix', 'Vermiform appendix', 'large', 0.3),
         ('o_kidney_r', 'kidney_r', 'Right kidney', 'kidney', ORGAN_ERR), ('o_kidney_l', 'kidney_l', 'Left kidney', 'kidney', ORGAN_ERR),
         ('o_renal_pelvis_r', 'renal_pelvis_r', 'Right renal pelvis', 'kidney', ORGAN_ERR), ('o_renal_pelvis_l', 'renal_pelvis_l', 'Left renal pelvis', 'kidney', ORGAN_ERR),
         ('o_suprarenal_r', 'suprarenal_gland_r', 'Right suprarenal gland', 'supra', 0.4),
         ('o_suprarenal_l', 'suprarenal_gland_l', 'Left suprarenal gland', 'supra', 0.4),
         ('p_greater_omentum', 'greater_omentum', 'Greater omentum', 'perit', 0.35),
         ('p_lesser_omentum', 'lesser_omentum', 'Lesser omentum', 'perit', SHEET_ERR),
         ('p_transverse_mesocolon', 'mesocolon', 'Transverse mesocolon', 'perit', SHEET_ERR),
         ('p_meso_appendix', 'meso_appendix', 'Meso-appendix', 'perit', 0.3)])
ZDUCT = [('o_bile_duct', 'bile_duct', 'Bile duct', 'bile'), ('o_pancreatic_duct', 'pancreatic_duct', 'Pancreatic duct', 'pancreas'),
         ('o_accessory_pancreatic_duct', 'accessory_pancreatic_duct', 'Accessory pancreatic duct', 'pancreas')]
# BodyParts3D 3.0 organs: (key, FMA file, name, kind)
BP = [('o_stomach', 'FMA7148', 'Stomach', 'stomach'), ('o_duodenum', 'FMA7206', 'Duodenum', 'small'), ('o_jejunum', 'FMA7207', 'Jejunum', 'small'), ('o_ileum', 'FMA7208', 'Ileum', 'small'), ('o_rectum', 'FMA14544', 'Rectum', 'large'),
      ('o_ureter_r', 'FMA15571', 'Right ureter', 'kidney'), ('o_ureter_l', 'FMA15572', 'Left ureter', 'kidney')]
ORDER = ['bone', 'cart', 'muscle', 'artery', 'vein', 'liver', 'bile', 'stomach', 'small', 'large', 'pancreas', 'spleen', 'kidney', 'supra', 'perit']


def copy(p, default_err, kind):
    return {'key': p['key'], 'name': p['name'], 'fma': p['fma'], 'files': p['files'], 'group': 'abdo',
            'error_mm': p.get('error_mm', default_err), '_kind': kind}


def part(key, name, fma, file, err, kind):
    return {'key': key, 'name': name, 'fma': fma, 'files': [file], 'group': 'abdo', 'error_mm': err, '_kind': kind}


def take(cfg, keys, kind):
    by = {p['key']: p for p in cfg['parts']}
    miss = [k for k in keys if k not in by]; assert not miss, miss
    return [copy(by[k], cfg['error_mm'], kind) for k in keys]


parts, zips = [], []
sk = load('skeleton'); zips += sk['zips']
parts += take(sk, BONES, 'bone') + take(sk, CART, 'cart')
idx = {r['file']: r for r in csv.DictReader(open(os.path.join(ZAN, 'z-index-abdo.tsv')), delimiter='\t')}
for o in ORD[7:10]:
    for s, sl in (('right', 'r'), ('left', 'l')):
        f = 'Z_costal_cartilage_of_%s_rib_%s' % (o, sl); assert f in idx, f
        parts.append(part('%s_%s_costal_cartilage' % (s, o), '%s %s costal cartilage' % (s.capitalize(), o), '', f, CART_ERR, 'cart'))
mu = load('body-muscles'); zips += mu['zips']
parts += take(mu, ['m_diaphragm'], 'muscle')
ve = load('body-vessels'); zips += ve['zips']
parts += take(ve, ['v_' + k for k in ARTERIES], 'artery') + take(ve, ['v_' + k for k in VEINS], 'vein')
ly = load('body-lymph'); zips += ly['zips']
parts += take(ly, ['l_spleen'], 'spleen')
for key, f, nm, kind, err in ZORG:
    assert 'Z_' + f in idx, f
    parts.append(part(key, nm, '', 'Z_' + f, err, kind))
cidx = {r['file'] for r in csv.DictReader(open(os.path.join(ZAN, 'z-index-abdo-curves.tsv')), delimiter='\t')}
for key, f, nm, kind in ZDUCT:
    assert 'Z_' + f in cidx, f
    parts.append(part(key, nm, '', 'Z_' + f, DUCT_ERR, kind))
for key, fma, nm, kind in BP:
    parts.append(part(key, nm, fma, fma, ORGAN_ERR, kind))
zips += [ZIP_ABDO, ZIP_CURVES]
parts.sort(key=lambda p: ORDER.index(p['_kind']))   # stable: keeps the order inside each kind

assert len({p['key'] for p in parts}) == len(parts)
kinds = {p['key']: {'kind': p.pop('_kind'), 'mirror': False} for p in parts}
cfg = {'name': 'abdo', 'zips': list(dict.fromkeys(zips)), 'out': '../../../anatomy/models/abdo',
       'error_mm': 0.5, 'contact_mm': 0.5, 'contacts_across_groups_only': True, 'pack': True,
       'source': 'Bones, stomach, duodenum, jejunum, ileum, rectum and ureters: BodyParts3D, (c) The Database Center for Life Science, '
                 'CC BY-SA 2.1 Japan. Liver segments, gallbladder, bile and pancreatic ducts, pancreas, colon, '
                 'appendix, omenta, mesocolon, meso-appendix, suprarenal glands, spleen, kidneys and renal pelves (Kidney by Lissie Cowley, CC BY-NC 4.0, in Z-Anatomy), costal cartilages 8-10, diaphragm and vessels: '
                 'Z-Anatomy, CC BY-SA 4.0 (from BodyParts3D), moved into the BodyParts3D frame; ducts and vessels are curves swept into tubes',
       'parts': parts}
out = os.path.join(CFG, 'abdo.json')
assert not os.path.exists(out) or json.load(open(out)).get('name') == 'abdo'
json.dump(cfg, open(out, 'w'), indent=1)
os.makedirs(os.path.join(MODELS, 'abdo'), exist_ok=True)
json.dump({'note': 'written by tools/abdomen-pelvis/organs_config.py', 'parts': kinds},
          open(os.path.join(MODELS, 'abdo', 'kinds.json'), 'w'), indent=0)
from collections import Counter
print(len(parts), 'parts', dict(Counter(k['kind'] for k in kinds.values())))
