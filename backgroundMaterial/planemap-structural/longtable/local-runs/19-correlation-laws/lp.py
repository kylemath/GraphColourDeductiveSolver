"""[exploratory] Item 19 task 3: LP bound implied by the valid families.
Per degree: variables f_sigma (per filled sequence, one per dihedral orbit), u_tau (per unfilled sequence, one per orbit); by symmetry (averaging over D_d)
an optimum is constant on orbits. maximise r = U/F = sum |tau| u_tau  s.t. sum |sigma| f_sigma <= 1 and u_tau <= sum_{t in S} f_orb(t) for every
minimal valid S of every unfilled orbit tau. Then the implied floor is F/(F+U) >= 1/(1+r).
usage: lp.py TAG"""
import json, sys
from fractions import Fraction as Fr
import lib, simplex
tag = sys.argv[1]; L = json.load(open("laws-%s.json" % tag)); summary = {}
for d in (5, 6, 7):
    D = lib.Deg(d); fo = [k for k, o in enumerate(D.orbits) if lib.is_filled(D.seqs[o[0]])]; uo = [k for k, o in enumerate(D.orbits) if not lib.is_filled(D.seqs[o[0]])]
    nv = len(fo) + len(uo); A = []; b = []
    A.append([len(D.orbits[k]) for k in fo] + [0] * len(uo)); b.append(1)
    for o in L[str(d)]["orbits"]:
        tau = uo[[ "".join(map(str, D.seqs[D.orbits[k][0]])) for k in uo].index(o["rep"])]
        rows = set()
        for S in o["minimal_valid_S"]:
            row = [0] * len(fo)
            for w in S: row[fo.index(D.orbit_of[D.idx[tuple(int(c) for c in w)]])] += 1
            rows.add(tuple(row))
        rows = [r for r in rows if not any(q != r and all(x <= y for x, y in zip(q, r)) for q in rows)]  # keep dominance-minimal
        for r in rows:
            row = [-x for x in r] + [0] * len(uo); row[len(fo) + uo.index(tau)] = 1; A.append(row); b.append(0)
    c = [0] * len(fo) + [len(D.orbits[k]) for k in uo]
    val, x = simplex.maximise(c, A, b)
    if val is None: summary[d] = {"floor": None, "note": "LP unbounded: some unfilled orbit has no valid family within the search size"}; print(d, summary[d]); continue
    fl = 1 / (1 + val)
    summary[d] = {"r_max": str(val), "implied_floor": str(fl), "implied_floor_float": float(fl), "n_lp_rows": len(A),
                  "f": {"".join(map(str, D.seqs[D.orbits[k][0]])): str(x[i]) for i, k in enumerate(fo)},
                  "u": {"".join(map(str, D.seqs[D.orbits[k][0]])): str(x[len(fo) + i]) for i, k in enumerate(uo)}}
    print(d, "implied floor", fl, float(fl), "rows", len(A), flush=True)
json.dump(summary, open("lp-%s.json" % tag, "w"), indent=1)
