#!/usr/bin/env python3
"""Track Q: a minimal set of connectivity constraints (state, pair, part) that still forces e >= 1 (mcf LP > base + 0.5)
for a window W of states with LOCAL ground set (tq_local.py).  Greedy deletion filter (an IIS in terms of parts).
usage: tq_iis.py DATA.json START K"""
import sys, os, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from tq_exact import build
from tq_mcf import solve_mcf
from tq_roles import roles
d0 = json.load(open(sys.argv[1])); s0, k = int(sys.argv[2]), int(sys.argv[3])
n = d0['n']; E = {frozenset(e) for e in d0['E']}; cols = d0['cols']; L = len(cols)
W = [(s0 + i) % L for i in range(k)]; cs = [cols[i] for i in W]
U, parts, forced = build(n, E, cs); base = 3 * (n - 1) - 8
dd = dict(n=n, cols=cs, forced=forced)
def lpval(ps): return solve_mcf(dd, U, ps, None, 900, True).get('e', -99)
v = lpval(parts); print('window', W, 'U', len(U), 'parts', len(parts), 'LP e', v, flush=True)
keep = list(parts)
# try to drop parts, largest first (keeps the certificate small in vertices)
for P in sorted(parts, key=lambda x: -len(x[3])):
    trial = [x for x in keep if x is not P]
    if lpval(trial) > 0.5: keep = trial
def name(t, p, q):
    j, (a, m, A, B) = roles(cs[t]); nm = {a: 'a', m: 'm', A: 'A', B: 'B'}
    return ''.join(sorted(nm[p] + nm[q], key='amAB'.index))
print('minimal set:', len(keep), 'LP e', lpval(keep))
for (t, p, q, P) in keep:
    print('  state', W[t], 'N', d0['Nprof'][W[t]], 'pair', name(t, p, q), 'size', len(P), 'link', sorted(P & set(range(1, 6))), sorted(P))
