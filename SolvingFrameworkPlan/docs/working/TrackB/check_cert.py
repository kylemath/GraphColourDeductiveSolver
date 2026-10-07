#!/usr/bin/env python3
"""[Track B] Exact (rational) re-check of a discharging certificate written by discharge_lp.py / discharge_lp2.py.
sigma and phi are rationalised (limit_denominator(DEN)); then, in exact arithmetic:
  d = 7  : every cyclic sequence (enumerated: (z) for the 3-key rule; (z,w) pairs via exact max-plus DP for the 5-key rule)
           receives <= 1;
  d >= 8 : every transition satisfies weight <= 1/4 + phi(next) - phi(cur)  (=> every cycle has mean <= 1/4 => receipt <= d/4 <= d-6);
  S      : recomputed exactly as {w : sent(w) < 1} and compared with the JSON.
Usage: python3 check_cert.py RULE.json [DEN]"""
import sys, json, ast, itertools
from fractions import Fraction as F
from words import canon, fmt
R = json.load(open(sys.argv[1])); DEN = int(sys.argv[2]) if len(sys.argv) > 2 else 240
sig = {ast.literal_eval(k): F(v).limit_denominator(DEN) for k, v in R['sigma'].items()}
phi = {ast.literal_eval(k): F(v).limit_denominator(DEN) for k, v in R['phi'].items()}
L = [5, 6, 7, 8]; kind = len(next(iter(sig)))
def s3(p, D, q): return sig.get((min(p, q), D, max(p, q)), F(0))
def s5(D, a, b, c, e): return sig.get(min((D, a, b, c, e), (D, e, c, b, a)), F(0))
ok = True
if kind == 3:
    mx = max(sum(s3(z[i - 1], 7, z[(i + 1) % 7]) for i in range(7) if z[i] == 5) for z in itertools.product(L, repeat=7))
    print('d=7 max receipt', mx); ok &= mx <= 1
    for a in L:
        for b in L:
            for c in L:
                w = s3(a, 8, c) if b == 5 else F(0)
                if w > F(1, 4) + phi[(b, c)] - phi[(a, b)]: ok = False; print('potential violated', a, b, c)
    def sent(w): return sum(s3(w[i - 1], w[i], w[(i + 1) % 5]) for i in range(5) if w[i] >= 7)
else:
    states = list(itertools.product(L, repeat=4))
    def wt(s, t, D): z0, w0, z1, w1 = s; z2 = t[2]; return s5(D, z2, w1, w0, z0) if z1 == 5 else F(0)
    succ = {s: [(s[2], s[3], z, w) for z in L for w in L] for s in states}
    mx = F(-1)
    for s0 in states:
        val = {t: wt(s0, t, 7) for t in succ[s0]}
        for step in range(6):
            nv = {}
            for s, v in val.items():
                for t in succ[s]:
                    x = v + wt(s, t, 7)
                    if t not in nv or x > nv[t]: nv[t] = x
            val = nv
        if s0 in val and val[s0] > mx: mx = val[s0]
    print('d=7 max receipt', mx); ok &= mx <= 1
    for s in states:
        for t in succ[s]:
            if wt(s, t, 8) > F(1, 4) + phi[t] - phi[s]: ok = False; print('potential violated', s, t); break
    def sent(w): return sum(s5(w[i], w[(i + 1) % 5], w[(i + 2) % 5], w[(i + 3) % 5], w[(i + 4) % 5]) for i in range(5) if w[i] >= 7)
words = sorted({canon(list(w)) for w in itertools.product(L, repeat=5)})
S = {fmt(w, 8) for w in words if sent(w) < 1}
print('exact |S| =', len(S), 'matches JSON:', S == set(R['S_allowed']) | set(R['S_forbidden']))
print('CERTIFICATE', 'OK' if ok else 'FAILED')
