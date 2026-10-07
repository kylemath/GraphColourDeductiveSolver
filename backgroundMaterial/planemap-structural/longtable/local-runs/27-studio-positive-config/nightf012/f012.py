#!/usr/bin/env python3
"""f012.py (NightF012): k<=2 credit on (5,5,5,5,6) Gamma-cycles, from jobm-gamma-sequences.jsonl and jobo-steps.jsonl. Usage: python3 f012.py [DIR, default ../; ../jobr27/ for order 27].
Single core, < 1 s. Run from this directory: python3 f012.py"""
import json, itertools
from collections import Counter, defaultdict
import sys
D = sys.argv[1] if len(sys.argv) > 1 else '../'
K1 = {1: 0, 2: 1, 4: 2, 8: 3, 16: 4}
cycles = []   # (run, name, hole, list of (type, k, exit, f))
for l in open(D + 'jobm-gamma-sequences.jsonl'):
    r = json.loads(l)
    if r['pattern'] != '5,5,5,5,6': continue
    for cyc in r['jobm']:
        s0 = next(i for i, x in enumerate(cyc) if x[0] == 3 and x[1] == 16)
        cyc = cyc[s0:] + cyc[:s0]
        cycles.append((r['run'], r['name'], r['hole'], [(t, K1[km], e, f) for t, km, e, f in cyc]))
# (the jobm 'X' label = jobq fixed-point flag at every R3 state: see xcheck.py)
def cr(x): return 3 * x[3] - 1 if x[0] == 3 and x[2] == 'L' else 0
def lab(x):
    if x[0] != 3: return '.'
    return {'L': 'L%d' % x[3], 'X': 'X'}.get(x[2], 'S' + x[2])
print('cycle records', len(cycles), 'L:', Counter(len(c[3]) for c in cycles))
# 1. per period credits (period = 10 states from R3k4)
pk = Counter(); pt = Counter(); low = []
for run, name, hole, cyc in cycles:
    L = len(cyc)
    for b in range(0, L, 10):
        per = cyc[b:b + 10]
        c012 = sum(cr(x) for x in per if x[1] <= 2); c34 = sum(cr(x) for x in per if x[0] == 3 and x[1] >= 3)
        pk[c012] += 1; pt[c012 + c34] += 1
        if c012 < 7: low.append((run, name, hole, b // 10, c012, c34, ' '.join(lab(x) for x in per if x[0] == 3)))
print('\n[1] per-period k<=2 credit (period from R3k4) histogram:', sorted(pk.items()))
print('    periods with k<=2 credit < 7: %d of %d' % (len(low), sum(pk.values())))
for x in low: print('     ', x)
# 2. all 10 phases: per-window k<=2 credit min and total credit min
print('\n[2] windows of 10 consecutive states (any phase): min k<=2 credit, min total credit, #windows with total < 10')
for ph in range(10):
    m012 = 99; mt = 99; nb = 0; nw = 0
    for run, name, hole, cyc in cycles:
        L = len(cyc)
        for b in range(ph, L + ph, 10):
            per = [cyc[(b + i) % L] for i in range(10)]
            c = sum(cr(x) for x in per if x[1] <= 2); t = sum(cr(x) for x in per)
            m012 = min(m012, c); mt = min(mt, t); nb += t < 10; nw += 1
    print('    phase %d (starts at %s): min k<=2 %d, min total %d, total<10 in %d/%d' % (ph, 'R%dk%d' % (cycles[0][3][ph][0], cycles[0][3][ph][1]), m012, mt, nb, nw))
# 3. per cycle: k<=2 credit / (7L/20), and the L=60 sliding windows of 2 periods
print('\n[3] per cycle k<=2 credit minus 7L/20 histogram:', sorted(Counter(sum(cr(x) for x in c[3] if x[1] <= 2) - 7 * len(c[3]) // 20 for c in cycles).items()))
for run, name, hole, cyc in cycles:
    if len(cyc) == 60:
        w = [sum(cr(x) for x in cyc[b:b + 10] if x[1] <= 2) for b in range(0, 60, 10)]
        print('    L=60 %s %s h%d per-period k<=2 credits %s' % (run, name, hole, w))
# 4. joint lemmas
print('\n[4] joint statements')
def per_list(cyc):
    return [cyc[b:b + 10] for b in range(0, len(cyc), 10)]
J1 = Counter(); J2 = Counter(); J3 = Counter()
for run, name, hole, cyc in cycles:
    pers = per_list(cyc); n = len(pers)
    for i, per in enumerate(pers):
        r3 = {x[1]: x for x in per if x[0] == 3}
        nfx = sum(1 for k in (0, 1, 2) if r3[k][2] == 'X')
        good34 = lambda P: all(P[k][2] == 'L' and P[k][3] == 3 for k in (3, 4))
        if nfx:
            J1[good34(r3)] += 1
            nxt = {x[1]: x for x in pers[(i + 1) % n] if x[0] == 3}
            J2[good34(nxt)] += 1
            J3[good34(r3) or good34(nxt)] += 1
print('    J1 (period with a k<=2 fixed point has k=3,4 lockless f=3 in the SAME period): holds %d, fails %d' % (J1[True], J1[False]))
print('    J2 (... in the NEXT period): holds %d, fails %d' % (J2[True], J2[False]))
print('    J3 (... in the same or the next): holds %d, fails %d' % (J3[True], J3[False]))
# failure count per period vs credit at k3,k4
tab = Counter()
for run, name, hole, cyc in cycles:
    for per in per_list(cyc):
        r3 = {x[1]: x for x in per if x[0] == 3}
        bad012 = sum(1 for k in (0, 1, 2) if r3[k][2] != 'L'); bad34 = sum(1 for k in (3, 4) if r3[k][2] != 'L')
        tab[(bad34, bad012)] += 1
print('    periods by (#k>=3 failures, #k<=2 failures):', sorted(tab.items()))
# 5. patterns of the five R3 exits per period (k = 4,3,2,1,0 order), with f
pat = Counter()
for run, name, hole, cyc in cycles:
    for per in per_list(cyc): pat[' '.join(lab(x) for x in per if x[0] == 3)] += 1
print('\n[5] per-period R3 exit labels (order k=4,3,2,1,0; L<f> lockless, X fixed, S1/S2 single-lock):')
for k, v in pat.most_common(): print('    %3d  %s' % (v, k))
# 6. what precedes/follows low f at k<=2
print('\n[6] f at R3k_i (k<=2, lockless) vs the exit of the next R3 state (two pi-steps later) and the previous one')
nx = defaultdict(Counter); pv = defaultdict(Counter)
for run, name, hole, cyc in cycles:
    r3 = [x for x in cyc if x[0] == 3]; n = len(r3)
    for i, x in enumerate(r3):
        if x[1] <= 2 and x[2] == 'L':
            nx[(x[1], x[3])][lab(r3[(i + 1) % n])] += 1; pv[(x[1], x[3])][lab(r3[i - 1])] += 1
for key in sorted(nx): print('    k=%d f=%d: next %s | prev %s' % (key[0], key[1], dict(nx[key]), dict(pv[key])))
# 7. per k: label counts
print('\n[7] per k label counts:')
for k in range(5):
    print('    k=%d' % k, sorted(Counter(lab(x) for c in cycles for x in c[3] if x[0] == 3 and x[1] == k).items()))
# 8. per cycle summary with k<=2 credit, k>=3 credit
print('\n[8] cycles with k<=2 credit - 7L/20 <= 3 (L, k<=2 credit, k>=3 credit, R3 labels):')
for run, name, hole, cyc in cycles:
    c = sum(cr(x) for x in cyc if x[1] <= 2); t = sum(cr(x) for x in cyc)
    if c - 7 * len(cyc) / 20 <= 3: print('    %s %s h%d L%d k<=2 %d k>=3 %d | %s' % (run, name, hole, len(cyc), c, t - c, ' '.join(lab(x) for x in cyc if x[0] == 3)))
# 9. the shifted window W = (R3k3, R3k2, R3k1, R3k0, next R3k4): states 2..11 of the period frame
print('\n[9] shifted windows W(r) = r, pi^2 r, pi^4 r, pi^6 r, pi^8 r for r = R3k3 (k = 3,2,1,0,4)')
wp = Counter(); wt = Counter(); wlow = Counter(); wproved = Counter(); wproved2 = Counter()
for run, name, hole, cyc in cycles:
    L = len(cyc)
    for b in range(2, L + 2, 10):
        per = [cyc[(b + i) % L] for i in range(10)]; r3 = [x for x in per if x[0] == 3]
        t = sum(cr(x) for x in r3); wt[t] += 1
        lbl = ' '.join(lab(x) for x in r3); wp[(lbl, t)] += 1
        # proved worths at k=3 (5), F4 at k=4 (8), actual at k<=2
        pw = sum((5 if x[1] == 3 else 8 if x[1] == 4 else cr(x)) if x[2] == 'L' else 0 for x in r3); wproved[pw] += 1
        pw2 = sum((5 if x[1] == 3 else 8 if x[1] == 4 else 2) if x[2] == 'L' else 0 for x in r3); wproved2[pw2] += 1
print('    total credit histogram:', sorted(wt.items()))
print('    with k=3 worth 5, k=4 worth 8 (F4), k<=2 actual:', sorted(wproved.items()))
print('    with k=3 worth 5, k=4 worth 8, k<=2 worth 2:', sorted(wproved2.items()))
print('    window labels (k=3,2,1,0,4) and credit:')
for (lbl, t), v in sorted(wp.items(), key=lambda a: (a[0][1], a[0][0])): print('      %3d  %-22s %d' % (v, lbl, t))
# 10. sub-statements on W
print('\n[10] sub-statements on the windows W (k = 3,2,1,0,4\')')
s = Counter()
for run, name, hole, cyc in cycles:
    L = len(cyc)
    for b in range(2, L + 2, 10):
        r3 = [x for x in (cyc[(b + i) % L] for i in range(10)) if x[0] == 3]
        e = {x[1]: x for x in r3}
        s['k3 and k4\' both fail'] += e[3][2] != 'L' and e[4][2] != 'L'
        s['no lockless k<=2 exit'] += all(e[k][2] != 'L' for k in (0, 1, 2))
        s['three k<=2 fixed points'] += all(e[k][2] == 'X' for k in (0, 1, 2))
        nl = sum(1 for x in r3 if x[2] == 'L'); s['lockless count %d' % nl] += 1
        c34 = sum(cr(e[k]) for k in (3, 4)); c012 = sum(cr(e[k]) for k in (0, 1, 2)); s[('c34', c34, 'c012', c012)] += 1
        if e[4][2] != 'L': s[('k4\' fails: k3 label, k<=2 credit', lab(e[3]), c012)] += 1
        if e[3][2] != 'L': s[('k3 fails: k4\' label, k<=2 credit', lab(e[4]), c012)] += 1
for k, v in sorted(s.items(), key=str): print('    ', k, v)
# 11. Job O: y ~ z in {c(y),c(z)} at R3 states by k (the local ring path predicts 1 at k<=2)
yz = Counter()
for l in open(D + 'jobo-steps.jsonl'):
    r = json.loads(l)
    if r['pattern'] != '5,5,5,5,6': continue
    for cyc in r['jobo']['cycles']:
        for x in cyc:
            if x[1] == 3: yz[(K1[x[2]], x[6])] += 1
print('\n[11] Job O: (k, y~z in {c(y),c(z)}) at R3 states:', sorted(yz.items()))
