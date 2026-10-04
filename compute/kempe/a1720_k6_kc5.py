"""
a1720_k6_kc5.py -- Agent 1720, group K6: Kempe-class hypothesis at degree 5 (KC5).

KC5 at (G, v): G a planar triangulation, deg(v) = 5, H = G - v.  Every Kempe
class of proper 4-colourings of H (swaps of any (a,b)-component of H) that
contains a colouring with |c(N(v))| = 4 also contains one with |c(N(v))| <= 3.

Colourings are handled modulo the symmetric group S_4 on colours.  This is
exact, not a heuristic:
  * a global transposition (a b) is the composition of the Kempe swaps on all
    (a,b)-components, so every Kempe class is a union of S_4-orbits;
  * pi o swap_K(a,b) = swap_K(pi(a),pi(b)) o pi, so Kempe adjacency descends to
    the quotient and quotient components are exactly images of Kempe classes;
  * |c(N(v))| is S_4-invariant.
So "bad class" is well-defined on normalised colourings (colours relabelled
in order of first appearance along the vertex order 0..m-1).
"""

from __future__ import annotations

import json
import random
import sys
import time
from collections import deque
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence, Set, Tuple

Col = Tuple[int, ...]


# ---------------------------------------------------------------------------
# Graph helpers
# ---------------------------------------------------------------------------

def adjacency(n: int, edges: Iterable[Sequence[int]]) -> List[Set[int]]:
    """Adjacency sets for vertices 0..n-1."""
    adj: List[Set[int]] = [set() for _ in range(n)]
    for u, w in edges:
        adj[u].add(w)
        adj[w].add(u)
    return adj


def delete_vertex(adj: List[Set[int]], v: int) -> Tuple[List[int], List[int], List[int]]:
    """
    Return (masks, nbr_idx, old_of_new) for H = G - v with vertices relabelled
    0..m-1.  masks[i] is the neighbour bitmask of i in H; nbr_idx lists the
    new indices of N_G(v).
    """
    old = [u for u in range(len(adj)) if u != v]
    new_of = {u: i for i, u in enumerate(old)}
    masks = [0] * len(old)
    for i, u in enumerate(old):
        for w in adj[u]:
            if w != v:
                masks[i] |= 1 << new_of[w]
    nbr_idx = sorted(new_of[u] for u in adj[v])
    return masks, nbr_idx, old


def normalise(c: Sequence[int]) -> Col:
    """Relabel colours in order of first appearance (canonical S_4 representative)."""
    rel: Dict[int, int] = {}
    out = []
    for x in c:
        if x not in rel:
            rel[x] = len(rel)
        out.append(rel[x])
    return tuple(out)


# ---------------------------------------------------------------------------
# Colourings and Kempe moves
# ---------------------------------------------------------------------------

def enumerate_normalised(masks: List[int], k: int = 4) -> List[Col]:
    """All proper k-colourings of H modulo S_k (normalised representatives)."""
    m = len(masks)
    res: List[Col] = []
    c = [0] * m

    def bt(i: int, mx: int) -> None:
        if i == m:
            res.append(tuple(c))
            return
        forbidden = 0
        nb = masks[i] & ((1 << i) - 1)
        while nb:
            low = nb & -nb
            forbidden |= 1 << c[low.bit_length() - 1]
            nb ^= low
        for col in range(min(mx + 2, k)):
            if not (forbidden >> col) & 1:
                c[i] = col
                bt(i + 1, max(mx, col))

    bt(0, -1)
    return res


def kempe_neighbours(c: Col, masks: List[int], k: int = 4) -> Set[Col]:
    """Normalised colourings reachable from c by one Kempe swap (excluding c's orbit)."""
    m = len(c)
    cls = [0] * k
    for i, x in enumerate(c):
        cls[x] |= 1 << i
    out: Set[Col] = set()
    for a in range(k):
        for b in range(a + 1, k):
            ab = cls[a] | cls[b]
            rest = ab
            while rest:
                seed = rest & -rest
                comp = seed
                frontier = seed
                while frontier:
                    low = frontier & -frontier
                    frontier ^= low
                    nb = masks[low.bit_length() - 1] & ab & ~comp
                    comp |= nb
                    frontier |= nb
                rest &= ~comp
                if comp == ab:
                    continue  # global transposition: same S_4-orbit
                d = list(c)
                x = comp
                while x:
                    low = x & -x
                    x ^= low
                    j = low.bit_length() - 1
                    d[j] = b if d[j] == a else a
                out.add(normalise(d))
    return out


def ncols_on(c: Col, idx: Sequence[int]) -> int:
    """Number of distinct colours c uses on the vertex set idx."""
    return len({c[i] for i in idx})


# ---------------------------------------------------------------------------
# Full KC5 analysis at one (G, v)
# ---------------------------------------------------------------------------

def analyse_vertex(adj: List[Set[int]], v: int) -> Dict:
    """
    Enumerate all Kempe classes of H = G - v (mod S_4) and classify them.
    Returns counts, bad-class witnesses, and the maximum Kempe distance from a
    4-on-N(v) colouring to the nearest <=3-on-N(v) colouring (in its class).
    """
    masks, nbr, old = delete_vertex(adj, v)
    cols = enumerate_normalised(masks)
    index = {c: i for i, c in enumerate(cols)}
    nbrs = [[index[d] for d in kempe_neighbours(c, masks)] for c in cols]
    good = [ncols_on(c, nbr) <= 3 for c in cols]

    comp = [-1] * len(cols)
    classes: List[List[int]] = []
    for s in range(len(cols)):
        if comp[s] >= 0:
            continue
        cid = len(classes)
        comp[s] = cid
        q = deque([s])
        members = [s]
        while q:
            x = q.popleft()
            for y in nbrs[x]:
                if comp[y] < 0:
                    comp[y] = cid
                    members.append(y)
                    q.append(y)
        classes.append(members)

    # multi-source BFS from good colourings: Kempe distance to fixability
    dist = [-1] * len(cols)
    q = deque(i for i in range(len(cols)) if good[i])
    for i in q:
        dist[i] = 0
    while q:
        x = q.popleft()
        for y in nbrs[x]:
            if dist[y] < 0:
                dist[y] = dist[x] + 1
                q.append(y)

    bad, mixed, only3, only4 = [], 0, 0, 0
    for members in classes:
        g = sum(good[i] for i in members)
        has4 = g < len(members)
        if g == 0:
            bad.append(members)
        elif has4:
            mixed += 1
        else:
            only3 += 1
    max_dist = max((dist[i] for i in range(len(cols)) if not good[i]), default=0)
    wit = []
    for members in bad:
        c = cols[members[0]]
        wit.append({
            "class_size_mod_S4": len(members),
            "class_size": 24 * len(members),
            "colouring_G_minus_v": {str(old[i]): c[i] for i in range(len(c))},
        })
    return {
        "v": v,
        "n_colourings_mod_S4": len(cols),
        "n_classes": len(classes),
        "n_classes_mixed": mixed,
        "n_classes_only_le3": only3,
        "n_bad_classes": len(bad),
        "max_kempe_distance_to_fix": max_dist,
        "bad_witnesses": wit,
    }


def degree5_vertices(adj: List[Set[int]]) -> List[int]:
    return [u for u in range(len(adj)) if len(adj[u]) == 5]


# ---------------------------------------------------------------------------
# Class exploration from a single start (for larger graphs)
# ---------------------------------------------------------------------------

def explore_class(masks: List[int], nbr: Sequence[int], start: Col,
                  limit: int = 5_000_000) -> Tuple[bool, int]:
    """
    BFS the Kempe class of `start` (mod S_4).  Returns (fixable, visited).
    Stops early at the first colouring with <= 3 colours on nbr.  If the class
    is exhausted with no fixable colouring, returns (False, class size).
    Raises RuntimeError if more than `limit` colourings are visited.
    """
    start = normalise(start)
    seen = {start}
    q = deque([start])
    while q:
        c = q.popleft()
        if ncols_on(c, nbr) <= 3:
            return True, len(seen)
        for d in kempe_neighbours(c, masks):
            if d not in seen:
                seen.add(d)
                q.append(d)
                if len(seen) > limit:
                    raise RuntimeError("class exploration limit exceeded")
    return False, len(seen)


# ---------------------------------------------------------------------------
# Drivers
# ---------------------------------------------------------------------------

ROOT = Path(__file__).resolve().parents[2]
CACHE = ROOT / "compute" / "data" / "triangulations_n4_11.json"


def run_cache(ns: Iterable[int]) -> Dict:
    data = json.loads(CACHE.read_text())
    out: Dict = {}
    for n in ns:
        t0 = time.time()
        graphs = data["graphs"][str(n)]
        tot = {"n": n, "n_triangulations": len(graphs), "n_pairs_G_v": 0,
               "n_graphs_with_deg5": 0, "n_classes": 0, "n_bad_classes": 0,
               "n_pairs_multi_class": 0, "max_classes_at_one_pair": 0,
               "max_kempe_distance_to_fix": 0, "n_pairs_needing_ge2_swaps": 0,
               "bad": []}
        for gi, E in enumerate(graphs):
            adj = adjacency(n, E)
            d5 = degree5_vertices(adj)
            if d5:
                tot["n_graphs_with_deg5"] += 1
            for v in d5:
                r = analyse_vertex(adj, v)
                tot["n_pairs_G_v"] += 1
                tot["n_classes"] += r["n_classes"]
                tot["n_bad_classes"] += r["n_bad_classes"]
                tot["n_pairs_multi_class"] += r["n_classes"] > 1
                tot["max_classes_at_one_pair"] = max(tot["max_classes_at_one_pair"], r["n_classes"])
                tot["max_kempe_distance_to_fix"] = max(tot["max_kempe_distance_to_fix"],
                                                      r["max_kempe_distance_to_fix"])
                tot["n_pairs_needing_ge2_swaps"] += r["max_kempe_distance_to_fix"] >= 2
                if r["n_bad_classes"]:
                    tot["bad"].append({"graph": f"T_{n}_{gi}", "edges": E, **r})
        tot["elapsed_seconds"] = round(time.time() - t0, 2)
        print(json.dumps({k: v for k, v in tot.items() if k != "bad"}), flush=True)
        out[str(n)] = tot
    return out


def run_named(name: str, n: int, edges: List[Tuple[int, int]]) -> Dict:
    """Full KC5 analysis on a named triangulation (all degree-5 vertices)."""
    t0 = time.time()
    adj = adjacency(n, edges)
    res = {"name": name, "n": n, "m": len(edges),
           "degree_sequence": sorted(len(a) for a in adj), "vertices": []}
    for v in degree5_vertices(adj):
        r = analyse_vertex(adj, v)
        res["vertices"].append(r)
        print(name, "v", v, {k: r[k] for k in r if k != "bad_witnesses"}, flush=True)
    res["elapsed_seconds"] = round(time.time() - t0, 2)
    return res


if __name__ == "__main__":
    ns = [int(x) for x in sys.argv[1:]] or list(range(4, 12))
    result = run_cache(ns)
    outp = ROOT / "backgroundMaterial" / "agent1720" / "groups" / f"K6_cache_n{min(ns)}_{max(ns)}.json"
    outp.write_text(json.dumps(result, indent=1))
    print("wrote", outp)
