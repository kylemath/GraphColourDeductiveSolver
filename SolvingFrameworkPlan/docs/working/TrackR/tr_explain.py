#!/usr/bin/env python3
"""Track R: express every partition inequality of a price certificate (tr_lag.py --out) structurally:
find the smallest set of 'structural partitions' whose meet with the part P gives exactly the blocks used.
Structural partitions at a window state s:  Pi(s, R) for a role label R in {P1, P2, P3} (vertex partition into the
components of the two pair graphs of that role at s), and the swap split {K_s, V - K_s}.
usage: tr_explain.py DATA.json CERT.json [maxsize]"""
import sys, os, json, itertools, collections
from fractions import Fraction
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from tr_lag import load
from tr_show import decompose, rolename
sys.path.insert(0, os.path.join(HERE, '..', 'TrackQ'))
from tq_roles import roles
from tn_forest import components, PAIRS

ROLEOF = {'am': 'P1', 'AB': 'P1', 'aA': 'P2', 'mB': 'P2', 'aB': 'P3', 'mA': 'P3'}


def struct_partitions(D):
    n = D['n']; E = [tuple(e) for e in D['E'] if 0 not in e]; cols = D['cols']; L = len(cols); out = []
    for s, c in enumerate(cols):
        lab = {}
        for (p, q) in PAIRS:
            V = [v for v in range(1, n) if c[v] in (p, q)]
            for P in components(V, [e for e in E if c[e[0]] in (p, q) and c[e[1]] in (p, q)]):
                R = ROLEOF[rolename(c, p, q)]
                for v in P: lab.setdefault(R, {})[v] = (p, q, min(P))
        for R in ('P1', 'P2', 'P3'): out.append(((s, R), lab[R]))
        if s + 1 < L or len(cols) == len(D.get('Wfull', cols)):
            c2 = cols[(s + 1) % L]; j, (a, m, A, B) = roles(c); j2, (a2, m2, A2, B2) = roles(c2)
            mp = {a: a2, m: A2, B: m2, A: B2}
            if s + 1 < L:
                K = {v for v in range(1, n) if mp[c[v]] != c2[v]}
                out.append(((s, 'K'), {v: (v in K) for v in range(1, n)}))
    return out


def meet_blocks(P, labs):
    g = collections.defaultdict(list)
    for v in P: g[tuple(l[v] for l in labs)].append(v)
    return sorted((sorted(x) for x in g.values()), key=lambda x: (-len(x), x))


def main():
    C = json.load(open(sys.argv[2])); mx = int(sys.argv[3]) if len(sys.argv) > 3 else 3
    D = load(sys.argv[1], None, (C['W'][0], len(C['W']))) if C.get('glob') else (load(sys.argv[1]) if len(C['W']) == len(json.load(open(sys.argv[1]))['cols']) else load(sys.argv[1], (C['W'][0], len(C['W']))))
    u = {(t, k): Fraction(v) for t, k, v in C['u']}
    SP = struct_partitions(D)
    print('src', D['src'], 'W', D['W'], 'Nprof', D['Nprof'], 'cert', C['cert'])
    stats = collections.Counter()
    for (t, p, q, P, terms) in decompose(D, u):
        rn = rolename(D['cols'][t], p, q)
        for lam, bl in terms:
            target = sorted((sorted(x) for x in bl), key=lambda x: (-len(x), x))
            found = None
            if all(len(x) == 1 for x in bl): found = 'singletons'
            else:
                cand = [(nm, lab) for nm, lab in SP if nm[0] != t]
                for r in range(1, mx + 1):
                    for comb in itertools.combinations(cand, r):
                        if meet_blocks(P, [lab for _, lab in comb]) == target:
                            found = ' ^ '.join('%s@%+d' % (nm[1], nm[0] - t) for nm, _ in comb); break
                    if found: break
            stats[found is not None] += 1
            print('  t=%d(N=%s) %s |P|=%d  %s x %d blocks : %s' % (t, D['Nprof'][t], rn, len(P), lam, len(bl), found or 'NOT a meet of <= %d structural partitions' % mx))
    print('explained', stats[True], 'unexplained', stats[False])


if __name__ == '__main__':
    main()
