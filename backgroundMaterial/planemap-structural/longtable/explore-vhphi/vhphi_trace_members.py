"""EXPLORATORY. Trace game on all k-face members (k = 4, 5) derived from plantri -m4 n -a.

Member = T - x, where deg_T(x) = k, the link of x is chordless in T, every vertex outside N[x]
has degree >= 5, and (k = 5) at least two vertices lie outside N[x] (wheels excluded).
The designated face is the link of x, in rotation order. Runs the pure trace game
(vhphi_trace_k.solve) at degree-5 vertices off the face, stopping at the first winning pair.
If the pure game fails for every vertex, retries with slides (mixed).

Usage: plantri -m4 N -a | python3 vhphi_trace_members.py N OUT.json [WORKERS]   (N <= 18)
"""
import json
import sys
import time
from multiprocessing import Pool

import vhphi_explore as E
import vhphi_trace_k as K


def parse(line):
    _, body = line.split()
    return [[ord(c) - 97 for c in r] for r in body.split(",")]


def members_of(rot):
    n = len(rot)
    adj = [set(r) for r in rot]
    for x in range(n):
        k = len(rot[x])
        if k not in (4, 5):
            continue
        link = rot[x]
        closed = set(link) | {x}
        if any(len(rot[w]) < 5 for w in range(n) if w not in closed):
            continue
        if k == 5 and n - 6 < 2:
            continue
        chord = any(link[j] in adj[link[i]] for i in range(k) for j in range(k)
                    if (j - i) % k not in (1, k - 1) and i != j)
        if chord:
            continue
        yield x, k, link


def examine(args):
    idx, line = args
    rot = parse(line)
    n = len(rot)
    out = []
    for x, k, link in members_of(rot):
        # build G = T - x, relabel to drop x
        keep = [w for w in range(n) if w != x]
        mp = {w: i for i, w in enumerate(keep)}
        rotG = [[mp[u] for u in rot[w] if u != x] for w in keep]
        adjG = [set(r) for r in rotG]
        face = [mp[u] for u in link]
        fset = set(face)
        deg5 = [w for w in range(n - 1) if w not in fset and len(rotG[w]) == 5]
        verdict, winner = "FAIL", None
        for mode in (False, True):
            for v in deg5:
                fans = E.legal_fans(rotG, v, adjG)
                res, size = K.solve(adjG, rotG, v, face, fans, mixed=mode)
                if res is None:
                    continue
                good = [i for i, w, t in res if w == t]
                if good:
                    verdict, winner = ("pure-pass" if not mode else "mixed-pass"), (v, good[0])
                    break
            if winner:
                break
        out.append({"idx": idx, "x": x, "k": k, "order_G": n - 1, "verdict": verdict,
                    "winner": winner, "line": None if winner else line.strip()})
    return out


def main():
    n = int(sys.argv[1])
    assert n <= 18
    lines = [l for l in sys.stdin if l.strip()]
    workers = int(sys.argv[3]) if len(sys.argv) > 3 else 12
    t0 = time.time()
    res = []
    with Pool(workers) as pool:
        for o in pool.imap_unordered(examine, enumerate(lines), chunksize=16):
            for r in o:
                res.append(r)
                if r["verdict"] == "FAIL":
                    print("FAIL", json.dumps(r), flush=True)
    summ = {}
    for r in res:
        key = f"k{r['k']}-{r['verdict']}"
        summ[key] = summ.get(key, 0) + 1
    json.dump({"T_order": n, "T_graphs": len(lines), "summary": summ, "results": res},
              open(sys.argv[2], "w"))
    print("T order", n, "graphs", len(lines), "summary", summ, f"{time.time()-t0:.0f}s", flush=True)


if __name__ == "__main__":
    main()
