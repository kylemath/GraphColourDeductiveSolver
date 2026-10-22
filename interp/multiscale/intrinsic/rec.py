# Step 3(a): bottom-up W1 recursion with the intrinsic invariant: every pocket tau_int <= 1 AND |t| <= TMAX.
# Records per merge: parity class of (A,B) (whole-disc vortex parity), |t_U| of the glued+repaired colouring,
# R (all 24 renamings), w (min collar, exact tau_int SAT, dmax=2), tau_Hodge of U's pockets after re-level.
# usage: rec.py map seed L TMAX
import sys, json, time, math, collections
sys.path.insert(0, '/mnt/project-files/multiscale/intrinsic')
import ic
from wk import Disc, G, build_tree, proper_repair_at
from lev import PERMS, multi_bfs
from e1_hier import make
name, seed, L = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]); TMAX = None if sys.argv[4] == 'none' else float(sys.argv[4])
g = G(make(name)); nodes = build_tree(g, L=L, seed=seed)
out = open('/mnt/project-files/multiscale/intrinsic/rec_%s_s%d_L%d_t%s.jsonl' % (name, seed, L, sys.argv[4]), 'w')
col = {}; order = []; st = [0]
while st: i = st.pop(); order.append(i); st.extend(nodes[i]['kids'])
order.reverse(); t0 = time.time()
def tn(W, c):
    t = ic.tvec(W, c); return None if W['odd'] else (round(math.sqrt(ic.n2(t)), 3) if t else 0.0)
for i in order:
    if i == 0: continue
    nd = nodes[i]; D = Disc(g, nd['S'])
    if not nd['kids']:
        c = ic.sat_disc(D, D.pockets, 1.0, dmax=2.0, tmax=TMAX)
        if c is None: c = ic.sat_disc(D, [], 1.0); out.write(json.dumps(dict(leaf_fail=len(D.S)))+'\n')
        col.update(c); continue
    a, b = nd['kids']; A, B = nodes[a]['S'], nodes[b]['S']
    DA, DBB = Disc(g, A), Disc(g, B)
    par = ''.join('o' if X.whole['odd'] else 'e' for X in (DA, DBB))
    seam = [(u, w) for (u, w) in D.edges if (u in A) != (w in A)]
    data = []
    for p in PERMS:
        cc = {v: col[v] for v in A}; cc.update({v: p[col[v]] for v in B})
        K = set(x for e in seam if cc[e[0]] == cc[e[1]] for x in e); data.append((len(K), p, cc, K))
    data.sort(key=lambda t: t[0]); R = None
    for RR in range(8):
        for nk, p, cc, K in data:
            r, c2 = (0, cc) if not K else proper_repair_at(g, D.S, cc, K, RR)
            if r is not None: R, cR, glued = RR, c2, cc; break
        if R is not None: break
    zone = set(v for v in D.S if cR[v] != glued[v])
    dB = multi_bfs(g.adj, list(D.bset), D.S)
    ok0 = all(ic.tau_int(W, cR) <= 1+1e-9 and (TMAX is None or W['odd'] or (tn(W, cR) or 0) <= TMAX+1e-9) for W in D.pockets)
    w = 0 if ok0 else None; c3 = cR if ok0 else None
    if w is None:
        for ww in range(9):
            fx = {v: cR[v] for v in D.S if dB[v] > ww and v not in zone}
            r = ic.sat_disc(D, D.pockets, 1.0, fixed=fx, dmax=2.0, tmax=TMAX, budget=2*10**6)
            if r not in (None, 'UNK'): w, c3 = ww, r; break
    if c3 is None: c3 = ic.sat_disc(D, D.pockets, 1.0, dmax=2.0, tmax=TMAX) or cR
    col.update(c3)
    rec = dict(nU=len(D.S), mU=len(D.whole['walk']), pockets=len(D.pockets), parity=par, R=R, w=w,
               tA=tn(DA.whole, col), tB=tn(DBB.whole, col), tU_glued=tn(D.whole, cR), tU_final=tn(D.whole, c3),
               pocket_t_glued=max([tn(W, cR) or 0 for W in D.pockets]), tau_int_before=round(max(ic.tau_int(W, cR) for W in D.pockets), 3),
               hodge_after=round(max(ic.tau_hodge(W, c3) for W in D.pockets), 3), onelap_after=round(max(ic.tau_walk(W, c3) for W in D.pockets), 3))
    out.write(json.dumps(rec)+'\n'); out.flush()
# closing
a, b = nodes[0]['kids']; A, B = nodes[a]['S'], nodes[b]['S']
E = set((u, w) for u in range(g.n) for w in g.adj[u] if u < w); best = None
for p in PERMS:
    cc = {v: col[v] for v in A}; cc.update({v: p[col[v]] for v in B})
    K = set(x for (u, w) in E if cc[u] == cc[w] for x in (u, w)); best = min(best or (K, cc), (K, cc), key=lambda t: len(t[0]))
from wk import proper_repair
Rf = proper_repair(g, set(range(g.n)), E, best[1], best[0], 12)[0] if best[0] else 0
out.write(json.dumps(dict(final=True, R_final=Rf, sec=round(time.time()-t0)))+'\n'); print('done', name, Rf, round(time.time()-t0))
