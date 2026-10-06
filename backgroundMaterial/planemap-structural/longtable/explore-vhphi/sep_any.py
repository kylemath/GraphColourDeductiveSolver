"""EXPLORATORY. SEP test: is every unfilled state at a degree-5 hole Tilley-separable for at
least one of its admitting (legal) fans?  State = proper colouring of T - x with a 4-coloured
link.  For fan j (apex y_j), starts = colourings c of T - x y_j with c(x) = c(y_j) (forget x);
separable = class in T - x y_j contains c with c(x) != c(y_j).
Usage: plantri ... -a | python3 sep_any.py N OUT.json [WORKERS]    (N <= 17)"""
import json, sys
from collections import deque
from multiprocessing import Pool
import tilley_apex as TA, vhphi_explore as E

def parse(line):
    return TA.parse(line)

def forget(c, x):
    t = tuple(v for i, v in enumerate(c) if i != x)
    return TA.canon(t)

def examine(args):
    idx, line = args
    rot = parse(line); n = len(rot); adj = [set(r) for r in rot]
    out = []
    for x in range(n):
        if len(rot[x]) != 5: continue
        ring = rot[x]
        legal = {f[0] for f in E.legal_fans(rot, x, adj)}
        starts = {}      # key -> list of (fan j, separable?)
        for j in legal:
            y = ring[j]
            G = [set(a) for a in adj]; G[x].discard(y); G[y].discard(x)
            allc = [TA.canon(c) for c in TA.colourings(G, n)]
            good = {c for c in allc if c[x] != c[y]}
            q = deque(good)
            while q:
                c = q.popleft()
                for d in TA.kempe_nbrs(G, c):
                    if d not in good: good.add(d); q.append(d)
            for c in allc:
                if c[x] == c[y]:
                    k = forget(c, x)
                    link = {c[w] for w in ring}
                    if len(link) == 4:        # unfilled (for filled, nothing to prove)
                        starts.setdefault(k, []).append((j, c in good))
        bad = [k for k, v in starts.items() if not any(s for _, s in v)]
        out.append({"idx": idx, "x": x, "states": len(starts), "bad_states": len(bad),
                    "legal_fans": len(legal)})
    return out

def main():
    n = int(sys.argv[1]); assert n <= 18
    lines = [l for l in sys.stdin if l.strip()]
    workers = int(sys.argv[3]) if len(sys.argv) > 3 else 12
    res = []
    with Pool(workers) as pool:
        for r in pool.imap_unordered(examine, enumerate(lines), chunksize=8): res.extend(r)
    bad = [r for r in res if r["bad_states"]]
    print("order", n, "graphs", len(lines), "degree-5 vertices", len(res),
          "states", sum(r["states"] for r in res), "bad states (no separable admitting fan)",
          sum(r["bad_states"] for r in res), "at", len(bad), "vertices", flush=True)
    json.dump({"order": n, "records": res}, open(sys.argv[2], "w"))

if __name__ == "__main__":
    main()
