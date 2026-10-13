"""Real planar near-rigid runs (sphere) in matching form.  INVARIANTS-1, Long Table, 13 Oct 2026.

Engine: TrackM tm_lib.Hole (primal 4-colourings of T - h, pi, Nch; read-only import), and TrackT
tt_lib.tait_dual (dual G5 with the primal edge of every dual edge).  Transport (TrackS S1/S3):
a DL state with link colours (alpha, mu, alpha, A, B) at x_j..x_{j+4} has Tait colouring
col(e) = c(u) xor c(w) on the dual of primal edge uw; M_t = colour-2 class = {col = alpha xor A},
whose v-edge is f_{j+2}.  NR run = maximal pi-run of DL states with Nch <= 9 (Census33 definition).
Output: one JSON line per run (graph, hole, primal rotation, dual edges, fv, prim, M_t list, Nch list),
re-checked against the matching-form successor rule of ax_lib.
Usage: planar_runs.py GRAPHS.txt HOLESPEC_FILE minlen out.jsonl
"""
import sys, os, json
sys.path.insert(0, os.path.expanduser('~/GraphColour/SolvingFrameworkPlan/docs/working/TrackM'))
sys.path.insert(0, os.path.expanduser('~/GraphColour/SolvingFrameworkPlan/docs/working/TrackT'))
from tm_lib import Hole
import tt_lib
from ax_lib import G5


def succ(g, M):
    d = g.dl(M)
    if d is None: return None
    k, lp = d
    Q = set(range(g.m)) - set(M)
    # unique PM of the figure-eight Q containing f_{k-2}
    f = g.fv[(k - 2) % 5]
    out = set()
    for key in ('X', 'Y'):
        s0, s1, verts, edges = lp[key]
        if key == 'X':
            # path X - v: edges[1:-1] alternate, starting with edges[1]
            out |= set(edges[1:-1:2])
        else:
            # Y: two alternating classes, each with one v-edge
            cls0 = set(edges[0::2]); cls1 = set(edges[1::2])
            out |= cls0 if f in cls0 else cls1
    return frozenset(out)


graphs = {}
for l in open(sys.argv[1]):
    p = l.split()
    if len(p) >= 3: graphs[p[0]] = [list(map(int, r.split(','))) for r in p[2].split(';')]
specs = [l.split()[0] for l in open(sys.argv[2]) if l.strip()]
minlen = int(sys.argv[3]); out = open(sys.argv[4], 'w')
for spec in specs:
    name, h = spec.rsplit(':', 1); h = int(h); rot = graphs[name]
    Hl = Hole(rot, h); sp = Hl.sp
    td = tt_lib.tait_dual(rot, h)
    g = G5(td.n, list(td.E), list(td.fv)); prim = td.prim
    dl = {x for x in range(Hl.S) if not Hl.filled[x] and Hl.phi[x] == 2}
    nr = {x for x in dl if Hl.Nch[x] <= 9}
    runs = []
    for x in nr:
        p = Hl.pinv[x]
        if p is not None and p in nr and Hl.pi[p] == x: continue
        r = [x]; y = Hl.pi[x]
        while y is not None and y in nr and y not in r: r.append(y); y = Hl.pi[y]
        if len(r) >= minlen: runs.append(r)
    for r in runs:
        Ms = []; ok = True
        for k in r:
            s = sp.states[k]; col = lambda u: s[sp.idx[u]]
            j = Hl.j[k]; c = [s[sp.linki[t]] for t in range(5)]
            want = c[j] ^ c[(j + 3) % 5]
            M = frozenset(e for e in range(g.m) if col(prim[e][0]) ^ col(prim[e][1]) == want)
            if g.fv[(j + 2) % 5] not in M or len(M) * 2 != g.n: ok = False
            Ms.append(M)
        # matching-form check: successor rule reproduces the run
        chk = all(succ(g, Ms[t]) == Ms[t + 1] for t in range(len(Ms) - 1))
        words = [g.ncomp(Ms[t - 1] | Ms[t]) for t in range(1, len(Ms))]
        rec = dict(name=name, hole=h, nprim=len(rot), rot=rot, n=g.n, E=g.E, fv=g.fv, prim=[list(p) for p in prim],
                   M=[sorted(M) for M in Ms], Nch=[Hl.Nch[k] for k in r], j=[Hl.j[k] for k in r],
                   word=words, transport_ok=ok, succ_ok=chk)
        out.write(json.dumps(rec) + '\n'); out.flush()
        print(name, h, 'len', len(r), 'Nch', rec['Nch'], 'word', words, 'transport', ok, 'succ', chk, flush=True)
