"""V3 = R0 + NRC word 1212 (M_{2j} u M_{2j+1} Hamiltonian, M_{2j+1} u M_{2j+2} exactly 2 components), no DL,
no planarity: SAT + lazy word cuts (as sat_t1v.Enc.check, word part only).  Enumerates all labelled graphs
(chord set + labels f1 f3 f4) carrying a closed V3 sequence of length L, and prints their TrackU lines.
Validated against r0enum.py at n = 16 (V3 with L in V3_L).  usage: v3sat.py n L [tlimit]"""
import sys, time, json
sys.path.insert(0, '../proof')
from sat_t1v import Enc
from pysat.solvers import Cadical153

n, L = int(sys.argv[1]), int(sys.argv[2]); tl = float(sys.argv[3]) if len(sys.argv) > 3 else 550
enc = Enc(n, L, 0, eager=0, closed=True)
s = Cadical153(bootstrap_with=enc.cl)
t0 = time.time(); nsol = 0; ncuts = 0; status = 'DONE'


def comps_of(U, adj_edges):
    seen = set(); out = []
    for x0 in range(n):
        if x0 in seen: continue
        cyc = []; x = x0; e = None
        while True:
            seen.add(x)
            e = [g for g in adj_edges[x] if g in U and g != e][0]
            cyc.append(e); x = enc.other(e, x)
            if x == x0: break
        out.append(cyc)
    return out


while True:
    if time.time() - t0 > tl: status = 'TIMEOUT'; break
    if not s.solve(): break
    E, M, fv = enc.decode(s.get_model())
    adjE = [[] for _ in range(n)]
    for e in E:
        a, b = enc.edges[e]; adjE[a].append(e); adjE[b].append(e)
    cuts = []
    for t in range(L):
        tp = (t - 1) % L; U = M[tp] | M[t]
        comps = comps_of(U, adjE); want = 1 if t % 2 == 1 else 2
        lit = lambda e: -enc.Y[tp, e] if e in M[tp] else -enc.Y[t, e]
        if len(comps) > want:
            comps.sort(key=len); cuts.append([lit(e) for cyc in comps[:want + 1] for e in cyc])
        elif len(comps) < want:
            cuts.append([lit(e) for e in comps[0]])
    if cuts:
        for c in cuts: s.add_clause(c)
        ncuts += len(cuts); continue
    nsol += 1
    idx = {e: i for i, e in enumerate(E)}
    print(' '.join(map(str, [n, len(E)] + [x for e in E for x in enc.edges[e]] + [idx[f] for f in fv])), flush=True)
    s.add_clause([-enc.X[e] for e in E if enc.X[e] is not None] + [-enc.lab[x][fv[x]] for x in (1, 3, 4)])
print(json.dumps(dict(n=n, L=L, nsol=nsol, cuts=ncuts, status=status, sec=round(time.time() - t0, 1))), file=sys.stderr)
