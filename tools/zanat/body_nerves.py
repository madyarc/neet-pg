"""The peripheral nerves of the whole body, for the Anatomy home page (same pattern as body_vessels.py).

  body_nerves.py config      write tools/bones-rs/configs/body-nerves.json from z-index-nerves.tsv (tubes swept along
                             Z-Anatomy's nerve curves, export_curves.py "7: Nervous system") and z-index-nerve-mesh.tsv
                             (spinal dura, a spinal ganglion, the sympathetic ganglia: export_mod.py)
  body_nerves.py post        after `bones build`: anatomy/models/body-nerves/nerves.json — each part's kind (nerve,
                             ganglion, dura), group (cranial, brachial plexus, lumbosacral plexus, spinal, autonomic),
                             region, side, and whether the page mirrors it to the left

Z-Anatomy has no phrenic nerve, no inferior gluteal nerve and no spinal cord mesh (the spinal dura stands for the
dural sac); pages say so where it matters."""
import sys, os, json, csv, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from body_muscles import mirror
from body_vessels import rows, region, nice

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, '..', '..'))
CFG = os.path.join(ROOT, 'tools', 'bones-rs', 'configs')
OUT = os.path.join(ROOT, 'anatomy', 'models', 'body-nerves')
SKIP = {"Central canal'"}            # inside the (absent) spinal cord
MESH = {'Spinal dura': 'dura', 'Spinal ganglion.r': 'ganglion', 'Ganglia of sympathetic trunk.r': 'ganglion',
        'Cochlear nerve': 'nerve'}


def kind(o):
    return MESH.get(o, 'nerve')


def group(o, cs):
    c = cs.split('|')
    if 'Cranial nerves' in c or o == 'Cochlear nerve': return 'cranial'
    if 'Sympathetic trunk' in c or o.startswith('Ganglia of sympathetic'): return 'autonomic'
    if any('brachial plexus' in x.lower() for x in c) or 'upper limb' in cs: return 'brachial'
    if any(x in cs for x in ('Lumbosacral plexus', 'Lumbar plexus', 'Sciatic nerve', 'lower limb')): return 'lumbosacral'
    return 'spinal'


def config():
    parts, keys = [], set()
    def add(key, name, fn, err):
        k, i = key, 1
        while k in keys: i += 1; k = '%s_%d' % (key, i)
        keys.add(k)
        parts.append({'key': k, 'name': name, 'fma': '', 'files': [fn], 'error_mm': err, 'group': 'nerve'})
    src = {}
    for r in rows('z-index-nerves.tsv'):
        if r['object'] in SKIP: continue
        add('n_' + r['file'][2:], nice(r['object']), r['file'], 0.02); src[r['file']] = r['object']
    for r in rows('z-index-nerve-mesh.tsv'):
        add('n_' + r['file'][2:], nice(r['object']), r['file'], 0.3 if r['object'] == 'Spinal dura' else 0.1)
        src[r['file']] = r['object']
    order = {'nerve': 0, 'ganglion': 1, 'dura': 2}   # one colour per run: one draw call each
    parts.sort(key=lambda p: order[kind(src[p['files'][0]])])
    cfg = {'name': 'body-nerves',
           'zips': ['../../../sources-local/zanat/z-bp3d-nerves.zip', '../../../sources-local/zanat/z-bp3d-nerve-mesh.zip'],
           'out': '../../../anatomy/models/body-nerves', 'error_mm': 0.3, 'contact_mm': 0.5,
           'contacts_across_groups_only': True, 'pack': True,
           'source': 'Z-Anatomy, CC BY-SA 4.0 (nerve curves swept into tubes), moved into the BodyParts3D frame',
           'parts': parts}
    json.dump(cfg, open(os.path.join(CFG, 'body-nerves.json'), 'w'), indent=1)
    print(len(parts), 'parts')


def post():
    cfg = json.load(open(os.path.join(CFG, 'body-nerves.json')))
    src = {}
    for r in rows('z-index-nerves.tsv'): src[r['file']] = (r['object'], r['collections'], r['mirror'] == '1')
    for r in rows('z-index-nerve-mesh.tsv'): src[r['file']] = (r['object'], r['collections'], r['object'].endswith('.r'))
    Q, t = mirror()
    info = {}
    for p in cfg['parts']:
        o, cs, mir = src[p['files'][0]]
        side = 'right' if o.endswith('.r') else 'left' if o.endswith('.l') else 'midline'
        info[p['key']] = {'kind': kind(o), 'group': group(o, cs), 'region': region(cs), 'side': side, 'mirror': mir}
    json.dump({'note': 'written by tools/zanat/body_nerves.py post', 'mirror': {'m': Q.tolist(), 't': t.tolist()},
               'parts': info}, open(os.path.join(OUT, 'nerves.json'), 'w'), indent=0)
    from collections import Counter
    print(Counter(d['group'] for d in info.values()), Counter(d['kind'] for d in info.values()),
          sum(d['mirror'] for d in info.values()), 'mirrored')


if __name__ == '__main__':
    {'config': config, 'post': post}[sys.argv[1]]()
