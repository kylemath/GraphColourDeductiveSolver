"""Small exact 4-colouring CSP solver for near-triangulations (independent of the transfer-matrix code).

Constraints: every edge is 'different'; every triangle is 'all-different' (redundant but gives strong propagation:
it is exactly what turns a 2-coloured alternating run into a forced cone).  Propagation = generalised arc
consistency (GAC) on the triangle and edge constraints; search = DFS with MRV.  Complete and sound.

API:
   solve(n, edges, tris, dom)  -> colouring list or None ;  dom: list of sets (fixed vertices: singletons)
   propagate_only(...)         -> False if GAC alone wipes out a domain (a short, checkable certificate)
"""
import sys
sys.setrecursionlimit(100000)

def build_index(n, edges, tris):
    nb = [set() for _ in range(n)]
    for u, v in edges: nb[u].add(v); nb[v].add(u)
    tri_of = [[] for _ in range(n)]
    for t in tris:
        for x in t: tri_of[x].append(t)
    return nb, tri_of

def gac(dom, nb, tri_of, queue):
    """dom: list of frozenset/set (mutated copy semantics handled by caller). returns False on wipe-out."""
    inq = set(queue); queue = list(queue)
    while queue:
        x = queue.pop(); inq.discard(x)
        # edge constraints: a singleton removes its value from neighbours
        if len(dom[x]) == 1:
            (c,) = tuple(dom[x])
            for y in nb[x]:
                if c in dom[y]:
                    dom[y] = dom[y] - {c}
                    if not dom[y]: return False
                    if y not in inq: inq.add(y); queue.append(y)
        # triangle all-different GAC
        for t in tri_of[x]:
            a, b, c = t
            for (p, q, r) in ((a, b, c), (b, a, c), (c, a, b)):
                keep = set()
                for vp in dom[p]:
                    ok = False
                    for vq in dom[q]:
                        if vq == vp: continue
                        for vr in dom[r]:
                            if vr != vp and vr != vq: ok = True; break
                        if ok: break
                    if ok: keep.add(vp)
                if len(keep) < len(dom[p]):
                    if not keep: return False
                    dom[p] = keep
                    if p not in inq: inq.add(p); queue.append(p)
    return True

def solve(n, edges, tris, dom, nb=None, tri_of=None, stats=None):
    if nb is None: nb, tri_of = build_index(n, edges, tris)
    dom = [set(d) for d in dom]
    if not gac(dom, nb, tri_of, range(n)): return None
    return _dfs(dom, nb, tri_of, stats)

def _dfs(dom, nb, tri_of, stats):
    if stats is not None: stats['nodes'] = stats.get('nodes', 0) + 1
    best = None
    for v in range(len(dom)):
        if len(dom[v]) > 1 and (best is None or len(dom[v]) < len(dom[best])): best = v
    if best is None: return [next(iter(d)) for d in dom]
    for c in sorted(dom[best]):
        d2 = [set(d) for d in dom]; d2[best] = {c}
        if gac(d2, nb, tri_of, [best]):
            r = _dfs(d2, nb, tri_of, stats)
            if r is not None: return r
    return None

def propagate_only(n, edges, tris, dom):
    nb, tri_of = build_index(n, edges, tris)
    dom = [set(d) for d in dom]
    return gac(dom, nb, tri_of, range(n))
