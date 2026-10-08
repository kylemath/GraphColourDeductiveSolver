"""The 24 return pairs on the 21-vertex witness, and the other continuations.

A return pair restores the original colouring or a global renaming of it.
A third swap from that landing is a one-swap image of the original.  This
script keeps the first swap, skips the returning second swap, and walks one
further swap.  The component walk is two_swap_branches, which uses mass_core.
No second graph is built.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from two_swap_branches import (  # noqa: E402
    ASCII,
    START,
    apply_swap,
    canon,
    coloured_tuple,
    link_view,
    nonglobal,
    parse_ascii,
    proper,
    sorted_counts,
)


def main() -> None:
    rot = parse_ascii(ASCII)
    assert proper(rot, START)
    assert link_view(rot, START)["colours"] == (0, 2, 3, 0, 1, 2, 0, 3, 1)
    start_canon = canon(coloured_tuple(START))
    moves = nonglobal(rot, START)
    assert len(moves) == 16

    rows = []
    for m1 in moves:
        col1 = apply_swap(START, m1)
        assert link_view(rot, col1)["frozen"]
        for m2 in nonglobal(rot, col1):
            col2 = apply_swap(col1, m2)
            rows.append({
                "m1": m1,
                "m2": m2,
                "col1": col1,
                "col2": col2,
                "view2": link_view(rot, col2),
                "ret": col2 == START or canon(coloured_tuple(col2)) == start_canon,
                "exact": col2 == START,
            })

    returns = [r for r in rows if r["ret"]]
    assert len(returns) == 24
    assert sum(r["exact"] for r in returns) == 16
    assert sum(r["ret"] and not r["exact"] for r in returns) == 8

    cycle = {START}
    for r in returns:
        cycle.add(r["col1"])
        cycle.add(r["col2"])
    assert len({r["col1"] for r in returns}) == 16
    assert len(cycle) == 21

    # Every return-pair intermediate has a non-returning second swap to a
    # unique link colour.  None is frozen through the following swap.
    by_mid: dict[tuple, list] = {}
    for r in rows:
        by_mid.setdefault(r["col1"], []).append(r)
    assert len(by_mid) == 16
    escapes = []
    for col1, group in by_mid.items():
        off = [r for r in group if not r["ret"]]
        uniq = [r for r in off if r["view2"]["has_unique"]]
        assert uniq, "intermediate with no unique-colour continuation"
        escapes.extend(uniq)
        for r in off:
            if not r["view2"]["frozen"]:
                continue
            opened = False
            for m3 in nonglobal(rot, r["col2"]):
                if link_view(rot, apply_swap(r["col2"], m3))["has_unique"]:
                    opened = True
                    break
            assert opened, "frozen non-return with no unique third swap"
    assert len(escapes) == 52

    # Published escape: same first swap as the (0,3) return on {0}.
    m1 = next(m for m in moves if m["pair"] == (0, 3) and m["comp"] == frozenset({0}))
    mid = apply_swap(START, m1)
    assert sorted_counts(mid) == (5, 5, 5, 5)
    seconds = nonglobal(rot, mid)
    assert len(seconds) == 14
    ret_here = []
    uniq_here = []
    frozen_here = []
    for m2 in seconds:
        col2 = apply_swap(mid, m2)
        back = col2 == START or canon(coloured_tuple(col2)) == start_canon
        view = link_view(rot, col2)
        if back:
            ret_here.append(m2)
        elif view["has_unique"]:
            assert sorted_counts(col2) == (4, 5, 5, 6)
            uniq_here.append((m2, col2, view))
        else:
            assert view["frozen"]
            assert sorted_counts(col2) == (5, 5, 5, 5)
            frozen_here.append((m2, col2))
    assert len(ret_here) == 2
    assert len(uniq_here) == 4
    assert len(frozen_here) == 8

    published = next(
        (m2, col2, view)
        for m2, col2, view in uniq_here
        if m2["pair"] == (0, 1)
        and m2["comp"] == frozenset({2, 4, 6, 7, 12, 13, 14, 16, 17})
    )
    _, col2, view = published
    assert view["colours"] == (3, 2, 3, 1, 0, 2, 0, 3, 0)
    assert view["unique"] == [6]
    assert sorted_counts(col2) == (4, 5, 5, 6)
    assert col2 == (
        3, None, 0, 2, 0, 2, 1, 0, 2, 0, 3, 3, 1, 0, 1, 2, 1, 0, 3, 3, 2,
    )

    # A frozen non-return, then a third swap, still reaches a unique colour.
    m2 = next(
        m for m, _ in frozen_here
        if m["pair"] == (1, 2) and m["comp"] == frozenset({2, 3, 4, 5, 13, 15, 17, 20})
    )
    col2 = apply_swap(mid, m2)
    assert link_view(rot, col2)["frozen"]
    assert sorted_counts(col2) == (5, 5, 5, 5)
    m3 = next(
        m for m in nonglobal(rot, col2)
        if m["pair"] == (1, 3) and m["comp"] == frozenset({7, 15, 18})
    )
    col3 = apply_swap(col2, m3)
    view3 = link_view(rot, col3)
    assert view3["colours"] == (3, 1, 3, 0, 3, 2, 0, 3, 2)
    assert view3["unique"] == [5]
    assert sorted_counts(col3) == (4, 5, 5, 6)

    print("WALL")
    print("closed", len(cycle))
    print("returns", len(returns))
    print("intermediates_with_unique_second", len(by_mid))
    print("unique_seconds", len(escapes))


if __name__ == "__main__":
    main()
