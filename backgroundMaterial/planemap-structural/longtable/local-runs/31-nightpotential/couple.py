"""[exploratory] NightPotential: on all Gamma-cycle records of jobah.json + jobae.json (joined by index; same hole order and rotation),
test (i) step-8 break => R3k0 fixed (F8); (ii) break in period b => F4 (R3k2 fixed) in period b+1; (iii) W2*: not F4 and F8 in one period;
and the rank-vector potential (AB, muA, muB) at the R3 positions."""
import json, os
from collections import Counter
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../27-studio-positive-config/jobuv/')
AH = json.load(open(D + 'jobah.json')); AE = json.load(open(D + 'jobae.json'))
assert len(AH) == len(AE)
T = Counter()
for a, e in zip(AH, AE):
    assert (a['run'], a['name'], a['hole'], a['L']) == (e['run'], e['name'], e['hole'], e['L'])
    assert all(r['ty'] == s['ty'] and r['k'] == s['k'] for r, s in zip(a['rows'], e['rows']))
    d = a['deg']; R = a['rows']; E = e['rows']; n = a['L']; P = n // 10
    brk = [E[10*b + 8]['J'] and not E[10*b + 9]['J'] for b in range(P)]
    F = [[R[10*b + t]['fixed'] for t in (4, 6, 8)] for b in range(P)]
    AB8 = [R[10*b + 8]['AB'] for b in range(P)]
    for b in range(P):
        nb = (b + 1) % P
        T[(d, 'brk', brk[b], 'F8', F[b][2])] += 1
        if brk[b]: T[(d, 'brk => next F4', F[nb][0], 'next brk', brk[nb], 'P', P)] += 1
        T[(d, 'F4&F8 same period (W2*)', F[b][0] and F[b][2])] += 1
        T[(d, 'F8(b) & F4(b+1)', F[b][2] and F[nb][0], 'brk', brk[b])] += 1
        T[(d, 'all three fixed', all(F[b]))] += 1
        if brk[b]: T[(d, 'brk: rank vector (AB,muA,muB) at pos8', (R[10*b+8]['AB'], R[10*b+8]['muA'], R[10*b+8]['muB']))] += 1
for k in sorted(T, key=str): print(k, T[k])
