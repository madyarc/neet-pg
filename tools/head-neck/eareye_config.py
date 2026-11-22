"""Config for the page "The Ear and the Eye" (anatomy/head-neck/ear-eye.html, module 34): one packed model of the right ear
(auricle, middle and inner ear in the temporal bone) and the right eye (eyeball, lacrimal apparatus, eyelid plates, extraocular
muscles) with the optic nerves, chiasm, tracts and pituitary gland. Same pattern as tools/head-neck/regions_config.py.

Parts and where they come from (keys, names, files and error_mm of the whole-body configs where the part is already in one):
  bone     configs/skeleton.json         skull bones round the orbit and the ear (frontal, sphenoid, ethmoid, occipital, right
                                         parietal, maxilla, zygomatic, lacrimal, nasal, palatine bones; mandible)
           z-bp3d-eareye.zip             the RIGHT TEMPORAL BONE is Z-Anatomy's, not BodyParts3D's: Z-Anatomy's inner ear,
                                         ossicles and tympanic membrane fit its own temporal bone (vestibule median 0.9 mm from
                                         it) much better than BodyParts3D's (4.8 mm): fill-eareye-scripts/zipbbox.py --dist
  ossicle  z-bp3d-eareye.zip             malleus, incus, stapes (Z-Anatomy)
  tm       z-bp3d-eareye.zip             tympanic membrane
  labyr    z-bp3d-eareye.zip             cochlea and vestibule with the semicircular canals (bony labyrinth; Z-Anatomy, adapted from
                                         "Anatomy of the Inner Ear" by the University of Dundee School of Medicine, CC BY-NC-SA 4.0)
  cart     z-bp3d-eareye.zip             auditory tube (Solidify, Subsurf applied; the same mesh as models/oro, coloured as there)
  auricle  z-bp3d-eareye.zip             Z-Anatomy's surface patches of the auricle (helix, antihelix and crura, scapha, triangular
                                         fossa, concha, tragus, antitragus, lobule, back of the auricle), joined into 9 parts
  sclera / cornea / iris / lens / retina / vitreous / aqueous   z-bp3d-eareye.zip  (Z-Anatomy eyeball; Subsurf applied).
                                         Z-Anatomy has no choroid or ciliary body mesh (its ciliary body is a curve without bevel)
  lacgl / lacdr / tarsus  z-bp3d-eareye.zip   lacrimal gland; canaliculus with its ampulla, sac, nasolacrimal duct; superior and
                                         inferior tarsus
  muscle   configs/body-muscles.json     the four recti, the two obliques, levator palpebrae superioris, orbicularis oculi
  optic    BodyParts3D 3.0               right and left optic nerves, optic chiasm, right and left optic tracts (meshes)
  pit      BodyParts3D 3.0               pituitary gland
  artery / vein / nerve   configs/body-vessels.json, body-nerves.json (curves swept into tubes; the cochlear nerve is a mesh)
Z-Anatomy has no tensor tympani or stapedius, no ciliary muscle, sphincter or dilator pupillae (the iris is one mesh), no
choroid, no auricular cartilage separate from the auricle, no external acoustic meatus as a part (it is the canal in the
temporal bone), no posterior or deep auricular, anterior tympanic or stylomastoid artery, no labyrinthine artery and no
ciliary ganglion: the page shows these in schematics.
Export (2026-11-22):
  fill-eareye-scripts/export_eareye.py Startup.blend z-to-bp3d.json sources-local/zanat/z-bp3d-eareye.zip tools/zanat/z-index-eareye.tsv
      "name:Tympanic membrane.r" "name:Malleus.r" ... (43 objects, list in the index)
Right-side eyeball parts are mirrored on the page (both eyes for the visual pathway) with the body layers' reflection
(copied into kinds.json). Parts are ordered by colour (the viewer draws neighbouring parts of one colour with a single call).
One group, contacts not needed.

Also writes anatomy/models/eareye/kinds.json: {"mirror": {m, t}, "parts": {key: {"kind", "mirror"}}} for the page.

usage: python3 -I tools/head-neck/eareye_config.py   ->  tools/bones-rs/configs/eareye.json (+ anatomy/models/eareye/kinds.json)
then:  cd tools/bones-rs && target/release/bones build configs/eareye.json   (through tools/capped)"""
import json, os, re, csv
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
CFG = os.path.join(ROOT, 'tools', 'bones-rs', 'configs')
MODELS = os.path.join(ROOT, 'anatomy', 'models')
ZAN = os.path.join(ROOT, 'tools', 'zanat')
load = lambda n: json.load(open(os.path.join(CFG, n + '.json')))
meta = lambda g, f: json.load(open(os.path.join(MODELS, g, f + '.json')))
ZIP_EE = '../../../sources-local/zanat/z-bp3d-eareye.zip'
BP3 = '../../../sources-local/bp3d/BodyParts3D_3.0_obj_95.zip'
GROUP = 'eareye'

BONES = re.compile(r'^(frontal_bone|sphenoid_bone|ethmoid|occipital_bone|right_parietal_bone|'
                   r'right_(maxilla|zygomatic_bone|lacrimal_bone|nasal_bone|palatine_bone)|mandible)$')
# Z-Anatomy exports: (key, [files], name, kind, mirror, error_mm)
AUR = lambda *f: ['Z_' + x + '_r' for x in f]
ZPARTS = [
    ('z_temporal', ['Z_temporal_bone_r'], 'Right temporal bone', 'bone', False, 0.12),
    ('z_malleus', ['Z_malleus_r'], 'Malleus', 'ossicle', False, 0.03),
    ('z_incus', ['Z_incus_r'], 'Incus', 'ossicle', False, 0.03),
    ('z_stapes', ['Z_stapes_r'], 'Stapes', 'ossicle', False, 0.02),
    ('z_tm', ['Z_tympanic_membrane_r'], 'Tympanic membrane', 'tm', False, 0.03),
    ('z_cochlea', ['Z_cochlea_r'], 'Cochlea (bony)', 'labyr', False, 0.015),
    ('z_vestibule', ['Z_vestibule_r'], 'Vestibule and semicircular canals (bony)', 'labyr', False, 0.015),
    ('z_auditory_tube', ['Z_auditory_tube_r'], 'Auditory (pharyngotympanic) tube', 'cart', False, 0.1),
    ('a_helix', AUR('helix', 'apex_of_auricle', 'auricular_tubercle'), 'Helix', 'auricle', False, 0.1),
    ('a_antihelix', AUR('antihelix', 'crura_of_antihelix'), 'Antihelix and its crura', 'auricle', False, 0.1),
    ('a_scapha', AUR('scapha'), 'Scapha', 'auricle', False, 0.1),
    ('a_triangular', AUR('triangular_fossa'), 'Triangular fossa', 'auricle', False, 0.1),
    ('a_concha', AUR('concha_of_auricle', 'cavity_of_concha', 'cymba_conchae'), 'Concha', 'auricle', False, 0.1),
    ('a_tragus', AUR('tragus', 'anterior_notch_of_auricle'), 'Tragus', 'auricle', False, 0.1),
    ('a_antitragus', AUR('antitragus', 'intertragic_incisure'), 'Antitragus', 'auricle', False, 0.1),
    ('a_lobule', AUR('lobule_of_auricle'), 'Lobule', 'auricle', False, 0.1),
    ('a_back', AUR('eminentia_conchae', 'eminentia_scaphae', 'eminentia_fossae_triangularis', 'fossa_antihelica',
                   'posterior_auricular_groove'), 'Back (cranial surface) of the auricle', 'auricle', False, 0.1),
    ('e_sclera', ['Z_sclera_r'], 'Sclera', 'sclera', True, 0.05),
    ('e_cornea', ['Z_cornea_r'], 'Cornea', 'cornea', True, 0.04),
    ('e_iris', ['Z_iris_r'], 'Iris', 'iris', True, 0.04),
    ('e_lens', ['Z_lens_r'], 'Lens', 'lens', True, 0.04),
    ('e_retina', ['Z_retina_r'], 'Retina', 'retina', True, 0.05),
    ('e_vitreous', ['Z_vitreous_body_r'], 'Vitreous body', 'vitreous', True, 0.08),
    ('e_aqueous', ['Z_anterior_chamber_of_eyeball_r'], 'Anterior chamber (aqueous humour)', 'aqueous', True, 0.05),
    ('l_gland', ['Z_lacrimal_gland_r'], 'Lacrimal gland', 'lacgl', False, 0.06),
    ('l_canal', ['Z_lacrimal_canaliculus_r', 'Z_ampulla_of_lacrimal_canaliculus_r'], 'Lacrimal canaliculi', 'lacdr', False, 0.04),
    ('l_sac', ['Z_lacrimal_sac_r'], 'Lacrimal sac', 'lacdr', False, 0.05),
    ('l_duct', ['Z_nasolacrimal_duct_r'], 'Nasolacrimal duct', 'lacdr', False, 0.05),
    ('t_sup', ['Z_superior_tarsus_r'], 'Superior tarsus (tarsal plate)', 'tarsus', False, 0.05),
    ('t_inf', ['Z_inferior_tarsus_r'], 'Inferior tarsus (tarsal plate)', 'tarsus', False, 0.05)]
# BodyParts3D 3.0 meshes: (key, FMA, name, kind, error_mm)
BPARTS = [('o_nerve_r', 'FMA50875', 'Right optic nerve', 'optic', 0.08), ('o_nerve_l', 'FMA50878', 'Left optic nerve', 'optic', 0.08),
          ('o_chiasm', 'FMA62045', 'Optic chiasm', 'optic', 0.06), ('o_tract_r', 'FMA62382', 'Right optic tract', 'optic', 0.08),
          ('o_tract_l', 'FMA67936', 'Left optic tract', 'optic', 0.08), ('p_pituitary', 'FMA13889', 'Pituitary gland', 'pit', 0.05)]
MUSCLES = ['m_sup_rectus', 'm_inf_rectus', 'm_med_rectus', 'm_lat_rectus', 'm_sup_oblique', 'm_inf_oblique', 'm_lps', 'm_orb_oculi']
MUSCLE_ERR = 0.15
ARTERIES = ['v_internal_carotid_artery_r', 'v_ophthalmic_artery_r', 'v_central_retinal_artery_r', 'v_short_posterior_ciliary_arteries_r',
            'v_long_posterior_ciliary_arteries_r', 'v_lacrimal_artery_r', 'v_basilar_artery', 'v_anterior_inferior_cerebellar_artery_r']
VEINS = ['v_superior_ophthalmic_vein_r', 'v_inferior_ophthalmic_vein_r', 'v_cavernous_sinus_r', 'v_anterior_intercavernous_sinus',
         'v_posterior_intercavernous_sinus', 'v_superior_petrosal_sinus_r', 'v_inferior_petrosal_sinus_r', 'v_transverse_sinus_r',
         'v_sigmoid_sinus_r', 'v_internal_jugular_vein_r']
NERVES = ['n_facial_nerve_vii_r', 'n_chorda_tympani_r', 'n_vestibulocochlear_nerve_viii_r', 'n_vestibular_nerve_r', 'n_cochlear_nerve',
          'n_trigeminal_nerve_v_r', 'n_ophthalmic_nerve_r', 'n_oculomotor_nerve_iii_r', 'n_trochlear_nerve_iv_r', 'n_abducens_nerve_vi_r']
NV_ERR = 0.05


def copy(p, default_err, kind, mirror=False, err=None):
    return {'key': p['key'], 'name': p['name'], 'fma': p['fma'], 'files': p['files'], 'group': GROUP,
            'error_mm': err if err is not None else p.get('error_mm', default_err), '_kind': kind, '_mirror': bool(mirror)}


def zpart(key, name, files, err, kind, mirror, fma=''):
    return {'key': key, 'name': name, 'fma': fma, 'files': files, 'group': GROUP, 'error_mm': err, '_kind': kind, '_mirror': mirror}


idx = {r['file'] for r in csv.DictReader(open(os.path.join(ZAN, 'z-index-eareye.tsv')), delimiter='\t')}
for k, fs, *_ in ZPARTS:
    assert all(f in idx for f in fs), (k, fs)
ORDER = ['bone', 'ossicle', 'tm', 'labyr', 'cart', 'auricle', 'sclera', 'cornea', 'iris', 'lens', 'retina', 'vitreous', 'aqueous',
         'lacgl', 'lacdr', 'tarsus', 'muscle', 'optic', 'pit', 'artery', 'vein', 'nerve']
parts, zips = [], []
sk = load('skeleton'); zips += sk['zips']
parts += [copy(p, sk['error_mm'], 'bone') for p in sk['parts'] if BONES.match(p['key'])]
parts += [zpart(k, nm, fs, e, kd, mi) for k, fs, nm, kd, mi, e in ZPARTS]
zips.append(ZIP_EE)
parts += [zpart(k, nm, [f], e, kd, False, f) for k, f, nm, kd, e in BPARTS]
zips.append(BP3)
mu = load('body-muscles'); zips += mu['zips']; mp = {p['key']: p for p in mu['parts']}
mmeta = meta('body-muscles', 'muscles')['parts']
parts += [copy(mp[k], mu['error_mm'], 'muscle', False, MUSCLE_ERR) for k in MUSCLES]
ve = load('body-vessels'); zips += ve['zips']; vp = {p['key']: p for p in ve['parts']}
vmeta = meta('body-vessels', 'vessels')
for kind, keys in (('artery', ARTERIES), ('vein', VEINS)):
    for k in keys:
        assert vmeta['parts'][k]['kind'] == kind, k
        parts.append(copy(vp[k], ve['error_mm'], kind, False, NV_ERR))
ne = load('body-nerves'); zips += ne['zips']; np_ = {p['key']: p for p in ne['parts']}
parts += [copy(np_[k], ne['error_mm'], 'nerve', False, NV_ERR) for k in NERVES]
parts.sort(key=lambda p: ORDER.index(p['_kind']))          # stable: keeps the order above within a kind

assert len({p['key'] for p in parts}) == len(parts)
kinds = {p['key']: {'kind': p.pop('_kind'), 'mirror': p.pop('_mirror')} for p in parts}
cfg = {'name': 'eareye', 'zips': list(dict.fromkeys(zips)), 'out': '../../../anatomy/models/eareye',
       'error_mm': 0.3, 'contact_mm': 0.0, 'contacts_across_groups_only': True, 'pack': True,
       'source': 'Bones, optic nerves, chiasm, tracts, pituitary: BodyParts3D, (c) The Database Center for Life Science, CC BY-SA 2.1 '
                 'Japan. Temporal bone, ossicles, tympanic membrane, auricle, eyeball, lacrimal apparatus, tarsi, auditory tube, muscles, '
                 'vessels and nerves: Z-Anatomy, CC BY-SA 4.0 (from BodyParts3D), moved into the BodyParts3D frame; cochlea and '
                 'vestibule: Z-Anatomy after "Anatomy of the Inner Ear", University of Dundee School of Medicine, CC BY-NC-SA 4.0; '
                 'vessels and nerves are curves swept into tubes',
       'parts': parts}
out_cfg = os.path.join(CFG, 'eareye.json')
assert not os.path.exists(out_cfg) or json.load(open(out_cfg)).get('name') == 'eareye'
json.dump(cfg, open(out_cfg, 'w'), indent=1)
os.makedirs(os.path.join(MODELS, 'eareye'), exist_ok=True)
json.dump({'note': 'written by tools/head-neck/eareye_config.py', 'mirror': vmeta['mirror'], 'parts': kinds},
          open(os.path.join(MODELS, 'eareye', 'kinds.json'), 'w'), indent=0)
from collections import Counter
print(len(parts), 'parts', dict(Counter(k['kind'] for k in kinds.values())), 'mirrored', sum(k['mirror'] for k in kinds.values()))
