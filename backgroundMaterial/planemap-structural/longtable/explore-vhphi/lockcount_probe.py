"""EXPLORATORY. Colour-class sizes of locked Kempe classes (post hoc). Long Table lock-counting, 2026-10-05.
Usage: plantri FLAGS N -a | python3 lockcount_probe.py N OUT.json [WORKERS]   (N <= 18)
For each degree-5 x, legal apex-fan neighbour y: classes of G=T-xy; a class is locked if all members have
c(x)=c(y) and none has c(x)!=c(y). Records, per member, sorted class sizes in T-x, degrees, chain fullness."""
import json, sys
from collections import Counter
from multiprocessing import Pool
import tilley_apex as TA, vhphi_explore as E, lock_anatomy as LA

def examine(args):
    idx, line = args
    rot = TA.parse(line); n = len(rot); adj = [set(r) for r in rot]
    out = []
    for x in range(n):
        if len(rot[x]) != 5: continue
        legal = {f[0] for f in E.legal_fans(rot, x, adj)}
        for i, y in enumerate(rot[x]):
            if i not in legal: continue
            G = [set(a) for a in adj]; G[x].discard(y); G[y].discard(x)
            allc, comp = LA.classes(G, n)
            sep = {comp[c] for c in allc if c[x] != c[y]}
            locked = {comp[c] for c in allc if c[x] == c[y]} - sep
            for k in locked:
                mem = [c for c in allc if comp[c] == k]
                sizes = Counter(); full = 0
                for c in mem:
                    sizes[tuple(sorted(Counter(c[w] for w in range(n) if w != x).values()))] += 1
                    ok = True
                    for o in set(range(4)) - {c[y]}:
                        ok &= LA.chain(G, c, y, o) == {w for w in range(n) if c[w] in (c[y], o)}
                    full += ok
                out.append({"idx": idx, "x": x, "y": y, "deg_x": 5, "deg_y": len(rot[y]),
                            "ring_degs": [len(rot[w]) for w in rot[x]], "members": len(mem),
                            "sizes": {str(s): v for s, v in sizes.items()}, "full_members": full})
    return out

if __name__ == "__main__":
    n = int(sys.argv[1]); assert n <= 18
    lines = [l for l in sys.stdin if l.strip()]
    w = int(sys.argv[3]) if len(sys.argv) > 3 else 8
    res = []
    with Pool(w) as p:
        for r in p.imap_unordered(examine, enumerate(lines), chunksize=4): res += r
    tot = Counter()
    for r in res:
        for s, v in r["sizes"].items(): tot[s] += v
    print("order", n, "graphs", len(lines), "locked classes", len(res), "size multisets", dict(tot), flush=True)
    json.dump({"order": n, "graphs": len(lines), "records": res}, open(sys.argv[2], "w"))
