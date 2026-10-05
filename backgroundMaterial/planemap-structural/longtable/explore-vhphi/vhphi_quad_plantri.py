"""EXPLORATORY. Exhaustive quadrilateral members from plantri -c4m4 N -a (N <= 18).

Member: G = T - st with phi = (s, x, t, y) the merged 4-face, xy not an edge, and every vertex
of G off phi of degree >= 5. For each member, run the pure free-adversary game
(vhphi_quad_explore.pure_game) at every degree-5 vertex off phi.
Counts members where no pair wins (free-game failures) and where the adversary changes nothing.

Usage: plantri -c4m4 N -a | python3 vhphi_quad_plantri.py N OUT.json [WORKERS]
"""
import json
import sys
import time
from multiprocessing import Pool

import vhphi_explore as E
import vhphi_quad_explore as Q


def parse(line):
    _, body = line.split()
    return [[ord(c) - 97 for c in r] for r in body.split(",")]


def examine(args):
    idx, line = args
    rot = parse(line)
    n = len(rot)
    adjT = [set(r) for r in rot]
    out = []
    for s in range(n):
        for k, t in enumerate(rot[s]):
            if t <= s:
                continue
            d = len(rot[s])
            x = rot[s][(k + 1) % d]
            y = rot[s][(k - 1) % d]
            if x in adjT[y]:
                continue
            phi = {s, t, x, y}
            adj = [set(a) for a in adjT]
            adj[s].discard(t)
            adj[t].discard(s)
            if any(len(adj[w]) < 5 for w in range(n) if w not in phi):
                continue
            deg5 = [w for w in range(n) if w not in phi and len(adj[w]) == 5]
            win_any = False
            hurt = 0
            for w in deg5:
                fans = Q.legal_fans_adj(rot, w, adj)
                res, _ = Q.pure_game(adj, w, fans, phi)
                if any(ok for _, ok in res):
                    win_any = True
                    break
            out.append({"idx": idx, "edge": [s, t], "phi": sorted(phi), "free_game_pass": win_any,
                        "line": None if win_any else line.strip()})
    return out


def main():
    n = int(sys.argv[1])
    assert n <= 18
    lines = [l for l in sys.stdin if l.strip()]
    workers = int(sys.argv[3]) if len(sys.argv) > 3 else 12
    t0 = time.time()
    res = []
    with Pool(workers) as pool:
        for o in pool.imap_unordered(examine, enumerate(lines), chunksize=32):
            res.extend(o)
    fails = [r for r in res if not r["free_game_pass"]]
    json.dump({"order": n, "graphs": len(lines), "members": len(res), "free_game_fail": len(fails),
               "fails": fails}, open(sys.argv[2], "w"))
    print("order", n, "graphs", len(lines), "quad members", len(res), "free-game failures", len(fails),
          f"{time.time()-t0:.0f}s")


if __name__ == "__main__":
    main()
