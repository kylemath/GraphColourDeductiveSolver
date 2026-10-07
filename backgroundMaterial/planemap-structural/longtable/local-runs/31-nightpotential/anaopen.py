"""[exploratory] NightPotential: Rtot along open DL runs (or2x.jsonl) vs Gamma-cycles (gamma54.json)."""
import json, sys, glob
from collections import Counter
runs = [json.loads(l) for f in sorted(glob.glob('or2*.jsonl')) for l in open(f)]
T = Counter()
for r in runs:
    P, J, F, R = r['pos'], r['J'], r['fixed'], r['Rtot']; L = len(P)
    T[('min Rtot on DL states', min(R) >= 0)] += 1
    for i in range(L - 1):
        if P[i] is None or P[i+1] is None: T['non-R state in run'] += 1; continue
        d = R[i+1] - R[i]; T[('step', P[i], 'dRtot', d)] += 1
    for i in range(L - 1):
        if P[i] == 8 and J[i] and not J[i+1]: T[('break: Rtot at 8,9', R[i], R[i+1])] += 1
    for i in range(L - 4):
        if P[i] == 4:
            f = (F[i], F[i+2], F[i+4]); T[('window F4 F6 F8', f, 'Rtot468', (R[i], R[i+2], R[i+4]))] += 1
    T[('leave', r['leave'], 'Rtot last DL', R[-1], 'leaveRtot', r['leaveRtot'])] += 1
    T[('last pos', P[-1], r['leave'])] += 1
    b = [i for i in range(L - 1) if P[i] == 8 and J[i] and not J[i+1]]
    if any(y - x == 10 for x in b for y in b): print('DOUBLE BREAK', r['n'], r['g'], r['mir'], r['h'], 'L', L, 'breaks at', b, '\n  pos ', P, '\n  Rtot', R, '\n  J   ', [int(x) for x in J], 'leave', r['leave'], r['leaveRtot'])
    if any(P[i] == 4 and i + 4 < L and F[i] and F[i+4] for i in range(L)): print('W2* FAIL', r['n'], r['g'], r['mir'], r['h'], 'L', L, '\n  pos ', P, '\n  Rtot', R, '\n  fixed', [int(x) for x in F], 'leave', r['leave'], r['leaveRtot'])
for k in sorted(T, key=str): print(k, T[k])
