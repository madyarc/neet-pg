"""Config for the neuroanatomy I pages (module 36): anatomy/neuro/meninges-cord.html and anatomy/neuro/brainstem.html share one
packed model: the spinal cord with its grey matter and main tracts in the vertebral canal, the dural sac and cauda equina, the
brainstem with the cerebellum, ventricles, cranial nerve roots and the arteries of the brainstem and cord.
Same pattern as tools/head-neck/eareye_config.py.

Parts and where they come from (licences checked 2026-11-22, sources-local/facts/fill-neuro1.md "Models"):
  bone     configs/skeleton.json      vertebrae C1-L5, sacrum, occipital bone (BodyParts3D 3.0, 0.6 mm as on the home)
  brain    BodyParts3D 3.0            medulla oblongata, pons, midbrain (+ cerebral peduncles, colliculi and their brachia),
                                      cerebellum (one mesh: BodyParts3D has no lobes, vermis or peduncles of the cerebellum)
  dien     BodyParts3D 3.0            thalami, pineal body, mammillary bodies (context above the midbrain)
  csf      BodyParts3D 3.0            fourth ventricle, cerebral aqueduct, third ventricle, lateral ventricles, interventricular
                                      foramen, central canal (its medullary part)
  chp      BodyParts3D 3.0            choroid plexus of the lateral ventricles
  olive / pyr   z-bp3d-neuro1.zip     Z-Anatomy olive and pyramid (drawn by Z-Anatomy on the BodyParts3D medulla: their surfaces
                                      lie a median 1.6-2.0 mm from it, zcompare_batch.py). The Z-Anatomy brainstem parts themselves are
                                      BodyParts3D's (pons, medulla, midbrain, peduncle base, colliculi, aqueduct, fourth ventricle:
                                      median 0.3-0.8 mm), so BodyParts3D's are used. Z-Anatomy's CEREBELLAR LOBULES, flocculus and
                                      superior cerebellar peduncle do NOT match BodyParts3D (median 2-6 mm): their origin cannot be
                                      shown (Z-Anatomy lists the unlicensed "Brainder"/"White matter" brain models among its sources),
                                      so they are not used.
  nucleus  z-bp3d-neuro1.zip          Z-Anatomy cranial nerve nuclei (small hand-placed blobs, Subsurf applied; positions approximate):
                                      kinds gse / sve / gve (motor, branchial motor, parasympathetic), ssa / sens (special and general
                                      or visceral sensory); red nucleus. Z-Anatomy's "Vestibular nuclei" blob lies in the upper pons,
                                      medial and ventral, not in the lateral floor of the fourth ventricle: left out
  dura     z-bp3d-nerve-mesh.zip, z-bp3d-neuro1.zip   spinal dura (Z-Anatomy; ends at L2 in the model: too high, see the page),
                                      tentorium cerebelli, falx cerebri
  cord / grey / tract   z-bp3d-neuro1-cord.zip   Z-Anatomy spinal cord rebuilt by fill-neuro1-scripts/export_cord.py from its
                                      cross-sections and path (Array + Curve modifiers): white matter (the cord), grey matter
                                      (anterior and posterior horns, intermediate grey), the main tracts (both sides)
  nerve    z-bp3d-nerves.zip, z-bp3d-neuro1-crop.zip   cauda equina, spinal nerve roots and ganglion (right, mirrored on the
                                      page), cranial nerves III-XII cropped to 14 mm round the brainstem (crop_nerves.py; right, mirrored)
  artery / vein   configs/body-vessels.json   vertebral, basilar, PICA, AICA, superior cerebellar, posterior cerebral, pontine
                                      branches, anterior spinal (right ones mirrored on the page); transverse sinus (mirrored)
Parts are ordered by kind/colour (the viewer draws neighbouring parts of one colour with a single call). One group.
Also writes anatomy/models/neuro1/kinds.json: {"mirror": {m, t}, "parts": {key: {"kind", "mirror", "tract"?}}}.

usage: python3 -I tools/neuro/neuro1_config.py  ->  tools/bones-rs/configs/neuro1.json (+ anatomy/models/neuro1/kinds.json)
then:  cd tools/bones-rs && ../capped target/release/bones build configs/neuro1.json"""
import json, os, re, csv
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
CFG = os.path.join(ROOT, 'tools', 'bones-rs', 'configs')
MODELS = os.path.join(ROOT, 'anatomy', 'models')
ZAN = os.path.join(ROOT, 'tools', 'zanat')
load = lambda n: json.load(open(os.path.join(CFG, n + '.json')))
meta = lambda g, f: json.load(open(os.path.join(MODELS, g, f + '.json')))
Z = '../../../sources-local/zanat/'
ZIP_N1, ZIP_CORD, ZIP_CROP = Z + 'z-bp3d-neuro1.zip', Z + 'z-bp3d-neuro1-cord.zip', Z + 'z-bp3d-neuro1-crop.zip'
BP3 = '../../../sources-local/bp3d/BodyParts3D_3.0_obj_95.zip'
GROUP = 'neuro1'

VERT = ['atlas', 'axis'] + [f'{n}_cervical_vertebra' for n in ('third', 'fourth', 'fifth', 'sixth', 'seventh')] + \
       [f'{n}_thoracic_vertebra' for n in ('first', 'second', 'third', 'fourth', 'fifth', 'sixth', 'seventh', 'eighth', 'ninth',
                                          'tenth', 'eleventh', 'twelfth')] + \
       [f'{n}_lumbar_vertebra' for n in ('first', 'second', 'third', 'fourth', 'fifth')] + ['sacrum', 'occipital_bone']
# BodyParts3D 3.0 meshes: (key, FMA, name, kind, error_mm)
BPARTS = [
    ('b_medulla', 'FMA62004', 'Medulla oblongata', 'medulla', 0.12), ('b_pons', 'FMA67943', 'Pons', 'pons', 0.12),
    ('b_midbrain', 'FMA61993nsn', 'Midbrain (tegmentum and tectum)', 'midbrain', 0.12),
    ('b_peduncles', 'FMA62394', 'Cerebral peduncles (crura)', 'midbrain', 0.12),
    ('b_sup_coll_r', 'FMA73422', 'Right superior colliculus', 'midbrain', 0.08), ('b_sup_coll_l', 'FMA73423', 'Left superior colliculus', 'midbrain', 0.08),
    ('b_inf_coll_r', 'FMA73434', 'Right inferior colliculus', 'midbrain', 0.08), ('b_inf_coll_l', 'FMA73435', 'Left inferior colliculus', 'midbrain', 0.08),
    ('b_brach_sc_r', 'FMA73461', 'Brachium of the right superior colliculus', 'midbrain', 0.08),
    ('b_brach_sc_l', 'FMA73462', 'Brachium of the left superior colliculus', 'midbrain', 0.08),
    ('b_brach_ic_r', 'FMA73463', 'Brachium of the right inferior colliculus', 'midbrain', 0.08),
    ('b_brach_ic_l', 'FMA73464', 'Brachium of the left inferior colliculus', 'midbrain', 0.08),
    ('b_cerebellum', 'FMA67944', 'Cerebellum', 'cblm', 0.25),
    ('b_thal_r', 'FMA258714', 'Right thalamus', 'dien', 0.2), ('b_thal_l', 'FMA258716', 'Left thalamus', 'dien', 0.2),
    ('b_pineal', 'FMA62033', 'Pineal body', 'dien', 0.08), ('b_mammillary', 'FMA74877', 'Mammillary bodies', 'dien', 0.08),
    ('c_fourth', 'FMA78469', 'Fourth ventricle', 'csf', 0.1), ('c_aqueduct', 'FMA78467', 'Cerebral aqueduct', 'csf', 0.06),
    ('c_third', 'FMA78454', 'Third ventricle', 'csf', 0.12), ('c_lat_r', 'FMA78449', 'Right lateral ventricle', 'csf', 0.2),
    ('c_lat_l', 'FMA78450', 'Left lateral ventricle', 'csf', 0.2), ('c_ivf', 'FMA75351', 'Interventricular foramen', 'csf', 0.06),
    ('c_canal', 'FMA78497', 'Central canal (in the medulla)', 'csf', 0.05),
    ('p_chp_r', 'FMA274027', 'Choroid plexus of the right lateral ventricle', 'chp', 0.25),
    ('p_chp_l', 'FMA274029', 'Choroid plexus of the left lateral ventricle', 'chp', 0.25)]
# Z-Anatomy objects in z-bp3d-neuro1.zip: (key, file stem without _r/_l, name, kind, error_mm); both sides exported
ZN = [('z_olive', 'Z_olive', 'olive', 'olive', 0.08), ('z_pyramid', 'Z_pyramid_of_medulla_oblongata', 'pyramid', 'pyr', 0.08),
      ('n3', 'Z_nucleus_of_oculomotor_nerve', 'oculomotor nucleus (III)', 'gse', 0.05),
      ('n3ew', 'Z_accessory_nucleus_of_oculomotor_nerve', 'Edinger–Westphal (accessory oculomotor) nucleus', 'gve', 0.05),
      ('n4', 'Z_nucleus_of_trochlear_nerve', 'trochlear nucleus (IV)', 'gse', 0.05),
      ('n6', 'Z_nucleus_of_abducens_nerve', 'abducens nucleus (VI)', 'gse', 0.05),
      ('n12', 'Z_nucleus_of_hypoglossal_nerve', 'hypoglossal nucleus (XII)', 'gse', 0.05),
      ('n7m', 'Z_motor_nucleus_of_facial_nerve', 'facial motor nucleus (VII)', 'sve', 0.05),
      ('namb', 'Z_nucleus_ambiguus', 'nucleus ambiguus (IX, X)', 'sve', 0.05),
      ('n11', 'Z_nucleus_of_accessory_nerve', 'accessory nucleus (XI, spinal)', 'sve', 0.05),
      ('nss', 'Z_superior_salivatory_nucleus', 'superior salivatory nucleus (VII)', 'gve', 0.05),
      ('nis', 'Z_inferior_salivatory_nucleus', 'inferior salivatory nucleus (IX)', 'gve', 0.05),
      ('n10d', 'Z_posterior_nucleus_of_vagus_nerve', 'dorsal (posterior) nucleus of the vagus (X)', 'gve', 0.05),
      ('ncoa', 'Z_anterior_cochlear_nucleus', 'anterior (ventral) cochlear nucleus (VIII)', 'ssa', 0.05),
      ('ncop', 'Z_posterior_cochlear_nucleus', 'posterior (dorsal) cochlear nucleus (VIII)', 'ssa', 0.05),
      ('nred', 'Z_red_nucleus', 'red nucleus', 'red', 0.05),
      ('d_tent', 'Z_tentorium_cerebelli', 'tentorium cerebelli', 'dura', 0.15)]
ZN1 = [('d_falx', 'Z_falx_cerebri', 'Falx cerebri', 'dura', 0.4)]
# rebuilt cord (z-bp3d-neuro1-cord.zip): (key, stem, name, kind, tract-group, paired)
CORD = [('s_white', 'Z_white_matter_of_spinal_cord', 'Spinal cord (white matter surface)', 'cord', None, False),
        ('s_ant_horn', 'Z_anterior_horn_of_spinal_cord', 'anterior (ventral) horn', 'grey', None, True),
        ('s_post_horn', 'Z_posterior_horn_of_spinal_cord', 'posterior (dorsal) horn', 'grey', None, True),
        ('s_int_grey', 'Z_lateral_intermediate_substance', 'intermediate grey matter and grey commissure', 'grey', None, True),
        ('t_gracile', 'Z_gracile_fasciculus', 'fasciculus gracilis', 'tract', 'dc', True),
        ('t_cuneate', 'Z_cuneate_fasciculus', 'fasciculus cuneatus', 'tract', 'dc', True),
        ('t_lst', 'Z_lateral_spinothalamic_tract', 'lateral spinothalamic tract', 'tract', 'st', True),
        ('t_ast', 'Z_anterior_spinothalamic_tract', 'anterior spinothalamic tract', 'tract', 'st', True),
        ('t_psct', 'Z_posterior_spinocerebellar_tract', 'posterior (dorsal) spinocerebellar tract', 'tract', 'sc', True),
        ('t_asct', 'Z_anterior_spinocerebellar_tract', 'anterior (ventral) spinocerebellar tract', 'tract', 'sc', True),
        ('t_lcst', 'Z_lateral_corticospinal_tract', 'lateral corticospinal tract', 'tract', 'cst', True),
        ('t_acst', 'Z_anterior_corticospinal_tract', 'anterior corticospinal tract', 'tract', 'cst', True)]
CROP = ['Z_oculomotor_nerve_iii_r', 'Z_trochlear_nerve_iv_r', 'Z_trigeminal_nerve_v_r', 'Z_abducens_nerve_vi_r', 'Z_facial_nerve_vii_r',
        'Z_vestibulocochlear_nerve_viii_r', 'Z_glossopharyngeal_nerve_ix_r', 'Z_vagus_nerve_x_r', 'Z_accessory_nerve_xi_r',
        'Z_hypoglossal_nerve_xii_r']
CN_NAME = {'iii': 'Oculomotor nerve (III)', 'iv': 'Trochlear nerve (IV)', 'v': 'Trigeminal nerve (V)', 'vi': 'Abducens nerve (VI)',
           'vii': 'Facial nerve (VII)', 'viii': 'Vestibulocochlear nerve (VIII)', 'ix': 'Glossopharyngeal nerve (IX)',
           'x': 'Vagus nerve (X)', 'xi': 'Accessory nerve (XI)', 'xii': 'Hypoglossal nerve (XII)'}
NERVES = ['n_cauda_equina', 'n_anterior_root_of_spinal_nerve_r', 'n_posterior_root_of_spinal_nerve_r', 'n_spinal_ganglion_r']
ARTERIES = ['v_vertebral_artery_r', 'v_basilar_artery', 'v_posterior_inferior_cerebellar_artery_r', 'v_anterior_inferior_cerebellar_artery_r',
            'v_superior_cerebellar_artery_r', 'v_posterior_cerebral_artery_r', 'v_medial_pontine_branches_of_basilar_artery_r',
            'v_lateral_pontine_branches_of_basilar_artery_r', 'v_anterior_spinal_artery_r']
VEINS = ['v_transverse_sinus_r']   # the straight and occipital sinus curves lie in front of the brainstem in this layer (misplaced) and
                                  # the sigmoid sinus is not described on the pages: left out (review 2026-11-22)
NV_ERR = 0.05


def copy(p, default_err, kind, mirror=False, err=None):
    return {'key': p['key'], 'name': p['name'], 'fma': p['fma'], 'files': p['files'], 'group': GROUP,
            'error_mm': err if err is not None else p.get('error_mm', default_err), '_kind': kind, '_mirror': bool(mirror)}


def zpart(key, name, files, err, kind, mirror, fma='', **extra):
    d = {'key': key, 'name': name, 'fma': fma, 'files': files, 'group': GROUP, 'error_mm': err, '_kind': kind, '_mirror': mirror}
    d.update({'_' + k: v for k, v in extra.items()})
    return d


def index(n): return {r['file'] for r in csv.DictReader(open(os.path.join(ZAN, n)), delimiter='\t')}


i_n1, i_cord, i_crop = index('z-index-neuro1.tsv'), index('z-index-neuro1-cord.tsv'), index('z-index-neuro1-crop.tsv')
ORDER = ['bone', 'dura', 'cord', 'grey', 'tract', 'medulla', 'pons', 'midbrain', 'cblm', 'dien', 'olive', 'pyr', 'csf', 'chp',
         'gse', 'sve', 'gve', 'ssa', 'red', 'nerve', 'artery', 'vein']
parts, zips = [], []
sk = load('skeleton'); zips += sk['zips']; skp = {p['key']: p for p in sk['parts']}
parts += [copy(skp[k], sk['error_mm'], 'bone') for k in VERT]
parts += [zpart(k, nm, [f], e, kd, False, f) for k, f, nm, kd, e in BPARTS]
zips.append(BP3)
for k, stem, nm, kd, e in ZN:   # nuclei and the red nucleus: right side only (the pages label the right ones; review 2026-11-22)
    for s, side in ((('r', 'Right'), ('l', 'Left')) if k in ('z_olive', 'z_pyramid', 'd_tent') else (('r', 'Right'),)):
        assert stem + '_' + s in i_n1, stem
        parts.append(zpart(f'{k}_{s}', f'{side} {nm}', [f'{stem}_{s}'], e, kd, False))
for k, stem, nm, kd, e in ZN1:
    assert stem in i_n1; parts.append(zpart(k, nm, [stem], e, kd, False))
zips.append(ZIP_N1)
for k, stem, nm, kd, tg, paired in CORD:
    sides = (('r', 'Right'), ('l', 'Left')) if paired else ((None, None),)
    for s, side in sides:
        f = f'{stem}_{s}' if s else stem; assert f in i_cord, f
        parts.append(zpart(f'{k}_{s}' if s else k, f'{side} {nm}' if s else nm, [f], 0.12 if kd != 'cord' else 0.1, kd, False,
                           **({'tract': tg} if tg else {})))
zips.append(ZIP_CORD)
for f in CROP:
    assert f in i_crop, f
    cn = re.search(r'_(i{1,3}|iv|v|vi{1,3}|ix|x|xi{1,2})_r$', f).group(1)
    parts.append(zpart('cn_' + cn, CN_NAME[cn], [f], NV_ERR, 'nerve', True))
zips.append(ZIP_CROP)
ne = load('body-nerves'); zips += ne['zips']; np_ = {p['key']: p for p in ne['parts']}
nmeta = meta('body-nerves', 'nerves')['parts']
for k in NERVES + ['n_spinal_dura']:
    parts.append(copy(np_[k], ne['error_mm'], 'dura' if k == 'n_spinal_dura' else 'nerve', nmeta[k]['mirror'],
                      0.2 if k == 'n_spinal_dura' else NV_ERR))
ve = load('body-vessels'); zips += ve['zips']; vp = {p['key']: p for p in ve['parts']}
vmeta = meta('body-vessels', 'vessels')
for kind, keys in (('artery', ARTERIES), ('vein', VEINS)):
    for k in keys:
        assert vmeta['parts'][k]['kind'] == kind, k
        parts.append(copy(vp[k], ve['error_mm'], kind, vmeta['parts'][k]['mirror'], NV_ERR))
parts.sort(key=lambda p: ORDER.index(p['_kind']))          # stable: keeps the order above within a kind

assert len({p['key'] for p in parts}) == len(parts)
kinds = {}
for p in parts:
    d = {'kind': p.pop('_kind'), 'mirror': p.pop('_mirror')}
    if '_tract' in p: d['tract'] = p.pop('_tract')
    kinds[p['key']] = d
cfg = {'name': 'neuro1', 'zips': list(dict.fromkeys(zips)), 'out': '../../../anatomy/models/neuro1',
       'error_mm': 0.3, 'contact_mm': 0.0, 'contacts_across_groups_only': True, 'pack': True,
       'source': 'Bones, medulla, pons, midbrain, cerebellum, thalami, pineal, mammillary bodies, ventricles, choroid plexus: BodyParts3D, '
                 '(c) The Database Center for Life Science, CC BY-SA 2.1 Japan. Spinal cord (rebuilt from its cross-sections and path), '
                 'olive, pyramid, cranial nerve nuclei, red nucleus, spinal dura, tentorium, falx, nerves and vessels: Z-Anatomy, '
                 'CC BY-SA 4.0 (from BodyParts3D), moved into the BodyParts3D frame; nerves and vessels are curves swept into tubes, '
                 'cranial nerves cropped near the brainstem',
       'parts': parts}
out_cfg = os.path.join(CFG, 'neuro1.json')
assert not os.path.exists(out_cfg) or json.load(open(out_cfg)).get('name') == 'neuro1'
json.dump(cfg, open(out_cfg, 'w'), indent=1)
os.makedirs(os.path.join(MODELS, 'neuro1'), exist_ok=True)
json.dump({'note': 'written by tools/neuro/neuro1_config.py', 'mirror': vmeta['mirror'], 'parts': kinds},
          open(os.path.join(MODELS, 'neuro1', 'kinds.json'), 'w'), indent=0)
from collections import Counter
print(len(parts), 'parts', dict(Counter(k['kind'] for k in kinds.values())), 'mirrored', sum(k['mirror'] for k in kinds.values()))
