"""WP14 check 2: census of hard states (no target within two swaps) on the discovery tables.

For every hard state h records:
  - sizes of the eight boundary-meeting components in the apex frame (Lemma 2 makes the boundary
    linkage of every locked state identical, so sizes / interior structure are the only data left);
  - target distance d(h) (3 or 4 on this domain) and which first-swap TYPES reach a non-hard state;
  - for d(h) = 4, which (type1, type2) two-swap macros reach a non-hard p=1 state;
  - whether h is stuck under (p,q), (p,lin) [no 2-macro endpoint with lower rank], using the
    complete endpoint lists in the table (cross-checked by recomputation).
"""
import json
from collections import Counter, defaultdict

from wp14_common import (RootState, all_components, comp_of, lock, ncol, pattern, setup, swap, tables, HERE)

NAMES = {0: "s0", 1: "A+", 2: "f1", 3: "f2", 4: "A-"}


def stype(B, i, K):
    hit = sorted(((B.index(v) - i) % 5) for v in K if v in B)
    return "{" + ",".join(NAMES[h] for h in hit) + "}" if hit else "interior"


def comp_sizes(adj, col, B, i):
    b = lambda k: B[(i + k) % 5]
    c = lambda v: col[v]
    out = {
        "XY(s0,f1)": comp_of(adj, col, b(0), c(b(0)), c(b(2))),
        "XZ(s0,f2)": comp_of(adj, col, b(0), c(b(0)), c(b(3))),
        "YZ(f1,f2)": comp_of(adj, col, b(2), c(b(2)), c(b(3))),
        "AX(A-,s0,A+)": comp_of(adj, col, b(0), c(b(0)), c(b(1))),
        "AY(A+,f1)": comp_of(adj, col, b(1), c(b(1)), c(b(2))),
        "AY(A-)": comp_of(adj, col, b(4), c(b(4)), c(b(2))),
        "AZ(A-,f2)": comp_of(adj, col, b(4), c(b(4)), c(b(3))),
        "AZ(A+)": comp_of(adj, col, b(1), c(b(1)), c(b(3))),
    }
    return {k: len(v) for k, v in out.items()}


def main():
    recs = []
    first_type_hist = Counter()
    pair_hist = Counter()
    per_graph = defaultdict(Counter)
    for name, d in tables():
        if not d["hard_states"]:
            continue
        rot, r, B, V, adj = setup(d)
        rs = RootState(rot, r)
        st = d["states"]
        idx = {tuple(s["coloring"]): k for k, s in enumerate(st)}
        hard = set(d["hard_states"])
        for h in d["hard_states"]:
            s = st[h]
            col = dict(zip(V, s["coloring"]))
            i, rho = pattern([col[v] for v in B])
            assert lock(adj, col, B)
            f0 = s["features"]
            # stuck under q / lin using the table's complete endpoint list
            eps = s["endpoints"]
            stuck = {}
            for feat in ("q", "lin", "L", "Lall", "links", "repMass"):
                stuck[feat] = not any(e["endpoint_p"] == 0 or e["endpoint_features"][feat] < f0[feat] for e in eps)
            # first swaps to non-hard states, and two-swap macros to non-hard states
            good1, good2 = Counter(), Counter()
            for pr, K in all_components(adj, col, V):
                c1 = swap(col, pr, K)
                t1 = stype(B, i, K)
                k1 = idx[tuple(_canon(c1[v] for v in V))]
                if k1 not in hard:
                    good1[t1] += 1
                    continue
                i1, _ = pattern([c1[v] for v in B])
                for pr2, K2 in all_components(adj, c1, V):
                    c2 = swap(c1, pr2, K2)
                    if ncol(c2, B) == 3:
                        raise AssertionError("hard state reached target in two swaps")
                    k2 = idx[tuple(_canon(c2[v] for v in V))]
                    if k2 not in hard:
                        good2[(t1, stype(B, i1, K2))] += 1
            dist = 3 if good1 else 4
            if dist == 4:
                assert good2, (name, h)
            for t in good1:
                first_type_hist[t] += 1
            for t in good2:
                pair_hist[t] += 1
            g = f"{d['graph']['order']}-{d['graph']['graph_index']}"
            per_graph[g]["hard"] += 1
            per_graph[g][f"d{dist}"] += 1
            for feat, v in stuck.items():
                per_graph[g][f"stuck_{feat}"] += v
            recs.append({"table": name, "state": h, "coloring": s["coloring"], "apex": B[i],
                         "apex_frame_boundary": [B[(i + k) % 5] for k in range(5)],
                         "features": f0, "component_sizes": comp_sizes(adj, col, B, i),
                         "interior_components": sum(1 for _, K in all_components(adj, col, V) if not (K & set(B))),
                         "target_distance": dist, "first_swap_types_to_nonhard": dict(good1),
                         "two_swap_types_to_nonhard": {f"{a}->{b}": v for (a, b), v in good2.items()} if dist == 4 else {},
                         "stuck": stuck})
    out = {"hard_states": len(recs), "per_graph": {k: dict(v) for k, v in sorted(per_graph.items())},
           "d3_first_swap_type_hist (states having >=1 such swap)": dict(first_type_hist.most_common()),
           "d4_two_swap_type_hist (states having >=1 such macro)": {f"{a}->{b}": v for (a, b), v in pair_hist.most_common()},
           "records": recs}
    (HERE / "hard_census.json").write_text(json.dumps(out, indent=1) + "\n")
    print(json.dumps({k: v for k, v in out.items() if k != "records"}, indent=1))


def _canon(xs):
    seen = {}
    return [seen.setdefault(x, len(seen)) for x in xs]


if __name__ == "__main__":
    main()
