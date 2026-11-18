"""Like export.py, but applies each object's Subsurf and Solidify modifiers (ligaments, capsules, discs, labra and
bursae are stored as coarse sheets; Blender shows them smoothed and thickened).
usage: export_mod.py blend transform.json out.zip index.tsv "all:Coll A,Coll B" | "name:Exact" [...]
"all:A,B" picks objects that are in collections whose names contain A and B (each may match a different collection)."""
import sys, os, re, json, zipfile, io, numpy as np
sys.path.insert(0, os.path.dirname(__file__))
import zblend, zmods

bf = zblend.open_blend(sys.argv[1]); T = json.load(open(sys.argv[2]))
R, t, s = np.array(T['R']), np.array(T['t']), T['scale']
wanted = sys.argv[5:]
coll = {}
def listbase(blk, field):
    p = blk.get_pointer((field, b'first'))
    while p is not None:
        yield p; p = p.get_pointer(b'next')
for g in bf.code_index[b'GR']:
    for co in listbase(g, b'gobject'):
        ob = co.get_pointer(b'ob')
        if ob is not None: coll.setdefault(ob.addr_old, []).append(g.id_name[2:].decode('utf-8', 'replace'))
def pick(name, cs):
    for w in wanted:
        if w.startswith('name:') and name == w[5:]: return True
        if w.startswith('all:') and all(any(x in c for c in cs) for x in w[4:].split(',')): return True
    return False
def slug(n): return 'Z_' + re.sub(r'[^a-z0-9]+', '_', n.lower()).strip('_')
seen = {}
with zipfile.ZipFile(sys.argv[3], 'w', zipfile.ZIP_DEFLATED) as zf, open(sys.argv[4], 'w') as idx:
    idx.write('file\tobject\tverts\ttris\tmirrored\tmodifiers\tcollections\n')
    for ob in bf.code_index[b'OB']:
        name = zblend.obname(ob)
        if re.search(r'\.(j|i|g|t|s|o\w*|e\w*)$', name): continue          # helpers, attachment patches
        cs = coll.get(ob.addr_old, [])
        if not pick(name, cs): continue
        me = ob.get_pointer(b'data')
        if me is None or me.code != b'ME' or me.get(b'totvert') < 3: continue
        V, polys = zblend.mesh_polys(me)
        if not polys: continue
        mods = zblend.modifiers(ob)
        # modifiers work in object space, before the object's transform (as in Blender)
        for typ, d in mods:
            if typ == 'Subsurf' and d['type'] == 0: V, polys = zmods.subsurf(V, polys, d['levels'])
            if typ == 'Solidify': V, polys = zmods.solidify(V, polys, d['offset'], d['fac'])
        F = np.array(zmods.tri(polys), np.int64)
        W = s * zblend.world(ob, V) @ R.T + t
        M = np.array(ob.get(b'obmat')).reshape(4, 4)
        if np.linalg.det(M[:3, :3]) < 0: F = F[:, ::-1]
        fn = slug(name)
        if fn in seen: seen[fn] += 1; fn += '_%d' % seen[fn]
        else: seen[fn] = 0
        buf = io.StringIO()
        buf.write('# %s (Z-Anatomy, CC BY-SA 4.0; from BodyParts3D), modifiers applied: %s; BodyParts3D 3.0 frame, mm\n'
                  % (name, ', '.join(m[0] for m in mods)))
        for v in W: buf.write('v %.4f %.4f %.4f\n' % tuple(v))
        for f in F + 1: buf.write('f %d %d %d\n' % tuple(f))
        zf.writestr(fn + '.obj', buf.getvalue())
        idx.write('\t'.join([fn, name, str(len(W)), str(len(F)), str(int(np.linalg.det(M[:3, :3]) < 0)),
                             ','.join(m[0] for m in mods), '|'.join(cs)]) + '\n')
print('done')
