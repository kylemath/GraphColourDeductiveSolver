"""WP15 raw inquiry: rank-free Kempe distance to targets at each degree-5 root.
Quick-and-dirty exploratory code. Uses mass_core.RootState move lists (all bichromatic
components, including those missing B)."""
import sys, json, time
from collections import Counter, deque
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from mass_core import RootState, parse_ascii, degree_five, FIXTURES

INF = None

def bfs_targets(n, nbrs, targets):
    dist = {t: 0 for t in targets}
    dq = deque(targets)
    while dq:
        i = dq.popleft()
        for t in nbrs[i]:
            if t not in dist:
                dist[t] = dist[i] + 1
                dq.append(t)
    return dist

def classes(n, nbrs):
    comp = [-1] * n; k = 0
    for s in range(n):
        if comp[s] >= 0: continue
        comp[s] = k; st = [s]
        while st:
            i = st.pop()
            for t in nbrs[i]:
                if comp[t] < 0:
                    comp[t] = k; st.append(t)
        k += 1
    return comp, k

def analyse_root(rot, r):
    S = RootState(rot, r)
    N = len(S.C)
    Bset = S.Bset
    nb_all = [sorted({t for _, _, t in S.info[i]["moves"] if t != i}) for i in range(N)]
    # swaps of components meeting B only (component vertex list are original labels)
    Blab = set(rot[r])
    nb_B = [sorted({t for _, k, t in S.info[i]["moves"] if t != i and Blab & set(k)}) for i in range(N)]
    targets = [i for i in range(N) if S.info[i]["p"] == 0]
    nontarget = [i for i in range(N) if S.info[i]["p"] == 1]
    out = {"root": r, "nbr_degrees": [len(rot[v]) for v in rot[r]], "states": N,
           "targets": len(targets), "non_target": len(nontarget)}
    for name, nb in (("all", nb_all), ("Bonly", nb_B)):
        d = bfs_targets(N, nb, targets)
        dd = [d.get(i) for i in nontarget]
        unreach = sum(x is None for x in dd)
        fin = [x for x in dd if x is not None]
        out[name] = {"ecc": max(fin) if fin else 0, "unreachable": unreach,
                     "dist_hist": dict(sorted(Counter(fin).items())),
                     "mean": (sum(fin) / len(fin)) if fin else 0}
        if name == "all":
            comp, k = classes(N, nb)
            tcls = {comp[t] for t in targets}
            out[name]["kempe_classes"] = k
            out[name]["classes_with_target"] = len(tcls)
            out[name]["classes_without_target"] = k - len(tcls)
            out[name]["class_sizes"] = sorted(Counter(comp).values(), reverse=True)
            ecc = out[name]["ecc"]
            hard = [i for i in nontarget if d.get(i) == ecc and ecc >= 2][:3]
            out[name]["hard_examples"] = [{"vertex_order": S.V, "coloring": S.C[i],
                                           "boundary_colours": [S.C[i][S.pos[v]] for v in rot[r]],
                                           "q": S.info[i]["q"]} for i in hard]
            # q-descent comparison: is dist monotone with something? record (dist,q) pairs
            out[name]["dist_q_pairs"] = sorted(Counter((d.get(i), S.info[i]["q"]) for i in nontarget).items(), key=str)[:200]
    return out

def main(max_order=20, sample20=None):
    corpus = json.loads((FIXTURES / "mass-macro-results.json").read_text())
    res = []
    t0 = time.time()
    for o in corpus["orders"]:
        if o["order"] > max_order: continue
        gl = o["graphs_checked"]
        for g in gl:
            rot = parse_ascii(g["ascii"])
            fail = g.get("failing_roots") or []
            if isinstance(fail, str): fail = json.loads(fail)
            roots = [analyse_root(rot, r) for r in degree_five(rot)]
            res.append({"order": o["order"], "graph_index": int(g["graph_index"]), "ascii": g["ascii"],
                        "q_failing_roots": fail, "roots": roots})
            print(o["order"], g["graph_index"], "ecc", [x["all"]["ecc"] for x in roots],
                  "unr", sum(x["all"]["unreachable"] for x in roots), "fail", fail,
                  f"{time.time()-t0:.0f}s", flush=True)
    (HERE / "kempe-distance-results.json").write_text(json.dumps(res, indent=0))

if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 20)
