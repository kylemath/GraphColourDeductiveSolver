#!/usr/bin/env python3
"""[exploratory] NightCutParity (SolvingFrameworkPlan/docs/working/NightCutParity.md). Run from jobuv/ (python3 nightcutparity.py; ~10 s, 1 core).
Part 1 (tables): from QuarterWindow xTab/wTab/mTab (row 10 = sig(row 0)): every step's swapped pair contains alpha (= letter 0); steps whose pair is the
complement of {c(w3), c(y)} are exactly 0 and 7, and x4 is swapped at both.
Part 2 (constructed degree-6 cycles, jobas/best-A7f*.json, both orientations): omega = the colour in every swapped pair; A_b = omega-class at the start of period b;
S_b = vertices in an odd number of the 10 swapped components; checks S_b = A_b xor A_{b+1}, S_b misses the ring, A_b never repeats at odd distance;
u* = apex of the outer face on the ring edge w3-y: u* in every S_b, u* swapped 3 times per period, exactly one of steps 0, 7 swaps u*."""
import sys, os, json
from collections import Counter
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, '../jobas')); os.chdir(HERE)
from uv_lib import Hole
from jobam import stepK, setup
from flipsearch import rotation
sig = [0, 3, 1, 2]
X = [[3,0,1,0,2],[3,0,1,2,0],[3,1,0,2,0],[0,1,0,2,3],[0,1,2,0,3],[1,0,2,0,3],[1,0,2,3,0],[1,2,0,3,0],[0,2,0,3,1],[0,2,3,0,1]]
W = [[2,3,2,3,1],[2,3,0,3,1],[2,3,1,3,1],[2,3,1,0,1],[2,3,1,2,1],[2,3,1,2,0],[2,3,1,2,3],[0,3,1,2,3],[1,3,1,2,3],[1,0,1,2,3]]
Mt = [0,0,0,3,3,3,0,2,2,2]
rows = [X[i] + W[i] + [Mt[i]] for i in range(10)]; rows.append([sig[c] for c in rows[0]])
nm = ['p=x0','x1','x2','x3','x4','z=w0','w1','w2','w3','y=w4','m']; W3, Y, X4 = 8, 9, 4
print('== Part 1: tables (letters of the anchoring R3k4 state, 0 = alpha)')
free = []
for i in range(10):
    a, b = rows[i], rows[i + 1]; ch = [k for k in range(11) if a[k] != b[k]]; pair = set()
    for k in ch: pair |= {a[k], b[k]}
    assert all({a[k], b[k]} == pair for k in ch) and 0 in pair
    if pair == set(range(4)) - {a[W3], a[Y]}: free.append(i); assert X4 in ch
    print('  step %d: pair %s, changed %s%s' % (i, sorted(pair), [nm[k] for k in ch], '  FREE (pair = complement of c(w3),c(y)); x4 swapped' if pair == set(range(4)) - {a[W3], a[Y]} else ''))
print('  every pair contains alpha: True; free steps:', free, '; row 0: c(w3), c(y), c(x4) =', rows[0][W3], rows[0][Y], rows[0][X4])
print('== Part 2: constructed cycles')
tot = Counter()
for g, hh in (('A7f1', 22), ('A7f2', 22), ('A7f3', 34), ('A7f4', 22)):
    for mir in (False, True):
        F = [tuple(t) for t in json.load(open('../jobas/best-%s.json' % g))['faces']]; H = Hole(g, hh, mir, rot=rotation(F)); rot = H.rot; h = H.h
        V = [v for v in range(len(rot)) if v != h]
        t6, p, y, z, w2, M, hv = setup(H); w3 = H.w[(t6 + 3) % 5]; x4 = H.L[(t6 + 4) % 5]
        ry = rot[y]; i = ry.index(w3); u = [c for c in (ry[(i + 1) % len(ry)], ry[(i - 1) % len(ry)]) if c != x4][0]
        assert u not in hv and w3 in rot[u]
        hi = [t for t in range(5) if len(rot[H.L[t]]) >= 6]
        for zc in H.cycles:
            if not all(H.DL[x] for x in zc): continue
            n = len(zc); fr = [H.frame(x) for x in zc]; s0 = next((i for i in range(n) if fr[i][1] == 3 and (hi[0] - fr[i][0]) % 5 == 4), 0); zc = zc[s0:] + zc[:s0]
            c = {v: H.col(zc[0], v) for v in V}; cols = [dict(c)]; Ks = []; prs = []
            for x in zc:
                K = stepK(H, x); ab = sorted({c[v] for v in K}); assert len(ab) == 2
                for v in K: c[v] = ab[0] if c[v] == ab[1] else ab[1]
                Ks.append(K); prs.append(set(ab)); cols.append(dict(c))
            om = set.intersection(*prs); assert len(om) == 1; om = om.pop(); m = n // 10
            A = [frozenset(v for v in V if cols[10 * b][v] == om) for b in range(m + 1)]; assert A[m] == A[0]
            tot['cycles'] += 1; tot['periods'] += m
            for b in range(m):
                cnt = Counter(v for K in Ks[10 * b:10 * b + 10] for v in K); S = {v for v in V if cnt[v] % 2}
                tot['S=AxorA'] += S == (A[b] ^ A[b + 1]); tot['ring misses S'] += not (S & hv); tot['u* in S'] += u in S
                tot['u* swapped 3x'] += cnt[u] == 3; tot['exactly one of K0,K7 has u*'] += (u in Ks[10 * b]) != (u in Ks[10 * b + 7])
            tot['no odd-distance repeat of A'] += not any(A[b] == A[(b + k) % m] for b in range(m) for k in range(1, m, 2))
            tot['L %d' % n] += 1
print(' ', dict(tot))
