"""Read meshes out of the Z-Anatomy .blend (Blender 3.5 format) without Blender.
mesh_arrays(me) -> (V float32 (n,3) in object space, F int32 (m,3) triangles)
world(ob, V) -> V in world space (obmat)."""
import pathlib, struct
import numpy as np
from blender_asset_tracer import blendfile

_LOCAL = {}

def open_blend(p):
    bf = blendfile.open_cached(pathlib.Path(p))
    # Blender 3.5 writes mesh arrays from temporary buffers whose addresses repeat across meshes,
    # so resolve a mesh's pointers among the DATA blocks written right after it.
    cur = None
    for b in bf.blocks:
        if b.code == b'DATA':
            if cur is not None: cur.setdefault(b.addr_old, b)
        else:
            cur = _LOCAL.setdefault(id(b), {}) if b.code == b'ME' else None
    return bf

def deref(owner, ptr):
    loc = _LOCAL.get(id(owner))
    if loc is not None and ptr in loc: return loc[ptr]
    try: return owner.bfile.dereference_pointer(ptr)
    except Exception: return None  # layer not written to the file

def layers(me, cd):
    n = me.get((cd, b'totlayer'))
    f, o = me.dna_type.field_from_path(me.bfile.header.pointer_size, (cd, b'layers'))
    lp = struct.unpack_from('<Q', me.raw_data(), o)[0]
    L = deref(me, lp) if lp else None
    out = []
    if L is None: return out
    sz = L.dna_type.size
    for i in range(n):
        off = i * sz
        t = struct.unpack_from('<i', L.raw_data(), off + L.dna_type.field_from_path(L.bfile.header.pointer_size, b'type')[1])[0]
        name = None
        f, o = L.dna_type.field_from_path(L.bfile.header.pointer_size, b'name')
        name = L.raw_data()[off + o: off + o + 64].split(b'\0')[0].decode()
        f, o = L.dna_type.field_from_path(L.bfile.header.pointer_size, b'data')
        ptr = struct.unpack_from('<Q', L.raw_data(), off + o)[0]
        out.append((t, name, deref(me, ptr) if ptr else None))
    return out

def mesh_arrays(me):
    nv, npoly, nl = me.get(b'totvert'), me.get(b'totpoly'), me.get(b'totloop')
    V = P = C = None
    for t, name, blk in layers(me, b'vdata'):
        if blk is None: continue
        raw = blk.raw_data()
        if name == 'position':
            V = np.frombuffer(raw, np.float32, nv * 3).reshape(nv, 3)
        elif t == 0 and V is None:  # legacy MVert: co[3] float, then other fields
            stride = len(raw) // nv
            V = np.frombuffer(raw, np.uint8).reshape(nv, stride)[:, :12].copy().view(np.float32).reshape(nv, 3)
    for t, name, blk in layers(me, b'pdata'):
        if blk is None or t != 25: continue
        raw = blk.raw_data()
        stride = len(raw) // npoly
        a = np.frombuffer(raw, np.uint8).reshape(npoly, stride)
        P = (a[:, 0:4].copy().view(np.int32).ravel(), a[:, 4:8].copy().view(np.int32).ravel())  # loopstart, totloop
    for t, name, blk in layers(me, b'ldata'):
        if blk is None or t != 26: continue
        raw = blk.raw_data()
        stride = len(raw) // nl
        C = np.frombuffer(raw, np.uint8).reshape(nl, stride)[:, 0:4].copy().view(np.int32).ravel()  # MLoop.v
    tris = []
    if P is None or C is None:
        if npoly: raise ValueError('mesh has %d faces but no face data' % npoly)
        return V, np.zeros((0, 3), np.int32)
    ls, tl = P
    for s, k in zip(ls, tl):
        for j in range(1, k - 1):
            tris.append((C[s], C[s + j], C[s + j + 1]))
    return V, np.array(tris, np.int32)

def world(ob, V):
    M = np.array(ob.get(b'obmat'), np.float64).reshape(4, 4)  # column-major: rows are basis vectors
    return V @ M[:3, :3] + M[3, :3]

def obname(ob): return ob.id_name[2:].decode('utf-8', 'replace')

def mesh_polys(me):
    """V (n,3) object space and the polygons (lists of vertex ids, quads kept), for applying modifiers"""
    nv, npoly, nl = me.get(b'totvert'), me.get(b'totpoly'), me.get(b'totloop')
    V = P = C = None
    for t, name, blk in layers(me, b'vdata'):
        if blk is None: continue
        raw = blk.raw_data()
        if name == 'position': V = np.frombuffer(raw, np.float32, nv * 3).reshape(nv, 3)
        elif t == 0 and V is None:
            stride = len(raw) // nv
            V = np.frombuffer(raw, np.uint8).reshape(nv, stride)[:, :12].copy().view(np.float32).reshape(nv, 3)
    for t, name, blk in layers(me, b'pdata'):
        if blk is None or t != 25: continue
        raw = blk.raw_data(); stride = len(raw) // npoly
        a = np.frombuffer(raw, np.uint8).reshape(npoly, stride)
        P = (a[:, 0:4].copy().view(np.int32).ravel(), a[:, 4:8].copy().view(np.int32).ravel())
    for t, name, blk in layers(me, b'ldata'):
        if blk is None or t != 26: continue
        raw = blk.raw_data(); stride = len(raw) // nl
        C = np.frombuffer(raw, np.uint8).reshape(nl, stride)[:, 0:4].copy().view(np.int32).ravel()
    if V is None or P is None or C is None: return None, []        # no face data written (e.g. an empty helper)
    return V.astype(np.float64), [list(C[s:s + k]) for s, k in zip(*P)]

def modifiers(ob):
    """[(type, {settings})] in stack order: Subsurf levels, Solidify thickness/offset"""
    out = []
    p = ob.get_pointer((b'modifiers', b'first'))
    while p is not None:
        t = p.dna_type_name.replace('ModifierData', ''); d = {}
        if t == 'Subsurf': d = {'levels': p.get(b'renderLevels'), 'type': p.get(b'subdivType')}
        if t == 'Solidify': d = {'offset': p.get(b'offset'), 'fac': p.get(b'offset_fac')}
        out.append((t, d))
        try: p = p.get_pointer(b'next')
        except KeyError: p = p.get_pointer((b'modifier', b'next'))
    return out
