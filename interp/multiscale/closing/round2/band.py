# round 2 helpers: fast level colourings via a boundary band + interior extension; band-form closing metrics.
import sys, time
sys.path.insert(0,'/mnt/project-files/multiscale/closing')
from cl import *
from pysat.solvers import Glucose4

def depth(T, cl):
    return multi_bfs(T.adj, list(cl.walk), cl.S)

def band_level_col(T, cl, rng, t=None, start=None, Wb=8, K2=1.0, dep=None):
    """level colouring of cl: SAT on the depth<=Wb band, then 4-colour the interior with depth<=Wb-3 fixed.
       returns colouring of cl.S, or None if the band level problem is UNSAT; retries extension."""
    if dep is None: dep = depth(T, cl)
    band = [v for v in cl.verts if dep[v] <= Wb]; bs = set(band)
    for attempt in range(6):
        enc = CNF(band)
        for u, w in cl.edges:
            if u in bs and w in bs: enc.neq(u, w)
        enc.level(cl, K2, t=t, start=start)
        r = enc.solve(phases=rand_phases(enc, rng), budget=None)
        if r is None or r == 'UNK': return None
        keep = {v: c for v, c in r.items() if dep[v] <= Wb-3}
        rest = [v for v in cl.verts if v not in keep]; rs = set(rest)
        e2 = CNF(rest)
        for u, w in cl.edges:
            if u in rs and w in rs: e2.neq(u, w)
            elif u in rs: e2.cls.append([-e2.x(u, keep[w])])
            elif w in rs: e2.cls.append([-e2.x(w, keep[u])])
        r2 = e2.solve()
        if r2:
            col = dict(keep); col.update(r2); return col
    return 'EXTFAIL'

def recol_stats(T, col, free, seamv):
    """solve with phases preferring old colours; return (#changed, max seam-distance of a changed vertex)"""
    fs = set(free); enc = CNF(sorted(fs))
    for v in fs:
        for w in T.adj[v]:
            if w in fs:
                if w > v: enc.neq(v, w)
            else: enc.cls.append([-enc.x(v, col[w])])
    ph = [enc.x(v, c)*(1 if c == col[v] else -1) for v in enc.verts for c in range(4)]
    s = Glucose4(bootstrap_with=enc.cls); s.set_phases(ph); ok = s.solve()
    if not ok: s.delete(); return None
    mod = set(l for l in s.get_model() if l > 0); s.delete()
    new = {v: next(c for c in range(4) if enc.x(v, c) in mod) for v in enc.verts}
    ch = [v for v in new if new[v] != col[v]]
    ds = multi_bfs(T.adj, list(seamv), set(range(len(T.adj))))
    return len(ch), max([ds[v] for v in ch], default=-1)

def closing_full(T, A, B, colA, colB, Rmax=8):
    """R_conf (old definition), W_band (recolour N_W(seam vertices)), with recolouring stats for each."""
    n = len(T.adj); allv = set(range(n))
    seamv = set(x for u in A for w in T.adj[u] if w not in A for x in (u, w))
    dS = multi_bfs(T.adj, list(seamv), allv)
    data = []
    for p in PERMS:
        col = dict(colA); col.update({v: p[colB[v]] for v in B})
        K = conflicts(T, A, col); data.append((len(K), p, col, K))
    data.sort(key=lambda t: t[0])
    out = {}
    # band form
    for W in range(0, Rmax+1):
        hit = None
        for nk, p, col, K in data:
            if nk == 0: hit = (p, col, []); break
            free = [v for v in range(n) if dS[v] <= W]
            if repair_ok(T, col, free): hit = (p, col, free); break
        if hit:
            st = recol_stats(T, hit[1], hit[2], seamv) if hit[2] else (0, -1)
            out.update(W_band=W, band_changed=st[0], band_maxd=st[1]); break
    # conflict form
    for R in range(0, Rmax+1):
        hit = None
        for nk, p, col, K in data:
            if nk == 0: hit = (p, col, [], 0); break
            d = multi_bfs(T.adj, list(K), allv)
            free = [v for v in range(n) if d.get(v, 99) <= R]
            if repair_ok(T, col, free): hit = (p, col, free, nk); break
        if hit:
            st = recol_stats(T, hit[1], hit[2], seamv) if hit[2] else (0, -1)
            out.update(R=R, nconf=hit[3], conf_changed=st[0], conf_maxd=st[1], nconf_min=data[0][0]); break
    return out
