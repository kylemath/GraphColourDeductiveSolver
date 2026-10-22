# Base-point-free tau (tau* = min over base points of the one-lap circumradius) and the W2 sub-union monodromy check.
import sys, os, json, time, random, collections, itertools, math
sys.path.insert(0, '/mnt/project-files/multiscale/merge_proof')
from mp import *

def rebase(W, j):
    """the same closed pocket walk started at boundary vertex index j (even walks only; odd tau is base-point free)."""
    walk, s = W['walk'], W['s']; m = len(walk)
    w2 = walk[j:]+walk[:j]; s2 = s[j:]+s[:j]; s2 = [x*s2[0] for x in s2]
    return dict(walk=w2, s=s2, odd=W['odd'], nv=W['nv'])

def tau_list(W, col):
    """one-lap tau for every base point (odd: single value repeated)."""
    if W['odd']: return [tau_walk(W, col)]
    return [tau_walk(rebase(W, j), col) for j in range(len(W['walk']))]

def tau_star(W, col): return min(tau_list(W, col))

def min_w_star(g, D, cR, zone, wmax=8, nb=None, budget=3*10**6):
    """min collar width w such that SOME choice of base point per even pocket admits a 1-level recolouring of
    N_w(dU) + zone.  Base points per pocket are tried in order of their one-lap tau under cR (at most nb of them).
    Returns (w, base points used, number of SAT calls)."""
    dB = multi_bfs(g.adj, list(D.bset), D.S); calls = 0
    ranks = []
    for W in D.pockets:
        tl = tau_list(W, cR); order = sorted(range(len(tl)), key=lambda j: (tl[j], j))
        if nb: order = order[:nb]
        if len(W['walk']) <= 4: order = order[:1]   # a triangle pocket is level at every base point
        ranks.append(order)
    # pockets already level (at their best base point) are kept at that base point; the others are enumerated jointly
    for ww in range(wmax+1):
        fx = {v: cR[v] for v in D.S if dB[v] > ww and v not in zone}
        if ww == 0 and all(tau_star(W, cR) <= 1+1e-9 for W in D.pockets): return 0, [r[0] for r in ranks], calls
        for combo in itertools.product(*ranks):
            walks = [rebase(W, j) for W, j in zip(D.pockets, combo)]
            calls += 1
            r = sat2(D, walks, 1.0, fixed=fx, budget=budget)
            if r not in (None, 'UNK'): return ww, list(combo), calls
    return '>%d' % wmax, None, calls

def remeasure(g, D, A, B, colA, colB, Rmax=5, wmax=8, nb=None):
    """merge_all24 (old w, base point = min vertex id) plus w* with base-point-free tau."""
    rec = merge_all24(g, D, A, B, colA, colB, Rmax=Rmax, wmax=wmax)
    if rec['R'] is None: return rec
    # rebuild the repaired colouring exactly as merge_all24 did (first renaming that works at min R)
    seam = [(u, w) for (u, w) in D.edges if (u in A) != (w in A)]
    data = []
    for p in PERMS:
        cc = {v: colA[v] for v in A}; cc.update({v: p[colB[v]] for v in B})
        K = set(x for e in seam if cc[e[0]] == cc[e[1]] for x in e)
        data.append((len(K), p, cc, K))
    data.sort(key=lambda t: t[0])
    for nk, p, cc, K in data:
        r, c2 = (0, cc) if not K else proper_repair_at(g, D.S, cc, K, rec['R'])
        if r is not None: break
    zone = set(v for v in D.S if c2[v] != cc[v])
    tl = [tau_list(W, c2) for W in D.pockets]
    t0 = time.time()
    ws, bps, calls = min_w_star(g, D, c2, zone, wmax=wmax, nb=nb)
    rec.update(w_star=ws, bp_star=bps, sat_calls=calls, tau_star_before=round(max(min(t) for t in tl), 3),
               tau_bp_spread=[round(min(t), 3) for t in tl] + [round(max(t), 3) for t in tl], nb=nb, sec_star=round(time.time()-t0, 1))
    return rec

def tau_strip(W, col):
    """reviewer's intrinsic tau: odd -> max |H_i - q| (q the reflection centre); even with t != 0 -> half-width of the
    narrowest strip parallel to t containing the periodic lift; t = 0 -> circumradius (half-lattice centres)."""
    walk, s = W['walk'], W['s']; m = len(walk); H = [(0, 0)]
    for i in range(m):
        l = col[walk[i]] ^ col[walk[(i+1) % m]]
        if l == 0: return 99.0
        d = INC[l]; H.append((H[-1][0]+s[i]*d[0], H[-1][1]+s[i]*d[1]))
    if W['odd'] or (H[-1] == H[0]): return tau_walk(W, col)
    t = (H[-1][0]-H[0][0], H[-1][1]-H[0][1])
    # euclidean coords of half-lattice point (A,B): (A + B/2, B*sqrt3/2)/2
    E = lambda p: ((p[0]+p[1]/2)/2, p[1]*math.sqrt(3)/4)
    tx, ty = E(t); nt = math.hypot(tx, ty); nx, ny = -ty/nt, tx/nt
    proj = [E(h)[0]*nx + E(h)[1]*ny for h in H]
    return (max(proj)-min(proj))/2
