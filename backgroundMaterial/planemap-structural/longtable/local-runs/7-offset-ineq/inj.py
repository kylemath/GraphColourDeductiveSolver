#!/usr/bin/env python3
"""[exploratory] Item 7 (3): the single-vertex swap maps behind the valid inequalities.
For an unfilled state s with repeat at {j, j+2} (alpha), m = x_{j+1} (mu), a = x_{j+3} (A), b = x_{j+4} (B):
  phi_a(s) = swap the {mu, A}-component of a   (defined when lock 1 fails, i.e. a not in the {mu,A}-component of m);
             the link becomes alpha mu alpha mu B, so the image is filled with the singleton at j+4 (offset 4);
  phi_b(s) = swap the {mu, B}-component of b   (defined when lock 2 fails); image filled, singleton at j+3 (offset 3).
phi(s) = phi_a(s) if lock 1 fails, else phi_b(s). Checked per class: the image is filled with the predicted singleton,
lies in the class, and phi is injective on the non-DL states of U_j into F_{j+3} + F_{j+4} (for each j).
Also: the 4-block floor classes, whether the DL block (repeat {i+1, i+4}, i = singleton position) reaches the filled block
in 2 swaps, and the number of distinct filled states so reached (a 2-swap injection would need >= |DL| of them).
usage: inj.py --orders 12 ... 20       (every degree-5 hole)   |   inj.py --floor ../6-quarter-floor/blocks-deg5.jsonl"""
import json, os, sys
from collections import Counter
H = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(H, "..", "common"))
from kempe_py import Space, gentri_rotation, adj_from_rot
from multiprocessing import Pool
GENTRI = os.path.join(H, "..", "..", "..", "studiointel", "gentri")


def check(task):
    n, gi, line, v, floor = task
    rot = gentri_rotation(line); adj = adj_from_rot(rot); S = Space(adj, v, link=rot[v]); S.build_graph(); cl, ncl = S.classes()
    L = S.linki; out = Counter(); filled = [S.filled(k) for k in range(len(S.states))]
    img = {}
    for s in range(len(S.states)):
        if filled[s]: continue
        c = S.states[s]; lc = [c[i] for i in L]; j = [j for j in range(5) if lc[j] == lc[(j + 2) % 5]][0]
        m, a, b = L[(j + 1) % 5], L[(j + 3) % 5], L[(j + 4) % 5]; cm = S.cmasks(c); mu = c[m]
        Ka = S.flood(1 << a, cm[mu] | cm[c[a]]); Kb = S.flood(1 << b, cm[mu] | cm[c[b]])
        l1, l2 = bool(Ka >> m & 1), bool(Kb >> m & 1)
        if l1 and l2: out["DL"] += 1; continue
        if not l1: t = S.index[S.swap(c, Ka, mu, c[a])]; want = (j + 4) % 5; out["phi_a"] += 1
        else: t = S.index[S.swap(c, Kb, mu, c[b])]; want = (j + 3) % 5; out["phi_b"] += 1
        tl = [S.states[t][i] for i in L]
        sing = [i for i in range(5) if tl.count(tl[i]) == 1]
        ok = filled[t] and sing == [want] and cl[t] == cl[s]
        out["image_ok" if ok else "image_BAD"] += 1
        key = (j, t)
        if key in img: out["collision"] += 1
        img[key] = s
    out["nonDL_states"] = out["phi_a"] + out["phi_b"]; res = {"order": n, "gentri_index": gi, "hole": v, **out}
    if floor:
        # DL block of each 1/4 class: 2-swap reach into the filled block
        for k in range(ncl):
            C = [s for s in range(len(S.states)) if cl[s] == k]; F = [s for s in C if filled[s]]
            if 4 * len(F) != len(C): continue
            DL = [s for s in C if not filled[s] and not any(filled[t] for t in S.G[s])]
            reach = set(); every = True
            for s in DL:
                r = {u for t in S.G[s] for u in S.G[t] if filled[u]}; reach |= r; every &= bool(r)
            res.setdefault("floor_classes", []).append({"size": len(C), "F": len(F), "DL": len(DL), "every_DL_fills_in_2": every,
                                                       "distinct_filled_reached_in_2_from_DL": len(reach)})
    return res


if __name__ == "__main__":
    tasks = []
    if "--floor" in sys.argv:
        seen = set(); lines = {}
        for l in open(sys.argv[sys.argv.index("--floor") + 1]):
            r = json.loads(l)
            if "summary" in r: continue
            key = (r["order"], r["gentri_index"], r["hole"])
            if key in seen: continue
            seen.add(key)
            if r["order"] not in lines: lines[r["order"]] = [x for x in open(os.path.join(GENTRI, "tri%d.txt" % r["order"])) if x.strip()]
            tasks.append((*key[:2], lines[r["order"]][r["gentri_index"]], r["hole"], True))
    else:
        for n in [int(x) for x in sys.argv[sys.argv.index("--orders") + 1:]]:
            for gi, l in enumerate(x for x in open(os.path.join(GENTRI, "tri%d.txt" % n)) if x.strip()):
                rot = gentri_rotation(l); tasks += [(n, gi, l, v, False) for v in range(len(rot)) if len(rot[v]) == 5]
    tot = Counter(); fl = Counter()
    with Pool(6) as pool:
        for r in pool.imap(check, tasks, chunksize=2):
            print(json.dumps(r), flush=True)
            for k, v in r.items():
                if isinstance(v, int) and k not in ("order", "gentri_index", "hole"): tot[k] += v
            for f in r.get("floor_classes", []):
                fl["classes"] += 1; fl["every_DL_fills_in_2"] += f["every_DL_fills_in_2"]; fl["reach_ge_DL"] += f["distinct_filled_reached_in_2_from_DL"] >= f["DL"]
    print(json.dumps({"summary": True, "holes": len(tasks), **tot, "floor": dict(fl)}))
