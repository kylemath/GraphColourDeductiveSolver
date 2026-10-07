#!/usr/bin/env python3
"""Job V: p27 #316043 h18, plantri orientation: the (5,5,5,6,6) Gamma-cycle with C = 18 < D = 20. Its sigma-group and (sigma u sigma')-group (links from DD endpoints:
sigma = {alpha,mu}-swap at m; sigma' = every link-free swap whose result is not DL), each cycle with w, L, #DD endpoints, links with target ids and credits."""
from uv_lib import Hole
from collections import defaultdict
H = Hole('p27#316043', 18, False)
print('p27 #316043 hole 18, plantri orientation; link degrees %s; states %d; pi-cycles %d; class sum w %d' % ([len(H.rot[x]) for x in H.L], H.S, len(H.cycles), sum(H.W)))
G = [ci for ci, z in enumerate(H.cycles) if all(H.DL[x] for x in z)]
lmask = 0
for i in H.sp.linki: lmask |= 1 << i
sig = defaultdict(list); sigp = defaultdict(list)
for k in range(H.S):
    if not H.isDDend(k): continue
    s = H.sigma(k); j, ty, hi, roles = H.frame(k)
    lk = H.locks(s); kind = 'filled' if H.filled(s) else ('lockless' if not lk[0] and not lk[1] else ('DL' if lk[0] and lk[1] else ('Lock1' if lk[0] else 'Lock2')))
    cr = 3 * H.f_after(s) - 1 if kind == 'lockless' else 0
    if H.cyc[s] != H.cyc[k]: sig[H.cyc[k]].append((H.cyc[s], 'R%d' % ty, kind, cr))
    for t, p, q, K in H.sp.moves(k):
        if t == k or K & lmask or H.DL[t]: continue
        if H.cyc[t] != H.cyc[k]: sigp[H.cyc[k]].append(H.cyc[t])
def group(links):
    up = list(range(len(H.cycles)))
    def f(x):
        while up[x] != x: up[x] = up[up[x]]; x = up[x]
        return x
    for a, L in links.items():
        for t in L: up[f(a)] = f(t[0] if isinstance(t, tuple) else t)
    return [ci for ci in range(len(H.cycles)) if f(ci) == f(G[0])]
for name, links in (('sigma-group', sig), ('(sigma u sigma\')-group', {a: list(sig[a]) + list(sigp[a]) for a in set(sig) | set(sigp)})):
    g = group(links); print('\n== %s of Gamma-cycle %d: %d cycles, total sum lambda = %d (sum w = %d)' % (name, G[0], len(g), 5 * sum(H.W[c] for c in g), sum(H.W[c] for c in g)))
    for c in g:
        z = H.cycles[c]; nDD = sum(1 for x in z if H.isDDend(x))
        sl = sorted(set(sig[c])); spl = sorted(set(sigp[c]))
        print('   cycle %3d: w %4d L %4d DD-endpoints %3d%s | sigma-links (target, type, image kind, credit): %s | sigma\'-targets: %s'
              % (c, H.W[c], len(z), nDD, ' GAMMA' if c in G else '', sl[:12] + (['...'] if len(sl) > 12 else []), spl[:20]))
z = H.cycles[G[0]]
print('\nGamma-cycle %d states in pi-order (type, high-degree positions relative to j, sigma image kind, f):' % G[0])
for x in z:
    j, ty, hi, roles = H.frame(x); s = H.sigma(x); lk = H.locks(s)
    kind = 'filled' if H.filled(s) else ('lockless' if not lk[0] and not lk[1] else ('fixed' if s == x else ('DL' if lk[0] and lk[1] else ('Lock1' if lk[0] else 'Lock2'))))
    print('   state %4d R%d hi %s exit %-8s f %s' % (x, ty, hi, kind if ty == 3 else '-', H.f_after(s) if kind == 'lockless' and ty == 3 else '-'))
print('R2 states on the Gamma-cycle:', [x for x in z if H.frame(x)[1] == 2])
