"""[exploratory] NightPotential: separation tables (step-8 break, fixed points) vs candidate potentials at fixed positions."""
import json, sys
from collections import Counter
G = json.load(open(sys.argv[1] if len(sys.argv) > 1 else 'gamma54.json'))
T = Counter(); rows = []
for x in G:
    R = x['rows']; n = len(R)
    for b in range(0, n, 10):
        per = [R[(b + t) % n] for t in range(10)]
        brk = per[8]['J'] and not per[9]['J']; fx = ''.join('X' if per[t]['fixed'] else '.' for t in (4, 6, 8))
        T[('brk', brk, 'esc8', per[8]['esc'])] += 1
        T[('brk', brk, 'Rtot8', per[8]['Rtot'])] += 1
        T[('brk', brk, 'Rtot9', per[9]['Rtot'])] += 1
        T[('brk', brk, 'alMu8', per[8]['alMu'])] += 1
        T[('brk', brk, 'AB8', per[8]['AB'])] += 1
        T[('brk', brk, 'fixed8', per[8]['fixed'])] += 1
        T[('fixpat', fx, 'Rtot468', (per[4]['Rtot'], per[6]['Rtot'], per[8]['Rtot']))] += 1
        T[('fixcount', fx.count('X'), 'minRtot', min(r['Rtot'] for r in per))] += 1
        T[('brk', brk, 'Rtot traj', tuple(r['Rtot'] for r in per))] += 1
        T[('brk', brk, 'Kst8has', per[8]['Kst_has'])] += 1
for k in sorted(T, key=str): print(k, T[k])
print('cycles with a break: per-period (brk, fixpattern, Rtot at pos 0..9)')
for x in G:
    R = x['rows']; n = len(R); s = []
    for b in range(0, n, 10):
        per = [R[(b + t) % n] for t in range(10)]
        s.append(((per[8]['J'] and not per[9]['J']), ''.join('X' if per[t]['fixed'] else '.' for t in (4, 6, 8)), ''.join(str(r['Rtot']) for r in per), ''.join(str(r['esc']) for r in per)))
    if any(t[0] for t in s): print(x['id'], s)
