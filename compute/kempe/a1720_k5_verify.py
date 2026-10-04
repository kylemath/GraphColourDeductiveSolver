"""a1720_k5_verify.py — Agent 1720 group K5: independent labelled cross-check
and witness extraction.

1. For n <= 8 rebuild R(G,5) on *labelled* colourings with the older helpers
   in kempe_ops.py (no quotient) and recompute: connectivity, and for every
   colouring the least plateau bound L admitting a monotone path to f = 0,
   using a different algorithm (search over (colouring, current run length)).
   Compare with the quotient results in K5_partA_raw.json / K5_partC_raw.json.
2. For the first graph at each n attaining the maximal plateau, write the
   witness colouring and an optimal monotone path (labelled) with each move.

Usage:
    .venv/bin/python compute/kempe/a1720_k5_verify.py
"""

from __future__ import annotations

import json
import sys
import time
from collections import deque
from pathlib import Path
from typing import Dict, List, Optional, Tuple

sys.path.insert(0, str(Path(__file__).resolve().parent))
import networkx as nx  # noqa: E402

from kempe_ops import (  # noqa: E402
    canonical_form, enumerate_colourings, get_all_kempe_chains, kempe_swap,
)
from a1720_k5_reconfig import load_graphs, OUT_DIR  # noqa: E402

Canon = Tuple[int, ...]


def labelled_R(G: nx.Graph):
    """Labelled R(G,5): list of colourings, index, adjacency with move labels."""
    cols = [canonical_form(G, c) for c in enumerate_colourings(G, 5)]
    idx = {c: i for i, c in enumerate(cols)}
    verts = sorted(G.nodes())
    nbrs: List[Dict[int, Tuple[int, int, List[int]]]] = []
    for c in cols:
        d = dict(zip(verts, c))
        out: Dict[int, Tuple[int, int, List[int]]] = {}
        for a in range(1, 6):
            for b in range(a + 1, 6):
                for ch in get_all_kempe_chains(G, d, a, b):
                    t = canonical_form(G, kempe_swap(d, ch, a, b))
                    j = idx[t]
                    if j != idx[c] and j not in out:
                        out[j] = (a, b, sorted(ch))
        nbrs.append(out)
    return cols, idx, nbrs


def least_L(cols: List[Canon], nbrs, Lmax: int = 12) -> List[Optional[int]]:
    """Least L per colouring via fixpoint on (colouring, run) states."""
    f = [c.count(5) for c in cols]
    N = len(cols)
    res: List[Optional[int]] = [None] * N
    for L in range(Lmax + 1):
        # good[r][i]: from colouring i having already used r plateau moves in
        # the current run, f = 0 is reachable.  Backward induction on r.
        good = [[fi == 0 for fi in f] for _ in range(L + 1)]
        changed = True
        while changed:
            changed = False
            for r in range(L, -1, -1):
                for i in range(N):
                    if good[r][i]:
                        continue
                    for j in nbrs[i]:
                        if (f[j] < f[i] and good[0][j]) or \
                           (f[j] == f[i] and r < L and good[r + 1][j]):
                            good[r][i] = True
                            changed = True
                            break
        for i in range(N):
            if res[i] is None and good[0][i]:
                res[i] = L
        if all(x is not None for x in res):
            break
    return res


def optimal_path(cols, nbrs, start: int, L: int):
    """BFS over (colouring, run) for a monotone path with plateau runs <= L."""
    f = [c.count(5) for c in cols]
    s0 = (start, 0)
    prev = {s0: None}
    dq = deque([s0])
    while dq:
        i, r = dq.popleft()
        if f[i] == 0:
            path = []
            s = (i, r)
            while prev[s] is not None:
                p, mv = prev[s]
                path.append((p[0], s[0], mv))
                s = p
            return list(reversed(path))
        for j, mv in nbrs[i].items():
            if f[j] < f[i]:
                ns = (j, 0)
            elif f[j] == f[i] and r < L:
                ns = (j, r + 1)
            else:
                continue
            if ns not in prev:
                prev[ns] = ((i, r), mv)
                dq.append(ns)
    return None


def main() -> None:
    A = json.loads((OUT_DIR / "K5_partA_raw.json").read_text())
    C = json.loads((OUT_DIR / "K5_partC_raw.json").read_text())
    report: Dict = {"cross_check": {}, "witnesses": []}
    t0 = time.time()
    for n in range(4, 9):
        mism = 0
        ok_conn = True
        for gi, edges in enumerate(load_graphs(n)):
            G = nx.Graph()
            G.add_nodes_from(range(n))
            G.add_edges_from(edges)
            cols, _, nbrs = labelled_R(G)
            Rg = nx.Graph()
            Rg.add_nodes_from(range(len(cols)))
            Rg.add_edges_from((i, j) for i in range(len(cols)) for j in nbrs[i])
            conn = nx.is_connected(Rg)
            ok_conn &= conn == (A[str(n)]["per_graph"][gi]["components"] == 1)
            L = least_L(cols, nbrs)
            maxL = max(x for x in L)
            if maxL != C[str(n)]["per_graph"][gi]["max_plateau"]:
                mism += 1
            if any(x is None for x in L):
                mism += 1
        report["cross_check"][str(n)] = {
            "connectivity_agrees": ok_conn, "max_plateau_mismatches": mism}
        print(n, report["cross_check"][str(n)], flush=True)
    report["cross_check_elapsed_seconds"] = round(time.time() - t0, 2)

    # Witnesses: first graph attaining the max plateau at each n in 5..9,
    # plus n = 10 (and n = 11 if present) using the quotient worst state.
    for n in range(5, 12):
        if str(n) not in C:
            continue
        per = C[str(n)]["per_graph"]
        m = C[str(n)]["summary"]["max_plateau"]
        gi = next(i for i, r in enumerate(per) if r["max_plateau"] == m)
        edges = load_graphs(n)[gi]
        ws = per[gi]["worst_state"]
        G = nx.Graph()
        G.add_nodes_from(range(n))
        G.add_edges_from(edges)
        cols, idx, nbrs = labelled_R(G)
        start = idx[tuple(ws["colouring"])]
        path = optimal_path(cols, nbrs, start, m)
        worse = optimal_path(cols, nbrs, start, m - 1)
        least = m if (path is not None and worse is None) else None
        L = {start: least}
        report["witnesses"].append({
            "n": n, "graph": f"T_{n}_{gi}", "edges": edges,
            "colouring_vertex_0_to_n-1": ws["colouring"], "f": ws["f"],
            "least_plateau_bound_labelled": L[start],
            "least_plateau_bound_quotient": ws["g"],
            "path_with_bound_minus_one_exists": worse is not None,
            "optimal_path": [
                {"swap_colours": [mv[0], mv[1]], "chain": mv[2],
                 "to": list(cols[j]), "f": cols[j].count(5)}
                for (_, j, mv) in path],
        })
        print("witness", n, f"T_{n}_{gi}", ws, "labelled L =", L[start], flush=True)
    report["elapsed_seconds"] = round(time.time() - t0, 2)
    (OUT_DIR / "K5_verify.json").write_text(json.dumps(report, indent=1))


if __name__ == "__main__":
    main()
