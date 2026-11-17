"""Inventory of a Z-Anatomy .blend: every mesh object with its collection, mesh, size, modifiers and transform.
usage: inventory.py file.blend out.tsv"""
import sys, pathlib
from blender_asset_tracer import blendfile
bf = blendfile.open_cached(pathlib.Path(sys.argv[1]))
def nm(b): return b.id_name[2:].decode('utf-8', 'replace')
def listbase(blk, field):
    p = blk.get_pointer((field, b'first'))
    while p is not None:
        yield p
        try: p = p.get_pointer(b'next')
        except KeyError: p = p.get_pointer((b'modifier', b'next'))
# collection membership
coll = {}
for g in bf.code_index[b'GR']:
    for co in listbase(g, b'gobject'):
        ob = co.get_pointer(b'ob')
        if ob is not None:
            coll.setdefault(ob.addr_old, []).append(nm(g))
MODT = {5:'mirror',3:'subsurf',8:'armature',10:'array',1:'subsurf?',6:'decimate',36:'solidify',43:'weld?',9:'boolean',16:'shrinkwrap',39:'skin',11:'displace'}
rows = []
for ob in bf.code_index[b'OB']:
    t = ob.get(b'type')
    data = ob.get_pointer(b'data')
    mods = [m.dna_type_name.replace('ModifierData','') for m in listbase(ob, b'modifiers')]
    M = ob.get(b'obmat')
    sc = [round((M[4*i]**2 + M[4*i+1]**2 + M[4*i+2]**2) ** .5, 4) for i in range(3)]
    tr = [round(M[12+k], 4) for k in range(3)]
    par = ob.get_pointer(b'parent')
    nv = data.get(b'totvert') if (data is not None and data.code == b'ME') else ''
    rows.append([nm(ob), {1:'mesh',2:'curve',4:'font',0:'empty'}.get(t, str(t)), nm(data) if data is not None else '', str(nv),
                 ','.join(mods), ' '.join(map(str, sc)), ' '.join(map(str, tr)), nm(par) if par is not None else '',
                 '|'.join(coll.get(ob.addr_old, []))])
with open(sys.argv[2], 'w') as f:
    f.write('object\ttype\tdata\tverts\tmods\tscale\ttrans\tparent\tcollections\n')
    for r in rows: f.write('\t'.join(r) + '\n')
print(len(rows), 'objects')
