"""[exploratory] NightPotential: for each potential and each phase t0, the sign of dPhi over the 10-step window that contains a step-8 break,
on Gamma-cycles (jobah+jobae joined, all 670 records; gamma54 for Rtot/esc) and on open runs (or2x.jsonl).  A potential with
'break window => dPhi < 0' at some phase proves A34' on L = 20 Gamma-cycles by closure (the two windows' changes sum to 0)."""
import json, os, glob
from collections import Counter, defaultdict
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../27-studio-positive-config/jobuv/')
AH = json.load(open(D + 'jobah.json')); AE = json.load(open(D + 'jobae.json'))
cyc = []
for a, e in zip(AH, AE):
    rows = [dict(r, **{k: s[k] for k in ('L1', 'L2', 'Kyz', 'J', 'Ksize')}) for r, s in zip(a['rows'], e['rows'])]
    for r in rows: r['R3'] = r['AB'] + r['muA'] + r['muB']; r['Jn'] = int(r['J']); r['L12'] = r['L1'] + r['L2']
    cyc.append((a['deg'], rows))
G54 = json.load(open('gamma54.json'))
for x in G54:
    for r in x['rows']: r['R3'] = r['AB'] + r['muA'] + r['muB']
def test(cycles, pots, closed, label):
    for P in pots:
        res = {}
        for t0 in range(10):
            sg = Counter()
            for deg, R in cycles:
                n = len(R)
                for i in range(n - 1 if not closed else n):
                    if R[i]['pos'] if 'pos' in R[i] else None: pass
                for b in range(0, n, 10) if closed else []:
                    pass
                for i in range(n if closed else n - 1):
                    pi = i % 10 if closed else R[i]['pos']
                    if pi != 8: continue
                    if not (R[i]['J'] and not R[(i + 1) % n]['J']): continue
                    st = i - ((8 - t0) % 10)
                    if closed: d = R[(st + 10) % n][P] - R[st % n][P]
                    else:
                        if st < 0 or st + 10 >= n: continue
                        d = R[st + 10][P] - R[st][P]
                    sg[(d > 0) - (d < 0)] += 1
            res[t0] = sg
        good = [t0 for t0 in range(10) if res[t0] and set(res[t0]) == {-1}]
        print('%-14s %-6s  phases with every break window dPhi<0: %s   per phase (neg,zero,pos): %s' % (label, P, good, ' '.join('%d:%d/%d/%d' % (t0, res[t0][-1], res[t0][0], res[t0][1]) for t0 in range(10))))
test([c for c in cyc if c[0] == 6], ['L1', 'L2', 'L12', 'AB', 'muA', 'muB', 'R3', 'Kyz', 'Ksize'], True, 'Gamma deg6')
test([c for c in cyc if c[0] == 7], ['L1', 'L2', 'L12', 'AB', 'muA', 'muB', 'R3', 'Kyz', 'Ksize'], True, 'Gamma deg7')
test([(6, x['rows']) for x in G54], ['Rtot', 'R3', 'alMu', 'alA', 'alB', 'esc', 'Kst'], True, 'Gamma54')
runs = []
for f in sorted(glob.glob('or2*.jsonl')):
    for l in open(f):
        r = json.loads(l); R = [dict(pos=p, J=j, Rtot=t, **rk) for p, j, t, rk in zip(r['pos'], r['J'], r['Rtot'], r['ranks'])]
        for x in R: x['R3'] = x['AB'] + x['muA'] + x['muB']
        runs.append((6, R))
test(runs, ['Rtot', 'R3', 'AB', 'muA', 'muB', 'alMu', 'alA', 'alB'], False, 'open 22-24')
