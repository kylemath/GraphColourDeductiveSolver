#!/usr/bin/env python3
"""Track R: dual restricted to STRUCTURAL partition inequalities.
Column (t, P, M): P a part at state t, M a meet of <= DEPTH structural partitions taken from other states
(Pi(s,R): components of the role-R pair graphs at s; K_s split) or 'singletons'.  Inequality: the kept edges of P
crossing the blocks of P ^ M number at least (#blocks after merging along forced link edges) - 1.
LP: max sum lam*val  s.t. for every non-forced ground edge e: sum of lam over columns whose crossing set contains e <= 1.
Bound on |E(G'-h)| = LP + 5 (link edges).  Reports e_struct = LP + 5 - base and the support.
usage: tr_family.py DATA.json [--depth D] [--states a,b,..] [--gwindow S,K] [--out F.json]"""
import sys, os, json, itertools, collections, time
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import coo_matrix
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from tr_lag import load, part_edges
from tr_explain import struct_partitions
from tr_show import rolename


def nblocks_contracted(P, labs, U, forced):
    key = {v: tuple(l[v] for l in labs) if labs is not None else v for v in P}
    par = {k: k for k in set(key.values())}
    def f(a):
        while par[a] != a: par[a] = par[par[a]]; a = par[a]
        return a
    for k in forced:
        a, b = U[k]
        if a in P and b in P: par[f(key[a])] = f(key[b])
    return len({f(k) for k in par}), key


def main():
    a = sys.argv[1:]; path = a.pop(0); depth = 2; out = None; gw = None
    if '--depth' in a: i = a.index('--depth'); depth = int(a[i + 1]); del a[i:i + 2]
    if '--out' in a: i = a.index('--out'); out = a[i + 1]; del a[i:i + 2]
    if '--gwindow' in a: i = a.index('--gwindow'); gw = tuple(int(z) for z in a[i + 1].split(',')); del a[i:i + 2]
    D = load(path, None, gw); base = 3 * (D['n'] - 1) - 8; U = D['U']; forced = set(D['forced'])
    PE = part_edges(U, D['parts']); SP = struct_partitions(D)
    cols = []  # (t, part index, name, val, crossing edge list)
    seen = set()
    for i, (t, p, q, P) in enumerate(D['parts']):
        cands = [(nm, lab) for nm, lab in SP if nm[0] != t]
        combos = [None] + [c for r in range(1, depth + 1) for c in itertools.combinations(cands, r)]
        for comb in combos:
            labs = None if comb is None else [lab for _, lab in comb]
            nb, key = nblocks_contracted(P, labs, U, forced)
            if nb <= 1: continue
            cross = tuple(k for k in PE[i] if k not in forced and key[U[k][0]] != key[U[k][1]])
            sig = (i, cross)
            if sig in seen: continue
            seen.add(sig)
            name = 'singletons' if comb is None else ' ^ '.join('%s@%+d' % (nm[1], nm[0] - t) for nm, _ in comb)
            cols.append((t, i, name, nb - 1, cross))
    m = len(U); nf = [k for k in range(m) if k not in forced]; row = {k: r for r, k in enumerate(nf)}
    ri, rj = [], []
    for j, (t, i, name, val, cross) in enumerate(cols):
        for k in cross: ri.append(row[k]); rj.append(j)
    A = coo_matrix((np.ones(len(ri)), (ri, rj)), shape=(len(nf), len(cols))).tocsr()
    c = -np.array([v for (_, _, _, v, _) in cols], float)
    t0 = time.time()
    res = linprog(c, A_ub=A, b_ub=np.ones(len(nf)), bounds=(0, None), method='highs')
    lp = -res.fun; e = lp + len(forced) - base
    print('src %s W %s depth %d columns %d  LP %.4f  e_struct %.4f  (%.1fs)' % (D['src'], D['W'], depth, len(cols), lp, e, time.time() - t0), flush=True)
    sup = [(cols[j], res.x[j]) for j in range(len(cols)) if res.x[j] > 1e-9]
    cnt = collections.Counter()
    for (t, i, name, val, cross), lam in sorted(sup, key=lambda z: (z[0][0], z[0][2])):
        tt, p, q, P = D['parts'][i]
        print('   t=%d(N=%s) %s |P|=%d  lam=%.3f  val=%d  |cross|=%d  M=%s' % (D['W'][t], D['Nprof'][t], rolename(D['cols'][t], p, q), len(P), lam, val, len(cross), name))
    if out: json.dump(dict(src=D['src'], W=D['W'], depth=depth, e=e, support=[[D['W'][t], rolename(D['cols'][t], *D['parts'][i][1:3]), len(D['parts'][i][3]), lam, val, name] for (t, i, name, val, cross), lam in sup]), open(out, 'w'))


if __name__ == '__main__':
    main()
