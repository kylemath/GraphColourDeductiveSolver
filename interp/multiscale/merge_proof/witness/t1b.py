# Interior tilt profile for odd (3-vortex) two-vortex-cap merges: tau of the sub-disc boundary at depth d from dU
# in the glued+repaired colouring, against w.  Usage: python t1b.py map kmin kmax seed ntrial
import sys, json, time, random
sys.path.insert(0, '/mnt/project-files/multiscale/merge_proof/witness')
from w2 import *
name, kmin, kmax, seed, ntrial = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5])
g = G(make(name)); rng = random.Random(seed); n = g.n
deg5 = [v for v in range(n) if g.deg[v] % 2 == 1]
log = open('/mnt/project-files/multiscale/merge_proof/witness/t1b_%s_s%d.jsonl' % (name, seed), 'a')
for k in range(kmin, kmax+1):
    for trial in range(ntrial):
        o1 = rng.choice(deg5); d1 = bfs(g.adj, o1, 40)
        d, o2 = sorted((d, o) for o, d in d1.items() if o != o1 and o in deg5)[0]
        path = [o2]
        while path[-1] != o1: path.append(min((w for w in g.adj[path[-1]] if w in d1), key=lambda w: d1[w]))
        mid = path[len(path)//2]; rA = d//2 + k; A = ball(g, mid, rA)
        dm = bfs(g.adj, mid, 3*rA); far = [v for v in dm if dm[v] == 2*rA+1]
        if not far: continue
        B = ball(g, rng.choice(far), rA) - A
        if any(check(g, S)[0] == 'nodisc' for S in (A, B, A | B)): continue
        D = Disc(g, A | B); dB = multi_bfs(g.adj, list(D.bset), D.S)
        odd = [v for v in D.S if g.deg[v] % 2 and v not in D.bset]
        if len(odd) % 2 == 0: continue
        cA = level_cols(g, A, 1, 'nonzero', seed0=11*seed+k, budget=3*10**7); cB = level_cols(g, B, 2, None, seed0=11*seed+k+5, budget=3*10**7)
        for ca in cA:
            for cb in cB:
                rec = merge_all24(g, D, A, B, ca, cb, Rmax=5, wmax=8)
                # glued+repaired colouring (same renaming order as merge_all24)
                seam = [(u, w) for (u, w) in D.edges if (u in A) != (w in A)]; data = []
                for p in PERMS:
                    cc = {v: ca[v] for v in A}; cc.update({v: p[cb[v]] for v in B})
                    K = set(x for e in seam if cc[e[0]] == cc[e[1]] for x in e); data.append((len(K), p, cc, K))
                data.sort(key=lambda t: t[0])
                for nk, p, cc, K in data:
                    r, c2 = (0, cc) if not K else proper_repair_at(g, D.S, cc, K, rec['R'])
                    if r is not None: break
                prof = []
                for dd in range(0, 8):
                    Ud = set(v for v in D.S if dB[v] > dd)
                    st = check(g, Ud)[0]
                    if st == 'nodisc': prof.append(None); continue
                    Dd = Disc(g, Ud); prof.append(round(tau_star(Dd.whole, c2), 3))
                # same for the two sides separately (depth from dA inside A, from dB inside B)
                def side(S):
                    dS = multi_bfs(g.adj, list(Disc(g, S).bset), S); out = []
                    for dd in range(0, 8):
                        Sd = set(v for v in S if dS[v] > dd)
                        if check(g, Sd)[0] == 'nodisc': out.append(None); continue
                        out.append(round(tau_star(Disc(g, Sd).whole, c2), 3))
                    return out
                rec.update(map=name, k=k, nodd=len(odd), depths=sorted(dB[o] for o in odd), tau_depth_U=prof, tau_depth_A=side(A), tau_depth_B=side(B))
                log.write(json.dumps(rec)+'\n'); log.flush()
                print({kk: rec.get(kk) for kk in ('k', 'nodd', 'depths', 'tA', 'tB', 'R', 'w', 'ptau_before', 'tau_depth_U', 'tau_depth_A', 'tau_depth_B')}, flush=True)
