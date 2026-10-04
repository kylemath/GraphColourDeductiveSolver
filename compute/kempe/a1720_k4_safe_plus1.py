"""
a1720_k4_safe_plus1.py -- Agent 1720, group K4 (M-Kempe, Track 1).

For every cached triangulation G on n vertices, every vertex v with
deg v in {4,5}, and every proper 5-colouring c of G with c(v)=5, compute

  d(c)   BFS distance in R(G-v,5) from c|_{G-v} to a colouring of G-v using
         at most four colours (same target as ``bfs_reduce_to_4``);
  s1(c)  least length of a K1-safe path in R(G-v,5) to such a colouring
         (K1-safe as in backgroundMaterial/agent1701/groups/K3_weaker_spec.md §1,
         i.e. no step has ``is_unsafe`` in ``classify_path_safety``);
  d2(c), s2(c)  the same two quantities for the stronger target T2: a colouring
         c' of G-v with |c'(G-v)| <= 4 and some colour x not in c'(N(v)) with
         |c'(G-v) u {x}| <= 4, i.e. c' extends to a proper 4-colouring of G by
         recolouring v alone;
  dG(c)  BFS distance in R(G,5) from c to a colouring of G using <= 4 colours;
  t3(c)  least length of a path in R(G,5) from c to a colouring of G using
         <= 4 colours in which every swapped G-chain K satisfies: K - {v} is
         empty or is a single Kempe chain of G-v (the swap lifts without merging
         chains of G-v through v; v's colour is tracked, not frozen at 5).

Symmetry reduction: all computations are done on orbits of colourings under
permutations of colours 1..4 (colour 5 fixed).  Kempe swaps are equivariant,
the K1 predicate only refers to colour 5 and to pairs (a,5) with a ranging over
1..4, and all targets are invariant, so every distance above is constant on an
orbit.  ``--verify`` re-checks this against ``classify_path_safety`` and
``all_kempe_neighbours`` without any quotient for small n.

Usage:
  .venv/bin/python compute/kempe/a1720_k4_safe_plus1.py --nmin 6 --nmax 10
  .venv/bin/python compute/kempe/a1720_k4_safe_plus1.py --verify 7
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from collections import Counter, deque
from itertools import combinations
from multiprocessing import Pool
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple

ROOT = Path(__file__).resolve().parents[2]
CACHE = ROOT / "compute" / "data" / "triangulations_n4_11.json"
OUT = ROOT / "backgroundMaterial" / "agent1720" / "groups" / "K4_results.json"
PAIRS: List[Tuple[int, int]] = list(combinations(range(1, 6), 2))
INF = -1

_GRAPHS: Dict[str, List[List[List[int]]]] = {}


def load_graphs() -> Dict[str, List[List[List[int]]]]:
    """Load the cached triangulation edge lists (waits if the cache is absent)."""
    for _ in range(30):
        if CACHE.exists():
            return json.loads(CACHE.read_text())["graphs"]
        time.sleep(60)
    raise FileNotFoundError(CACHE)


def canon(col: Sequence[int]) -> Tuple[int, ...]:
    """Relabel colours 1..4 by first occurrence (colour 5 fixed)."""
    m: Dict[int, int] = {}
    out = []
    for c in col:
        if c == 5:
            out.append(5)
        else:
            if c not in m:
                m[c] = len(m) + 1
            out.append(m[c])
    return tuple(out)


def orbit_size(col: Sequence[int]) -> int:
    """Size of the orbit of col under permutations of colours 1..4."""
    k = len({c for c in col if c != 5})
    return {0: 1, 1: 4, 2: 12, 3: 24, 4: 24}[k]


def enum_canonical(adj: List[List[int]]) -> List[Tuple[int, ...]]:
    """All proper 5-colourings (vertex order 0..m-1) that are canonical under S4 on 1..4."""
    m = len(adj)
    res: List[Tuple[int, ...]] = []
    col = [0] * m

    def bt(i: int, mx: int) -> None:
        if i == m:
            res.append(tuple(col))
            return
        used = {col[u] for u in adj[i] if u < i}
        for c in list(range(1, min(mx + 1, 4) + 1)) + [5]:
            if c not in used:
                col[i] = c
                bt(i + 1, max(mx, c) if c != 5 else mx)
        col[i] = 0

    bt(0, 0)
    return res


def chains(adj: List[List[int]], col: Sequence[int], a: int, b: int) -> List[List[int]]:
    """All (a,b)-Kempe chains of col, as vertex lists."""
    seen = set()
    out = []
    for s in range(len(col)):
        if col[s] in (a, b) and s not in seen:
            comp = [s]
            seen.add(s)
            q = [s]
            while q:
                x = q.pop()
                for y in adj[x]:
                    if y not in seen and col[y] in (a, b):
                        seen.add(y)
                        comp.append(y)
                        q.append(y)
            out.append(comp)
    return out


def swap(col: Sequence[int], comp: Sequence[int], a: int, b: int) -> Tuple[int, ...]:
    new = list(col)
    for x in comp:
        new[x] = b if col[x] == a else a
    return tuple(new)


def multi_bfs(nbrs: List[List[int]], sources: List[int]) -> List[int]:
    """Distances from a source set (INF = unreachable)."""
    dist = [INF] * len(nbrs)
    q = deque()
    for s in sources:
        dist[s] = 0
        q.append(s)
    while q:
        x = q.popleft()
        for y in nbrs[x]:
            if dist[y] == INF:
                dist[y] = dist[x] + 1
                q.append(y)
    return dist


def is_connected_in(adj: List[List[int]], verts: List[int]) -> bool:
    s = set(verts)
    start = verts[0]
    seen = {start}
    q = [start]
    while q:
        x = q.pop()
        for y in adj[x]:
            if y in s and y not in seen:
                seen.add(y)
                q.append(y)
    return len(seen) == len(s)


def analyse_graph(args: Tuple[int, int]) -> Dict:
    """All (v, c) records for one triangulation T_{n,gi}."""
    n, gi = args
    edges = _GRAPHS[str(n)][gi]
    adjG: List[List[int]] = [[] for _ in range(n)]
    for u, w in edges:
        adjG[u].append(w)
        adjG[w].append(u)

    # ---- R(G,5) modulo S4 on colours 1..4, with swapped chains recorded
    gstates = enum_canonical(adjG)
    gidx = {s: i for i, s in enumerate(gstates)}
    gedges: List[List[Tuple[int, frozenset]]] = []
    for s in gstates:
        lst = []
        for a, b in PAIRS:
            for comp in chains(adjG, s, a, b):
                t = gidx[canon(swap(s, comp, a, b))]
                lst.append((t, frozenset(comp)))
        gedges.append(lst)
    g4 = [i for i, s in enumerate(gstates) if len(set(s)) <= 4]
    dG = multi_bfs([[t for t, _ in lst] for lst in gedges], g4)

    records = []
    for v in range(n):
        if len(adjG[v]) not in (4, 5):
            continue
        hv = [u for u in range(n) if u != v]
        loc = {u: i for i, u in enumerate(hv)}
        adjH = [[loc[w] for w in adjG[u] if w != v] for u in hv]
        N = [loc[u] for u in adjG[v]]
        Nset = set(N)

        # ---- T3 edges in R(G,5): swapped chain minus v is empty or one chain of G-v
        conn_cache: Dict[frozenset, bool] = {}

        def liftable(comp: frozenset) -> bool:
            if v not in comp:
                return True
            rest = comp - {v}
            if not rest:
                return True
            if rest not in conn_cache:
                conn_cache[rest] = is_connected_in(adjG_minus_v, sorted(rest))
            return conn_cache[rest]

        adjG_minus_v = [[w for w in adjG[u] if w != v] if u != v else [] for u in range(n)]
        t3n = [[t for t, comp in lst if liftable(comp)] for lst in gedges]
        t3 = multi_bfs(t3n, g4)

        # ---- R(G-v,5) modulo S4, all edges and K1-safe edges
        hstates = enum_canonical(adjH)
        hidx = {s: i for i, s in enumerate(hstates)}
        allN: List[List[int]] = []
        safeN: List[List[int]] = []
        for s in hstates:
            la, ls = [], []
            for a, b in PAIRS:
                comps = chains(adjH, s, a, b)
                merge_prone = False
                if b == 5:
                    touching = sum(1 for comp in comps if Nset.intersection(comp))
                    merge_prone = touching >= 2
                for comp in comps:
                    t = hidx[canon(swap(s, comp, a, b))]
                    la.append(t)
                    if not (merge_prone and Nset.intersection(comp)):
                        ls.append(t)
            allN.append(la)
            safeN.append(ls)

        tgt1 = []
        tgt2 = []
        for i, s in enumerate(hstates):
            used = set(s)
            if len(used) > 4:
                continue
            tgt1.append(i)
            nb = {s[u] for u in N}
            if any(x not in nb and len(used | {x}) <= 4 for x in range(1, 6)):
                tgt2.append(i)
        d1 = multi_bfs(allN, tgt1)
        s1 = multi_bfs(safeN, tgt1)
        d2 = multi_bfs(allN, tgt2)
        s2 = multi_bfs(safeN, tgt2)

        for gi_state, gs in enumerate(gstates):
            if gs[v] != 5:
                continue
            h = tuple(gs[u] for u in hv)
            j = hidx[h]
            records.append((v, len(adjG[v]), gs, orbit_size(gs),
                            d1[j], s1[j], d2[j], s2[j], dG[gi_state], t3[gi_state]))
    return {"n": n, "gi": gi, "records": records}


def _init(graphs):
    global _GRAPHS
    _GRAPHS = graphs


def fmt(x: int) -> str:
    return "inf" if x == INF else str(x)


def run(nmin: int, nmax: int, procs: int, budget: float) -> Dict:
    graphs = load_graphs()
    out: Dict = {"command": " ".join(sys.argv), "processes": procs,
                 "symmetry": "orbits under permutations of colours 1..4 (colour 5 fixed); "
                             "weighted counts multiply by orbit size",
                 "by_n": {}}
    for n in range(nmin, nmax + 1):
        t0 = time.time()
        jobs = [(n, i) for i in range(len(graphs[str(n)]))]
        with Pool(procs, initializer=_init, initargs=(graphs,)) as pool:
            results = list(pool.imap_unordered(analyse_graph, jobs, chunksize=1))
        results.sort(key=lambda r: r["gi"])
        elapsed = time.time() - t0

        st: Dict = {"graphs": len(jobs), "vertex_instances": 0,
                    "orbits": 0, "colourings_weighted": 0, "elapsed_seconds": elapsed}
        dist = {k: Counter() for k in ("d_s1", "d_s2", "d2_s2", "d_d2", "dG_t3", "d_t3")}
        wdist = {k: Counter() for k in dist}
        by_deg = {4: Counter(), 5: Counter()}
        fails = {"K4_s1_gt_d+1": [], "T2_s2_gt_d+1": [], "T2_s2_gt_d2+1": [],
                 "T3_t3_gt_d+1": [], "T3_t3_gt_dG+1": []}
        fail_w = Counter()
        fail_orbits = Counter()
        vset = set()
        for r in results:
            for (v, deg, gs, w, d1, s1, d2, s2, dg, t3) in r["records"]:
                vset.add((r["gi"], v))
                st["orbits"] += 1
                st["colourings_weighted"] += w
                for key, (x, y) in (("d_s1", (d1, s1)), ("d_s2", (d1, s2)), ("d2_s2", (d2, s2)),
                                    ("d_d2", (d1, d2)), ("dG_t3", (dg, t3)), ("d_t3", (d1, t3))):
                    dist[key][f"{fmt(x)},{fmt(y)}"] += 1
                    wdist[key][f"{fmt(x)},{fmt(y)}"] += w
                by_deg[deg]["s1-d=" + (fmt(s1 - d1) if s1 != INF else "inf")] += w

                def bad(s: int, base: int) -> bool:
                    return s == INF or s > base + 1

                for name, s, base in (("K4_s1_gt_d+1", s1, d1), ("T2_s2_gt_d+1", s2, d1),
                                      ("T2_s2_gt_d2+1", s2, d2), ("T3_t3_gt_d+1", t3, d1),
                                      ("T3_t3_gt_dG+1", t3, dg)):
                    if bad(s, base):
                        fail_w[name] += w
                        fail_orbits[name] += 1
                        if len(fails[name]) < 5:
                            fails[name].append({
                                "graph": f"T_{n}_{r['gi']}", "graph_index": r["gi"], "vertex": v,
                                "degree": deg,
                                "colouring": {str(u): gs[u] for u in range(n)},
                                "d": d1, "s1": fmt(s1), "d2": fmt(d2), "s2": fmt(s2),
                                "dG": dg, "t3": fmt(t3)})
        st["vertex_instances"] = len(vset)
        st["distributions_orbits"] = {k: dict(sorted(c.items())) for k, c in dist.items()}
        st["distributions_weighted"] = {k: dict(sorted(c.items())) for k, c in wdist.items()}
        st["K4_s1_minus_d_by_degree_weighted"] = {str(k): dict(sorted(c.items()))
                                                   for k, c in by_deg.items()}
        st["failure_counts_weighted"] = dict(fail_w)
        st["failure_counts_orbits"] = dict(fail_orbits)
        st["first_failures"] = fails
        out["by_n"][str(n)] = st
        print(f"n={n}: graphs={st['graphs']} (G,v)={st['vertex_instances']} "
              f"orbits={st['orbits']} colourings={st['colourings_weighted']} "
              f"fails={dict(fail_w)} elapsed={elapsed:.1f}s", flush=True)
        OUT.write_text(json.dumps(out, indent=1))
        if elapsed > budget:
            out["stopped_reason"] = f"n={n} took {elapsed:.1f}s > {budget}s"
            print(out["stopped_reason"], flush=True)
            break
    OUT.write_text(json.dumps(out, indent=1))
    return out


# ---------------------------------------------------------------------------
# Independent cross-check without the S4 quotient, using the project functions.
# ---------------------------------------------------------------------------

def verify(nmax: int) -> Dict:
    """Recompute d and s1 with kempe_ops + classify_path_safety (no quotient) and compare."""
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import networkx as nx
    from kempe_ops import enumerate_colourings, all_kempe_neighbours, canonical_form, \
        colouring_from_canonical, num_colours
    from all_paths_analysis import classify_path_safety
    from reduction_search import bfs_reduce_to_4

    graphs = load_graphs()
    _init(graphs)
    report = {"checked_records": 0, "mismatches": 0, "bfs_reduce_checks": 0,
              "bfs_reduce_mismatches": 0}
    for n in range(6, nmax + 1):
        for gi, edges in enumerate(graphs[str(n)]):
            G = nx.Graph()
            G.add_edges_from(map(tuple, edges))
            fast = analyse_graph((n, gi))["records"]
            fast_by = {(v, gs): (d1, s1) for (v, _, gs, _, d1, s1, *_r) in fast}
            for v in G.nodes():
                if G.degree(v) not in (4, 5):
                    continue
                H = G.copy()
                H.remove_node(v)
                cols = [canonical_form(H, c) for c in enumerate_colourings(H, 5)]
                idx = {c: i for i, c in enumerate(cols)}
                allN = [[] for _ in cols]
                safeN = [[] for _ in cols]
                for i, c in enumerate(cols):
                    ch = colouring_from_canonical(H, c)
                    full = dict(ch)
                    full[v] = 5
                    for nb in all_kempe_neighbours(H, ch, 5):
                        j = idx[nb]
                        allN[i].append(j)
                        cls = classify_path_safety(G, H, v, full, [c, nb])
                        if cls["path_is_safe"]:
                            safeN[i].append(j)
                tg = [i for i, c in enumerate(cols) if len(set(c)) <= 4]
                d1 = multi_bfs(allN, tg)
                s1 = multi_bfs(safeN, tg)
                hv = sorted(H.nodes())
                for c in enumerate_colourings(G, 5):
                    if c[v] != 5:
                        continue
                    gs = tuple(c[u] for u in range(n))
                    key = (v, canon(gs))
                    j = idx[canonical_form(H, {u: c[u] for u in hv})]
                    report["checked_records"] += 1
                    if fast_by[key] != (d1[j], s1[j]):
                        report["mismatches"] += 1
                        if report["mismatches"] <= 5:
                            print("MISMATCH", n, gi, v, gs, fast_by[key], (d1[j], s1[j]))
                    if report["checked_records"] % 97 == 0:
                        p = bfs_reduce_to_4(H, {u: c[u] for u in hv}, 5)
                        report["bfs_reduce_checks"] += 1
                        if p is None or len(p) - 1 != d1[j]:
                            report["bfs_reduce_mismatches"] += 1
        print(f"verify n={n}: {report}", flush=True)
    return report


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--nmin", type=int, default=6)
    ap.add_argument("--nmax", type=int, default=10)
    ap.add_argument("--procs", type=int, default=3)
    ap.add_argument("--budget", type=float, default=600.0)
    ap.add_argument("--verify", type=int, default=0)
    a = ap.parse_args()
    if a.verify:
        t = time.time()
        rep = verify(a.verify)
        rep["elapsed_seconds"] = time.time() - t
        print(json.dumps(rep))
        (OUT.parent / "K4_verify.json").write_text(json.dumps(rep, indent=1))
    else:
        run(a.nmin, a.nmax, a.procs, a.budget)
