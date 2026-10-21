# s50 hand check of one refined column, y_ap key (7,5,5,6,6 | hr=6, hl=7) on the A78 cert, written without the pricer's code:
# (1) every receiverR2 row of the cert: fives w_i, root word, the two hats w_{i+2}, w_{i-2} read straight off the label;
# (2) every senderR2 row with root 7|5566: which exact (H4, H3) pairs its hat classes allow, with the six-admissibility test.
import json, itertools
from fractions import Fraction
B = '/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp'
C = json.load(open(B + '/s42a/run_A78/cert_q42aA78L.json'))
R6 = set()
for l in open('/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad/P/m/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/studio17/wheels17_verdicts.txt'):
    if l.startswith('#') or not l.strip(): continue
    f = l.split(); fam, wd = f[0].split('_')
    if fam != 'c5' and (f[2] == 'D' or (f[2] == 'C' and wd not in {'565667', '565676', '565677', '565757', '565767', '565777'})): R6.add(wd)
def canon(w): return min(min(s[k:] + s[:k] for k in range(len(w))) for s in (tuple(w), tuple(w)[::-1]))
def isR6(w): return ''.join(map(str, canon(w))) in R6 or any(w[i] == w[(i + 1) % 6] == w[(i + 2) % 6] == 5 for i in range(6))
for c in C:
    r = c['row']
    if r[0] != 'receiverR2': continue
    d = r[1]; w = [int(x) for x in r[2]]; s = [int(x) for x in r[3]]; U = min(d, 9)
    for i in range(d):
        if w[i] != 5: continue
        n = (U, w[(i + 1) % d], s[i], s[(i - 1) % d], w[(i - 1) % d]); rn = (U, n[4], n[3], n[2], n[1])
        k = min(n + (w[(i + 2) % d], w[(i - 2) % d]), rn + (w[(i - 2) % d], w[(i + 2) % d]))
        if k[:5] == (7, 5, 5, 6, 6): print('receiver', r[1:], 'w =', Fraction(c['w']).limit_denominator(10**7) * 421, '/421  five at', i, 'key', k)
CL = {0: (5, 6), 1: (7, 8, 9)}
for c in C:
    r = c['row']
    if r[0] != 'senderR2' or r[1] != '55667': continue
    b = r[2]; Hc = b[:5]; Fc = dict(zip([2, 3], b[6:])); w = (5, 5, 6, 6, 7)
    ok = set()
    for h in itertools.product(*[CL[x] for x in Hc]):
        if all(any(not isR6((5, w[(k + 1) % 5], h[k], q, h[(k - 1) % 5], w[(k - 1) % 5])) for q in CL[Fc[k]]) for k in (2, 3)):
            ok.add((h[4], h[3]))   # spoke 4 = 7: n = (7,5,5,6,6), hr = H4 (7-5 hat), hl = H3 (6-7 hat)
    print('sender 55667', b, 'w =', Fraction(c['w']).limit_denominator(10**7) * 421, '/421  exact (hr, hl) allowed:', sorted(ok))
