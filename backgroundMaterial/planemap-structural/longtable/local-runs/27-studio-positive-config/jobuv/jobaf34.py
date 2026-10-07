#!/usr/bin/env python3
"""Job AF parts 3 and 4. (3) p27m #167230 h23: excursions of Z29 and T21 and every sigma / sigma' link between them (from DD endpoints, both directions).
(4) (5,5,5,5,7) Lemma S failure Gamma-cycles: period tuples (k = 4..0: exit kind, f) and Lemma W windows (R3k3, R3k2, R3k1, R3k0, R3k4': credit >= 10?)."""
import json
from uv_lib import Hole
from jobaf import imgkind
H = Hole('p27#167230', 23, True)
def excs(c):
    z = H.cycles[c]; L = len(z)
    if all(not H.filled(x) for x in z): return [('all unfilled', L)]
    s0 = next(i for i in range(L) if H.filled(z[i - 1]) and not H.filled(z[i])); zz = z[s0:] + z[:s0]; i = 0; out = []
    while i < L:
        st = i; u = 0
        while i < L and not H.filled(zz[i]): u += 1; i += 1
        f = 0
        while i < L and H.filled(zz[i]): f += 1; i += 1
        out.append((u, f, sum(H.lam[x] for x in zz[st:i]), zz[st:i]))
    return out
print('p27m #167230 hole 23 (mirror): link degrees', [len(H.rot[x]) for x in H.L], 'states', H.S, 'cycles', len(H.cycles))
for c in (29, 21):
    ex = excs(c); print('\ncycle %d: w %d, L %d, Lambda %d; excursions (u, f, lambda-mass):' % (c, H.W[c], len(H.cycles[c]), 5 * H.W[c]), [(u, f, m) for u, f, m, _ in ex])
lmask = 0
for i in H.sp.linki: lmask |= 1 << i
print('\nlinks between cycles 29 and 21 (from DD endpoints):')
for a, b in ((29, 21), (21, 29)):
    exa = excs(a); exb = excs(b)
    def which(c, x, ex): return next(i for i, e in enumerate(ex) if x in e[3])
    for k in H.cycles[a]:
        if not H.isDDend(k): continue
        j, ty, hi, roles = H.frame(k); s = H.sigma(k)
        if H.cyc[s] == b: print('  sigma  %d -> %d: from state %d (R%d, excursion %d of %d) to state %d (%s, excursion %d of %d, f %d)' % (a, b, k, ty, which(a, k, exa), a, s, imgkind(H, s), which(b, s, exb), b, H.f_after(s) if imgkind(H, s) == 'lockless' else -1))
        for t, p, q, K in H.sp.moves(k):
            if t == k or K & lmask or H.DL[t] or H.cyc[t] != b: continue
            print('  sigma\' %d -> %d: from state %d (R%d, excursion %d) swap pair (%d,%d) |K| %d to state %d (%s, excursion %d, f %d)' % (a, b, k, ty, which(a, k, exa), p, q, bin(K).count('1'), t, imgkind(H, t), which(b, t, exb), H.f_after(t) if imgkind(H, t) == 'lockless' else -1))
# (4)
print('\n(4) (5,5,5,5,7) Lemma S failure Gamma-cycles: period tuples (k = 4,3,2,1,0) and Lemma W windows')
d = json.load(open('jobac.json'))
fails = {(x['run'], x['name'], x['hole'], x['L']) for x in d['part1'] if x['pattern'] == '5,5,5,5,7'}
for x in d['part2']:
    if (x['run'], x['name'], x['hole'], x['L']) not in fails: continue
    seq = x['seq']; n = len(seq); s0 = next(i for i, e in enumerate(seq) if e[0] == 'R3' and e[1] == 4); seq = seq[s0:] + seq[:s0]
    tup = []; cred = lambda e: 3 * e[3] - 1 if e[2] == 'lockless' else 0
    for b in range(0, n, 10):
        per = seq[b:b + 10]; r3 = {e[1]: e for e in per if e[0] == 'R3'}
        tup.append(' '.join(('L%d' % r3[k][3]) if r3[k][2] == 'lockless' else r3[k][2] for k in (4, 3, 2, 1, 0)) + ' | credit %d' % sum(cred(r3[k]) for k in r3))
    win = []
    for b in range(0, n, 10):   # window R3k3 (pos b+2), k2 (b+4), k1 (b+6), k0 (b+8), next R3k4 (b+10)
        es = [seq[(b + t) % n] for t in (2, 4, 6, 8, 10)]; win.append(sum(cred(e) for e in es))
    print('  %s %s h%d L %d: periods %s; Lemma W window credits %s (>= 10: %s)' % (x['run'], x['name'], x['hole'], n, tup, win, all(w >= 10 for w in win)))
