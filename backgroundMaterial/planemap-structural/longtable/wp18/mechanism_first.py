"""First moves on shortest fills of gap starts, with the link vertices each swap touches.
Orders 12-22, graphs already recorded in wp18-P1..P4.json. Exploratory, after the fact.

Link roles at the start hole: a0 b a2 g d in rotation order (a0, a2 coloured alpha; b the middle,
g adjacent to a2, d adjacent to a0). A Kempe first move is written pair:{roles in the
component}, e.g. ag:{a0} is Kempe's first swap; ag:{} swaps an interior component. Mirror
images (a0<->a2, g<->d) are merged into one class. A slide is S:b (middle) or S:side.
For each gap start we record the set of optimal first moves (moves to a state of length l-1).
Writes mechanism-first.txt.
"""
import json
import sys
from collections import Counter
from multiprocessing import Pool
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from wp18_core import deletion_states, filled, hole_of, legal_fans, moves, parse_ascii, shortest_fill  # noqa: E402
from mechanism_classify import comp  # noqa: E402
from mechanism_kempe import is_gap, roles_inv  # noqa: E402

MIRROR = {"a0": "a2", "a2": "a0", "g": "d", "d": "g", "b": "b", "a": "a"}


def optimal_first(rot, s, cap=6):
    """BFS from s keeping, for each state, the set of first moves of shortest paths to it.
    Returns (l, set of optimal first moves)."""
    first = {}
    dist = {s: 0}
    frontier = []
    for mv, y in moves(rot, s):
        if y not in dist:
            dist[y] = 1
            first[y] = set()
            frontier.append(y)
        if dist[y] == 1:
            first[y].add(mv)
    for d in range(1, cap + 1):
        hits = [y for y in frontier if filled(rot, y)]
        if hits:
            out = set()
            for y in hits:
                out |= first[y]
            return d, out
        nxt = []
        for x in frontier:
            for mv, y in moves(rot, x):
                if y not in dist:
                    dist[y] = d + 1
                    first[y] = set()
                    nxt.append(y)
                if dist[y] == d + 1:
                    first[y] |= first[x]
        frontier = nxt
    return None, None


def describe(rot, s, mv, roles, names):
    if mv[0] == "S":
        return "S:b" if roles[mv[1]] == "b" else "S:side"
    a, b = mv[1], mv[2]
    seed = mv[3]
    c = comp(rot, s, seed, a, b)
    pair = "".join(sorted(names[a] + names[b], key="abgd".index))
    touched = sorted((roles[x] for x in c if x in roles), key=["a0", "b", "a2", "g", "d"].index)
    d1 = f"{pair}:{{{','.join(touched)}}}"
    mp = "".join(sorted("".join(MIRROR[ch] for ch in pair), key="abgd".index))
    mt = sorted((MIRROR[t] for t in touched), key=["a0", "b", "a2", "g", "d"].index)
    d2 = f"{mp}:{{{','.join(mt)}}}"
    return min(d1, d2)


def work(args):
    order, idx, ascii_ = args
    rot = parse_ascii(ascii_)
    agg = Counter()
    for v in (u for u in range(len(rot)) if len(rot[u]) == 5):
        states = deletion_states(rot, v)
        seen = set()
        for i, c1, c2 in legal_fans(rot, v):
            for s in states:
                if s in seen or s[c1[0]] == s[c1[1]] or s[c2[0]] == s[c2[1]]:
                    continue
                seen.add(s)
                if filled(rot, s) or not is_gap(rot, s):
                    continue
                l, fm = optimal_first(rot, s)
                p0, p1, p2, p3, p4, cn = roles_inv(rot, s)
                roles = {p0: "a0", p1: "b", p2: "a2", p3: "g", p4: "d"}
                names = {c: n for n, c in cn.items()}
                opt = {describe(rot, s, mv, roles, names) for mv in fm}
                for o in opt:
                    agg[("any", l, o)] += 1
                agg[("set", l, tuple(sorted(opt)))] += 1
    return [[list(k), c] for k, c in agg.items()]


def main():
    jobs = []
    for ph in ("P1", "P2", "P3", "P4"):
        d = json.loads((HERE / f"wp18-{ph}.json").read_text())
        jobs += [(g["order"], g["graph_index"], g["ascii"]) for g in d["graphs"]]
    with Pool(12) as pool:
        res = pool.map(work, jobs, chunksize=4)
    agg = Counter()
    for a_ in res:
        for k, c in a_:
            agg[tuple(tuple(x) if isinstance(x, list) else x for x in k)] += c
    lines = ["Optimal first moves at gap starts (distinct starts), orders 12-22", ""]
    for l in (2, 3, 4):
        tot = sum(c for k, c in agg.items() if k[0] == "set" and k[1] == l)
        lines.append(f"l = {l}: {tot} gap starts. Starts admitting each optimal first move:")
        for k, c in sorted(((k, c) for k, c in agg.items() if k[0] == "any" and k[1] == l), key=lambda kc: -kc[1]):
            lines.append(f"  {k[2]:16s} {c}")
        lines.append(f"  most frequent optimal-first-move sets at l = {l}:")
        sets = sorted(((k, c) for k, c in agg.items() if k[0] == "set" and k[1] == l), key=lambda kc: -kc[1])
        for k, c in sets[:25]:
            lines.append(f"    {c:7d}  {' '.join(k[2])}")
        lines.append("")
    (HERE / "mechanism-first.txt").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
