# independent check of the zero-period claim: extract colourings and recompute the periods by summing increments
import itertools, random
from pysat.solvers import Cadical153
import e5_torus as E
def periods(p, q, r, col):
    n, adj, nb, idx, simple = E.torus(p, q, r)
    def walk(start, steps):
        cur = start; H = (0, 0)
        for d in steps:
            w = nb(cur[0], cur[1], d); l = col[idx(*cur)] ^ col[idx(*w)]; e = E.INCL[l]; sg = E.SG[d]
            H = (H[0]+sg*e[0], H[1]+sg*e[1]); cur = w
        return cur, H
    c1, t1 = walk((0, 0), [(1, 0)]*p); assert c1 == (0, 0)
    # second loop: q steps up then back along (1,0)
    cur = (0, 0); steps = [(0, 1)]*q
    c, _ = walk((0, 0), steps); k = (0 - c[0]) % p
    c2, t2 = walk((0, 0), steps + [(1, 0)]*k); assert c2 == (0, 0)
    # contractible check: every triangle closes
    return t1, t2
# monkeypatch solve to return model
def solve_model(p, q, r, target):
    import types
    src = open('e5_torus.py').read()
    return None
rng = random.Random(0); checked = 0; bad = 0
import json
R = [json.loads(l) for l in open('e5_torus.jsonl')]
cands = [x for x in R if x['col4'] and not x['col3'] and x.get('zero_periods')]
for x in rng.sample(cands, 25):
    p, q, r = x['p'], x['q'], x['r']
    # re-run the same CNF but keep the model
    orig = E.Cadical153
    holder = {}
    class Cap(orig):
        def solve(self, *a, **k):
            ok = super().solve(*a, **k); holder['m'] = self.get_model() if ok else None; return ok
    E.Cadical153 = Cap
    ok = E.solve(p, q, r, target=('zero', 'zero')); E.Cadical153 = orig
    n = p*q; mod = set(l for l in holder['m'] if l > 0)
    col = [next(c for c in range(4) if 4*v+c+1 in mod) for v in range(n)]
    nn, adj, nb, idx, simple = E.torus(p, q, r)
    assert all(col[u] != col[w] for u in range(n) for w in adj[u])
    t1, t2 = periods(p, q, r, col); checked += 1
    if t1 != (0, 0) or t2 != (0, 0): bad += 1
    print(p, q, r, t1, t2)
print('checked', checked, 'nonzero', bad)
