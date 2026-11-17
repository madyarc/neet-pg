"""Export Z-Anatomy meshes into the BodyParts3D 3.0 body frame (mm) as OBJ files in one zip, so that
tools/bones-rs can build them like BodyParts3D parts (config "files": ["Z_<slug>"]).
usage: export.py blend transform.json out.zip index.tsv "collection substring" | "name:Exact object name" [...]
Skips helper objects (.j .i .g .t .s), text and curves. Left objects are mirrored copies: their winding is flipped
back so normals point outward."""
import sys, os, re, json, zipfile, io, numpy as np
sys.path.insert(0, os.path.dirname(__file__))
import zblend

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

def slug(n): return 'Z_' + re.sub(r'[^a-z0-9]+', '_', n.lower()).strip('_')
seen = {}
with zipfile.ZipFile(sys.argv[3], 'w', zipfile.ZIP_DEFLATED) as zf, open(sys.argv[4], 'w') as idx:
    idx.write('file\tobject\tverts\ttris\tmirrored\tmodifiers\tcollections\n')
    for ob in bf.code_index[b'OB']:
        name = zblend.obname(ob)
        if re.search(r'\.(j|i|g|t|s)$', name): continue
        cs = coll.get(ob.addr_old, [])
        exact = [w[5:] for w in wanted if w.startswith('name:')]      # 'name:Thyroid cartilage' picks one object
        if not (name in exact or any(w in c for w in wanted if not w.startswith('name:') for c in cs)): continue
        me = ob.get_pointer(b'data')
        if me is None or me.code != b'ME' or me.get(b'totvert') < 4: continue
        V, F = zblend.mesh_arrays(me)
        W = s * zblend.world(ob, V) @ R.T + t
        M = np.array(ob.get(b'obmat')).reshape(4, 4)
        mir = np.linalg.det(M[:3, :3]) < 0
        if mir: F = F[:, ::-1]
        mods = []
        p = ob.get_pointer((b'modifiers', b'first'))
        while p is not None:
            mods.append(p.dna_type_name.replace('ModifierData', ''))
            try: p = p.get_pointer(b'next')
            except KeyError: p = p.get_pointer((b'modifier', b'next'))
        fn = slug(name)
        if fn in seen: seen[fn] += 1; fn += '_%d' % seen[fn]
        else: seen[fn] = 0
        buf = io.StringIO()
        buf.write('# %s (Z-Anatomy, CC BY-SA 4.0; from BodyParts3D, CC BY-SA 2.1 JP), BodyParts3D 3.0 frame, mm\n' % name)
        for v in W: buf.write('v %.4f %.4f %.4f\n' % tuple(v))
        for f in F + 1: buf.write('f %d %d %d\n' % tuple(f))
        zf.writestr(fn + '.obj', buf.getvalue())
        idx.write('\t'.join([fn, name, str(len(V)), str(len(F)), str(int(mir)), ','.join(mods), '|'.join(cs)]) + '\n')
print('done')
