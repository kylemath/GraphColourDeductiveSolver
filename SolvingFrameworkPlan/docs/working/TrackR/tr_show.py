#!/usr/bin/env python3
"""Track R: describe a price certificate (tr_lag.py --out) structurally.
For each state t: role names, the parts carrying positive MST value, and the Kruskal decomposition
MST_P(u) = sum_levels (theta_{i+1}-theta_i) * (#blocks of P under edges with u < theta_{i+1}  - 1),
i.e. the weighted family of partition inequalities x(delta(pi)) >= |pi| - 1 that the certificate uses.
usage: tr_show.py DATA.json CERT.json"""
import sys, os, json, collections
from fractions import Fraction
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from tr_lag import load, part_edges
sys.path.insert(0, os.path.join(HERE, '..', 'TrackQ'))
from tq_roles import roles


def rolename(c, p, q):
    j, (a, m, A, B) = roles(c); nm = {a: 'a', m: 'm', A: 'A', B: 'B'}
    return ''.join(sorted(nm[p] + nm[q], key='amAB'.index))


def blocks(P, U, ks, allowed):
    par = {v: v for v in P}
    def f(a):
        while par[a] != a: par[a] = par[par[a]]; a = par[a]
        return a
    for k in ks:
        if k in allowed:
            a, b = U[k]; par[f(a)] = f(b)
    g = collections.defaultdict(list)
    for v in P: g[f(v)].append(v)
    return sorted((sorted(x) for x in g.values()), key=lambda x: (-len(x), x))


def decompose(D, u):
    U, parts = D['U'], D['parts']; PE = part_edges(U, parts); out = []
    for i, (t, p, q, P) in enumerate(parts):
        w = {k: u.get((t, k), Fraction(0)) for k in PE[i]}
        levels = sorted(set(w.values()) | {Fraction(0)})
        terms = []
        for lo, hi in zip(levels, levels[1:]):
            bl = blocks(P, U, PE[i], {k for k in PE[i] if w[k] <= lo})
            if len(bl) > 1: terms.append((hi - lo, bl))
        if terms: out.append((t, p, q, P, terms))
    return out


def main():
    D = load(sys.argv[1]) if len(sys.argv) < 4 else load(sys.argv[1], tuple(int(z) for z in sys.argv[3].split(',')))
    C = json.load(open(sys.argv[2]))
    if C['W'] != D['W']: D = load(sys.argv[1], None, (C['W'][0], len(C['W']))) if C.get('glob') else load(sys.argv[1], (C['W'][0], len(C['W'])))
    u = {(t, k): Fraction(v) for t, k, v in C['u']}
    E = {tuple(e) for e in D['E']}; U = D['U']; cols = D['cols']
    print('src', D['src'], 'W', D['W'], 'Nprof', D['Nprof'], 'cert', C['cert'], 'base', C['base'])
    vals = collections.Counter(u.values()); print('price values', {str(k): v for k, v in sorted(vals.items())})
    col = collections.defaultdict(Fraction)
    for (t, k), v in u.items(): col[k] += v
    print('edges priced', len(col), 'of', len(U), '; in G:', sum(1 for k in col if U[k] in E), '; column sums', dict(collections.Counter(str(v) for v in col.values())))
    byt = collections.defaultdict(Fraction)
    for (t, k), v in u.items(): byt[t] += v
    print('price mass by state', {D['W'][t]: str(v) for t, v in sorted(byt.items())})
    tot = 0
    for (t, p, q, P, terms) in decompose(D, u):
        rn = rolename(cols[t], p, q); val = sum(l * (len(b) - 1) for l, b in terms); tot += val
        print('state %d (N=%s) %s |P|=%d link=%s MST=%s' % (D['W'][t], D['Nprof'][t], rn, len(P), sorted(P & set(range(1, 6))), val))
        for l, b in terms:
            print('     %s x (%d blocks) %s' % (l, len(b), ' | '.join(','.join(map(str, x)) for x in b)))
    print('sum MST', tot)


if __name__ == '__main__':
    main()
