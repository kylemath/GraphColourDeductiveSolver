# s78 test 0 (orientation / semantics): the engine's K* coefficient of a d = 7 receiver row (recv_coef_R2 key ('ks', 'K1'))
# against W6's own grammar code (grammar.py + gext.py, copied unchanged into tests/w6/): picture built as W6's certpics.recv_pic
# (link + apexes exact; 6-privates amask & ~extra6; 7-privates L3T & ~extra7 per side), column = coef_rows of
# EDGE(7->7)[S.L+1=B S.L-1=S S.L-2=5 S.L-3=5 S.A-1=B] (payer counted if SURE, payee if POSSIBLE).  Also the mirror rule and a
# deliberately mis-oriented rule (S.A+1 instead of S.A-1) as controls: the mirror must agree, the wrong one must not.
# usage: python3 test_orient.py [N] [stack]
import sys, os, random, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'w6'))
import numpy as np
from loadeng import load
import grammar as G, gext as X
NARR = int(sys.argv[1]) if len(sys.argv) > 1 else 20000; STACK = sys.argv[2] if len(sys.argv) > 2 else 's75'
ns = load(STACK, 'full', ['kstar']); ns['l3q_load'](); ns['kt_load']()
def pic(w, s):
    n = 7; priv = []
    for j in range(n):
        pv = [G.ALL] * (w[j] - 5)
        if w[j] == 6:
            am = ns['amask'](7, w[(j - 2) % n], w[(j - 1) % n], w[(j + 1) % n], w[(j + 2) % n], s[(j - 2) % n], s[(j - 1) % n], s[j], s[(j + 1) % n])
            pv = [am & ~ns['f2bm'].extra6(7, w, s, j)]
        if w[j] == 7:
            for sg, slot in ((1, 1), (-1, 0)):
                c = w[(j + sg) % n]; ap, o = (s[j], s[(j - 1) % n]) if sg == 1 else (s[(j - 1) % n], s[j])
                if c <= 6 and ap <= 6:
                    pv[slot] = ns['L3T'][(sg, c, w[(j + 2 * sg) % n], w[(j + 3 * sg) % n], w[(j + 4 * sg) % n], ap, o)] & ~ns['f2bm'].extra7(7, w, s, j, sg)
        priv.append(pv)
    return G.build('R', 'r', 7, list(w), [G.BIT[x] for x in s], priv)
def ctx(d): return {X.EPOS.index(p): G.SYM[m] for p, m in d.items()}
KSTAR = ctx({'S.L+1': 'B', 'S.L-1': 'S', 'S.L-2': '5', 'S.L-3': '5', 'S.A-1': 'B'})
MIRROR = ctx({'S.L-1': 'B', 'S.L+1': 'S', 'S.L+2': '5', 'S.L+3': '5', 'S.A+1': 'B'})
WRONG = ctx({'S.L+1': 'B', 'S.L-1': 'S', 'S.L-2': '5', 'S.L-3': '5', 'S.A+1': 'B'})
rng = random.Random(7801)
arrs = []
while len(arrs) < NARR:
    if len(arrs) % 2: w, s = ns['kstar_force'](rng, 7)
    else: w = [rng.choice((5, 6, 7, 8, 9)) for _ in range(7)]; s = [rng.choice((5, 6, 7, 8, 9)) for _ in range(7)]
    if rng.random() < 0.5 or ns['admissible'](7, ''.join(map(str, w)), ''.join(map(str, s))) is None: arrs.append((w, s))
items = []
for rid, (w, s) in enumerate(arrs):
    for sl in X.slots(pic(w, s)):
        if sl[0] == 'EDGE': items.append((rid, sl))
T = G.SlotTable(items).G['EDGE']
res = {}
for name, cx in (('K*', KSTAR), ('mirror', MIRROR), ('wrong S.A+1', WRONG)):
    res[name] = G.coef_rows(T, G.SYM['7'], G.SYM['7'], cx, len(arrs))
eng = np.array([ns['recv_coef_R2'](7, ''.join(map(str, w)), ''.join(map(str, s)), True).get(('ks', 'K1'), 0) for w, s in arrs], dtype=float)
pay = np.array([sum(ns['kstar_payer_slot'](w, s, i, e) for i in range(7) for e in (1, -1)) for w, s in arrs])
rec = np.array([sum(ns['kstar_payee_slot'](w, s, i, e) for i in range(7) for e in (1, -1)) for w, s in arrs])
print('orientation test (%s stack): %d d=7 arrangements (half with a planted K* pattern); engine K1 coefficient nonzero on %d (payer slots on %d, payee slots on %d; max payer %d, max payee %d)'
      % (STACK, len(arrs), int((eng != 0).sum()), int((pay > 0).sum()), int((rec > 0).sum()), pay.max(), rec.max()))
for name, g in res.items():
    mism = int((np.abs(g - eng) > 1e-9).sum())
    print('  grammar %-12s vs engine: %d mismatches%s' % (name, mism, '' if not mism else '  e.g. %s' % [(''.join(map(str, arrs[i][0])), ''.join(map(str, arrs[i][1])), g[i], eng[i]) for i in np.nonzero(np.abs(g - eng) > 1e-9)[0][:3]]))
ok = (np.abs(res['K*'] - eng) < 1e-9).all() and (np.abs(res['mirror'] - eng) < 1e-9).all() and (np.abs(res['wrong S.A+1'] - eng) > 1e-9).any()
print('ORIENT-TEST: %s' % ('PASS (K* and its mirror agree with grammar.py on every row; the mis-oriented control disagrees)' if ok else 'FAIL'))
