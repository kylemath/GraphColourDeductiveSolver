"""WP18 independent checker. Does not import wp18_core.

For every witness in a phase output: the start is a proper colouring of T - v whose two
fan chords are bichromatic; every move is legal; the final link uses at most three colours;
the move count equals the recorded L. It also confirms that no single move fills a start
whose L is at least 2 (an independent lower-bound check at depth 1).
"""
import hashlib
import json
import sys
from itertools import combinations

HOLE = 4


def parse(line):
    n, code = line.strip().split(" ", 1)
    rot = [[ord(c) - 97 for c in row] for row in code.split(",")]
    assert len(rot) == int(n)
    return rot


def relabel(st):
    m = {}
    return tuple(HOLE if x == HOLE else m.setdefault(x, len(m)) for x in st)


def proper(rot, st):
    return all(st[x] == HOLE or st[y] == HOLE or st[x] != st[y] for x in range(len(rot)) for y in rot[x])


def link_colours(rot, st):
    h = st.index(HOLE)
    return {st[w] for w in rot[h]}


def apply(rot, st, mv):
    h = st.index(HOLE)
    if mv[0] == "K":
        _, a, b, x0 = mv
        if st[x0] not in (a, b):
            raise ValueError("Kempe seed not in pair")
        comp, todo = {x0}, [x0]
        while todo:
            x = todo.pop()
            for y in rot[x]:
                if y not in comp and st[y] in (a, b):
                    comp.add(y)
                    todo.append(y)
        if min(comp) != x0:
            raise ValueError("seed is not the component minimum")
        nx = [(b if st[x] == a else a) if x in comp else st[x] for x in range(len(st))]
        return relabel(nx)
    if mv[0] == "S":
        u = mv[1]
        if u not in rot[h]:
            raise ValueError("slide target not adjacent to hole")
        if [st[w] for w in rot[h]].count(st[u]) != 1:
            raise ValueError("slide colour not singleton on link")
        nx = list(st)
        nx[h], nx[u] = st[u], HOLE
        return relabel(nx)
    raise ValueError("unknown move")


def one_move_fills(rot, st):
    h = st.index(HOLE)
    for a, b in combinations(range(4), 2):
        for x0 in range(len(st)):
            if st[x0] in (a, b):
                try:
                    if len(link_colours(rot, apply(rot, st, ("K", a, b, x0)))) <= 3:
                        return True
                except ValueError:
                    pass
    for u in rot[h]:
        try:
            if len(link_colours(rot, apply(rot, st, ("S", u)))) <= 3:
                return True
        except ValueError:
            pass
    return False


def check_witness(rot, row):
    v = row["v"]
    st = tuple(row["witness"]["start"])
    if st.index(HOLE) != v or st.count(HOLE) != 1 or not proper(rot, st):
        raise ValueError("start is not a proper colouring of T - v")
    for a, b in row["chords"]:
        if st[a] == st[b] or b in rot[a]:
            raise ValueError("chord not bichromatic or already an edge")
    moves = row["witness"]["moves"]
    if moves is None:  # capped: nothing to replay, record only
        return "capped"
    if len(moves) != row["L"]:
        raise ValueError("move count differs from L")
    if row["L"] >= 2 and (len(link_colours(rot, st)) <= 3 or one_move_fills(rot, st)):
        raise ValueError("a start with L >= 2 fills in at most one move")
    for mv in moves:
        st = apply(rot, st, tuple(mv))
        if not proper(rot, st):
            raise ValueError("improper after move")
    if len(link_colours(rot, st)) > 3:
        raise ValueError("final link uses four colours")
    return "ok"


def main(path):
    data = json.load(open(path))
    counts = {"ok": 0, "capped": 0}
    for g in data["graphs"]:
        if g.get("interrupted"):
            continue
        rot = parse(g["ascii"])
        assert hashlib.sha256(g["ascii"].encode()).hexdigest() == g["ascii_sha256"]
        for row in g["report"]["rows"]:
            if "witness" in row:
                counts[check_witness(rot, row)] += 1
    print(json.dumps({"file": path, **counts}))


if __name__ == "__main__":
    for p in sys.argv[1:]:
        main(p)
