"""[exploratory] NightPotential: per-step change of each of the six pair ranks (named by the PRE-step roles; swap pair {alpha,A}) on DL->DL R-steps,
Gamma (gamma54.json) and open runs (or2x.jsonl).  Role map across an R+3 step: alpha'=alpha, mu'=B, A'=mu, B'=A (absolute colours)."""
import json, glob
from collections import Counter, defaultdict
MAP = {'alMu': 'alA', 'alB': 'alMu', 'muA': 'AB', 'AB': 'muB', 'alA': 'alB', 'muB': 'muA'}   # old pair -> its role name in the new state
def seqs():
    for x in json.load(open('gamma54.json')):
        R = x['rows']; yield 'Gamma', R + [R[0]]
    for f in sorted(glob.glob('or2*.jsonl')):
        for l in open(f):
            r = json.loads(l); yield 'open', [dict(pos=p, Rtot=t, **rk) for p, t, rk in zip(r['pos'], r['Rtot'], r['ranks'])]
T = defaultdict(Counter)
for lab, R in seqs():
    for i in range(len(R) - 1):
        a, b = R[i], R[i + 1]
        if a['pos'] is None or b['pos'] is None: continue
        for old, new in MAP.items(): T[(lab, old)][b[new] - a[old]] += 1
        T[(lab, 'Rtot')][b['Rtot'] - a['Rtot']] += 1
        T[(lab, 'alpha-free R3 (role sum)')][(b['AB'] + b['muA'] + b['muB']) - (a['AB'] + a['muA'] + a['muB'])] += 1
for k in sorted(T): print(k, sorted(T[k].items()))
