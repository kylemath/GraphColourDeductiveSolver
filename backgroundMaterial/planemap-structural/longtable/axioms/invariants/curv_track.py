"""Curvature carried by colour classes along sphere NR runs (primal, Kempe-chain level).
Identity [hand, checked here]: in T - h (V' vertices, deg' = degree in T - h), if every pair graph
ab is a forest with c_ab components, then for every colour a
        4 n_a = V' + kappa_a - c_a,   kappa_a = sum_{v in a} (6 - deg' v),  c_a = sum_{b != a} c_ab
(and in general 4 n_a = V' + kappa_a - c_a + sum_b beta_ab, beta = cycle rank).  Colours are tracked
ABSOLUTELY through the pi swaps (K_{alpha A}(x_{j+2}) swapped, then canonical renaming undone).
Usage: curv_track.py GRAPHS HOLESPEC minlen out.jsonl"""
import sys, os, json
sys.path.insert(0, os.path.expanduser('~/GraphColour/SolvingFrameworkPlan/docs/working/TrackM'))
from tm_lib import Hole

graphs = {}
for l in open(sys.argv[1]):
    p = l.split()
    if len(p) >= 3: graphs[p[0]] = [list(map(int, r.split(','))) for r in p[2].split(';')]
specs = [l.split()[0] for l in open(sys.argv[2]) if l.strip()]
minlen = int(sys.argv[3]); out = open(sys.argv[4], 'w')
bad = 0
for spec in specs:
    name, h = spec.rsplit(':', 1); h = int(h); rot = graphs[name]
    Hl = Hole(rot, h); sp = Hl.sp; li = sp.linki; N = sp.N
    degp = [len(rot[sp.order[i]]) - (1 if h in rot[sp.order[i]] else 0) for i in range(N)]
    dl = {x for x in range(Hl.S) if not Hl.filled[x] and Hl.phi[x] == 2}
    nr = {x for x in dl if Hl.Nch[x] <= 9}
    for x in sorted(nr):
        p = Hl.pinv[x]
        if p is not None and p in nr and Hl.pi[p] == x: continue
        r = [x]; y = Hl.pi[x]
        while y is not None and y in nr and y not in r: r.append(y); y = Hl.pi[y]
        if len(r) < minlen: continue
        # absolute colouring: start with the canonical colouring of r[0]; then apply swaps
        cur = list(sp.states[r[0]]); rows = []
        for idx, k in enumerate(r):
            assert sp.index[sp.canon(cur)] == k
            cm = [0, 0, 0, 0]
            for i, c in enumerate(cur): cm[c] |= 1 << i
            xs = [li[(Hl.j[k] + t) % 5] for t in range(5)]
            al, mu, A, B = cur[xs[0]], cur[xs[1]], cur[xs[3]], cur[xs[4]]
            role = {al: 'a', mu: 'm', A: 'A', B: 'B'}
            n = [bin(cm[c]).count('1') for c in range(4)]
            kap = [sum(6 - degp[i] for i in range(N) if cur[i] == c) for c in range(4)]
            cc = [[0] * 4 for _ in range(4)]; beta = [[0] * 4 for _ in range(4)]
            for a in range(4):
                for b in range(a + 1, 4):
                    comps = sp.components(cur, a, b, cm)
                    m = bin(cm[a] | cm[b]).count('1')
                    # edges of the ab pair graph
                    e = sum(1 for i in range(N) if cur[i] in (a, b) for jx in range(N) if jx > i and cur[jx] in (a, b) and cur[jx] != cur[i] and (sp.nbm[i] >> jx & 1))
                    cc[a][b] = cc[b][a] = len(comps); beta[a][b] = beta[b][a] = e - m + len(comps)
            ca = [sum(cc[a][b] for b in range(4) if b != a) for a in range(4)]
            ba = [sum(beta[a][b] for b in range(4) if b != a) for a in range(4)]
            ok = all(4 * n[a] == N + kap[a] - ca[a] + ba[a] for a in range(4))
            bad += not ok
            K = sp.flood(1 << xs[2], cm[al] | cm[A])
            dk = sum(6 - degp[i] for i in range(N) if K >> i & 1 and cur[i] == A) - sum(6 - degp[i] for i in range(N) if K >> i & 1 and cur[i] == al)
            rows.append(dict(state=k, role=[role[c] for c in range(4)], n=n, kappa=kap, c=ca, beta=ba, identity=ok,
                             swap=(al, A), dkappa_alpha=dk, K=bin(K).count('1')))
            # pi: swap alpha <-> A on K
            nxt = list(cur)
            for i in range(N):
                if K >> i & 1: nxt[i] = A if cur[i] == al else al
            cur = nxt
            if idx + 1 < len(r) and sp.index[sp.canon(cur)] != r[idx + 1]:
                rows[-1]['pi_mismatch'] = True
        out.write(json.dumps(dict(name=name, hole=h, R=len(r), rows=rows)) + '\n'); out.flush()
print('identity failures', bad)
