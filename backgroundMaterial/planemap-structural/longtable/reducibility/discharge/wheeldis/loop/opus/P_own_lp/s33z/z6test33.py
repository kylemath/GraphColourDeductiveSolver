# s33z engine test for l6r (RELAY_SPEC_s23): family size (886 / 210), cons2_delta vs cons2_coef with random values (z6/Z6 + g/h),
# and the s34b physical edge test re-run on the engine's own key functions (zkey6_ab / zsig6_ab).  usage: python3 z6test33.py
import os, sys, random, itertools, numpy as np
E = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'eng')
M = '/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad/P/m/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis'
sys.argv = [os.path.join(E, 'pcheck.py'), 'none', 'root=' + M, 'xon', 'apexcls', 'hat5', 'consall', 'l6r', 'work=/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad/P/wr33t']
src = open(os.path.join(E, 'pcheck.py')).read().rstrip().rsplit('\n', 1)[0]; G = {'__file__': os.path.join(E, 'pcheck.py')}
exec(compile(src, 'pcheck.py', 'exec'), G); globals().update({k: v for k, v in G.items() if not k.startswith('__')})
F = z6_first(); print('first-family z6 keys %d, Z6 signatures %d' % (len(F), len({zsig6_of_key(K) for K in F})))
rng = random.Random(6)
Z6V.update({K: rng.random() for K in F}); Z6W.update({zsig6_of_key(K): rng.random() for K in F})
GV = {}; HV2 = {}; bad = 0; n = 0
A6 = all6_words()
for L in rng.sample(A6, 300):
    for k, c in cons2_coef(L, (5,) * 6).items(): pass
    D = cons2_delta(L, GV, HV2)
    for _ in range(40):
        idx = rng.randrange(len(SALL)); s_ = tuple(LET[v] for v in SALL[idx])
        val = sum(c * (Z6V.get(k[1], 0.0) if k[0] == 'z6' else Z6W.get(k[1], 0.0) if k[0] == 'Z6' else 0.0) for k, c in cons2_coef(L, s_).items())
        n += 1
        if abs(val - D[idx]) > 1e-9: bad += 1
print('cons2_delta vs cons2_coef (z6/Z6 terms, random values): %d (L, s) checks, %d mismatches' % (n, bad))
zkey6 = lambda L, s, j: zkey6_ab(L, j, s[j], s[(j - 1) % 6]); sig_payee = lambda L, s, k: zsig6_ab(L, k, s[k], s[(k - 1) % 6]); sig_of_key = zsig6_of_key
def phys(N, broken=False, seed=11):
    rng = random.Random(seed); bad = 0; badP = 0
    for _ in range(N):
        v = [rng.choice(LET) for _ in range(6)]; a_ = [rng.choice(LET) for _ in range(6)]; j = rng.randrange(6); v[j] = 6; Qv = rng.choice(LET)
        # vertices: x, V0..V5 (x's link), A0..A5 (A_i adjacent V_i, V_{i+1}), Q (y = V_j's vertex opposite x)
        tri = [('x', 'V%d' % i, 'V%d' % ((i + 1) % 6)) for i in range(6)] + [('V%d' % i, 'V%d' % ((i + 1) % 6), 'A%d' % i) for i in range(6)]
        y = 'V%d' % j; tri += [(y, 'A%d' % j, 'Q'), (y, 'Q', 'A%d' % ((j - 1) % 6))]
        let = {'x': 6, 'Q': Qv}; let.update({'V%d' % i: v[i] for i in range(6)}); let.update({'A%d' % i: a_[i] for i in range(6)})
        def cyc(c):   # cyclic link of c from the triangle list
            T = [t for t in tri if c in t]; nb = {}
            for t in T:
                o = [u for u in t if u != c]; nb.setdefault(o[0], []).append(o[1]); nb.setdefault(o[1], []).append(o[0])
            st = sorted(nb)[0]; seq = [st]; prev = None
            while True:
                nx = [u for u in nb[seq[-1]] if u != prev and u not in seq[-1:]]
                nx = [u for u in nx if u != (seq[-2] if len(seq) > 1 else None)]
                if not nx or nx[0] == st: break
                prev = seq[-1]; seq.append(nx[0])
            return seq
        def third(p, q, notv):
            for t in tri:
                if p in t and q in t and notv not in t: return [u for u in t if u not in (p, q)][0]
            return None
        def view(c, rot, rf):
            lk = cyc(c); assert len(lk) == 6
            if rf: lk = lk[::-1]
            lk = lk[rot:] + lk[:rot]
            ap_ = [third(lk[i], lk[(i + 1) % 6], c) for i in range(6)]
            return lk, ap_
        lx, axs = view('x', rng.randrange(6), rng.random() < .5)
        jj = lx.index(y); Lx = [let[u] for u in lx]; Sx = [ap(let[u]) for u in axs]
        K = zkey6(Lx, Sx, jj); Ptrue = let[lx[(jj + 3) % 6]]
        ly, ays = view(y, rng.randrange(6), rng.random() < .5)
        kk = ly.index('x'); Ly = [let[u] for u in ly]
        Sy = [ap(let[u]) if u is not None else 5 for u in ays]
        if broken: Sy[kk], Sy[(kk - 1) % 6] = Sy[(kk - 1) % 6], Sy[kk]
        if sig_payee(Ly, Sy, kk) != sig_of_key(K): bad += 1
        # P is x's vertex opposite y: not in y's closed 1-ball (y never sees it)
        if lx[(jj + 3) % 6] in ly or K[2] != Ptrue: badP += 1
    return bad, badP
# ---- non-vacuity of the negative keys: payer and payee 6-words (non-R6, incl. 2.122) that realise K / sigma(K)
A6 = all6_words()
def realise(K):
    g = sig_of_key(K); pay = set(); rec = set()
b0 = phys(100000); b1 = phys(100000, broken=True)
print('physical (s34b test on the engine key functions): sigma mismatches %d, P mismatches %d; broken control %d' % (b0[0], b0[1], b1[0]))
