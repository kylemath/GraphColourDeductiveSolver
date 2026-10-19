"""Stage 15 (RELAY_SPEC section 13, d3bc1f93) structure self-test, from the spec alone: counts of v keys, V signatures
and mrowV rows, h2 and g2 keys, distinct conservation rows over all (L, s), and the conservation rank, to compare
with section 13.5 (s16_struct.txt: v 9,165; V 2,850 / 13,869 mrowV; h2 12,347; g2 393; 151,056 rows; rank 13,670).
Uses s12r_check.py's spec-side code (sets, keys) up to its solution section; no solution is read.
Usage: python3 out/job31/st15_struct.py"""
import sys, os, itertools, collections
import numpy as np
D_ = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(D_, 's12r_check.py')).read()
src = src[:src.index('# ================= solution values')].replace('os.path.abspath(__file__)', repr(os.path.join(D_, 's12r_check.py')))
sys.argv = ['x', '/dev/null', '/dev/null', '/dev/null']
src = src.replace("SOL = json.load(open(SOLF)); CERT = json.load(open(CERTF)); ARGS = open(ARGF).read().split()", "SOL = CERT = None; ARGS = []")
exec(src)
def cv(l): return l if l < 7 else 7
def v_of(m, ar, al):
    m = tuple(m); return min(m + (cv(ar), cv(al)), (m[0], m[5], m[4], m[3], m[2], m[1]) + (cv(al), cv(ar)))
def sigV_of(U, wr, sr, sl, wl, ar, al): return min((U, wr, sr, sl, wl, ar, al), (U, wl, sl, sr, wr, al, ar))
def candV(sig):
    U, wr, sr, sl, wl, ar, al = sig
    return {v_of((U, wr, sr, p, sl, wl), ar, al) for p in LET if not isR6((U, wr, sr, p, sl, wl))}
CV = (5, 6, 7)
def cons2v_row(L, s):
    r = collections.Counter()
    for i in range(6):
        m = tuple(L[(i + k) % 6] for k in range(6))
        if L[i] == 5:
            r[('g', g2_raw(L[(i + 1) % 6], c(L[(i + 2) % 6]), c(L[(i + 3) % 6]), c(L[(i + 4) % 6]), L[(i + 5) % 6], ap(s[i]), ap(s[(i - 1) % 6])))] += 1
        if L[i] == 7: r[('v', v_of(m, s[i], s[(i - 1) % 6]))] += 1
        if L[i] >= 7: r[('h', h2_of(m, s[i], s[(i - 1) % 6]))] -= 1
    return tuple(sorted((k, v) for k, v in r.items() if v != 0))
ALL6 = sorted({canon(L) for L in itertools.product(LET, repeat=6) if not isR6(L)})
FIVE = [L for L in ALL6 if 5 in L]
out = {}
for name, LS in (('994 (with a five)', FIVE), ('1,424 (all non-R6)', ALL6)):
    rows = set(); keys = collections.defaultdict(set); blocks = {}
    for L in LS:
        bl = set()
        for s in itertools.product(CV, repeat=6):          # cv classes; ap is a function of cv (5, 6 small; 7 big)
            r = cons2v_row(L, s)
            if r: rows.add(r); bl.add(r)
            for k, _ in r: keys[k[0]].add(k[1])
        blocks[L] = bl
    out[name] = (rows, keys, blocks)
    print('L set %s: distinct conservation rows %d; keys g2 %d, h2 %d, v %d' % (name, len(rows), len(keys['g']), len(keys['h']), len(keys['v'])), flush=True)
SV = {}
for wr, sr, sl, wl in itertools.product(LET, repeat=4):
    for ar, al in itertools.product(CV, repeat=2):
        sg = sigV_of(7, wr, sr, sl, wl, ar, al); cd = candV(sg)
        if cd: SV[sg] = cd
print('V signatures (U = 7) %d, mrowV rows %d, v keys reachable from candV %d' % (len(SV), sum(len(v) for v in SV.values()), len(set().union(*SV.values()))), flush=True)
S2 = {}
for U in (7, 8, 9):
    for wr, sr, sl, wl in itertools.product(LET, repeat=4):
        for ar, al in itertools.product(AP, repeat=2):
            sg = sig2_of(U, wr, sr, sl, wl, ar, al); cd = cand2(sg)
            if cd: S2[sg] = cd
print('sig2 signatures %d, h2 keys reachable from cand2 %d' % (len(S2), len(set().union(*S2.values()))), flush=True)
# rank: h2 and v keys are local to a 6-type (they contain its link), g2 keys are shared
rows, keys, blocks = out['994 (with a five)']
for nm in ('994 (with a five)', '1,424 (all non-R6)'):
    rows, keys, blocks = out[nm]
    gi = {k: i for i, k in enumerate(sorted(keys['g']))}; Q = np.zeros((0, len(gi))); rloc = 0; nblk = 0
    for L, bl in blocks.items():
        if not bl: continue
        bl = sorted(bl); loc = sorted({k for r in bl for k, _ in r if k[0] != 'g'})
        li = {k: i for i, k in enumerate(loc)}
        B = np.zeros((len(bl), len(loc))); Gm = np.zeros((len(bl), len(gi)))
        for a, r in enumerate(bl):
            for k, v in r:
                if k[0] == 'g': Gm[a, gi[k[1]]] += v
                else: B[a, li[k]] += v
        if loc:
            U_, sv_, _ = np.linalg.svd(B); rb = int((sv_ > 1e-9).sum()); N = U_[:, rb:].T   # left null space of B
        else: rb = 0; N = np.eye(len(bl))
        rloc += rb; P = N @ Gm
        if P.size:
            M_ = np.vstack([Q, P]); u_, s_, vt = np.linalg.svd(M_, full_matrices=False); rk = int((s_ > 1e-9).sum()); Q = vt[:rk]
        nblk += 1
    print('conservation rank over L set %s: local %d + shared g2 part %d = %d (numerical, tol 1e-9)' % (nm, rloc, Q.shape[0], rloc + Q.shape[0]), flush=True)
