"""EXPLORATORY. Wernicke-pair apex test (core-brainstorm.md, idea A). Long Table 2026-10-05.

For every degree-5 vertex x and neighbour y with deg y in {5, 6}: is the fan at x with apex y
legal, and is it good (every start fills; pure first, then mixed with no restriction)?

Usage: plantri -m5 N -a | python3 wernicke_apex.py N OUT.json     (N <= 18)
"""
import json
import sys

import vhphi_explore as E


def parse(line):
    _, body = line.split()
    return [[ord(c) - 97 for c in r] for r in body.split(",")]


def main():
    n = int(sys.argv[1])
    assert n <= 18
    out = []
    for gi, line in enumerate(l for l in sys.stdin if l.strip()):
        rot = parse(line)
        adj = [set(r) for r in rot]
        for x in range(n):
            if len(rot[x]) != 5:
                continue
            pure, _ = E.pure_good_fans(rot, adj, x)
            legal = {f[0]: f for f in E.legal_fans(rot, x, adj)}
            mixed = None
            for i, y in enumerate(rot[x]):
                dy = len(rot[y])
                if dy not in (5, 6):
                    continue
                rec = {"graph": gi, "x": x, "y": y, "deg_y": dy, "fan": i, "legal": i in legal,
                       "pure_good": i in pure}
                if i in legal and i not in pure:
                    if mixed is None:
                        mixed = dict(E.mixed_good_fans(rot, adj, x, set()))
                    rec["mixed_good"] = mixed.get(i)
                out.append(rec)
    bad = [r for r in out if r["legal"] and not r["pure_good"] and not r.get("mixed_good")]
    json.dump({"order": n, "records": out}, open(sys.argv[2], "w"))
    tally = {}
    for r in out:
        k = f"deg{r['deg_y']}-" + ("illegal" if not r["legal"] else "pure" if r["pure_good"]
                                   else "mixed" if r.get("mixed_good") else "BAD")
        tally[k] = tally.get(k, 0) + 1
    print("order", n, tally, "bad", [(r["graph"], r["x"], r["y"]) for r in bad][:10])


if __name__ == "__main__":
    main()
