"""Independent depth-2 check for an m(T) >= 3 claim, using only wp18_check's move code.

For every (v, fan) row of the named graph, the recorded worst start must not fill within
two moves (all Kempe components, all legal slides), and its recorded path must replay.
"""
import json
import sys
from itertools import combinations

from wp18_check import HOLE, apply, check_witness, link_colours, parse


def neighbours(rot, st):
    h = st.index(HOLE)
    out = set()
    for a, b in combinations(range(4), 2):
        for x0 in range(len(st)):
            if st[x0] in (a, b):
                try:
                    out.add(apply(rot, st, ("K", a, b, x0)))
                except ValueError:
                    pass
    for u in rot[h]:
        try:
            out.add(apply(rot, st, ("S", u)))
        except ValueError:
            pass
    return out


def main(path, order, idx):
    d = json.load(open(path))
    g = next(x for x in d["graphs"] if x["order"] == order and x["graph_index"] == idx)
    rot = parse(g["ascii"])
    rows = g["report"]["rows"]
    assert all(r["L"] is not None and r["L"] >= 3 for r in rows), "some (v,fan) has L < 3"
    for r in rows:
        assert check_witness(rot, r) == "ok"
        st = tuple(r["witness"]["start"])
        assert len(link_colours(rot, st)) == 4
        one = neighbours(rot, st)
        assert all(len(link_colours(rot, x)) == 4 for x in one)
        assert all(len(link_colours(rot, y)) == 4 for x in one for y in neighbours(rot, x))
    print(json.dumps({"graph": [order, idx], "pairs": len(rows), "every_worst_start_needs_at_least_3": True,
                      "L_values": sorted({r["L"] for r in rows})}))


if __name__ == "__main__":
    main(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]))
