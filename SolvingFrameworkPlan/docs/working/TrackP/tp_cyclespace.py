#!/usr/bin/env python3
"""Track P: along a law R-cycle, the cycle space Z(s) of the union of the six pair graphs (bichromatic cycles) at each
state s (dim = B(s)); report dims of the intersection over all states, over rigid states, and over consecutive pairs.
usage: tp_cyclespace.py FILE [--max K]"""
import sys, json
from tn_lib import Engine
from tn_forest import parse_dump, cycles_in_R_law, PAIRS

def rref_add(basis, v):
    # basis: dict pivot->vec (ints as bitsets); returns True if independent
    for p in sorted(basis, reverse=True):
        if v >> p & 1: v ^= basis[p]
    if v == 0: return False
    basis[v.bit_length() - 1] = v
    # keep reduced
    return True

def span_basis(vecs):
    b = {}
    for v in vecs: rref_add(b, v)
    return list(b.values())

def cycle_basis(n, Elist, col):
    # fundamental cycles of each pair graph (edges as bit indices)
    vecs = []
    for (p, q) in PAIRS:
        par = {}; 
        def f(a):
            while par.setdefault(a, a) != a: a = par[a]
            return a
        tree_adj = {}
        for k, (u, v) in enumerate(Elist):
            if col[u] in (p, q) and col[v] in (p, q):
                a, b = f(u), f(v)
                if a != b: par[a] = b; tree_adj.setdefault(u, []).append((v, k)); tree_adj.setdefault(v, []).append((u, k))
                else:
                    # path u->v in tree
                    prev = {u: None}; st = [u]
                    while st:
                        x = st.pop()
                        for y, kk in tree_adj.get(x, []):
                            if y not in prev: prev[y] = (x, kk); st.append(y)
                    vec = 1 << k; x = v
                    while prev[x] is not None: x2, kk = prev[x]; vec ^= 1 << kk; x = x2
                    vecs.append(vec)
    return vecs

def intersect(B1, B2, m):
    # intersection of spans via Zassenhaus-like: solve a.B1 = b.B2 ; brute small dims
    # use: dim(U cap V) = dim U + dim V - dim(U+V); and get basis by kernel computation
    rows = [(v, 1 << i) for i, v in enumerate(B1)] + [(v, 0) for v in B2]
    # gaussian elimination on combined (v | tag) where tag tracks B1-combination
    piv = {}
    inter = []
    for v, tag in rows:
        for p in sorted(piv, reverse=True):
            if v >> p & 1: v ^= piv[p][0]; tag ^= piv[p][1]
        if v == 0:
            if tag:
                w = 0
                for i in range(len(B1)):
                    if tag >> i & 1: w ^= B1[i]
                inter.append(w)
        else: piv[v.bit_length() - 1] = (v, tag)
    return span_basis(inter)

def main():
    args = sys.argv[1:]; mx = 10 ** 9
    if '--max' in args: k = args.index('--max'); mx = int(args[k + 1]); del args[k:k + 2]
    eng = Engine(dump=True, maxstates=200000); cnt = 0
    for fn in args:
        for l in open(fn):
            if cnt >= mx: break
            if l.startswith('{'):
                d = json.loads(l); l = d.get('graph')
                if not l: continue
            p = l.split(); rot = [list(map(int, r.split(','))) for r in p[2].split(';')]; n = len(rot)
            Elist = sorted({tuple(sorted((u, v))) for u in range(1, n) for v in rot[u] if v != 0})
            js, tn, dump = eng.run(l)
            if tn is None: continue
            S = parse_dump(dump)
            for C in cycles_in_R_law(S, True)[:1]:
                cnt += 1
                cols = [[-1 if ch == '-' else int(ch) for ch in S[x]['col']] for x in C]
                bases = [span_basis(cycle_basis(n, Elist, c)) for c in cols]
                dims = [len(b) for b in bases]
                allI = bases[0]
                for b in bases[1:]: allI = intersect(allI, b, len(Elist))
                rig = [b for b, x in zip(bases, C) if S[x]['N'] == 8]
                rI = rig[0]
                for b in rig[1:]: rI = intersect(rI, b, len(Elist))
                cons = [len(intersect(bases[t], bases[(t + 1) % len(C)], len(Elist))) for t in range(len(C))]
                print(json.dumps(dict(src=p[0], E=len(Elist), excess=len(Elist) - (3 * (n - 1) - 8), dims=''.join(map(str, dims)), cap_all=len(allI), cap_rigid=len(rI),
                                      cap_consec=''.join(map(str, cons)), cap_all_lengths=[bin(v).count('1') for v in allI])), flush=True)

if __name__ == '__main__':
    main()
