"""Idea D: hub ledgers. Forget the target: a 'hub picture' is the cyclic slot sequence up to rotation and
reflection (the hub's dihedral group). Each picture carries a ledger: which spokes receive how much.
Counts pictures vs parts, real vs null, and how many ledgers are hub-symmetric splits."""
import collections as C
from common import *
from mir import mirror
def refl(slots):
    # reflection of the cyclic sequence about slot 0 = the validated part mirror (t=0)
    return mirror(dict(hub=len(slots), slots=slots), 0, 1, 'with_spoke')
def picture(p):
    h = p['hub']; S = tuple(p['slots']); best = None
    for T in (S, refl(S)):
        for r in range(h):
            x = T[r:] + T[:r]
            if best is None or x < best: best = x
    return (h, best)
def run(P):
    out = {}
    for name, sel in (('all', lambda p: True), ('SP', lambda p: p['pre'] == 'SP_'), ('drule', lambda p: p['pre'] == 'drule'), ('ST', lambda p: p['pre'][:2] == 'ST')):
        g = C.defaultdict(list)
        for p in P:
            if sel(p): g[picture(p)].append(p['w'])
        out[name] = (sum(len(v) for v in g.values()), len(g), sorted(C.Counter(tuple(sorted(v)) for v in g.values()).items(), key=lambda x: -x[1])[:6])
    return out
P = load()
print('real', run(P))
for i, Q in enumerate(nulls(P)): print('null', i, {k: v[:2] for k, v in run(Q).items()})
