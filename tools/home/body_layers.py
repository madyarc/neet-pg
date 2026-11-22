"""The Anatomy home's Joints-and-ligaments and Organs layers, gathered from the regional models (pattern of
tools/zanat/body_lymph.py): same keys, files and error_mm as the regional configs (raised for this zoomed-out view
where a pack would pass ~1.2 MB), right side + midline only; the page mirrors parts marked "mirror".

  body_layers.py config joints|organs   tools/bones-rs/configs/body-<layer>.json
  (then: tools/capped tools/bones-rs/target/release/bones build tools/bones-rs/configs/body-<layer>.json)
  body_layers.py post joints|organs     anatomy/models/body-<layer>/<layer>.json — per part: kind, region, side, mirror,
                                         colour (a CSS token) and page (a REGION_PAGES name in anatomy/index.html);
                                         "tokens" = organ colours the regional pages define for themselves
                                         ([light, dark]), which the home page adds to its stylesheet when it loads the layer.

Joints: the non-bone parts of ul-joints, ll-joints, ax-joints (+ the BodyParts3D intervertebral discs of ax-joints;
the joints-general menisci and interpubic disc are the same meshes as ll-joints / ax-joints, so they are not repeated).
Organs: lung, abdo, pelv, hn-reg, oro, eareye (not heart: its chambers are in the vessel layer, valves and papillary
muscles are inside them; not neuro1, not finished). Parts already on the home (spleen, palatine tonsil: lymph layer;
costal cartilages: skeleton), bones, muscles, vessels, nerves, nodes and parts hidden inside others are left out."""
import sys, os, json, re, zipfile
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, '..', '..'))
sys.path.insert(0, os.path.join(ROOT, 'tools', 'zanat'))
from body_muscles import mirror

CFG = os.path.join(ROOT, 'tools', 'bones-rs', 'configs')
MOD = os.path.join(ROOT, 'anatomy', 'models')

# ---------- joints ----------
JOINT_SRC = [('ul-joints', 'Upper limb', 'Upper limb joints'), ('ll-joints', 'Lower limb', 'Lower limb joints'),
             ('ax-joints', None, 'Axial joints')]
JOINT_COL = {'capsule': '--capsule', 'ligament': '--lig', 'membrane': '--lig', 'cartilage': '--cart', 'disc': '--cart',
             'bursa': '--bursa', 'fat pad': '--soft'}
JOINT_ERR_MIN = 0.08      # the 0.05 mm thin shells of the limb joints, a little coarser for the whole-body view


def joint_kind(key, name, group):
    n = name.lower()
    if key.startswith('disc_'): return 'disc'
    if group == 'bursa' or 'bursa' in n: return 'bursa'
    if 'capsule' in n: return 'capsule'
    if 'interosseous membrane' in n: return 'membrane'
    if 'fat pad' in n: return 'fat pad'
    if 'ligament' in n or 'cord' in n: return 'ligament'
    if re.search(r'disc|labrum|meniscus|nucleus pulposus|symphysis', n): return 'cartilage'
    return 'ligament'


def ax_region(n):
    n = n.lower()
    if re.search(r'temporomandibular|sphenomandibular|stylomandibular', n): return 'Head and neck'
    if re.search(r'sacro|pubic|interpubic|sacrococcygeal', n): return 'Pelvis'
    return 'Back'


# ---------- organs ----------
# (model, kinds kept, region, page) ; per-part overrides below
ORGAN_SRC = [
    ('lung', 'Thorax', 'Lungs'),
    ('abdo', 'Abdomen', 'Abdominal organs'),
    ('pelv', 'Pelvis', 'Pelvic viscera'),
    ('hn-reg', 'Head and neck', 'Neck glands'),
    ('oro', 'Head and neck', 'Mouth, pharynx, nose and larynx'),
    ('eareye', 'Head and neck', 'Ear and eye'),
]
KEEP = {
    'lung': {'r_trachea', 'g_oesophagus', 'r_right_main_bronchus', 'r_left_main_bronchus', 'r_right_superior_lobar_bronchus',
             'r_intermediate_bronchus_r', 'r_middle_lobar_bronchus_r', 'r_right_inferior_lobar_bronchus',
             'r_left_superior_lobar_bronchus', 'r_left_inferior_lobar_bronchus',
             'r_superior_lobe_of_right_lung', 'r_middle_lobe_of_right_lung', 'r_inferior_lobe_of_right_lung',
             'r_superior_lobe_of_left_lung', 'r_inferior_lobe_of_left_lung'},
    'abdo': {'o_liver_i', 'o_liver_ii', 'o_liver_iii', 'o_liver_iv', 'o_liver_v', 'o_liver_vi', 'o_liver_vii', 'o_liver_viii',
             'o_gallbladder', 'o_bile_duct', 'o_stomach', 'o_duodenum', 'o_jejunum', 'o_ileum', 'o_ascending_colon',
             'o_transverse_colon', 'o_descending_colon', 'o_sigmoid_colon', 'o_appendix', 'o_pancreas',
             'o_kidney_r', 'o_kidney_l', 'o_renal_pelvis_r', 'o_renal_pelvis_l', 'o_ureter_r', 'o_ureter_l',
             'o_suprarenal_r', 'o_suprarenal_l'},
    'pelv': {'o_bladder', 'o_urethra', 'o_rectum', 'o_prostate', 'o_seminal_vesicle_r', 'o_seminal_vesicle_l',
             'o_ductus_deferens_r', 'o_ductus_deferens_l', 'o_ejaculatory_duct_r', 'o_ejaculatory_duct_l',
             'o_epididymis_r', 'o_epididymis_l', 'o_testis_r', 'o_testis_l', 'o_corpus_cavernosum',
             'o_corpus_spongiosum', 'o_glans'},
    'hn-reg': {'g_parotid', 'g_acc_parotid', 'g_submandibular', 'g_sublingual', 'g_thyroid', 'g_sup_parathyroid',
               'g_inf_parathyroid', 'd_parotid', 'd_submandibular'},
    'oro': {'thyroid_cart', 'cricoid_cart', 'aryt_cart_r', 'aryt_cart_l', 'epiglottis', 'c_corniculate', 'c_septal',
            'c_septal_lat', 'z_auditory_tube', 'z_tongue', 'z_soft_palate', 'z_uvula', 'z_nasopharynx', 'z_oropharynx',
            'z_laryngopharynx', 'z_nasal_mucosa', 's_frontal', 's_sphenoid', 's_ethmoid_ant', 's_ethmoid_mid', 's_ethmoid_post'},
    'eareye': {'a_helix', 'a_antihelix', 'a_scapha', 'a_triangular', 'a_concha', 'a_tragus', 'a_antitragus', 'a_lobule',
               'a_back', 'e_sclera', 'e_cornea', 'l_gland'},
}
# the ureters are in abdo and pelv (same files): they open the abdominal organs page; the rectum the pelvic one
PAGE = {'o_ureter_r': 'Abdominal organs', 'o_ureter_l': 'Abdominal organs',
        'o_testis_r': 'Perineum', 'o_testis_l': 'Perineum', 'o_epididymis_r': 'Perineum', 'o_epididymis_l': 'Perineum',
        'o_corpus_cavernosum': 'Perineum', 'o_corpus_spongiosum': 'Perineum', 'o_glans': 'Perineum'}
# paired head parts the ear-and-eye page shows on one side: on the whole body both sides are shown (mirrored)
MIRROR_TOO = {'a_helix', 'a_antihelix', 'a_scapha', 'a_triangular', 'a_concha', 'a_tragus', 'a_antitragus', 'a_lobule',
              'a_back', 'l_gland'}
# colour token per (model, kind), from each page's own COL map
ORGAN_COL = {
    ('lung', 'airway'): '--airway', ('lung', 'gut'): '--gut',
    ('abdo', 'liver'): '--liver', ('abdo', 'bile'): '--bile', ('abdo', 'stomach'): '--stom', ('abdo', 'small'): '--gut',
    ('abdo', 'large'): '--colon', ('abdo', 'pancreas'): '--panc', ('abdo', 'kidney'): '--kidney', ('abdo', 'supra'): '--supra',
    ('pelv', 'urinary'): '--kidney', ('pelv', 'large'): '--colon', ('pelv', 'prostate'): '--prost', ('pelv', 'sv'): '--sv',
    ('pelv', 'duct'): '--duct', ('pelv', 'testis'): '--gonad', ('pelv', 'erect'): '--erect', ('pelv', 'spong'): '--spong',
    ('hn-reg', 'saliv'): '--saliv', ('hn-reg', 'thyroid'): '--thyroid', ('hn-reg', 'parathy'): '--parathy',
    ('hn-reg', 'duct'): '--sduct',
    ('oro', 'cart'): '--cart', ('oro', 'tube'): '--cart', ('oro', 'tongue'): '--tongue', ('oro', 'palate'): '--palate',
    ('oro', 'phar'): '--muc', ('oro', 'nmuc'): '--muc', ('oro', 'sinus'): '--sinus',
    ('eareye', 'auricle'): '--skin', ('eareye', 'sclera'): '--sclera', ('eareye', 'cornea'): '--cornea',
    ('eareye', 'lacgl'): '--lacgl',
}
LOBE = {'r_superior_lobe_of_right_lung': '--lobe-s', 'r_superior_lobe_of_left_lung': '--lobe-s',
        'r_middle_lobe_of_right_lung': '--lobe-m', 'r_inferior_lobe_of_right_lung': '--lobe-i',
        'r_inferior_lobe_of_left_lung': '--lobe-i'}
# [light, dark] copied from the pages' :root (--sduct = head-neck/regions.html --duct, --tongue = mouth page --musc,
# renamed because pelvis.html and ear-eye.html use those names for other colours)
TOKENS = {
    '--lobe-s': ['#f2b5a7', '#c98a7d'], '--lobe-m': ['#c2a7e0', '#9a83bb'], '--lobe-i': ['#9fd3c7', '#6fae9f'],
    '--airway': ['#2f7d79', '#5cb3ad'], '--gut': ['#d9a066', '#c08a52'],
    '--stom': ['#e7b7c8', '#8c5468'], '--colon': ['#a89a5a', '#8f8248'], '--liver': ['#9b6b5e', '#a77464'],
    '--bile': ['#5e8c6a', '#6fa07b'], '--panc': ['#8f6aa8', '#9d7ab6'], '--kidney': ['#b46e48', '#c07a52'],
    '--supra': ['#2dd4bf', '#3fbfae'],
    '--prost': ['#556b2f', '#7f9a4f'], '--sv': ['#8fbc8f', '#78a878'], '--duct': ['#826bdf', '#9a88ea'],
    '--gonad': ['#dc89e6', '#c77bd2'], '--erect': ['#c741d6', '#c25ad0'], '--spong': ['#89e6ae', '#5fbf88'],
    '--saliv': ['#f248ca', '#f279dc'], '--thyroid': ['#a55be5', '#ad6ae6'], '--parathy': ['#c9e55b', '#c5dd66'],
    '--sduct': ['#639aa5', '#6fa8b4'],
    '--tongue': ['#c96f68', '#9c4e48'], '--palate': ['#b0609e', '#94487f'], '--muc': ['#e9a04a', '#b87a34'],
    '--sinus': ['#5aa7c8', '#4a8fb0'],
    '--skin': ['#f1d3bf', '#7a5a48'], '--sclera': ['#ffffff', '#d9dee6'], '--cornea': ['#a5e6f5', '#5fa8bd'],
    '--lacgl': ['#b5179e', '#e05cc8'],
}
ORGAN_ERR = {'o_jejunum': 1.0, 'o_ileum': 1.0}      # the coiled small intestine: the largest meshes, coarser here


def load(g):
    return json.load(open(os.path.join(CFG, g + '.json')))


def zip_names(cfg):
    base = CFG
    # bones-rs matches a file by its base name (BodyParts3D entries sit in a folder, with backslashes)
    return [(z, set(re.split(r'[/\\\\]', n)[-1][:-4] for n in zipfile.ZipFile(os.path.normpath(os.path.join(base, z))).namelist()
                    if n.endswith('.obj'))) for z in cfg['zips']]


def first_zip(listing, f):
    return next((z for z, names in listing if f in names), None)


def zip_entry(z, f):
    Z = zipfile.ZipFile(os.path.normpath(os.path.join(CFG, z)))
    return Z.read(next(n for n in Z.namelist() if re.split(r'[/\\\\]', n)[-1] == f + '.obj'))


def write_cfg(name, parts, srcs, source, error_mm):
    """parts: (part dict, source config); zips = union in source order. bones-rs takes a file from the first zip that
    has it: every file must give the same bytes as in its own regional config, else that zip moves up the list."""
    zips = []
    for c in srcs:
        for z in c['zips']:
            if z not in zips: zips.append(z)
    owns = [(p, zip_names(c)) for p, c in parts]
    for _ in range(20):
        allz, moved = zip_names({'zips': zips}), False
        for p, own in owns:
            for f in p['files']:
                a, b = first_zip(own, f), first_zip(allz, f)
                assert a, (p['key'], f)
                if a != b and zip_entry(a, f) != zip_entry(b, f):
                    zips.remove(a); zips.insert(zips.index(b), a); moved = True
                    print('  zip order:', os.path.basename(a), 'before', os.path.basename(b), 'for', f)
                    break
            if moved: break
        if not moved: break
    else: raise SystemExit('zip order did not settle')
    out = [p for p, _ in parts]
    used = [z for z in zips if any(first_zip(allz, f) == z for p in out for f in p['files'])]
    cfg = {'name': name, 'zips': used, 'out': '../../../anatomy/models/' + name, 'error_mm': error_mm, 'contact_mm': 0.5,
           'contacts_across_groups_only': True, 'pack': True, 'source': source, 'parts': out}
    json.dump(cfg, open(os.path.join(CFG, name + '.json'), 'w'), indent=1)
    print(name, len(out), 'parts')


def joints():
    """-> list of (part, source cfg, meta)"""
    res, seen = [], set()
    for g, reg, page in JOINT_SRC:
        c = load(g)
        for p in c['parts']:
            k = p['key']
            if p.get('group') == 'bone' and not k.startswith('disc_'): continue
            if k in seen: continue
            seen.add(k)
            name = p['name'].strip('()')
            kind = joint_kind(k, name, p.get('group'))
            f = p['files'][0]
            side = 'right' if f.endswith('_r') else 'left' if f.endswith('_l') else 'midline'
            if k == 'ulnopisiform_ligament': side = 'right'         # Z-Anatomy object without ".r", in the right hand
            err = p.get('error_mm', c['error_mm'])
            q = {'key': k, 'name': name, 'fma': p.get('fma', ''), 'files': p['files'], 'group': 'joint',
                 'error_mm': max(err, JOINT_ERR_MIN)}
            meta = {'kind': kind, 'region': reg or ax_region(name), 'side': side, 'mirror': side != 'midline',
                    'colour': JOINT_COL[kind], 'page': page}
            res.append((q, c, meta))
    return res


def organs():
    res, seen = [], set()
    for g, reg, page in ORGAN_SRC:
        c = load(g)
        kinds = json.load(open(os.path.join(MOD, g, 'kinds.json')))['parts']
        man = {p['key']: p for p in json.load(open(os.path.join(MOD, g, g + '.json')))['parts']}
        for p in c['parts']:
            k = p['key']
            if k not in KEEP[g] or k in seen: continue
            seen.add(k)
            d = kinds[k]
            mir = bool(d.get('mirror')) or k in MIRROR_TOO
            name = man[k]['name']
            if mir: name = re.sub(r'^Right ', '', name); name = name[0].upper() + name[1:]
            err = max(p.get('error_mm', c['error_mm']), ORGAN_ERR.get(k, 0))
            q = {'key': k, 'name': name, 'fma': p.get('fma', ''), 'files': p['files'], 'group': 'organ', 'error_mm': err}
            side = 'right' if mir or re.search(r'_r$', k) else 'left' if re.search(r'_l$', k) else 'midline'
            meta = {'kind': d['kind'], 'region': reg, 'side': side, 'mirror': mir,
                    'colour': LOBE.get(k) or ORGAN_COL[(g, d['kind'])], 'page': PAGE.get(k, page)}
            res.append((q, c, meta))
    return res


LAYERS = {
    'joints': (joints, 'Bones: none. Ligaments, capsules, discs, labra, menisci, bursae: Z-Anatomy, CC BY-SA 4.0 (from '
               'BodyParts3D), modifiers applied, moved into the BodyParts3D frame; intervertebral discs: BodyParts3D, '
               '(c) The Database Center for Life Science, CC BY-SA 2.1 Japan', 0.2),
    'organs': (organs, 'Organs: Z-Anatomy, CC BY-SA 4.0 (from BodyParts3D), moved into the BodyParts3D frame, and '
               'BodyParts3D, (c) The Database Center for Life Science, CC BY-SA 2.1 Japan', 0.3),
}


def ordered(layer):
    fn = LAYERS[layer][0]
    res = fn()
    order = {}
    for _, _, m in res: order.setdefault(m['colour'], len(order))
    return sorted(res, key=lambda r: order[r[2]['colour']])      # neighbours of one colour: one draw call


def config(layer):
    res = ordered(layer)
    srcs = []
    for _, c, _ in res:
        if c not in srcs: srcs.append(c)
    _, source, err = LAYERS[layer]
    write_cfg('body-' + layer, [(q, c) for q, c, _ in res], srcs, source, err)


def post(layer):
    res = ordered(layer)
    Q, t = mirror()
    info = {q['key']: m for q, _, m in res}
    out = {'note': 'written by tools/home/body_layers.py post ' + layer, 'mirror': {'m': Q.tolist(), 't': t.tolist()}}
    if layer == 'organs':
        used = {m['colour'] for m in info.values()}
        out['tokens'] = {k: v for k, v in TOKENS.items() if k in used}
    out['parts'] = info
    os.makedirs(os.path.join(MOD, 'body-' + layer), exist_ok=True)
    json.dump(out, open(os.path.join(MOD, 'body-' + layer, layer + '.json'), 'w'), separators=(',', ':'))
    from collections import Counter
    print(len(info), 'parts', sum(m['mirror'] for m in info.values()), 'mirrored', dict(Counter(m['kind'] for m in info.values())))
    print(dict(Counter(m['page'] for m in info.values())))


if __name__ == '__main__':
    {'config': config, 'post': post}[sys.argv[1]](sys.argv[2])
