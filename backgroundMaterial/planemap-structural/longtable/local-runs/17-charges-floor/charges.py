#!/usr/bin/env python3
"""[exploratory] Item 17: Heawood charges on the filled / unfilled states of the degree-5 Kempe classes (see README.md).
usage: charges.py --orders 12 14 16 ... 20 [--floor-holes]  [--workers 2] > out.jsonl
  --floor-holes : instead of all holes, only the degree-5 holes that contain a 1/4 class (from ../6-quarter-floor/quarter-classes.jsonl), orders given.
One output line per (hole, class) with per-state records.

Conventions
- Faces come from the planar-code rotation: face (v, w, w') for consecutive neighbours w, w' of v; each face is found 3 times and
  checked to have the same cyclic orientation each time (asserted). Colours 0..3 = tetrahedron corners C0..C3 (1,1,1),(1,-1,-1),(-1,1,-1),(-1,-1,1).
  Face sign +1 iff (C[col a], C[col b], C[col c]) is outward-oriented, for the face (a,b,c) in the orientation just fixed.
  Reversing the orientation of the whole map (mirror) flips every sign.
- GAUGE: a state is a colouring up to renaming; its CANONICAL labelling is by first occurrence along Space.order (kempe_py.py).
  Every charge below is computed in the canonical labelling. An odd renaming flips every sign, so odd statistics (q(v), q(m), ...) are gauge dependent;
  products of two charges, squares, |.| and sign(q(v))*q(u) are gauge-free.
- link position k = k-th vertex of rot[hole] (rotation order). q(.) of a link vertex of an UNFILLED state is the partial charge in G = T - v (faces of G only).
- filled state: singleton colour at position i; capped by the missing colour; q(.) then the full charge in T; deg = sum q / 12.
- GAUGE FIXING (gauge-free charges Q = eps * q): filled eps = TS(missing, singleton, x_{i+1}) = sign q(v) (asserted); unfilled eps = TS(A, B, alpha) with alpha = colour x_j = x_{j+2}, A = x_{j+3}, B = x_{j+4}.
  If lock 1 fails, the swap of the {mu,A}-component of a gives a filled state with missing colour A, singleton B, x_{i+1} = alpha, so eps_F = TS(A,B,alpha) = eps_U: the labelled colouring along that move keeps the same eps.
- unfilled state: unique repeated colour at positions j, j+2; m = x_{j+1}, a = x_{j+3}, b = x_{j+4}. DL = unfilled with no filled state one move away.
"""
import json, os, sys, itertools, math
from collections import Counter
from multiprocessing import Pool
H = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(H, "..", "common"))
from kempe_py import Space, gentri_rotation, adj_from_rot
GENTRI = os.path.join(H, "..", "..", "..", "studiointel", "gentri")
s3 = 1 / math.sqrt(3)
CORN = [(s3, s3, s3), (s3, -s3, -s3), (-s3, s3, -s3), (-s3, -s3, s3)]
def tsign(a, b, c):
    A, B, C = CORN[a], CORN[b], CORN[c]
    u = [B[k] - A[k] for k in range(3)]; w = [C[k] - A[k] for k in range(3)]
    nr = [u[1]*w[2]-u[2]*w[1], u[2]*w[0]-u[0]*w[2], u[0]*w[1]-u[1]*w[0]]
    return 1 if sum(nr[k] * (A[k] + B[k] + C[k]) for k in range(3)) > 0 else -1
TS = {t: tsign(*t) for t in itertools.permutations(range(4), 3)}

def faces_of(rot):
    seen = {}
    for v, nb in enumerate(rot):
        d = len(nb)
        for k in range(d):
            f = (v, nb[k], nb[(k + 1) % d])
            r = min(range(3), key=lambda t: f[t]); g = f[r:] + f[:r]
            seen.setdefault(frozenset(f), set()).add(g)
    out = []
    for key, gs in seen.items():
        assert len(gs) == 1, "inconsistent orientation"
        out.append(next(iter(gs)))
    return out

def work(task):
    n, gi, line, hole = task
    rot = gentri_rotation(line); adj = adj_from_rot(rot); link = list(rot[hole])
    F = faces_of(rot)
    assert len(F) == 2 * len(rot) - 4
    S = Space(adj, hole, link=link); S.build_graph(); cl, ncl = S.classes()
    N = len(S.states); idx = S.idx
    filled = [S.filled(k) for k in range(N)]
    nearf = [filled[s] or any(filled[t] for t in S.G[s]) for s in range(N)]
    Gf = [tuple(idx[x] for x in f) for f in F if hole not in f]
    Hf = [f for f in F if hole in f]
    linkidx = [idx[x] for x in link]
    # position of link vertex in link
    faces_at_link = [[f for f in Gf if li in f] for li in linkidx]
    res = []
    for c in range(ncl):
        C = [s for s in range(N) if cl[s] == c]
        recs = []
        for s in C:
            col = S.states[s]
            q = [0] * (len(S.order)); W = 0
            for f in Gf:
                sg = TS[(col[f[0]], col[f[1]], col[f[2]])]; W += sg
                for x in f: q[x] += sg
            qL = [q[li] for li in linkidx]
            lc = [col[li] for li in linkidx]
            # faces of G touching link: number of positive / negative
            touch = {f for fl in faces_at_link for f in fl}
            pos = sum(1 for f in touch if TS[(col[f[0]], col[f[1]], col[f[2]])] > 0)
            r = {"qL": qL, "W": W, "lc": lc, "pos": pos, "ntouch": len(touch)}
            if filled[s]:
                miss = [k for k in range(4) if k not in set(lc)][0]
                cnt = Counter(lc); i = [k for k in range(5) if cnt[lc[k]] == 1]; assert len(i) == 1
                qf = q[:]; qv = 0
                for f in Hf:
                    t = tuple(miss if x == hole else col[idx[x]] for x in f)
                    sg = TS[t]; qv += sg
                    for x in f:
                        if x != hole: qf[idx[x]] += sg
                assert abs(qv) == 3, qv
                tot = sum(qf) + qv; assert tot % 12 == 0
                assert all(x % 3 == 0 for x in qf), "q not 0 mod 3"
                ii = i[0]
                eps = TS[(miss, lc[ii], lc[(ii + 1) % 5])]
                assert eps == (1 if qv > 0 else -1), "sigma != eps_F"
                r.update({"t": "F", "k": ii, "qv": qv, "deg": tot // 12, "qLfull": [qf[li] for li in linkidx], "miss": miss, "eps": eps})
            else:
                rep = [j for j in range(5) if lc[j] == lc[(j + 2) % 5]]; assert len(rep) == 1
                j = rep[0]; m, a, b = (j + 1) % 5, (j + 3) % 5, (j + 4) % 5
                eps = TS[(lc[a], lc[b], lc[j])]   # triangle (A, B, alpha) = (x_{j+3}, x_{j+4}, x_j); matches eps_F of the filled state after the swap of the {mu,A}-component of a
                r.update({"t": "U" if nearf[s] else "D", "k": j, "eps": eps})
            recs.append(r)
        res.append({"order": n, "gentri_index": gi, "hole": hole, "size": len(C), "nF": sum(1 for r in recs if r["t"] == "F"), "ldeg": [len(rot[x]) for x in link], "states": recs})
    return res

def args(flag):
    i = sys.argv.index(flag) + 1; out = []
    while i < len(sys.argv) and not sys.argv[i].startswith("--"): out.append(int(sys.argv[i])); i += 1
    return out

def main():
    orders = args("--orders"); wk = args("--workers")[0] if "--workers" in sys.argv else 2
    lines = {n: [x for x in open(os.path.join(GENTRI, "tri%d.txt" % n)) if x.strip()] for n in orders}
    tasks = []
    if "--floor-holes" in sys.argv:
        seen = set()
        for l in open(os.path.join(H, "..", "6-quarter-floor", "quarter-classes.jsonl")):
            r = json.loads(l)
            if r["deg"] == 5 and r["order"] in orders and (r["order"], r["gentri_index"], r["hole"]) not in seen:
                seen.add((r["order"], r["gentri_index"], r["hole"])); tasks.append((r["order"], r["gentri_index"], lines[r["order"]][r["gentri_index"]], r["hole"]))
    else:
        for n in orders:
            for gi, l in enumerate(lines[n]):
                rot = gentri_rotation(l)
                for v in range(len(rot)):
                    if len(rot[v]) == 5: tasks.append((n, gi, l, v))
    with Pool(wk) as pool:
        for res in pool.imap(work, tasks, chunksize=4):
            for r in res: print(json.dumps(r), flush=True)

if __name__ == "__main__":
    main()
