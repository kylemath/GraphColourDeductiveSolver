"""WP18 core: fan starts, the mixed move graph, and shortest fill length.

Declaration: ../WP18-fan-selection-length-declaration.md. A state is (hole, colouring of
T - hole), stored as a tuple over all vertices with HOLE at the hole, canonical under
renaming colours by first occurrence. Moves are Kempe swaps (hole fixed) and singleton
slides (hole moves). Both moves are reversible, so the move graph is undirected.
"""
from __future__ import annotations

import itertools
import sys
from collections import deque
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from mass_core import parse_ascii, validate_triangulation  # noqa: E402,F401

HOLE = 4
CAP = 6
PAIRS = list(itertools.combinations(range(4), 2))


def canon(state):
    seen = {}
    out = []
    for x in state:
        if x == HOLE:
            out.append(HOLE)
        else:
            out.append(seen.setdefault(x, len(seen)))
    return tuple(out)


def hole_of(state):
    return state.index(HOLE)


def filled(rot, state):
    h = hole_of(state)
    return len({state[w] for w in rot[h]}) <= 3


def legal_fans(rot, v):
    """Fans τ_i = {i(i+2), i(i+3)} on the rotation-ordered link of degree-5 vertex v."""
    link = rot[v]
    assert len(link) == 5
    fans = []
    for i in range(5):
        a, far, near = link[i], link[(i + 2) % 5], link[(i + 3) % 5]
        if far in rot[a] or near in rot[a]:
            continue
        fans.append((i, (a, far), (a, near)))
    return fans


def deletion_states(rot, v):
    """Every proper 4-colouring of T - v, canonical, as full-length tuples with HOLE at v."""
    n = len(rot)
    order = [u for u in range(n) if u != v]
    pos = {u: i for i, u in enumerate(order)}
    earlier = [[pos[w] for w in rot[u] if w != v and pos[w] < i] for i, u in enumerate(order)]
    cur = [0] * len(order)
    out = []

    def go(i, top):
        if i == len(order):
            st = [HOLE] * n
            for j, u in enumerate(order):
                st[u] = cur[j]
            out.append(canon(st))
            return
        blocked = {cur[j] for j in earlier[i]}
        for a in range(min(3, top + 1) + 1):
            if a not in blocked:
                cur[i] = a
                go(i + 1, max(top, a))

    go(0, -1)
    return out


def moves(rot, state):
    """Yield (move, next_state). move = ('K', a, b, min_vertex_of_component) or ('S', u)."""
    h = hole_of(state)
    for a, b in PAIRS:
        seen = set()
        for s, col in enumerate(state):
            if col not in (a, b) or s in seen:
                continue
            comp = {s}
            stack = [s]
            while stack:
                x = stack.pop()
                for y in rot[x]:
                    if y not in comp and state[y] in (a, b):
                        comp.add(y)
                        stack.append(y)
            seen |= comp
            nxt = list(state)
            for x in comp:
                nxt[x] = b if state[x] == a else a
            yield ("K", a, b, min(comp)), canon(nxt)
    link_cols = [state[w] for w in rot[h]]
    for u in rot[h]:
        if link_cols.count(state[u]) == 1:
            nxt = list(state)
            nxt[h] = state[u]
            nxt[u] = HOLE
            yield ("S", u), canon(nxt)


def shortest_fill(rot, start, cap=CAP):
    """Breadth-first search. Returns (length, path of moves) or (None, None) if > cap."""
    if filled(rot, start):
        return 0, []
    parent = {start: None}
    frontier = [start]
    for depth in range(1, cap + 1):
        nxt_frontier = []
        for st in frontier:
            for mv, nx in moves(rot, st):
                if nx in parent:
                    continue
                parent[nx] = (st, mv)
                if filled(rot, nx):
                    path = []
                    cur = nx
                    while parent[cur] is not None:
                        prev, m = parent[cur]
                        path.append(m)
                        cur = prev
                    return depth, path[::-1]
                nxt_frontier.append(nx)
        frontier = nxt_frontier
        if not frontier:
            return None, None
    return None, None


class Interrupted(Exception):
    pass


def graph_report(rot, cap=CAP, deadline=None):
    """L(v,τ) for every degree-5 v and legal fan τ, with witnesses for L >= 2 or capped.

    deadline: time.monotonic() value; past it, raise Interrupted (recorded, never a pass).
    """
    import time
    memo = {}
    rows = []
    for v in (u for u in range(len(rot)) if len(rot[u]) == 5):
        states = deletion_states(rot, v)
        for i, c1, c2 in legal_fans(rot, v):
            starts = [s for s in states if s[c1[0]] != s[c1[1]] and s[c2[0]] != s[c2[1]]]
            hist = {}
            worst, witness = -1, None
            for s in starts:
                if deadline is not None and time.monotonic() > deadline:
                    raise Interrupted(f"v={v} fan={i}")
                if s not in memo:
                    memo[s] = shortest_fill(rot, s, cap)
                ell, path = memo[s]
                key = "capped" if ell is None else str(ell)
                hist[key] = hist.get(key, 0) + 1
                score = cap + 1 if ell is None else ell
                if score > worst:
                    worst, witness = score, (s, path)
            capped = "capped" in hist
            row = {
                "v": v,
                "fan_index": i,
                "chords": [list(c1), list(c2)],
                "starts": len(starts),
                "L": None if capped else worst,
                "L_at_least": worst,
                "hist": hist,
            }
            if worst >= 2:
                s, path = witness
                row["witness"] = {"start": list(s), "moves": [list(m) for m in path] if path else None}
            rows.append(row)
    exact = [r["L"] for r in rows if r["L"] is not None]
    lower = [r["L_at_least"] for r in rows]
    m_exact = min(exact) if exact else None
    # m(T) is exact when some (v,τ) is exact and attains min over all lower bounds.
    m = m_exact if exact and m_exact <= min(lower) else None
    return {
        "pairs": len(rows),
        "m": m,
        "m_at_least": min(lower) if rows else None,
        "max_L_at_least": max(lower) if rows else None,
        "rows": rows,
    }
