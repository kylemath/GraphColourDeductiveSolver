"""nprove_dfree17.py: D'-free Kempe class of c' and c'' for every rigid disc of order 17 (out_17.txt, 75 discs)
and for the 2 triply locked ones.  Prints class size, edges, degree profile, comps-vector multiset,
isomorphism class of the class graph, first member with broken chain/3-coloured ring."""
import sys
from collections import Counter
from nprove_lib import *
fn = sys.argv[1]
def pairvec(adj, x, c):
    return tuple(len(comps(adj, c, p, x)[0]) for p in [(D,AL),(D,BE),(D,GA),(AL,BE),(AL,GA),(BE,GA)])
def refine(G):
    h = {v: len(G[v]) for v in G}
    for _ in range(4):
        h = {v: hash((h[v], tuple(sorted(h[w] for w in G[v])))) for v in G}
    return h
def iso(A, B):
    if len(A) != len(B): return False
    ha, hb = refine(A), refine(B)
    if sorted(ha.values()) != sorted(hb.values()): return False
    va = sorted(A, key=lambda v: (ha[v], v)); m = {}; used = set()
    def bt(i):
        if i == len(va): return True
        v = va[i]
        for w in B:
            if w in used or hb[w] != ha[v]: continue
            if all((m[u] in B[w]) == (u in A[v]) for u in m):
                m[v] = w; used.add(w)
                if bt(i + 1): return True
                del m[v]; used.discard(w)
        return False
    return bt(0)
shapes = []
for i, line in enumerate(l for l in open(fn) if 'DISC' in l):
    col, E = parse(line); x, adj = build(col, E)
    cp, cpp, K2, K0 = neighbours_cprime(adj, x, col + [0])
    for name, c0, apex in (("c'", cp, 0), ("c''", cpp, 2)):
        dist, rep, g = dfree_class(adj, x, c0, apex)
        G = {a: set(bs) for a, bs in g.items()}
        gd = [dist[k] for k, c in rep.items() if chain_broken(adj, x, c, apex)]
        # D-free pair structure at each member: the three D-free comps
        s = c0[apex]; free = [(a, b) for a in range(4) for b in range(a + 1, 4) if s not in (a, b)]
        prof = Counter(tuple(sorted(len(comps(adj, c, p, x)[0]) for p in free)) for c in rep.values())
        shapes.append((i, name, G, min(gd) if gd else None, dict(prof), c0[apex]))
        print(i, name, "class", len(G), "edges", sum(len(v) for v in G.values())//2, "deg", sorted(len(v) for v in G.values()),
              "first-good-dist", min(gd) if gd else None, "D-free comps profile", dict(prof))
# isomorphism classes
reps = []
for s in shapes:
    for r in reps:
        if iso(s[2], r[2][2]): r[0].append((s[0], s[1])); break
    else: reps.append(([(s[0], s[1])], s[2], s))
print("isomorphism classes of D-free class graphs:", len(reps))
for members, G, s in reps:
    print(" size", len(G), "edges", sum(len(v) for v in G.values())//2, "count", len(members), "first-good-dist", s[3], members[:6])
