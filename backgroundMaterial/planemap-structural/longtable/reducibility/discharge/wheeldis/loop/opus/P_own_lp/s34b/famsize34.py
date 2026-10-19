# family size of z6 / Z6 (first family) over all canonical non-R6 6-words x apex classes; s34b.
import os, sys, itertools
B = '/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp'
sys.path.insert(0, os.path.join(B, 's28q')); import eng_exec
M = '/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad/P/m/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis'
G = {}; eng_exec.engine(['root=' + M, 'apexcls', 'work=/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad/P/wr34b'], G)
globals().update({k: v for k, v in G.items() if not k.startswith('__')})
def refl7(a): return (a[4], a[3], a[2], a[1], a[0], a[6], a[5])
def zkey6(L, s, j):
    a = (L[(j + 1) % 6], ap(L[(j + 2) % 6]), L[(j + 3) % 6], ap(L[(j + 4) % 6]), L[(j + 5) % 6], s[j], s[(j - 1) % 6]); return min(a, refl7(a))
def refl6(g): return (g[3], g[2], g[1], g[0], g[5], g[4])
def sig_payee(L, s, k):
    g = (L[(k + 1) % 6], s[k], s[(k - 1) % 6], L[(k - 1) % 6], ap(L[(k + 2) % 6]), ap(L[(k - 2) % 6])); return min(g, refl6(g))
A6 = all6_words(); K = set(); S = set(); Sall = set(); np6 = 0
for L in A6:
    for s0, s1 in itertools.product((5, 7), repeat=2):
        for j in range(6):
            if L[j] != 6: continue
            s = [5] * 6; s[j], s[(j - 1) % 6] = s0, s1
            Sall.add(sig_payee(L, s, j))
            if 5 in L: K.add(zkey6(L, s, j))
print('non-R6 canonical 6-words', len(A6), '| with a 6:', sum(1 for L in A6 if 6 in L), '| first-family z6 keys', len(K),
      '| Z6 signatures sigma(K)', len({(k[0], k[1], k[3], k[4], k[5], k[6]) if (k[0], k[1], k[3], k[4], k[5], k[6]) <= refl6((k[0], k[1], k[3], k[4], k[5], k[6])) else refl6((k[0], k[1], k[3], k[4], k[5], k[6])) for k in K}),
      '| payee signatures over all 6-words', len(Sall))
