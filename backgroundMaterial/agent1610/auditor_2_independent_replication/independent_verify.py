#!/usr/bin/env python3
"""
Independent Verification of Kempe Reconfiguration MTL Claims
============================================================
Written entirely from scratch — no code from compute/kempe/.

Tests the Merge-Then-Lift (MTL) claim:
  For any planar triangulation G, removing vertex v, every proper
  ≤4-colouring of G-v that is REACHABLE from a problematic 5-colouring
  via Kempe swaps leaves a free colour for v among the colours used.

Phase 1: Direct check — for ALL ≤4-colourings of G-v, does v's
         neighbourhood use strictly fewer colours than are present?
Phase 2: BFS reachability — can every problematic 5-colouring reach
         a state where v has a free colour?
"""

import networkx as nx
from itertools import combinations
from collections import deque
import time
import sys

GLOBAL_START = time.time()


# ─────────────────────────────────────────────────────────────────────
# 1. COLOURING ENUMERATION (backtracking, from scratch)
# ─────────────────────────────────────────────────────────────────────

def enumerate_colourings(G, k):
    """
    Enumerate every proper k-colouring of G via backtracking.
    Returns (nodes, list_of_tuples).
    """
    nodes = sorted(G.nodes())
    n = len(nodes)
    idx = {v: i for i, v in enumerate(nodes)}

    adj = [[] for _ in range(n)]
    for u, v in G.edges():
        adj[idx[u]].append(idx[v])
        adj[idx[v]].append(idx[u])

    results = []
    col = [0] * n

    def bt(pos):
        if pos == n:
            results.append(tuple(col))
            return
        forbidden = set()
        for j in adj[pos]:
            if j < pos:
                forbidden.add(col[j])
        for c in range(1, k + 1):
            if c not in forbidden:
                col[pos] = c
                bt(pos + 1)

    bt(0)
    return nodes, results


# ─────────────────────────────────────────────────────────────────────
# 2. KEMPE CHAIN OPERATIONS (from scratch)
# ─────────────────────────────────────────────────────────────────────

def find_kempe_chains(G, col_dict, c1, c2):
    """Connected components of the (c1,c2)-bichromatic subgraph."""
    verts = [v for v in G.nodes() if col_dict[v] in (c1, c2)]
    if not verts:
        return []
    return [frozenset(cc) for cc in nx.connected_components(G.subgraph(verts))]


def do_swap(col_dict, chain, c1, c2):
    """Return new colouring dict with c1<->c2 on chain."""
    out = dict(col_dict)
    for v in chain:
        out[v] = c2 if out[v] == c1 else c1
    return out


# ─────────────────────────────────────────────────────────────────────
# 3. TRIANGULATION GENERATION
# ─────────────────────────────────────────────────────────────────────

EXPECTED = {4: 1, 5: 1, 6: 2, 7: 5, 8: 14, 9: 50}


def is_tri(G):
    """Is G a connected planar triangulation on ≥4 vertices?"""
    n = G.number_of_nodes()
    if n < 4 or G.number_of_edges() != 3 * n - 6:
        return False
    if not nx.is_connected(G):
        return False
    return nx.check_planarity(G)[0]


def _ccw_next(emb, node, ref):
    """
    In the CW ordering around `node`, return the CCW successor of `ref`.
    CCW successor = CW predecessor.
    """
    cw = list(emb.neighbors_cw_order(node))
    i = cw.index(ref)
    return cw[(i - 1) % len(cw)]


def planar_faces(G):
    """Return (list_of_faces, embedding).  Each face = list of vertices."""
    ok, emb = nx.check_planarity(G)
    assert ok, "Graph is not planar"
    seen = set()
    faces = []
    for v in emb:
        for w in emb.neighbors_cw_order(v):
            if (v, w) in seen:
                continue
            face = []
            a, b = v, w
            while (a, b) not in seen:
                seen.add((a, b))
                face.append(a)
                c = _ccw_next(emb, b, a)
                a, b = b, c
            faces.append(face)
    return faces, emb


def face_nbrs(emb, u, v):
    """Return the two face-neighbour vertices of edge (u,v)."""
    cw_u = list(emb.neighbors_cw_order(u))
    iv = cw_u.index(v)
    w1 = cw_u[(iv - 1) % len(cw_u)]
    w2 = cw_u[(iv + 1) % len(cw_u)]
    return w1, w2


def _dedup_add(H, lst):
    """Append H if it's a valid triangulation not isomorphic to anything in lst."""
    if is_tri(H) and not any(nx.is_isomorphic(H, X) for X in lst):
        lst.append(H)
        return True
    return False


def atlas_triangulations(n):
    """All triangulations on exactly n vertices from NetworkX graph atlas (n ≤ 7)."""
    target_m = 3 * n - 6
    result = []
    for G in nx.graph_atlas_g():
        if G.number_of_nodes() == n and G.number_of_edges() == target_m:
            if nx.is_connected(G) and nx.check_planarity(G)[0]:
                _dedup_add(G, result)
    return result


def build_triangulations(max_n, verbose=True):
    """Generate non-isomorphic planar triangulations for n=4..max_n."""
    by_n = {}

    # Exact enumeration via atlas for n ≤ 7
    for n in range(4, min(8, max_n + 1)):
        by_n[n] = atlas_triangulations(n)
        _log_count(n, by_n[n], verbose)

    # Recursive build + flip expansion for n ≥ 8
    for n in range(8, max_n + 1):
        cands = []
        for G in by_n[n - 1]:
            faces, emb = planar_faces(G)

            # (a) Face stacking
            for f in faces:
                if len(f) == 3:
                    H = G.copy()
                    H.add_node(n - 1)
                    for u in f[:3]:
                        H.add_edge(n - 1, u)
                    _dedup_add(H, cands)

            # (b) Edge splitting (using planar face-neighbours)
            for u, v in list(G.edges()):
                w1, w2 = face_nbrs(emb, u, v)
                H = G.copy()
                H.remove_edge(u, v)
                H.add_node(n - 1)
                H.add_edges_from([(n - 1, u), (n - 1, v),
                                  (n - 1, w1), (n - 1, w2)])
                _dedup_add(H, cands)

        # (c) Flip expansion: repeatedly flip edges to find new triangulations
        for _ in range(50):
            added = 0
            for G in list(cands):
                _, emb = planar_faces(G)
                for u, v in list(G.edges()):
                    w1, w2 = face_nbrs(emb, u, v)
                    if G.has_edge(w1, w2):
                        continue
                    H = G.copy()
                    H.remove_edge(u, v)
                    H.add_edge(w1, w2)
                    if _dedup_add(H, cands):
                        added += 1
            if added == 0:
                break

        by_n[n] = cands
        _log_count(n, cands, verbose)

    return by_n


def _log_count(n, lst, verbose):
    got = len(lst)
    exp = EXPECTED.get(n, "?")
    sym = "✓" if got == exp else f"✗ (expected {exp})"
    if verbose:
        print(f"  n={n}: {got} triangulation(s) {sym}")


# ─────────────────────────────────────────────────────────────────────
# 4. SANITY CHECKS
# ─────────────────────────────────────────────────────────────────────

def sanity_checks():
    """Run basic correctness tests before the main analysis."""
    print("Running sanity checks...")

    # Check K4 is a triangulation
    K4 = nx.complete_graph(4)
    assert is_tri(K4), "K4 should be a triangulation"

    # Check colouring enumeration on K3
    K3 = nx.complete_graph(3)
    nodes, cols = enumerate_colourings(K3, 3)
    assert len(cols) == 6, f"K3 should have 6 proper 3-colourings, got {len(cols)}"

    # Check Kempe swap preserves properness
    nodes4, cols4 = enumerate_colourings(K4, 5)
    swaps_checked = 0
    for ct in cols4[:20]:
        cd = dict(zip(nodes4, ct))
        for c1, c2 in combinations(range(1, 6), 2):
            for chain in find_kempe_chains(K4, cd, c1, c2):
                nd = do_swap(cd, chain, c1, c2)
                for u, v in K4.edges():
                    assert nd[u] != nd[v], "Kempe swap broke properness!"
                swaps_checked += 1
    print(f"  {swaps_checked} Kempe swaps verified proper ✓")

    # Check 5-colouring count of K4
    assert len(cols4) == 5 * 4 * 3 * 2, f"K4 5-colourings: expected 120, got {len(cols4)}"
    print(f"  K4 has {len(cols4)} proper 5-colourings ✓")

    print("  All sanity checks passed ✓\n")


# ─────────────────────────────────────────────────────────────────────
# 5. PHASE 1: Direct MTL check on ALL ≤4-colourings
# ─────────────────────────────────────────────────────────────────────

def phase1_check(G, v, k=5):
    """
    For vertex v of triangulation G:
    - Enumerate all proper k-colourings of G-v
    - For each colouring using ≤ k-1 colours: check if v's neighbours
      use strictly fewer colours than present (MTL property).
    """
    nbrs = sorted(G.neighbors(v))
    Gv = G.copy()
    Gv.remove_node(v)

    nodes, colourings = enumerate_colourings(Gv, k)

    stats = dict(total=len(colourings), n_leq4=0, n_5ok=0, n_5prob=0,
                 mtl_pass=0, mtl_fail=0, fail_examples=[])

    for ct in colourings:
        cd = dict(zip(nodes, ct))
        used = set(ct)
        nc = set(cd[u] for u in nbrs if u in cd)
        free_all = set(range(1, k + 1)) - nc

        if len(used) == k:
            if free_all:
                stats['n_5ok'] += 1
            else:
                stats['n_5prob'] += 1
        else:
            stats['n_leq4'] += 1
            free_in_used = used - nc
            if free_in_used:
                stats['mtl_pass'] += 1
            else:
                stats['mtl_fail'] += 1
                if len(stats['fail_examples']) < 5:
                    stats['fail_examples'].append(
                        (ct, sorted(used), sorted(nc)))

    return stats


# ─────────────────────────────────────────────────────────────────────
# 6. PHASE 2: BFS reachability from problematic 5-colourings
# ─────────────────────────────────────────────────────────────────────

def phase2_bfs(G, v, k=5, timeout=120):
    """
    Check every problematic 5-colouring of G-v (v's neighbours use all 5
    colours) can reach a "good" state via Kempe swaps.

    Uses reverse BFS from all "good" colourings (where v has ≥1 free colour).
    """
    t0 = time.time()
    nbrs = sorted(G.neighbors(v))
    Gv = G.copy()
    Gv.remove_node(v)

    nodes, colourings = enumerate_colourings(Gv, k)

    def has_free(ct):
        cd = dict(zip(nodes, ct))
        nc = set(cd[u] for u in nbrs if u in cd)
        return len(set(range(1, k + 1)) - nc) > 0

    problematic = [ct for ct in colourings if not has_free(ct)]
    if not problematic:
        return dict(n_prob=0, all_reach=True, elapsed=time.time() - t0)

    # Reverse BFS from all good colourings
    good = set(ct for ct in colourings if has_free(ct))
    visited = set(good)
    queue = deque(good)

    while queue:
        if time.time() - t0 > timeout:
            break
        ct = queue.popleft()
        cd = dict(zip(nodes, ct))
        for c1, c2 in combinations(range(1, k + 1), 2):
            for chain in find_kempe_chains(Gv, cd, c1, c2):
                nd = do_swap(cd, chain, c1, c2)
                nt = tuple(nd[n_] for n_ in nodes)
                if nt not in visited:
                    visited.add(nt)
                    queue.append(nt)

    reached = sum(1 for p in problematic if p in visited)
    timed_out = time.time() - t0 > timeout

    return dict(
        n_prob=len(problematic),
        reached=reached,
        unreached=len(problematic) - reached,
        all_reach=reached == len(problematic),
        explored=len(visited),
        timed_out=timed_out,
        elapsed=time.time() - t0,
    )


# ─────────────────────────────────────────────────────────────────────
# 7. MAIN DRIVER
# ─────────────────────────────────────────────────────────────────────

def main():
    print("=" * 70)
    print("INDEPENDENT VERIFICATION — Kempe Reconfiguration MTL Claims")
    print("Written from scratch.  No code from compute/kempe/.")
    print("=" * 70)
    print()

    sanity_checks()

    # ── Generate triangulations ──
    print("Generating planar triangulations...")
    by_n = build_triangulations(9)
    total_tri = sum(len(v) for v in by_n.values())
    print(f"  Total: {total_tri} triangulations across n=4..9\n")

    totals = dict(graphs=0, verts=0, leq4_checked=0,
                  p1_fail=0, p2_checks=0, p2_unreach=0)

    # ── Phase 1 ──
    print("=" * 70)
    print("PHASE 1: MTL check on every ≤4-colouring of G-v")
    print("=" * 70)

    for n in range(4, 10):
        tris = by_n.get(n, [])
        if not tris:
            continue
        print(f"\n── n = {n}  ({len(tris)} graph(s)) ──")

        for gi, G in enumerate(tris):
            degs = sorted(dict(G.degree()).values())
            print(f"\n  Graph {gi + 1}: degrees {degs}")
            totals['graphs'] += 1
            any_fail = False

            for v in sorted(G.nodes()):
                r = phase1_check(G, v)
                totals['verts'] += 1
                totals['leq4_checked'] += r['n_leq4']
                totals['p1_fail'] += r['mtl_fail']

                deg = len(list(G.neighbors(v)))
                tag = "✓" if r['mtl_fail'] == 0 else "✗ FAIL"
                if r['n_leq4'] == 0:
                    tag = "–"
                print(f"    v={v} deg={deg}: "
                      f"{r['total']} cols, {r['n_leq4']} ≤4c, "
                      f"{r['n_5prob']} prob | MTL {tag} "
                      f"({r['mtl_pass']}p/{r['mtl_fail']}f)")

                if r['mtl_fail'] > 0:
                    any_fail = True
                    for ex in r['fail_examples'][:2]:
                        print(f"      FAIL ex: used={ex[1]} nbr={ex[2]}")

            if not any_fail:
                print(f"  ✓ All MTL checks pass for this graph")

    # ── Phase 2 (n ≤ BFS_MAX) ──
    BFS_MAX = 8
    print(f"\n\n{'=' * 70}")
    print(f"PHASE 2: BFS reachability (n ≤ {BFS_MAX})")
    print(f"{'=' * 70}")

    for n in range(4, BFS_MAX + 1):
        tris = by_n.get(n, [])
        if not tris:
            continue
        print(f"\n── n = {n}  ({len(tris)} graph(s)) ──")

        for gi, G in enumerate(tris):
            print(f"\n  Graph {gi + 1}:")
            for v in sorted(G.nodes()):
                r = phase2_bfs(G, v, timeout=90)
                totals['p2_checks'] += 1
                if r['n_prob'] == 0:
                    print(f"    v={v}: no problematic 5-colourings")
                else:
                    totals['p2_unreach'] += r.get('unreached', 0)
                    tag = "✓ all reachable" if r['all_reach'] else "✗ UNREACHABLE"
                    extra = ""
                    if r.get('timed_out'):
                        extra = " [TIMEOUT]"
                    print(f"    v={v}: {r['n_prob']} prob, "
                          f"{r['reached']}/{r['n_prob']} reached | "
                          f"{tag}{extra}  ({r['elapsed']:.1f}s)")

    # ── Summary ──
    elapsed = time.time() - GLOBAL_START
    print(f"\n\n{'=' * 70}")
    print("SUMMARY")
    print(f"{'=' * 70}")
    print(f"Triangulations tested:     {totals['graphs']}")
    print(f"Vertex removals (Phase 1): {totals['verts']}")
    print(f"≤4-colourings checked:     {totals['leq4_checked']}")
    print(f"Phase 1 MTL failures:      {totals['p1_fail']}")
    print(f"Phase 2 BFS checks:        {totals['p2_checks']}")
    print(f"Phase 2 unreachable:       {totals['p2_unreach']}")
    print(f"Total runtime:             {elapsed:.1f}s")
    print()

    if totals['p1_fail'] == 0 and totals['p2_unreach'] == 0:
        print("VERDICT: MTL property HOLDS for ALL tested cases.")
        print("  Every ≤4-colouring of G-v leaves a free colour for v")
        print("  among the colours used.  Every problematic 5-colouring")
        print("  can reach a good state via Kempe swaps.")
    elif totals['p1_fail'] > 0 and totals['p2_unreach'] == 0:
        print("VERDICT: Phase 1 found ≤4-colourings where v has no free")
        print(f"  colour in the used set ({totals['p1_fail']} cases).")
        print("  HOWEVER, Phase 2 confirms all problematic 5-colourings")
        print("  can reach a good state.  The failing 4-colourings may")
        print("  not be reachable from problematic starts.")
    else:
        print("VERDICT: Issues found!")
        if totals['p1_fail'] > 0:
            print(f"  {totals['p1_fail']} Phase 1 MTL failures")
        if totals['p2_unreach'] > 0:
            print(f"  {totals['p2_unreach']} unreachable problematic colourings")


if __name__ == "__main__":
    main()
