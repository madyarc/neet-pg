"""The heart and blood vessels of the whole body, for the Anatomy home page.

  body_vessels.py config      write tools/bones-rs/configs/body-vessels.json from z-index-vessels.tsv (tubes swept
                              along Z-Anatomy's vessel curves, export_curves.py) and z-index-heart.tsv (the heart
                              chambers and the venous sinuses that are meshes, export_mod.py)
  body_vessels.py post        after `bones build`: anatomy/models/body-vessels/vessels.json — for each part its kind
                              (artery, vein, heart), region, side and whether the page mirrors it to the left

Right-side vessels only (+ midline and the few left ones that are not mirror images); the page makes the left side
with the same reflection as the muscles (Z-Anatomy x -> -x)."""
import sys, os, json, csv, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from body_muscles import mirror

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, '..', '..'))
CFG = os.path.join(ROOT, 'tools', 'bones-rs', 'configs')
OUT = os.path.join(ROOT, 'anatomy', 'models', 'body-vessels')
# heart meshes shown on the whole body: the chambers (valves and papillary muscles are inside them)
HEART = {'Right atrium', 'Right ventricle', 'Left atrium', 'Left ventricle'}
MESH_VEINS = {'Cavernous sinus.r', 'Basilar venous plexus'}
MESH_ARTERIES = {'Pulmonary trunk', 'Anterior communicating artery'}


def rows(fn):
    return list(csv.DictReader(open(os.path.join(HERE, fn)), delimiter='\t'))


def kind(name, cs):
    if name in HEART: return 'heart'
    if name in MESH_VEINS or 'vein' in cs.lower() or 'Cardiac veins' in cs or 'sinus' in name.lower(): return 'vein'
    return 'artery'


def region(cs):
    c = cs.split('|')
    if any('lower limb' in x or 'foot' in x for x in c): return 'Lower limb'
    if any('upper limb' in x or 'hand' in x for x in c): return 'Upper limb'
    if 'Head' in c: return 'Head and neck'
    if 'Neck' in c: return 'Head and neck'
    return 'Trunk'


def nice(name):
    n = name.strip()
    n = re.sub(r'\.(r|l)$', '', n).strip('()').strip()
    n = re.sub(r"\s*\(//.*$", '', n)
    return n[0].upper() + n[1:]


def error_mm(rmin):
    # thin tubes keep their shape: allowed error about a third of the smallest radius
    return 0.02           # the tubes are already as coarse as they should be (export_curves.py thin()); weld only


def config():
    parts, keys = [], set()
    def add(key, name, fn, err):
        k = key
        i = 1
        while k in keys: i += 1; k = '%s_%d' % (key, i)
        keys.add(k)
        parts.append({'key': k, 'name': name, 'fma': '', 'files': [fn], 'error_mm': err, 'group': 'vessel'})
    for r in rows('z-index-vessels.tsv'):
        rmin = float(r['radius_mm'].split('-')[0])
        add('v_' + r['file'][2:], nice(r['object']), r['file'], error_mm(rmin))
    for r in rows('z-index-heart.tsv'):
        o = r['object']
        if o in HEART or o in MESH_VEINS or o in MESH_ARTERIES:
            add('v_' + r['file'][2:], nice(o), r['file'], 0.3 if o in HEART else 0.15)
    # arteries, then veins, then the heart: parts of one colour next to each other are drawn with one call
    src = {r['file']: (r['object'], r['collections']) for f in ('z-index-vessels.tsv', 'z-index-heart.tsv') for r in rows(f)}
    order = {'artery': 0, 'vein': 1, 'heart': 2}
    parts.sort(key=lambda p: order[kind(*src[p['files'][0]])])
    cfg = {'name': 'body-vessels',
           'zips': ['../../../sources-local/zanat/z-bp3d-vessels.zip', '../../../sources-local/zanat/z-bp3d-heart.zip'],
           'out': '../../../anatomy/models/body-vessels', 'error_mm': 0.3, 'contact_mm': 0.5,
           'contacts_across_groups_only': True, 'pack': True,
           'source': 'Z-Anatomy, CC BY-SA 4.0 (vessel curves swept into tubes; heart from BodyParts3D), '
                     'moved into the BodyParts3D frame',
           'parts': parts}
    json.dump(cfg, open(os.path.join(CFG, 'body-vessels.json'), 'w'), indent=1)
    print(len(parts), 'parts')


def post():
    cfg = json.load(open(os.path.join(CFG, 'body-vessels.json')))
    src = {}
    for r in rows('z-index-vessels.tsv'): src[r['file']] = (r['object'], r['collections'], r['mirror'] == '1')
    for r in rows('z-index-heart.tsv'): src[r['file']] = (r['object'], r['collections'], False)
    Q, t = mirror()
    info = {}
    for p in cfg['parts']:
        o, cs, mir = src[p['files'][0]]
        side = 'right' if o.endswith('.r') else 'left' if o.endswith('.l') else 'midline'
        info[p['key']] = {'kind': kind(o, cs), 'region': region(cs), 'side': side, 'mirror': mir}
    out = {'note': 'written by tools/zanat/body_vessels.py post', 'mirror': {'m': Q.tolist(), 't': t.tolist()},
           'parts': info}
    json.dump(out, open(os.path.join(OUT, 'vessels.json'), 'w'), indent=0)
    from collections import Counter
    print(Counter(d['kind'] for d in info.values()), Counter(d['region'] for d in info.values()),
          sum(d['mirror'] for d in info.values()), 'mirrored')


if __name__ == '__main__':
    {'config': config, 'post': post}[sys.argv[1]]()
