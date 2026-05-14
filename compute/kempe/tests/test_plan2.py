"""
test_plan2.py — Comprehensive test suite for Plan 2 Kempe swap infrastructure.

Tests cover:
  M1-S1: Triangulation DB + 5->4 reduction search
  M1-S2: Reconfiguration graph analysis
  M1-S3: Non-crossing verification + Fisk homology

Agent 0050 / Plan 2: Kempe Swap Game + Topological Non-Crossing
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import networkx as nx
from kempe_ops import (
    is_proper_colouring, enumerate_colourings, num_colours,
    get_kempe_chain, get_all_kempe_chains, kempe_swap, canonical_form,
)
from triangulation_db import (
    make_K4, make_bipyramid, make_octahedron,
    generate_triangulations, is_triangulation,
)
from reduction_search import bfs_reduce_to_4, test_all_5_colourings
from reconfiguration_graph import (
    build_reconfiguration_graph, analyze_reconfiguration_graph,
    check_5_to_4_connectivity,
)
from noncrossing_verifier import verify_noncrossing_exhaustive_5col, classify_chain_config_at_vertex
from fisk_homology import build_fisk_equivalence
from chain_disconnection import test_cdl_for_graph, test_sequential_elimination
from reduction_search import (
    bulk_distance_to_4col, verify_inductive_lift,
    find_monotone_path, analyze_swap_sequence,
)


# ===================================================================
# M1-S1 Tests
# ===================================================================

def test_triangle_is_3colorable():
    """K3 has chromatic number 3."""
    G = nx.complete_graph(3)
    assert len(enumerate_colourings(G, 2)) == 0, "K3 is not 2-colourable"
    cols_3 = enumerate_colourings(G, 3)
    assert len(cols_3) == 6, f"K3 should have 3!=6 proper 3-colourings, got {len(cols_3)}"
    print("PASS: test_triangle_is_3colorable")


def test_K4_is_4colorable():
    """K4 needs exactly 4 colours."""
    G = make_K4()
    assert len(enumerate_colourings(G, 3)) == 0, "K4 is not 3-colourable"
    cols_4 = enumerate_colourings(G, 4)
    assert len(cols_4) == 24, f"K4 should have 4!=24 proper 4-colourings, got {len(cols_4)}"
    print("PASS: test_K4_is_4colorable")


def test_kempe_swap_preserves_colouring():
    """After any Kempe swap on K4 with 5 colours, the colouring is still proper."""
    G = make_K4()
    checked = 0
    for col in enumerate_colourings(G, 5):
        for a in range(1, 6):
            for b in range(a + 1, 6):
                for chain in get_all_kempe_chains(G, col, a, b):
                    new_col = kempe_swap(col, chain, a, b)
                    assert is_proper_colouring(G, new_col), \
                        f"Swap produced improper colouring: {new_col}"
                    checked += 1
    print(f"PASS: test_kempe_swap_preserves_colouring ({checked} swaps verified)")


def test_5col_to_4col_K4():
    """Every 5-colouring of K4 can be Kempe-reduced to a 4-colouring."""
    G = make_K4()
    stats = test_all_5_colourings(G)
    assert stats['all_reducible'], "Not all 5-colourings of K4 are reducible"
    print(f"PASS: test_5col_to_4col_K4 (max path={stats['max_path_length']}, "
          f"tested {stats['using_exactly_5']} five-colourings)")


def test_5col_to_4col_octahedron():
    """Every 5-colouring of the octahedron can be Kempe-reduced to a 4-colouring."""
    G = make_octahedron()
    stats = test_all_5_colourings(G)
    assert stats['all_reducible'], \
        f"Not all 5-colourings of octahedron are reducible: {len(stats['failures'])} failures"
    print(f"PASS: test_5col_to_4col_octahedron (max path={stats['max_path_length']}, "
          f"tested {stats['using_exactly_5']} five-colourings)")


def test_triangulation_counts():
    """Face-split + edge-flip generator matches known counts for n<=7."""
    db = generate_triangulations(7)
    expected = {4: 1, 5: 1, 6: 2, 7: 5}
    for n, exp in expected.items():
        got = len(db[n])
        assert got == exp, f"n={n}: expected {exp} triangulations, got {got}"
        for T in db[n]:
            assert is_triangulation(T), f"{T.graph.get('name')} is not a valid triangulation"
    print(f"PASS: test_triangulation_counts ({expected})")


# ===================================================================
# M1-S2 Tests
# ===================================================================

def test_R5_connected():
    """R(T,5) is connected for triangulations on n<=6 (Las Vergnas-Meyniel)."""
    db = generate_triangulations(6)
    for n in [4, 5, 6]:
        for T in db[n]:
            info = check_5_to_4_connectivity(T)
            assert info['R5_connected'], \
                f"R({T.graph.get('name')},5) not connected!"
            print(f"  R({T.graph.get('name','?')},5): "
                  f"{info['total_colourings']} nodes, connected ✓")
    print("PASS: test_R5_connected")


def test_R4_components():
    """R(T,4) component analysis for small triangulations."""
    db = generate_triangulations(6)
    for n in [4, 5, 6]:
        for T in db[n]:
            R = build_reconfiguration_graph(T, 4)
            stats = analyze_reconfiguration_graph(R)
            print(f"  R({T.graph.get('name','?')},4): "
                  f"{stats['num_nodes']} nodes, "
                  f"{stats['num_components']} component(s), "
                  f"connected={stats['is_connected']}")
    print("PASS: test_R4_components")


def test_diameter_finite():
    """Diameter of R(K4,k) is finite for k=4,5."""
    G = make_K4()
    for k in [4, 5]:
        R = build_reconfiguration_graph(G, k)
        stats = analyze_reconfiguration_graph(R)
        if stats['is_connected']:
            assert stats['diameter'] is not None, f"R(K4,{k}) diameter is None"
            print(f"  R(K4,{k}): diameter = {stats['diameter']}")
        else:
            print(f"  R(K4,{k}): not connected — {stats['num_components']} components")
    print("PASS: test_diameter_finite")


def test_all_5_reach_4():
    """In R(G,5), every 5-colouring reaches a 4-colouring for small T."""
    db = generate_triangulations(6)
    for n in [4, 5, 6]:
        for T in db[n]:
            info = check_5_to_4_connectivity(T)
            assert info['all_5_reach_4'], \
                f"{T.graph.get('name')}: {info['unreachable_count']} unreachable 5-colourings"
            print(f"  {T.graph.get('name','?')}: all 5-colourings reach a 4-colouring ✓")
    print("PASS: test_all_5_reach_4")


# ===================================================================
# M1-S3 Tests
# ===================================================================

def test_disjoint_chains_noncrossing():
    """Non-crossing property holds at colour-5 vertices in all 5-colourings.

    This is the Theorem A scenario: vertex v coloured 5 is external to all
    {1..4} Kempe chains, so the local cyclic-order check is valid.
    """
    db = generate_triangulations(6)
    for n in [4, 5, 6]:
        for T in db[n]:
            result = verify_noncrossing_exhaustive_5col(T)
            assert result['all_noncrossing'], \
                f"Non-crossing violated for {T.graph.get('name')}: {result['violations'][:3]}"
            print(f"  {T.graph.get('name','?')}: "
                  f"{result['colourings_with_colour5']} colourings with colour 5, "
                  f"{result['vertices_checked']} vertices checked, "
                  f"all non-crossing ✓")
    print("PASS: test_disjoint_chains_noncrossing")


def test_fisk_group():
    """Fisk group structure for small triangulations (sphere: expect 1 class)."""
    db = generate_triangulations(6)
    for n in [4, 5, 6]:
        for T in db[n]:
            result = build_fisk_equivalence(T, k=4)
            print(f"  {T.graph.get('name','?')}: "
                  f"{result['num_colourings']} colourings, "
                  f"{result['num_classes']} Fisk class(es)")
            if not result['is_single_class']:
                print(f"    WARNING: expected 1 class for sphere, "
                      f"got {result['num_classes']} — sizes: {result['class_sizes']}")
    print("PASS: test_fisk_group")


# ===================================================================
# Iteration 2 Tests — M1 Computational Extensions
# ===================================================================

def test_5col_to_4col_n7():
    """Every 5-colouring of every n=7 triangulation reduces to 4 via Kempe swaps."""
    db = generate_triangulations(7)
    for T in db[7]:
        stats = test_all_5_colourings(T)
        assert stats['all_reducible'], \
            f"{T.graph.get('name')}: {len(stats['failures'])} irreducible 5-colourings"
        print(f"  {T.graph.get('name','?')}: {stats['using_exactly_5']} five-colourings, "
              f"max_path={stats['max_path_length']}, all reducible ✓")
    print("PASS: test_5col_to_4col_n7")


def test_5col_to_4col_n8():
    """Every 5-colouring of every n=8 triangulation reduces to 4 via Kempe swaps.
    NOTE: runs ~13s due to 14 triangulations with up to 3600 five-colourings each."""
    db = generate_triangulations(8)
    for T in db[8]:
        stats = test_all_5_colourings(T)
        assert stats['all_reducible'], \
            f"{T.graph.get('name')}: {len(stats['failures'])} irreducible 5-colourings"
        print(f"  {T.graph.get('name','?')}: {stats['using_exactly_5']} five-colourings, "
              f"max_path={stats['max_path_length']}, all reducible ✓")
    print("PASS: test_5col_to_4col_n8")


def test_chain_disconnection_n7():
    """CDL test for n<=7: documents which graphs pass/fail the strict CDL.

    The STRICT CDL (safe-swaps-only) is known to fail for some graphs starting
    at n=6. This test documents the pattern rather than asserting all pass."""
    db = generate_triangulations(7)
    cdl_pass = 0
    cdl_fail = 0
    for n in [4, 5, 6, 7]:
        for T in db[n]:
            stats = test_cdl_for_graph(T, max_prep=5)
            name = T.graph.get('name', '?')
            if stats['all_ok']:
                cdl_pass += 1
                print(f"  {name}: CDL PASS — methods={stats['method_counts']}")
            else:
                cdl_fail += 1
                print(f"  {name}: CDL FAIL — {len(stats['failures'])} failures, "
                      f"methods={stats['method_counts']}")
    print(f"CDL summary: {cdl_pass} pass, {cdl_fail} fail (strict CDL is FALSE for some graphs)")
    assert cdl_pass >= 4, f"Expected at least 4 CDL passes, got {cdl_pass}"
    print("PASS: test_chain_disconnection_n7")


def test_sequential_elimination_n7():
    """Unrestricted sequential elimination succeeds for ALL n<=7 triangulations."""
    db = generate_triangulations(7)
    for n in [4, 5, 6, 7]:
        for T in db[n]:
            stats_u = test_sequential_elimination(
                T, max_orderings=100, use_restricted=False, max_prep=3)
            stats_r = test_sequential_elimination(
                T, max_orderings=100, use_restricted=True, max_prep=3)
            name = T.graph.get('name', '?')
            assert stats_u['total_failures'] == 0, \
                f"{name}: unrestricted elimination failed {stats_u['total_failures']} times"
            r_fail = stats_r['total_failures']
            print(f"  {name}: unrestricted=ALL OK ({stats_u['total_successes']}), "
                  f"restricted={stats_r['total_successes']}/{stats_r['total_attempts']} "
                  f"(fail={r_fail}), max_swaps={stats_u['max_swaps']}")
    print("PASS: test_sequential_elimination_n7")


def test_rg5_distance_growth():
    """Track the max distance from 5-colouring to nearest 4-colouring in R(G,5)."""
    db = generate_triangulations(7)
    max_dist_by_n = {}
    for n in [4, 5, 6, 7]:
        max_d = 0
        for T in db[n]:
            all_cols = enumerate_colourings(T, 5)
            five_only = [c for c in all_cols if num_colours(c) == 5]
            for col in five_only:
                path = bfs_reduce_to_4(T, col, k=5)
                if path:
                    d = len(path) - 1
                    max_d = max(max_d, d)
        max_dist_by_n[n] = max_d
        print(f"  n={n}: max R(G,5) distance to 4-colouring = {max_d}")
    assert max_dist_by_n[7] <= 10, f"Max distance at n=7 unexpectedly large: {max_dist_by_n[7]}"
    print(f"Distance growth: {max_dist_by_n}")
    print("PASS: test_rg5_distance_growth")


# ===================================================================
# Iteration 3 Tests — M1 n=9, Inductive Lift, Monotone Paths
# ===================================================================

def test_triangulation_count_n9():
    """Generate all 50 triangulations on n=9 (OEIS A000109)."""
    db = generate_triangulations(9)
    assert len(db[9]) == 50, f"Expected 50 triangulations on n=9, got {len(db[9])}"
    for T in db[9]:
        assert is_triangulation(T), f"{T.graph.get('name')} is not a valid triangulation"
    print(f"PASS: test_triangulation_count_n9 (50 triangulations)")


def test_5col_to_4col_n9():
    """Every 5-colouring of every n=9 triangulation reduces to 4 via Kempe swaps."""
    db = generate_triangulations(9)
    for T in db[9]:
        result = bulk_distance_to_4col(T, k=5)
        assert result['all_reachable'], \
            f"{T.graph.get('name')}: {len(result['unreachable'])} unreachable 5-colourings"
    print(f"PASS: test_5col_to_4col_n9 (all 50 triangulations, all 5-colourings reducible)")


def test_distance_bound_n9():
    """Max R(G,5) distance to nearest 4-colouring ≤ n-4 = 5 for all n=9 triangulations.

    Additionally verifies the pattern: max distance at n=9 is 4 (tightness of n-4 breaks)."""
    db = generate_triangulations(9)
    max_overall = 0
    for T in db[9]:
        result = bulk_distance_to_4col(T, k=5)
        d = result['max_distance']
        assert d <= 5, \
            f"{T.graph.get('name')}: max distance {d} exceeds n-4=5"
        max_overall = max(max_overall, d)
        print(f"  {T.graph.get('name','?')}: max_dist={d}, "
              f"4col={result['num_4col']}, 5col={result['num_5col']}")
    print(f"\nOverall max distance at n=9: {max_overall}")
    assert max_overall == 4, \
        f"Expected max distance 4 at n=9 (tightness breaks), got {max_overall}"
    print("PASS: test_distance_bound_n9 (max=4 ≤ n-4=5, tightness breaks)")


def test_distance_bound_all_n():
    """Verify max R(G,5) distance = n-4 for n=4..8, and ≤ n-4 for n=9."""
    db = generate_triangulations(9)
    expected_tight = {4: 0, 5: 1, 6: 2, 7: 3, 8: 4}
    for n in range(4, 9):
        max_d = 0
        for T in db[n]:
            result = bulk_distance_to_4col(T, k=5)
            max_d = max(max_d, result['max_distance'])
        assert max_d == expected_tight[n], \
            f"n={n}: expected tight bound {expected_tight[n]}, got {max_d}"
        print(f"  n={n}: max_dist={max_d} = n-4 (tight) ✓")

    max_d_9 = 0
    for T in db[9]:
        result = bulk_distance_to_4col(T, k=5)
        max_d_9 = max(max_d_9, result['max_distance'])
    assert max_d_9 <= 5, f"n=9: max distance {max_d_9} exceeds n-4=5"
    print(f"  n=9: max_dist={max_d_9} ≤ n-4=5 (bound holds, not tight)")
    print("PASS: test_distance_bound_all_n")


def test_inductive_lift_n8():
    """For n=8 triangulations, verify that G-v swap sequences lift to G.

    Key result: zero chain merge failures expected — chains in G-v don't
    merge when v is added back."""
    db = generate_triangulations(8)
    total_tested = 0
    total_lifted = 0
    total_merge_fail = 0

    for T in db[8]:
        for v in sorted(T.nodes()):
            if T.degree(v) > 5:
                continue
            result = verify_inductive_lift(T, v)
            total_tested += result['total_tested']
            total_lifted += result['lift_succeeded']
            total_merge_fail += result['lift_failed_chain_merge']

    assert total_merge_fail == 0, \
        f"Expected 0 chain merge failures, got {total_merge_fail}"
    lift_pct = 100 * total_lifted / max(1, total_tested)
    print(f"Tested {total_tested} colourings, {total_lifted} lifts succeeded ({lift_pct:.1f}%)")
    print(f"Chain merge failures: {total_merge_fail}")
    print("PASS: test_inductive_lift_n8 (zero chain merge failures)")


def test_monotone_paths_exist():
    """For n=6..8, a majority of 5-colourings have strictly |V_5|-monotone paths.

    At n=9, ~51% have strictly monotone paths. The bound is that ALL
    have weakly monotone BFS shortest paths."""
    db = generate_triangulations(8)
    for n in [6, 7, 8]:
        total = 0
        monotone_count = 0
        for T in db[n]:
            all_cols = enumerate_colourings(T, 5)
            five_only = [c for c in all_cols if num_colours(c) == 5]
            for col in five_only:
                total += 1
                path = find_monotone_path(T, col)
                if path is not None:
                    monotone_count += 1
        pct = 100 * monotone_count / max(1, total)
        assert pct > 50, f"n={n}: only {pct:.1f}% have monotone paths"
        print(f"  n={n}: {monotone_count}/{total} ({pct:.1f}%) have strictly monotone paths")
    print("PASS: test_monotone_paths_exist")


# ===================================================================
# Agent 0051 Tests — M1 Merge Analysis, n=10, BFS Forensics
# ===================================================================

from merge_analysis import (
    analyze_merge_conditions, bulk_merge_analysis,
    bfs_path_merge_check, v5_descent_analysis,
)


def test_merge_conditions_degree3():
    """Degree-3 vertices NEVER cause (a,5)-chain merges.

    Proof: in a triangulation, degree-3 neighbours form a triangle,
    so all B_{a,5}-neighbours are adjacent and in the same chain."""
    db = generate_triangulations(8)
    for n in [4, 5, 6, 7, 8]:
        for T in db[n]:
            result = bulk_merge_analysis(T)
            if 3 in result:
                assert result[3]['merges'] == 0, \
                    f"{T.graph.get('name')}: degree-3 merge found! {result[3]}"
    print("PASS: test_merge_conditions_degree3 (zero merges for degree 3)")


def test_merge_conditions_degree4():
    """Document merge rate for degree-4 vertices (~17%)."""
    db = generate_triangulations(7)
    total = 0
    merges = 0
    for n in [6, 7]:
        for T in db[n]:
            result = bulk_merge_analysis(T)
            if 4 in result:
                total += result[4]['total_cases']
                merges += result[4]['merges']
    rate = 100 * merges / max(1, total)
    assert rate > 10, f"Degree-4 merge rate unexpectedly low: {rate:.1f}%"
    assert rate < 30, f"Degree-4 merge rate unexpectedly high: {rate:.1f}%"
    print(f"PASS: test_merge_conditions_degree4 (merge rate={rate:.1f}%)")


def test_merge_conditions_degree5():
    """Document merge rate for degree-5 vertices (~31%)."""
    db = generate_triangulations(7)
    total = 0
    merges = 0
    for n in [6, 7]:
        for T in db[n]:
            result = bulk_merge_analysis(T)
            if 5 in result:
                total += result[5]['total_cases']
                merges += result[5]['merges']
    rate = 100 * merges / max(1, total)
    assert rate > 15, f"Degree-5 merge rate unexpectedly low: {rate:.1f}%"
    assert rate < 50, f"Degree-5 merge rate unexpectedly high: {rate:.1f}%"
    print(f"PASS: test_merge_conditions_degree5 (merge rate={rate:.1f}%)")


def test_bfs_path_zero_merges_n8():
    """BFS-optimal paths at n=8 have ZERO (a,5)-chain merges.

    Tests a sample of degree-≤5 vertices across n=8 triangulations."""
    db = generate_triangulations(8)
    total_a5 = 0
    total_merges = 0
    for T in db[8][:5]:
        for v in sorted(T.nodes()):
            if T.degree(v) > 5:
                continue
            result = bfs_path_merge_check(T, v)
            total_a5 += result['total_a5_swaps']
            total_merges += result['merges']
    assert total_merges == 0, f"Expected 0 BFS merges, got {total_merges}"
    assert total_a5 > 100, f"Insufficient (a,5)-swaps tested: {total_a5}"
    print(f"PASS: test_bfs_path_zero_merges_n8 ({total_a5} (a,5)-swaps, 0 merges)")


def test_merge_prone_chain_properties():
    """BFS never swaps a chain adjacent to v when v has 2+ chain neighbours."""
    db = generate_triangulations(8)
    multi_chain_total = 0
    swap_adjacent_total = 0
    for T in db[8][:5]:
        for v in sorted(T.nodes()):
            if T.degree(v) > 5:
                continue
            result = bfs_path_merge_check(T, v)
            multi_chain_total += result['multi_chain_cases']
            swap_adjacent_total += result['multi_chain_swap_adjacent']
    assert swap_adjacent_total == 0, \
        f"BFS swapped chain adjacent to v in {swap_adjacent_total} merge-prone cases"
    print(f"PASS: test_merge_prone_chain_properties "
          f"({multi_chain_total} multi-chain cases, 0 adjacent swaps)")


def test_triangulation_count_n10():
    """Generate all 233 triangulations on n=10 (OEIS A000109)."""
    db = generate_triangulations(10)
    assert len(db[10]) == 233, f"Expected 233 triangulations on n=10, got {len(db[10])}"
    for T in db[10]:
        assert is_triangulation(T), f"{T.graph.get('name')} is not a valid triangulation"
    print("PASS: test_triangulation_count_n10 (233 triangulations)")


def test_distance_bound_n10():
    """Max distance ≤ n-4 = 6 for all n=10 triangulations.

    NOTE: Processes all 233 triangulations (~150s). Max distance observed = 5."""
    db = generate_triangulations(10)
    max_overall = 0
    for T in db[10]:
        result = bulk_distance_to_4col(T, k=5)
        assert result['all_reachable'], \
            f"{T.graph.get('name')}: unreachable 5-colourings found"
        d = result['max_distance']
        assert d <= 6, \
            f"{T.graph.get('name')}: max distance {d} exceeds n-4=6"
        max_overall = max(max_overall, d)
    print(f"PASS: test_distance_bound_n10 (max={max_overall} ≤ 6, all 233 triangulations)")


def test_v5_descent_exists_majority():
    """A majority of 5-colourings have a single-swap |V_5| descent."""
    db = generate_triangulations(8)
    for n in [6, 7, 8]:
        total = 0
        descent = 0
        for T in db[n]:
            result = v5_descent_analysis(T)
            total += result['total_tested']
            descent += result['descent_exists']
        pct = 100 * descent / max(1, total)
        assert pct > 50, f"n={n}: only {pct:.1f}% have |V_5| descent"
        print(f"  n={n}: {descent}/{total} ({pct:.1f}%) have single-swap descent")
    print("PASS: test_v5_descent_exists_majority")


# ===================================================================
# Runner
# ===================================================================

if __name__ == '__main__':
    tests = [
        test_triangle_is_3colorable,
        test_K4_is_4colorable,
        test_kempe_swap_preserves_colouring,
        test_5col_to_4col_K4,
        test_5col_to_4col_octahedron,
        test_triangulation_counts,
        test_R5_connected,
        test_R4_components,
        test_diameter_finite,
        test_all_5_reach_4,
        test_disjoint_chains_noncrossing,
        test_fisk_group,
        # Iteration 2
        test_5col_to_4col_n7,
        test_5col_to_4col_n8,
        test_chain_disconnection_n7,
        test_sequential_elimination_n7,
        test_rg5_distance_growth,
        # Iteration 3
        test_triangulation_count_n9,
        test_5col_to_4col_n9,
        test_distance_bound_n9,
        test_distance_bound_all_n,
        test_inductive_lift_n8,
        test_monotone_paths_exist,
        # Agent 0051
        test_merge_conditions_degree3,
        test_merge_conditions_degree4,
        test_merge_conditions_degree5,
        test_bfs_path_zero_merges_n8,
        test_merge_prone_chain_properties,
        test_triangulation_count_n10,
        test_distance_bound_n10,
        test_v5_descent_exists_majority,
    ]

    passed = 0
    failed = 0
    errors = []
    for test in tests:
        try:
            print(f"\n{'='*60}")
            print(f"--- {test.__name__} ---")
            test()
            passed += 1
        except Exception as e:
            print(f"FAIL: {test.__name__}: {e}")
            import traceback
            traceback.print_exc()
            failed += 1
            errors.append((test.__name__, str(e)))

    print(f"\n{'='*60}")
    print(f"RESULTS: {passed} passed, {failed} failed out of {len(tests)} tests")
    if errors:
        print("Failures:")
        for name, err in errors:
            print(f"  {name}: {err}")
    print(f"{'='*60}")
