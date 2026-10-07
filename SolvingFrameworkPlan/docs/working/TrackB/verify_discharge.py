#!/usr/bin/env python3
"""[Track B] Independent check of a discharging rule (out/discharge*.json) on actual graphs.
For each graph: apply the rule with true degrees (D = min(deg,8), letters capped at 8), compute final charges, and check
 (1) total charge = 12 (Euler sanity), (2) every vertex of degree >= 7 ends <= 0, (3) every 5-vertex whose word is not in
 S ends <= 0, (4) hence some 5-vertex has a word in S.  Supports the one-step rule (keys (p,D,q)) and the word rule
 (keys (D,a,b,c,e)).
Usage: python3 verify_discharge.py RULE.json graphfile [...]"""
import sys, json, ast
from words import load, canon, fmt
R = json.load(open(sys.argv[1])); sig = {ast.literal_eval(k): v for k, v in R['sigma'].items()}
S = set(R['S_allowed']) | set(R['S_forbidden'])
kind = 3 if len(next(iter(sig))) == 3 else 5
def amount(y, u, rot, deg):
    r = rot[y]; i = r.index(u); c = lambda x: min(deg[x], 8)
    D = c(u)
    if kind == 3:
        p, q = c(r[(i - 1) % 5]), c(r[(i + 1) % 5]); return sig.get((min(p, q), D, max(p, q)), 0.0)
    t = (D, c(r[(i + 1) % 5]), c(r[(i + 2) % 5]), c(r[(i + 3) % 5]), c(r[(i + 4) % 5]))
    t2 = (D, t[4], t[3], t[2], t[1]); return sig.get(min(t, t2), 0.0)
G = load(sys.argv[2:]); bad = 0; mx7 = -9; mx5 = -9
for name, n, rot in G:
    deg = [len(r) for r in rot]; ch = [6.0 - d for d in deg]
    for y in range(n):
        if deg[y] != 5: continue
        for u in rot[y]:
            if deg[u] >= 7:
                a = amount(y, u, rot, deg); ch[y] -= a; ch[u] += a
    assert abs(sum(ch) - 12) < 1e-6
    for v in range(n):
        if deg[v] >= 7: mx7 = max(mx7, ch[v]); bad += ch[v] > 1e-9
        if deg[v] == 5 and fmt(canon([min(deg[u], 8) for u in rot[v]]), 8) not in S:
            mx5 = max(mx5, ch[v]); bad += ch[v] > 1e-9
    if not any(deg[v] == 5 and fmt(canon([min(deg[u], 8) for u in rot[v]]), 8) in S for v in range(n)):
        bad += 1; print('no S word in', name)
print('graphs', len(G), 'violations', bad, 'max final charge at deg>=7: %.4f, at 5-vertices outside S: %.4f' % (mx7, mx5))
