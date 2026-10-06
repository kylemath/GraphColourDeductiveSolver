#!/usr/bin/env python3
"""[exploratory] Census table and Birkhoff-diamond test for the max-radius holes.

Birkhoff diamond (as used here): four degree-5 vertices a, b, c, d with faces abc and bcd
(two triangles sharing the edge bc). For each record at the order's max radius: is the hole one
of the four vertices of such a diamond, and does the graph contain one at all.
usage: analyse.py ORDERS... > table.md   (reads summary-N.json and out-N.jsonl in this directory)
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def parse(line):
    n, body = line.split()
    return [[ord(c) - 97 for c in r] for r in body.split(",")]


def diamonds(rot):
    deg5 = {v for v in range(len(rot)) if len(rot[v]) == 5}
    faces = set()
    for v, nb in enumerate(rot):
        for i in range(len(nb)):
            faces.add(frozenset((v, nb[i], nb[(i + 1) % len(nb)])))
    out = []
    for b in deg5:
        for c in rot[b]:
            if c <= b or c not in deg5:
                continue
            apex = [x for x in rot[b] if x in rot[c] and frozenset((b, c, x)) in faces]
            if len(apex) == 2 and apex[0] in deg5 and apex[1] in deg5:
                out.append({b, c, apex[0], apex[1]})
    return out


def main():
    orders = [int(x) for x in sys.argv[1:]]
    radii = range(1, 8)
    print("| order | graphs | hole classes | " + " | ".join("rho=%d" % r for r in radii) +
          " | null | max rho | max-rho holes in a diamond | max-rho graphs with a diamond |")
    print("|" + "---|" * (6 + len(radii)))
    for n in orders:
        s = json.load(open(os.path.join(HERE, "summary-%d.json" % n)))
        h = s["rho_hist"]
        mx = s["max_rho"]
        hole_in, graph_has, tot = 0, 0, 0
        for line in open(os.path.join(HERE, "out-%d.jsonl" % n)):
            rec = json.loads(line)
            if rec["rho"] != mx or "graph" not in rec:
                continue
            tot += 1
            ds = diamonds(parse(rec["graph"]))
            graph_has += bool(ds)
            hole_in += any(rec["hole"] in d for d in ds)
        print("| %d | %d | %d | %s | %s | %d | %s | %s |" % (
            n, s["graphs"], s["hole_classes"], " | ".join(str(h.get(str(r), 0)) for r in radii),
            h.get("None", 0), mx,
            "%d/%d" % (hole_in, tot) if mx >= 4 else "-", "%d/%d" % (graph_has, tot) if mx >= 4 else "-"))


if __name__ == "__main__":
    main()
