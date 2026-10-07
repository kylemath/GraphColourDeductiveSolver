"""[exploratory] NightPotential: Lock1/Lock2 witness sizes (jobae.json, all Gamma records) around step-8 breaks."""
import json, os
from collections import Counter, defaultdict
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../27-studio-positive-config/jobuv/')
AE = json.load(open(D + 'jobae.json')); T = Counter(); traj = defaultdict(list)
for e in AE:
    d = e['deg']; R = e['rows']; n = e['L']; P = n // 10
    for b in range(P):
        brk = R[10*b+8]['J'] and not R[10*b+9]['J']
        T[(d, 'brk', brk, 'L2@9', R[10*b+9]['L2'])] += 1
        T[(d, 'brk', brk, 'L2@9 - L2@8', R[10*b+9]['L2'] - R[10*b+8]['L2'])] += 1
        traj[(d, brk)].append([R[(10*b + t) % n]['L2'] for t in range(8, 20)])
        traj[(d, brk, 'L1')].append([R[(10*b + t) % n]['L1'] for t in range(8, 20)])
for k in sorted(T, key=str): print(k, T[k])
for k, v in sorted(traj.items(), key=str):
    print(k, 'n', len(v), 'mean witness size, positions 8..19:', ' '.join('%5.2f' % (sum(x[t] for x in v) / len(v)) for t in range(12)), ' min', ' '.join('%2d' % min(x[t] for x in v) for t in range(12)))
