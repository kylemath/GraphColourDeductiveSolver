"""[exploratory] NightPotential: per-step / per-period statistics of candidate potentials on the regenerated Gamma-cycles (gamma54.json)."""
import json, sys
from collections import Counter, defaultdict
G = json.load(open(sys.argv[1] if len(sys.argv) > 1 else 'gamma54.json'))
for x in G:
    for r in x['rows']: r['R3'] = r['AB'] + r['muA'] + r['muB']; r['Ra'] = r['alMu'] + r['alA'] + r['alB']; r['L12'] = r['L1'] + r['L2']; r['Jn'] = int(r['J'])
POT = ['L1', 'L2', 'L12', 'AB', 'muA', 'muB', 'R3', 'alMu', 'alA', 'alB', 'Ra', 'Rtot', 'Ntot', 'Ksig', 'Kst', 'KstL1', 'KstL2', 'esc', 'Kyz', 'Jn']
print('cycles', len(G), 'L', Counter(x['L'] for x in G), 'periods', sum(x['L'] // 10 for x in G))
print('identity Rtot = Ntot - 8:', Counter(r['Rtot'] - r['Ntot'] for x in G for r in x['rows']))
print('min Rtot', min(r['Rtot'] for x in G for r in x['rows']), ' min per pair alA, alB (role ranks):', min(r['alA'] for x in G for r in x['rows']), min(r['alB'] for x in G for r in x['rows']))
# failures
def periods(x):
    n = x['L']; R = x['rows']
    for b in range(0, n, 10):
        per = [R[(b + t) % n] for t in range(10)]; nxt = R[(b + 10) % n]
        brk8 = per[8]['J'] and not per[9]['J']          # => k4 failure at next period start
        fix = sum(per[t]['fixed'] for t in (4, 6, 8))
        yield b, per, nxt, brk8, fix
ev = Counter()
for x in G:
    for b, per, nxt, brk8, fix in periods(x): ev[('break8', brk8)] += 1; ev[('fixed', fix)] += 1; ev[('k4fail', not per[0]['ex'])] += 1; ev[('k3fail', not per[2]['ex'])] += 1
print('events', sorted(ev.items(), key=str))
print('\n%-6s | per-step mean dPhi at steps 0..9 | per-period dPhi distribution | Phi(period start) constant within cycle | spread' % 'pot')
for P in POT:
    st = defaultdict(list); pp = Counter(); const = 0; spread = []
    for x in G:
        R = x['rows']; n = len(R)
        for i in range(n): st[i % 10].append(R[(i + 1) % n][P] - R[i][P])
        starts = [R[b][P] for b in range(0, n, 10)]
        for b in range(0, n, 10): pp[R[(b + 10) % n][P] - R[b][P]] += 1
        const += len(set(starts)) == 1; spread.append(max(r[P] for r in R) - min(r[P] for r in R))
    print('%-6s | %s | %s | %d/%d | max %d' % (P, ' '.join('%+5.2f' % (sum(st[i]) / len(st[i])) for i in range(10)), sorted(pp.items())[:9], const, len(G), max(spread)))
# separation: windows (period b) with brk8 vs not; with fix>=2 vs not
print('\nseparation: mean Phi at positions 0..9 in break periods vs others (break = step-8 break in this period)')
for P in POT:
    A = defaultdict(list); B = defaultdict(list)
    for x in G:
        for b, per, nxt, brk8, fix in periods(x):
            for t in range(10): (A if brk8 else B)[t].append(per[t][P])
    if not A[0]: continue
    print('%-6s brk %s\n%-6s oth %s' % (P, ' '.join('%5.2f' % (sum(A[t]) / len(A[t])) for t in range(10)), '', ' '.join('%5.2f' % (sum(B[t]) / len(B[t])) for t in range(10))))
