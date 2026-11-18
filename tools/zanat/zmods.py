"""Apply Blender's Subsurf (Catmull-Clark) and Solidify modifiers to a polygon mesh, as Z-Anatomy shows its
ligaments, capsules and discs (stored as coarse sheets that rely on these modifiers).
subsurf(V, polys, levels) -> V, quads ; solidify(V, polys, thickness, fac) -> V, triangles"""
import numpy as np


def catmull_clark(V, polys):
    V = np.asarray(V, float); n = len(V)
    fpt = np.array([V[p].mean(0) for p in polys])
    edges = {}                                   # (a,b) sorted -> list of face ids
    for fi, p in enumerate(polys):
        for i in range(len(p)):
            e = tuple(sorted((p[i], p[(i + 1) % len(p)])))
            edges.setdefault(e, []).append(fi)
    eid = {e: n + len(fpt) + i for i, e in enumerate(edges)}
    ept = []
    for e, fs in edges.items():
        if len(fs) == 2: ept.append((V[e[0]] + V[e[1]] + fpt[fs[0]] + fpt[fs[1]]) / 4)
        else: ept.append((V[e[0]] + V[e[1]]) / 2)          # boundary: midpoint
    ept = np.array(ept)
    # new positions of the old vertices
    vf = [[] for _ in range(n)]; ve = [[] for _ in range(n)]
    for fi, p in enumerate(polys):
        for v in p: vf[v].append(fi)
    for e, fs in edges.items():
        ve[e[0]].append(e); ve[e[1]].append(e)
    NV = V.copy()
    for v in range(n):
        bnd = [e for e in ve[v] if len(edges[e]) == 1]
        if bnd:                                   # boundary vertex: smooth along the boundary only
            if len(bnd) == 2:
                o = [e[0] if e[1] == v else e[1] for e in bnd]
                NV[v] = (V[o[0]] + V[o[1]] + 6 * V[v]) / 8
            continue
        k = len(ve[v])
        if k < 3 or not vf[v]: continue
        F = fpt[vf[v]].mean(0); R = np.mean([(V[e[0]] + V[e[1]]) / 2 for e in ve[v]], 0)
        NV[v] = (F + 2 * R + (k - 3) * V[v]) / k
    P = np.vstack([NV, fpt, ept])
    quads = []
    for fi, p in enumerate(polys):
        c = n + fi
        for i in range(len(p)):
            a, b, z = p[i - 1], p[i], p[(i + 1) % len(p)]
            quads.append([b, eid[tuple(sorted((b, z)))], c, eid[tuple(sorted((a, b)))]])
    return P, quads


def subsurf(V, polys, levels):
    for _ in range(levels): V, polys = catmull_clark(V, polys)
    return V, polys


def tri(polys):
    return [(p[0], p[j], p[j + 1]) for p in polys for j in range(1, len(p) - 1)]


def vnormals(V, T):
    T = np.asarray(T); N = np.zeros_like(V)
    fn = np.cross(V[T[:, 1]] - V[T[:, 0]], V[T[:, 2]] - V[T[:, 0]])
    for k in range(3): np.add.at(N, T[:, k], fn)
    l = np.linalg.norm(N, axis=1, keepdims=True); l[l == 0] = 1
    return N / l


def solidify(V, polys, thick, fac):
    """Blender's simple Solidify: the sheet is offset along the vertex normals to make two shells
    (fac -1: the shell grows inward, +1 outward, 0 centred) joined by a rim along the open edges"""
    T = tri(polys); N = vnormals(V, T); n = len(V)
    A = V + N * thick * (fac + 1) / 2; B = V + N * thick * (fac - 1) / 2
    out = [list(t) for t in T] + [[t[0] + n, t[2] + n, t[1] + n] for t in T]
    cnt = {}
    for p in polys:
        for i in range(len(p)):
            e = (p[i], p[(i + 1) % len(p)]); k = tuple(sorted(e)); cnt[k] = cnt.get(k, 0) + 1
    for p in polys:
        for i in range(len(p)):
            a, b = p[i], p[(i + 1) % len(p)]
            if cnt[tuple(sorted((a, b)))] == 1: out += [[b, a, a + n], [b, a + n, b + n]]
    return np.vstack([A, B]), out
