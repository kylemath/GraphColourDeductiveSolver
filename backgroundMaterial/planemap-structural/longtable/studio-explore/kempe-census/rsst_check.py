#!/usr/bin/env python3
"""[exploratory] For census records at rho >= MIN: does the graph contain the Birkhoff diamond (RSST 0.7322,
index 0) or RSST 2.122 (index 1), is the hole one of that configuration's vertices, and how many of the 633 RSST
configurations does the graph contain. Uses Studio intel's rsst_contain.py (commit 7f99280) and
routeb/rsst_parse.py + routeb/rsst/unavoidable.conf (sha256 1c92fc28...4e84) unchanged; the hole-pinned search
below is a copy of rsst_contain.contains with one extra condition (the hole is in the image).
usage: rsst_check.py MIN ORDERS...   (run with cwd = .../studiointel)
"""
import json
import os
import sys

sys.path.insert(0, os.getcwd())
sys.path.insert(0, os.path.join(os.getcwd(), "routeb"))
import rsst_parse  # noqa: E402
import rsst_contain as rc  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))


def graph(line):
    n, body = line.split()
    rot = [[ord(c) - 97 for c in r] for r in body.split(",")]
    adj = {v: set(nb) for v, nb in enumerate(rot)}
    faces = {frozenset((v, nb[i], nb[(i + 1) % len(nb)])) for v, nb in enumerate(rot) for i in range(len(nb))}
    return adj, faces


def contains_hole(adj, tfaces, P, hole):
    degT = {u: len(a) for u, a in adj.items()}
    order = P['order']
    phi, used = {}, set()

    def rec(i):
        if i == len(order):
            return hole in used and all(frozenset(phi[x] for x in f) in tfaces for f in P['faces'])
        u = order[i]
        placed = order[:i]
        nbr = [w for w in placed if w in P['E'][u]]
        for t in (adj[phi[nbr[0]]] if nbr else adj.keys()):
            if t in used or degT[t] != P['deg'][u]:
                continue
            if any((w in P['E'][u]) != (phi[w] in adj[t]) for w in placed):
                continue
            phi[u] = t
            used.add(t)
            if rec(i + 1):
                return True
            del phi[u]
            used.discard(t)
        return False
    return rec(0)


def main():
    mn = int(sys.argv[1])
    confs = rsst_parse.parse('routeb/rsst/unavoidable.conf')
    P = [rc.prep_conf(c) for c in confs]
    assert confs[0]['name'] == '0.7322' and confs[1]['name'] == '2.122'
    for n in [int(x) for x in sys.argv[2:]]:
        for line in open(os.path.join(HERE, "out-%d.jsonl" % n)):
            rec = json.loads(line)
            if "graph" not in rec or rec["rho"] is None or rec["rho"] < mn:
                continue
            adj, tf = graph(rec["graph"])
            out = {"order": n, "index": rec["index"], "hole": rec["hole"], "rho": rec["rho"],
                   "diamond": rc.contains(adj, tf, P[0]), "diamond_at_hole": contains_hole(adj, tf, P[0], rec["hole"]),
                   "c2122": rc.contains(adj, tf, P[1]), "c2122_at_hole": contains_hole(adj, tf, P[1], rec["hole"]),
                   "n_rsst": sum(rc.contains(adj, tf, p) for p in P)}
            print(json.dumps(out), flush=True)


if __name__ == "__main__":
    main()
