"""Slide-only closure after a third Kempe swap on the 21-vertex frozen hole.

Starts from the colouring in two-kempe-kill.md. A pair of swaps is one of the
84 when every third swap that creates a singleton still leaves a four-colour
link at that singleton. From each such image, singleton slides run with no
further Kempe swap.
"""

from __future__ import annotations

import sys
from collections import Counter, deque
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from mass_core import parse_ascii

ASCII = (
    "21 bcdef,aflghijkc,abkmd,acmnoe,adopqf,aeqlb,blrsh,bgsoi,bhotj,"
    "bituk,bjumc,bfqrg,ckund,dmuto,dntihspe,eosrq,eprlf,glqps,grpoh,ionuj,jtnmk"
)
HOLE = 1
COLOURS = (0, -1, 1, 2, 1, 2, 0, 1, 2, 0, 3, 3, 0, 1, 0, 2, 0, 1, 3, 3, 2)


def canon(colours: list[int]) -> tuple[int, ...]:
    seen: dict[int, int] = {}
    out = []
    for value in colours:
        if value < 0:
            out.append(-1)
        else:
            out.append(seen.setdefault(value, len(seen)))
    return tuple(out)


def link_counts(rot, hole: int, colours: list[int]) -> Counter:
    return Counter(colours[v] for v in rot[hole])


def frozen(rot, hole: int, colours: list[int]) -> bool:
    counts = link_counts(rot, hole, colours)
    return len(counts) == 4 and all(k >= 2 for k in counts.values())


def unique_vertices(rot, hole: int, colours: list[int]) -> list[int]:
    counts = link_counts(rot, hole, colours)
    if len(counts) > 3:
        return [v for v in rot[hole] if counts[colours[v]] == 1]
    return []


def components(rot, hole: int, colours: list[int]):
    n = len(rot)
    found = []
    for a in range(4):
        for b in range(a + 1, 4):
            remaining = {v for v in range(n) if v != hole and colours[v] in (a, b)}
            while remaining:
                start = min(remaining)
                stack = [start]
                comp: set[int] = set()
                while stack:
                    v = stack.pop()
                    if v in comp:
                        continue
                    comp.add(v)
                    for w in rot[v]:
                        if w in remaining and w not in comp:
                            stack.append(w)
                remaining -= comp
                yield (a, b), tuple(sorted(comp))


def swap(colours: list[int], a: int, b: int, comp: tuple[int, ...]) -> list[int]:
    out = colours[:]
    for v in comp:
        out[v] = b if colours[v] == a else a
    return out


def slide_fills(rot, hole: int, colours: list[int], cap: int = 8000):
    start = (hole, canon(colours))
    seen = {start}
    queue = deque([(hole, colours)])
    while queue:
        if len(seen) > cap:
            return "truncated", len(seen)
        h, cols = queue.popleft()
        counts = link_counts(rot, h, cols)
        if len(counts) <= 3:
            return "filled", len(seen)
        for x in rot[h]:
            if counts[cols[x]] != 1:
                continue
            nxt = cols[:]
            nxt[h] = cols[x]
            nxt[x] = -1
            key = (x, canon(nxt))
            if key not in seen:
                seen.add(key)
                queue.append((x, nxt))
    return "closed", len(seen)


def main() -> None:
    rot = parse_ascii(ASCII)
    base = list(COLOURS)
    assert frozen(rot, HOLE, base)
    swaps = []
    for pair, comp in components(rot, HOLE, base):
        image = swap(base, *pair, comp)
        if canon(image) == canon(base):
            continue
        swaps.append((pair, comp, image))
    assert len(swaps) == 16, len(swaps)

    eighty_four = []
    for i, (_p1, _c1, mid) in enumerate(swaps):
        second = []
        for pair, comp in components(rot, HOLE, mid):
            image = swap(mid, *pair, comp)
            if canon(image) == canon(mid):
                continue
            second.append((pair, comp, image))
        for pair, comp, image in second:
            if not frozen(rot, HOLE, image):
                continue
            if canon(image) == canon(base):
                continue
            thirds = []
            for p3, c3 in components(rot, HOLE, image):
                nxt = swap(image, *p3, c3)
                if canon(nxt) == canon(image):
                    continue
                if unique_vertices(rot, HOLE, nxt):
                    thirds.append((p3, c3, nxt))
            if thirds and all(
                frozen(rot, x, nxt)
                for _p, _c, nxt in thirds
                for x in unique_vertices(rot, HOLE, nxt)
            ):
                eighty_four.append((i, pair, comp, image, thirds))

    print("pairs in the 84 class", len(eighty_four))
    outcomes = Counter()
    worst = None
    for i, pair, comp, image, thirds in eighty_four:
        for p3, c3, nxt in thirds:
            for x in unique_vertices(rot, HOLE, nxt):
                moved = nxt[:]
                moved[HOLE] = nxt[x]
                moved[x] = -1
                kind, size = slide_fills(rot, x, moved)
                outcomes[kind] += 1
                if kind != "filled" and (worst is None or size > worst[0]):
                    worst = (size, kind, i, p3, c3, x)
    print(dict(outcomes))
    print("worst", worst)


if __name__ == "__main__":
    main()
