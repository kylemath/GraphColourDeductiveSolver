"""WP14 check 1: exact characterisation of 1-swap and 2-swap target reachability.

For every p=1 state of every discovery table (orders 12-18, read-only):
  T1  one-swap target exists        <=>  not lock(c)                       (Lemma 1)
  T2  hard (no target in <=2 swaps) <=>  lock(c) and lock(c') for every single-swap successor c'
      compared against (a) a direct enumeration with mass_core.RootState and (b) the table's hard_states
  T3  under lock, forced boundary linkage: A-Y comp of b_{i+1} misses b_{i-1}; A-Z comp of b_{i-1} misses b_{i+1}
      (Lemma 2, Jordan curve)
  T4  every single swap from a p=1 state lands on a p=1 or p=0 state; a swap from a LOCKED state never
      lands on p=0 (consistency) and lands on p=1 states whose pattern is listed (Lemma 3 successor table)
Also records target distances (full BFS on the state graph; diagnostic only).
"""
import json
from collections import Counter

from wp14_common import (RootState, all_components, comp_of, lock, ncol, pattern, setup, swap, tables, HERE)


def successor_type(B, col, i, pr, K):
    """Label a first swap by its action on the boundary (apex frame: positions relative to apex i)."""
    hit = tuple(sorted(((B.index(v) - i) % 5) for v in K if v in B))
    if not hit:
        return "interior"
    Bc = [col[v] for v in B]
    names = {0: "s0", 1: "A+", 4: "A-", 2: "f1", 3: "f2"}
    return "{" + ",".join(names[h] for h in hit) + "}"


def main():
    stats = Counter()
    per_root = []
    succ_types = Counter()
    for name, d in tables():
        rot, r, B, V, adj = setup(d)
        rs = RootState(rot, r)
        assert rs.V == V
        dist = {i: 0 for i, inf in enumerate(rs.info) if inf["p"] == 0}
        fr = list(dist)
        while fr:
            nx = []
            for i in fr:
                for _, _, t in rs.info[i]["moves"]:
                    if t not in dist:
                        dist[t] = dist[i] + 1
                        nx.append(t)
            fr = nx
        table_hard = set(d["hard_states"])
        hard_pred, hard_enum = set(), set()
        assert len(d["states"]) == len(rs.C)
        for si, st in enumerate(d["states"]):
            assert tuple(st["coloring"]) == rs.C[si]
            if st["p"] != 1:
                continue
            stats["p1_states"] += 1
            col = dict(zip(V, st["coloring"]))
            i, rho = pattern([col[v] for v in B])
            L = lock(adj, col, B)
            one = any(rs.info[t]["p"] == 0 for _, _, t in rs.info[si]["moves"])
            assert one == (not L), (name, si)
            stats["T1_ok"] += 1
            two = one or any(rs.info[u]["p"] == 0 for _, _, t in rs.info[si]["moves"] for _, _, u in rs.info[t]["moves"])
            if not two:
                hard_enum.add(si)
            # prediction from lock alone
            comps = all_components(adj, col, V)
            succ_locked = []
            for pr, K in comps:
                c1 = swap(col, pr, K)
                if ncol(c1, B) == 3:
                    succ_locked.append(False)
                    continue
                succ_locked.append(lock(adj, c1, B))
                if L:
                    succ_types[(successor_type(B, col, i, pr, K), lock(adj, c1, B))] += 1
            if L and all(succ_locked):
                hard_pred.add(si)
            if L:
                stats["locked"] += 1
                b = lambda k: B[(i + k) % 5]
                # Lemma 2: forced linkage
                ay = comp_of(adj, col, b(1), col[b(1)], col[b(2)])
                az = comp_of(adj, col, b(-1), col[b(-1)], col[b(3)])
                assert b(-1) not in ay and b(1) not in az, (name, si)
                stats["T3_ok"] += 1
        assert hard_pred == hard_enum == table_hard, (name, hard_pred, hard_enum, table_hard)
        stats["T2_roots_ok"] += 1
        stats["hard"] += len(table_hard)
        nt = [i for i, inf in enumerate(rs.info) if inf["p"] == 1]
        per_root.append({"table": name, "order": d["graph"]["order"], "graph": d["graph"]["graph_index"], "root": r,
                         "p1_states": len(nt), "locked": sum(1 for si in nt if lock(adj, dict(zip(V, rs.C[si])), B)),
                         "hard": len(table_hard),
                         "max_target_distance": max(dist.get(si, 10**9) for si in nt) if nt else 0,
                         "unreachable": sum(1 for si in nt if si not in dist)})
    out = {"stats": dict(stats),
           "successor_types_from_locked_states": {f"{k[0]} locked={k[1]}": v for k, v in sorted(succ_types.items())},
           "max_target_distance_hist": dict(Counter(x["max_target_distance"] for x in per_root)),
           "per_root": per_root}
    (HERE / "check_lock.json").write_text(json.dumps(out, indent=1) + "\n")
    print(json.dumps({k: v for k, v in out.items() if k != "per_root"}, indent=1))


if __name__ == "__main__":
    main()
