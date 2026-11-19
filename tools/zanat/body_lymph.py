"""Lymph nodes and lymphoid organs of the whole body, for the Anatomy home page (pattern of body_vessels.py).

  body_lymph.py config      tools/bones-rs/configs/body-lymph.json from z-index-lymph.tsv
                            (export_mod.py "all:Lymphoid organs": right + midline objects; the page mirrors the right)
  body_lymph.py post        anatomy/models/body-lymph/lymph.json — kind (node, organ), region, side, mirror

Z-Anatomy draws node groups as small blobs at their usual sites; it has no lymphatic vessels and no thoracic duct."""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from body_muscles import mirror
from body_vessels import rows, region, nice

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, '..', '..'))
CFG = os.path.join(ROOT, 'tools', 'bones-rs', 'configs')
OUT = os.path.join(ROOT, 'anatomy', 'models', 'body-lymph')
ORGANS = ('Spleen', 'Left lobe of thymus', 'Right lobe of thymus', 'Palatine tonsil.r')


def keep(r):
    return not r['object'].endswith('.l') and int(r['verts']) >= 4


def config():
    parts = []
    for r in rows('z-index-lymph.tsv'):
        if keep(r):
            parts.append({'key': 'l_' + r['file'][2:], 'name': nice(r['object']), 'fma': '', 'files': [r['file']],
                          'error_mm': 0.1, 'group': 'lymph'})
    cfg = {'name': 'body-lymph', 'zips': ['../../../sources-local/zanat/z-bp3d-lymph.zip'],
           'out': '../../../anatomy/models/body-lymph', 'error_mm': 0.2, 'contact_mm': 0.5,
           'contacts_across_groups_only': True, 'pack': True,
           'source': 'Z-Anatomy, CC BY-SA 4.0, moved into the BodyParts3D frame', 'parts': parts}
    json.dump(cfg, open(os.path.join(CFG, 'body-lymph.json'), 'w'), indent=1)
    print(len(parts), 'parts')


def post():
    cfg = json.load(open(os.path.join(CFG, 'body-lymph.json')))
    allrows = rows('z-index-lymph.tsv'); objs = {r['object'] for r in allrows}
    src = {r['file']: r for r in allrows}
    Q, t = mirror()
    info = {}
    for p in cfg['parts']:
        r = src[p['files'][0]]; o = r['object']
        side = 'right' if o.endswith('.r') else 'midline'
        info[p['key']] = {'kind': 'organ' if o in ORGANS else 'node', 'region': region(r['collections']), 'side': side,
                          'mirror': o.endswith('.r') and (o[:-2] + '.l') in objs}
    json.dump({'note': 'written by tools/zanat/body_lymph.py post', 'mirror': {'m': Q.tolist(), 't': t.tolist()},
               'parts': info}, open(os.path.join(OUT, 'lymph.json'), 'w'), indent=0)
    print(len(info), 'parts', sum(d['mirror'] for d in info.values()), 'mirrored')


if __name__ == '__main__':
    {'config': config, 'post': post}[sys.argv[1]]()
