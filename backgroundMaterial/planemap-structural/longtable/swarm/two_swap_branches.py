"""Ordered pairs of Kempe swaps on the 21-vertex witness.

The hole is vertex 1, of degree 9, so this does not build a mass_core.RootState
and does not enumerate deletion colourings.  Graph loading, colour canonicalisation,
and the bichromatic-component walk follow mass_core.
"""

from __future__ import annotations

import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from mass_core import PAIRS, canon, parse_ascii

ASCII = (
    "21 bcdef,aflghijkc,abkmd,acmnoe,adopqf,aeqlb,blrsh,bgsoi,bhotj,"
    "bituk,bjumc,bfqrg,ckund,dmuto,dntihspe,eosrq,eprlf,glqps,grpoh,ionuj,jtnmk"
)
HOLE = 1
START = (0, None, 1, 2, 1, 2, 0, 1, 2, 0, 3, 3, 0, 1, 0, 2, 0, 1, 3, 3, 2)

# The sixteen non-global swaps recorded in two-kempe-kill.md.
EXPECTED = [
    ((0, 1), frozenset({0, 2, 4, 6, 7, 12, 13, 14, 16, 17})),
    ((0, 1), frozenset({9})),
    ((0, 2), frozenset({0, 3, 5, 8, 9, 12, 14, 15, 16, 20})),
    ((0, 2), frozenset({6})),
    ((0, 3), frozenset({0})),
    ((0, 3), frozenset({6, 9, 10, 11, 12, 14, 16, 18, 19})),
    ((1, 2), frozenset({2, 3, 4, 5, 13, 15, 17, 20})),
    ((1, 2), frozenset({7, 8})),
    ((1, 3), frozenset({2, 10})),
    ((1, 3), frozenset({4})),
    ((1, 3), frozenset({7, 11, 17, 18})),
    ((1, 3), frozenset({13, 19})),
    ((2, 3), frozenset({3})),
    ((2, 3), frozenset({5, 11})),
    ((2, 3), frozenset({8, 10, 19, 20})),
    ((2, 3), frozenset({15, 18})),
]


def coloured_tuple(col: tuple) -> tuple:
    return tuple(c for v, c in enumerate(col) if v != HOLE)


def sorted_counts(col: tuple) -> tuple:
    return tuple(sorted(Counter(coloured_tuple(col)).values()))


def proper(rot, col: tuple) -> bool:
    for v, c in enumerate(col):
        if c is None:
            continue
        for w in rot[v]:
            if w != HOLE and col[w] == c and w > v:
                return False
    return True


def components(rot, col: tuple) -> list[dict]:
    """Bichromatic components of T minus the hole, in the mass_core pair order.

    A component is global when it is the only component of its colour pair:
    swapping it renames the two colours everywhere.
    """
    adj = {v: [w for w in rot[v] if w != HOLE] for v in range(len(rot)) if v != HOLE}
    found = []
    for a, b in PAIRS:
        pending = {v for v, c in enumerate(col) if c in (a, b)}
        comps = []
        while pending:
            seed = min(pending)
            pending.remove(seed)
            comp = {seed}
            stack = [seed]
            while stack:
                i = stack.pop()
                for j in adj[i]:
                    if j in pending:
                        pending.remove(j)
                        comp.add(j)
                        stack.append(j)
            comps.append(frozenset(comp))
        global_pair = len(comps) == 1
        for comp in comps:
            na = sum(col[v] == a for v in comp)
            nb = sum(col[v] == b for v in comp)
            found.append({
                "pair": (a, b),
                "comp": comp,
                "global": global_pair,
                "imbalance": abs(na - nb),
            })
    return found


def nonglobal(rot, col: tuple) -> list[dict]:
    return [m for m in components(rot, col) if not m["global"]]


def apply_swap(col: tuple, move: dict) -> tuple:
    a, b = move["pair"]
    out = list(col)
    for v in move["comp"]:
        if out[v] == a:
            out[v] = b
        elif out[v] == b:
            out[v] = a
        else:
            raise AssertionError(f"vertex {v} has colour {out[v]} outside {(a, b)}")
    return tuple(out)


def link_view(rot, col: tuple) -> dict:
    link = list(rot[HOLE])
    colours = [col[v] for v in link]
    cnt = Counter(colours)
    unique = [v for v in link if cnt[col[v]] == 1]
    n_colours = len(cnt)
    frozen = n_colours == 4 and not unique
    return {
        "link": link,
        "colours": tuple(colours),
        "counts": dict(sorted(cnt.items())),
        "n_colours": n_colours,
        "unique": unique,
        "frozen": frozen,
        "fill": n_colours <= 3,
        "has_unique": bool(unique),
    }


def key(move: dict) -> tuple:
    return (move["pair"], tuple(sorted(move["comp"])))


def fmt_move(move: dict) -> str:
    verts = ",".join(str(v) for v in sorted(move["comp"]))
    a, b = move["pair"]
    return f"({a},{b}) on {{{verts}}}"


def main() -> None:
    rot = parse_ascii(ASCII)
    assert len(rot[HOLE]) == 9
    assert [len(rot[v]) for v in range(21)] == [
        5, 9, 5, 6, 6, 5, 5, 5, 5, 5, 5, 5, 5, 5, 8, 5, 5, 5, 5, 5, 5,
    ]
    assert proper(rot, START)
    assert coloured_tuple(START) == (
        0, 1, 2, 1, 2, 0, 1, 2, 0, 3, 3, 0, 1, 0, 2, 0, 1, 3, 3, 2,
    )
    assert canon(coloured_tuple(START)) == coloured_tuple(START)
    start_link = link_view(rot, START)
    assert start_link["colours"] == (0, 2, 3, 0, 1, 2, 0, 3, 1)
    assert start_link["frozen"]
    assert sorted_counts(START) == (4, 5, 5, 6)

    moves = nonglobal(rot, START)
    got = [(m["pair"], m["comp"]) for m in moves]
    assert got == EXPECTED, got
    assert all(link_view(rot, apply_swap(START, m))["frozen"] for m in moves)
    globals_at_start = [m for m in components(rot, START) if m["global"]]
    assert globals_at_start == []

    # The published two-swap escape: (0,3) on {0}, then (0,1) on the named set.
    first = next(m for m in moves if m["pair"] == (0, 3) and m["comp"] == frozenset({0}))
    mid = apply_swap(START, first)
    assert sorted_counts(mid) == (5, 5, 5, 5)
    assert link_view(rot, mid)["colours"] == (3, 2, 3, 0, 1, 2, 0, 3, 1)
    second_set = frozenset({2, 4, 6, 7, 12, 13, 14, 16, 17})
    second = next(
        m for m in nonglobal(rot, mid)
        if m["pair"] == (0, 1) and m["comp"] == second_set
    )
    escaped = apply_swap(mid, second)
    esc_link = link_view(rot, escaped)
    assert esc_link["colours"] == (3, 2, 3, 1, 0, 2, 0, 3, 0)
    assert esc_link["unique"] == [6]
    assert sorted_counts(escaped) == (4, 5, 5, 6)
    # Slide 1 -> 6, then colour 2 is missing on the link of 6.
    assert list(rot[6]) == [1, 11, 17, 18, 7]
    slid = [escaped[w] if w != HOLE else escaped[6] for w in rot[6]]
    assert slid == [1, 3, 0, 3, 0]

    start_canon = canon(coloured_tuple(START))
    one_canons = {canon(coloured_tuple(apply_swap(START, m))) for m in moves}

    rows = []
    second_sizes = []
    omitted_global = 0
    omitted_global_frozen = 0
    for m1 in moves:
        col1 = apply_swap(START, m1)
        all2 = components(rot, col1)
        swaps2 = [m for m in all2 if not m["global"]]
        second_sizes.append(len(swaps2))
        for m in all2:
            if m["global"]:
                omitted_global += 1
                if link_view(rot, apply_swap(col1, m))["frozen"]:
                    omitted_global_frozen += 1
        pop1 = sorted_counts(col1) != sorted_counts(START)
        for m2 in swaps2:
            col2 = apply_swap(col1, m2)
            view = link_view(rot, col2)
            can = canon(coloured_tuple(col2))
            rows.append({
                "m1": m1,
                "m2": m2,
                "col": col2,
                "view": view,
                "canon": can,
                "pop1": pop1,
                "pop2": sorted_counts(col2) != sorted_counts(col1),
                "undo": col2 == START,
                "canon_start": can == start_canon,
                "canon_one": can in one_canons,
                "sorted": sorted_counts(col2),
            })

    def third_stats(col: tuple) -> tuple[int, int]:
        swaps3 = nonglobal(rot, col)
        escapes = 0
        for m3 in swaps3:
            if not link_view(rot, apply_swap(col, m3))["frozen"]:
                escapes += 1
        return escapes, len(swaps3)

    # Cache third-swap stats by the concrete colouring.
    third_cache: dict[tuple, tuple[int, int]] = {}
    for row in rows:
        if row["view"]["frozen"] and row["col"] not in third_cache:
            third_cache[row["col"]] = third_stats(row["col"])
        if row["view"]["frozen"]:
            esc, total = third_cache[row["col"]]
            row["third_escape"] = esc
            row["third_total"] = total

    frozen = [r for r in rows if r["view"]["frozen"]]
    escape = [r for r in rows if not r["view"]["frozen"]]
    assert len(frozen) + len(escape) == len(rows)

    print("ordered_pairs", len(rows))
    print("second_swap_counts", sorted(set(second_sizes)), "per_first", second_sizes)
    print("omitted_global_second_swaps", omitted_global, "of_which_frozen", omitted_global_frozen)
    print("frozen", len(frozen), "escape", len(escape))
    print("escape_fill", sum(r["view"]["fill"] for r in escape))
    print("escape_unique", sum(r["view"]["has_unique"] for r in escape))
    print("escape_both", sum(r["view"]["fill"] and r["view"]["has_unique"] for r in escape))
    print("escape_unique_only", sum(r["view"]["has_unique"] and not r["view"]["fill"] for r in escape))
    print("escape_fill_only", sum(r["view"]["fill"] and not r["view"]["has_unique"] for r in escape))
    print("frozen_exact_undo", sum(r["undo"] for r in frozen))
    print("frozen_canon_start", sum(r["canon_start"] for r in frozen))
    print("frozen_canon_one_not_start", sum(r["canon_one"] and not r["canon_start"] for r in frozen))
    print("frozen_new", sum(not r["canon_start"] and not r["canon_one"] for r in frozen))

    # Population cross-tab on the sixteen, then on pairs.
    pop_changed = []
    for m in moves:
        changed = sorted_counts(apply_swap(START, m)) != sorted_counts(START)
        pop_changed.append(changed)
        print("first", fmt_move(m), "imbalance", m["imbalance"], "pop_changes", changed)
    print("first_pop_changing", sum(pop_changed))

    def pop_key(r):
        return ("chg" if r["pop1"] else "keep", "chg" if r["pop2"] else "keep")

    buckets = {}
    for r in rows:
        k = pop_key(r) + ("frozen" if r["view"]["frozen"] else "escape",)
        buckets[k] = buckets.get(k, 0) + 1
    for k in sorted(buckets):
        print("bucket", k, buckets[k])

    # Distinct frozen colourings.
    by_col: dict[tuple, list] = {}
    for r in frozen:
        by_col.setdefault(r["col"], []).append(r)
    print("distinct_frozen_colourings", len(by_col))
    by_canon: dict[tuple, list] = {}
    for r in frozen:
        by_canon.setdefault(r["canon"], []).append(r)
    print("distinct_frozen_canons", len(by_canon))

    third_pairs_unlock = sum(r["third_escape"] > 0 for r in frozen)
    third_pairs_stuck = sum(r["third_escape"] == 0 for r in frozen)
    print("frozen_pairs_with_third_escape", third_pairs_unlock)
    print("frozen_pairs_all_third_frozen", third_pairs_stuck)

    # Per canonical frozen state: one representative and third-swap behaviour.
    print("--- frozen canons ---")
    for can, group in sorted(by_canon.items(), key=lambda kv: (-len(kv[1]), kv[0])):
        rep = group[0]
        kinds = {
            "undo": sum(r["undo"] for r in group),
            "canon_start": sum(r["canon_start"] for r in group),
            "canon_one": sum(r["canon_one"] for r in group),
        }
        print(
            "canon_pairs", len(group),
            "colours", rep["view"]["colours"],
            "sorted", rep["sorted"],
            "third", rep["third_escape"], "/", rep["third_total"],
            "kinds", kinds,
            "example", fmt_move(rep["m1"]), "then", fmt_move(rep["m2"]),
        )

    # Escapes that are the published pair, and a few other escape shapes.
    published = [
        r for r in escape
        if r["m1"]["comp"] == frozenset({0}) and r["m1"]["pair"] == (0, 3)
        and r["m2"]["comp"] == second_set and r["m2"]["pair"] == (0, 1)
    ]
    print("published_escape_rows", len(published))

    esc_canons = {}
    for r in escape:
        esc_canons.setdefault(r["canon"], []).append(r)
    print("distinct_escape_canons", len(esc_canons))
    print("distinct_escape_colourings", len({r["col"] for r in escape}))
    fill_counts = Counter(r["view"]["n_colours"] for r in escape)
    print("escape_n_colours", dict(fill_counts))
    uniq_sizes = Counter(len(r["view"]["unique"]) for r in escape)
    print("escape_n_unique_vertices", dict(uniq_sizes))

    # Among escapes, how many slides of a unique vertex immediately miss a colour.
    immediate = 0
    for r in escape:
        col = r["col"]
        view = r["view"]
        if view["fill"]:
            immediate += 1
            continue
        for v in view["unique"]:
            cols = [col[w] if w != HOLE else col[v] for w in rot[v]]
            if len(set(cols)) <= 3:
                immediate += 1
                break
    print("escape_pairs_with_immediate_fill_or_direct", immediate)

    # Third-swap witness on a frozen colouring that is not the start.
    new_frozen = [r for r in frozen if not r["canon_start"]]
    print("new_frozen_pairs", len(new_frozen))
    if new_frozen:
        # Prefer a representative whose third swaps are not all frozen, and one whose are.
        unlock = next((r for r in new_frozen if r["third_escape"] > 0), None)
        stuck = next((r for r in new_frozen if r["third_escape"] == 0), None)
        for label, r in (("unlock", unlock), ("stuck", stuck)):
            if r is None:
                print(label, "NONE")
                continue
            print(label, "FIRST", fmt_move(r["m1"]))
            print(label, "SECOND", fmt_move(r["m2"]))
            print(label, "LINK", r["view"]["colours"], "SORTED", r["sorted"],
                  "THIRD", r["third_escape"], "/", r["third_total"])
            if r["third_escape"]:
                for m3 in nonglobal(rot, r["col"]):
                    col3 = apply_swap(r["col"], m3)
                    view3 = link_view(rot, col3)
                    if not view3["frozen"]:
                        print("third_example", fmt_move(m3), "link", view3["colours"],
                              "n", view3["n_colours"], "unique", view3["unique"])
                        break

    # Same-colour-pair complement: second swap of the other component of the same pair.
    # Record how many of those return to the start up to renaming.
    complement_rename = 0
    for r in rows:
        if r["m1"]["pair"] == r["m2"]["pair"] and r["m1"]["comp"] != r["m2"]["comp"]:
            if r["canon_start"]:
                complement_rename += 1
    print("same_pair_complement_back_to_start_canon", complement_rename)


if __name__ == "__main__":
    main()
