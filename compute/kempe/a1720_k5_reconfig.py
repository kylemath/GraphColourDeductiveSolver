"""a1720_k5_reconfig.py — Agent 1720 group K5.

Part A: for every cached triangulation, build the Kempe reconfiguration graph
R(G,5) modulo the full colour group S_5 (states = set partitions of V(G) into
at most 5 independent blocks) and check (i) connectivity, (ii) every class
contains a colouring using at most 4 colours.

Part C: monotone reduction.  f(c) = |c^{-1}(5)|.  Work modulo the group S_4
permuting colours 1..4 and fixing colour 5 (f is invariant under exactly this
group).  A colouring is *monotone-good* if a Kempe path exists along which f
never increases and which ends at f = 0.  For the strict version, the
*plateau cost* g(c) is the least L such that some such path has every run of
consecutive f-preserving moves of length <= L; g(c) = 0 means a strictly
f-decreasing Kempe path to f = 0 exists.

Justification of the quotients (see K5_report.md, section 1):
  * for any colour permutation pi, pi o swap_{a,b,K}(c) = swap_{pi a, pi b, K}(pi o c),
    so pi is an automorphism of R(G,k);
  * a transposition (a b) applied globally equals the product of the swaps of
    all (a,b)-chains, hence c and pi o c lie in the same Kempe class;
  * therefore Kempe classes are unions of orbits, and components of R/Gamma
    correspond bijectively to components of R, for Gamma = S_5 or S_4.

Usage:
    .venv/bin/python compute/kempe/a1720_k5_reconfig.py A 10
    .venv/bin/python compute/kempe/a1720_k5_reconfig.py C 10
"""

from __future__ import annotations

import json
import sys
import time
from collections import deque
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple

ROOT = Path(__file__).resolve().parents[2]
CACHE = ROOT / "compute" / "data" / "triangulations_n4_11.json"
OUT_DIR = ROOT / "backgroundMaterial" / "agent1720" / "groups"

State = Tuple[int, ...]


def load_graphs(n: int) -> List[List[List[int]]]:
    """Return the cached edge lists of all triangulations on n vertices."""
    data = json.loads(CACHE.read_text())
    return data["graphs"][str(n)]


def adjacency_masks(edges: Sequence[Sequence[int]], n: int) -> List[int]:
    """Bitmask adjacency list for vertices 0..n-1."""
    adj = [0] * n
    for u, v in edges:
        adj[u] |= 1 << v
        adj[v] |= 1 << u
    return adj


def canon_s5(col: Sequence[int]) -> State:
    """Relabel colours by order of first appearance (orbit rep. under S_5)."""
    relabel: Dict[int, int] = {}
    out = []
    for x in col:
        if x not in relabel:
            relabel[x] = len(relabel) + 1
        out.append(relabel[x])
    return tuple(out)


def canon_s4(col: Sequence[int]) -> State:
    """Relabel colours 1..4 by first appearance, keep colour 5 fixed (S_4 rep.)."""
    relabel: Dict[int, int] = {5: 5}
    nxt = 1
    out = []
    for x in col:
        if x not in relabel:
            relabel[x] = nxt
            nxt += 1
        out.append(relabel[x])
    return tuple(out)


def enumerate_states(adj: List[int], n: int, mode: str) -> List[State]:
    """Enumerate orbit representatives of proper 5-colourings.

    mode 'S5': restricted-growth strings over {1..5}.
    mode 'S4': colour 5 always allowed; colours 1..4 in restricted growth.
    """
    res: List[State] = []
    col = [0] * n

    def rec(i: int, maxc: int) -> None:
        if i == n:
            res.append(tuple(col))
            return
        forbidden = {col[j] for j in range(i) if adj[i] >> j & 1}
        if mode == "S5":
            options = range(1, min(maxc + 1, 5) + 1)
        else:
            options = list(range(1, min(maxc + 1, 4) + 1)) + [5]
        for c in options:
            if c in forbidden:
                continue
            col[i] = c
            new_max = maxc if c == 5 and mode == "S4" else max(maxc, c)
            rec(i + 1, new_max)
        col[i] = 0

    rec(0, 0)
    return res


def kempe_neighbours(state: State, adj: List[int], n: int, canon) -> set:
    """All orbit representatives reachable by one Kempe swap (excluding self)."""
    cmask = [0] * 6
    for v, x in enumerate(state):
        cmask[x] |= 1 << v
    out = set()
    for a in range(1, 6):
        for b in range(a + 1, 6):
            ab = cmask[a] | cmask[b]
            if cmask[a] == 0 and cmask[b] == 0:
                continue
            rem = ab
            while rem:
                low = rem & -rem
                comp = low
                frontier = low
                while frontier:
                    nb = 0
                    f = frontier
                    while f:
                        lb = f & -f
                        nb |= adj[lb.bit_length() - 1]
                        f ^= lb
                    nb &= ab & ~comp
                    comp |= nb
                    frontier = nb
                rem &= ~comp
                new = list(state)
                m = comp
                while m:
                    lb = m & -m
                    v = lb.bit_length() - 1
                    new[v] = b if state[v] == a else a
                    m ^= lb
                t = canon(new)
                if t != state:
                    out.add(t)
    return out


def build_graph(adj: List[int], n: int, mode: str):
    """Return (states, index, neighbour lists) of R(G,5)/Gamma."""
    canon = canon_s5 if mode == "S5" else canon_s4
    states = enumerate_states(adj, n, mode)
    index = {s: i for i, s in enumerate(states)}
    nbrs: List[List[int]] = []
    for s in states:
        lst = []
        for t in kempe_neighbours(s, adj, n, canon):
            lst.append(index[t])  # KeyError would signal a canonicalisation bug
        nbrs.append(lst)
    return states, index, nbrs


def components(nbrs: List[List[int]]) -> List[int]:
    """Component label per node."""
    lab = [-1] * len(nbrs)
    k = 0
    for s in range(len(nbrs)):
        if lab[s] >= 0:
            continue
        lab[s] = k
        dq = deque([s])
        while dq:
            u = dq.popleft()
            for w in nbrs[u]:
                if lab[w] < 0:
                    lab[w] = k
                    dq.append(w)
        k += 1
    return lab


def part_a_graph(edges, n: int) -> Dict:
    """Part A check for one triangulation."""
    adj = adjacency_masks(edges, n)
    states, _, nbrs = build_graph(adj, n, "S5")
    lab = components(nbrs)
    ncomp = max(lab) + 1
    has4 = [False] * ncomp
    n_le4 = 0
    for s, l in zip(states, lab):
        if max(s) <= 4:
            has4[l] = True
            n_le4 += 1
    # P(G,5) = sum over partitions with k blocks of 5!/(5-k)!
    falling = {1: 5, 2: 20, 3: 60, 4: 120, 5: 120}
    p5 = sum(falling[max(s)] for s in states)
    return {
        "orbits": len(states),
        "P5_labelled": p5,
        "orbits_le4_colours": n_le4,
        "components": ncomp,
        "all_classes_contain_le4": all(has4),
        "edges_quotient": sum(len(x) for x in nbrs) // 2,
    }


def plateau_costs(states: List[State], nbrs: List[List[int]]) -> List[Optional[int]]:
    """g(c) per state; None if no monotone path to f = 0 exists."""
    f = [s.count(5) for s in states]
    N = len(states)
    g: List[Optional[int]] = [None] * N
    levels: Dict[int, List[int]] = {}
    for i, x in enumerate(f):
        levels.setdefault(x, []).append(i)
    for i in levels.get(0, []):
        g[i] = 0
    for k in sorted(levels):
        if k == 0:
            continue
        lvl = levels[k]
        # entry cost e(s): best g of a strictly lower neighbour
        entry: Dict[int, int] = {}
        for s in lvl:
            best = None
            for w in nbrs[s]:
                if f[w] < k and g[w] is not None:
                    if best is None or g[w] < best:
                        best = g[w]
            if best is not None:
                entry[s] = best
        if not entry:
            continue
        # g(c) = min_s max(d_k(c,s), e(s)), d_k = distance inside level k
        for t in sorted(set(entry.values())):
            src = [s for s, e in entry.items() if e <= t]
            dist = {s: 0 for s in src}
            dq = deque(src)
            while dq:
                u = dq.popleft()
                for w in nbrs[u]:
                    if f[w] == k and w not in dist:
                        dist[w] = dist[u] + 1
                        dq.append(w)
            for c, d in dist.items():
                val = max(d, t)
                if g[c] is None or val < g[c]:
                    g[c] = val
    return g


def part_c_graph(edges, n: int) -> Dict:
    """Part C check for one triangulation."""
    adj = adjacency_masks(edges, n)
    states, _, nbrs = build_graph(adj, n, "S4")
    lab = components(nbrs)
    g = plateau_costs(states, nbrs)
    f = [s.count(5) for s in states]
    bad = [i for i, x in enumerate(g) if x is None]
    no_local_decrease = 0
    for i, s in enumerate(states):
        if f[i] > 0 and not any(f[w] < f[i] for w in nbrs[i]):
            no_local_decrease += 1
    maxg = max((x for x in g if x is not None), default=0)
    worst = None
    if maxg > 0:
        i = max(range(len(states)), key=lambda j: -1 if g[j] is None else g[j])
        worst = {"colouring": list(states[i]), "f": f[i], "g": g[i]}
    return {
        "orbits_S4": len(states),
        "components_S4": max(lab) + 1,
        "monotone_failures": len(bad),
        "failure_example": list(states[bad[0]]) if bad else None,
        "max_plateau": maxg,
        "g_histogram": {str(v): sum(1 for x in g if x == v) for v in range(maxg + 1)},
        "states_without_decreasing_swap": no_local_decrease,
        "worst_state": worst,
    }


def main() -> None:
    part = sys.argv[1]
    ns = [int(x) for x in sys.argv[2:]]
    results: Dict = {}
    for n in ns:
        graphs = load_graphs(n)
        t0 = time.time()
        per = []
        for i, edges in enumerate(graphs):
            r = part_a_graph(edges, n) if part == "A" else part_c_graph(edges, n)
            r["name"] = f"T_{n}_{i}"
            per.append(r)
        el = time.time() - t0
        if part == "A":
            summ = {
                "graphs": len(per),
                "all_connected": all(r["components"] == 1 for r in per),
                "all_classes_contain_le4": all(r["all_classes_contain_le4"] for r in per),
                "total_orbits": sum(r["orbits"] for r in per),
                "total_labelled_colourings": sum(r["P5_labelled"] for r in per),
                "max_orbits": max(r["orbits"] for r in per),
                "elapsed_seconds": round(el, 2),
            }
        else:
            summ = {
                "graphs": len(per),
                "all_connected_S4": all(r["components_S4"] == 1 for r in per),
                "monotone_failures": sum(r["monotone_failures"] for r in per),
                "graphs_with_failures": [r["name"] for r in per if r["monotone_failures"]],
                "max_plateau": max(r["max_plateau"] for r in per),
                "graphs_needing_plateau": sum(1 for r in per if r["max_plateau"] > 0),
                "states_without_decreasing_swap": sum(r["states_without_decreasing_swap"] for r in per),
                "total_orbits_S4": sum(r["orbits_S4"] for r in per),
                "elapsed_seconds": round(el, 2),
            }
        print(n, json.dumps(summ), flush=True)
        results[str(n)] = {"summary": summ, "per_graph": per}
    out = OUT_DIR / f"K5_part{part}_raw.json"
    prev = json.loads(out.read_text()) if out.exists() else {}
    prev.update(results)
    out.write_text(json.dumps(prev, indent=1))


if __name__ == "__main__":
    main()
