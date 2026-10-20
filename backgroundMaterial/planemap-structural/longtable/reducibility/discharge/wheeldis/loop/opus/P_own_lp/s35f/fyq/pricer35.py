# Stage 35f-fyq pricer (Opus). Pricing only: do fy columns (RELAY_SPEC_s20 level-1 face-aware z, s25c "fy") price
# negative against the l3q-only cert s33z/run_A67/cert_q66L.json (LOWER VALID 55686/438047 = 0.127123 on A67)?
# Rows are rebuilt with the s33z engine (q66 flags FQ, args_A67, reg_A67 kill and l3q tables), exactly as lowerR2.
# fy column z[K] (uncapped, as in the s35f fy solve): sender coef +1 per big spoke j, K = fy_sender_key(w, H, j);
# receiver coef +1 per link five, K = fy_recv_key(...)  (definitions copied verbatim from s25c/prelay2.py).
# rc(K) = -(sum_rows dual * coef) / tco.  Two prices:
#   label-only: each cert sender row at its own label (the deduped representative R2_sender_rows keeps);
#   lifting LP: each cert sender row replaced by the best convex mix of ALL sender contexts with the same old coef row
#   (contexts enumerated without R2_sender_rows' dedup); receivers have no hidden hats at level 1.
import os, sys, json, collections, itertools, re
from fractions import Fraction
import numpy as np
from scipy.optimize import linprog
B = '/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp'
E = B + '/s33z/eng'; Q = B + '/s33z/reg_A67'
M = '/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad/P/m/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis'
ARGS = ['root=' + M, 'args=' + Q + '/args_A67.txt', 'rpat=' + B + '/rpatD.txt', 'xon', 'apexcls', 'filt16',
        'killtab=' + Q + '/f/kill/kill6', 'hat5', 'consall', 'l3q', 'l3qtab=' + Q + '/tab_1.json,' + Q + '/tab_-1.json',
        'lqcap=3', 'xcap=3', 'work=/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad/P/wr35_fyq']
CERT = B + '/s33z/run_A67/cert_q66L.json'
MYDIR = B + '/s35f/fyq'   # (pcheck defines HERE)
sys.argv = [E + '/pcheck.py', 'none'] + ARGS
src = open(E + '/pcheck.py').read(); last = src.rstrip().rsplit('\n', 1); assert "'lowerR2': cmd_lowerR2" in last[1]
G = {'__file__': E + '/pcheck.py', '__name__': 'pcheck_exec'}; exec(compile(last[0], E + '/pcheck.py', 'exec'), G)
globals().update({k: v for k, v in G.items() if not k.startswith('__')})
OUT = open(os.path.join(MYDIR, 'pricer35.log'), 'w')
def P(*a):
    s = ' '.join(str(x) for x in a); print(s, flush=True); OUT.write(s + '\n'); OUT.flush()
# ---- non-deduped sender enumerator: R2_sender_rows' own source with the dedup line made unconditional
p2 = open(E + '/prelay2.py').read()
m_ = re.search(r'\ndef R2_sender_rows\(\):\n(.*?)\n(?=\S)', p2, re.S); fsrc = m_.group(0)
DED = "if k_ not in seen: seen.add(k_); out.append((''.join(map(str, w)), dict(cf), list(hb) + ['|'] + list(fb)))"
assert fsrc.count(DED) == 1
fsrc = fsrc.replace('def R2_sender_rows():', 'def R2_sender_rows_all():').replace(DED, "out.append((''.join(map(str, w)), dict(cf), list(hb) + ['|'] + list(fb), dict(H)))")
exec(fsrc, G); R2_sender_rows_all = G['R2_sender_rows_all']
# ---- fy key (verbatim from s25c/prelay2.py)
FYMASK = 2
def fy_vis(n): return (True, n[1] == 5, False, n[4] == 5, True)
def fykey(n, h):
    v = fy_vis(n); hm = tuple(h[k] if v[k] else FYMASK for k in range(5))
    a = tuple(n) + hm; b = (n[0], n[4], n[3], n[2], n[1]) + tuple(reversed(hm)); return min(a, b)
def fy_sender_key(w, H, j): return fykey(tuple(w[(j + i) % 5] for i in range(5)), tuple(H[(j + i) % 5] for i in range(5)))
def fy_recv_key(U, a, b, e, f, p, q, r, s_):
    n = (U, e, r, q, b)
    return fykey(n, (c2(f), c2(s_) if e == 5 else FYMASK, FYMASK, c2(p) if b == 5 else FYMASK, c2(a)))
def fy_sender(wd, H):
    w = [int(ch) for ch in wd]; cf = collections.Counter()
    for j in range(5):
        if w[j] >= 7: cf[('fy', fy_sender_key(w, H, j))] += 1
    return cf
def fy_recv(d, w, s):
    U = min(d, 9); cf = collections.Counter()
    for j in range(d):
        if w[j] == 5:
            cf[('fy', fy_recv_key(U, w[(j - 2) % d], w[(j - 1) % d], w[(j + 1) % d], w[(j + 2) % d], s[(j - 2) % d], s[(j - 1) % d], s[j], s[(j + 1) % d]))] += 1
    return cf
# ---- rebuild the cert exactly as lowerR2 (control)
load_patterns(); xon = True
C = json.load(open(CERT))
SRA = R2_sender_rows_all(); SRD = R2_sender_rows()
assert len(SRD[0]) == 3
byword = collections.defaultdict(list)
for wd, cf, b, H in SRA: byword[wd].append((tuple(map(str, b)), cf, H))
SR = {(wd, tuple(map(str, b))): cf for wd, cf, b in SRD}
P('sender contexts: %d deduped (R2_sender_rows), %d without dedup' % (len(SRD), len(SRA)))
tot = collections.defaultdict(Fraction); tco = Fraction(0); D = Fraction(0); rows = []
for c in C:
    w = Fraction(c['w']).limit_denominator(10 ** 7); row = c['row']
    if row[0] == 'senderR2':
        lab = tuple(map(str, row[2])); cf = SR[(row[1], lab)]
        for k, v in cf.items(): tot[k] += w * v
        tco += w; D += w
        mine = [x for x in byword[row[1]] if x[0] == lab]; assert len(mine) == 1 and mine[0][1] == cf
        same = [x for x in byword[row[1]] if x[1] == cf]
        rows.append(('S', '%s %s' % (row[1], ''.join(row_ for row_ in map(str, row[2]))), w, [(''.join(x[0]), fy_sender(row[1], x[2])) for x in same], 0))
        rows[-1] = rows[-1][:4] + ([i for i, x in enumerate(same) if x[0] == lab][0],)
    elif row[0] == 'cons2':
        for k, v in cons2_coef(tuple(row[1]), tuple(row[2])).items(): tot[k] += w * v
    elif row[0] == 'mrowR2':
        tot[('h', tuple(row[2]))] += w; tot[('M', tuple(row[1]))] -= w
    elif row[0] == 'mrowL':
        tot[('lq', tuple(row[2]))] += w; tot[('lQ', tuple(row[1]))] -= w
    elif row[0] == 'receiverR2':
        d, lk, sv = int(row[1]), row[2], row[3]; assert admissible(d, lk, sv) is None
        for k, v in recv_coef_R2(d, lk, sv, xon).items(): tot[k] += w * v
        tco -= w; D += w * (d - 6)
        rows.append(('R', '%d %s %s' % (d, lk, sv), w, [('-', fy_recv(d, [int(ch) for ch in lk], [int(ch) for ch in sv]))], 0))
    else: raise SystemExit('row type ' + row[0])
Db = D / tco; neg = []
for k, v in tot.items():
    rc = -v / tco
    if rc < 0:
        if k[0] == 'x': Db += rc * 3
        elif k[0] == 'lq': Db += rc * 3
        else: neg.append((k, rc))
P('CONTROL (fy absent): cert %s rows %d tco %s bound %s = %.9f, uncapped rc<0: %d' % (os.path.basename(CERT), len(C), tco, Db, float(Db), len(neg)))
assert Db == Fraction(55686, 438047) and not neg
nS = sum(1 for r in rows if r[0] == 'S'); P('cert senders %d (lift contexts: %d total, max %d per row), receivers %d' % (
    nS, sum(len(r[3]) for r in rows if r[0] == 'S'), max(len(r[3]) for r in rows if r[0] == 'S'), len(rows) - nS))
# ---- label-only pricing (exact)
ft = collections.defaultdict(Fraction)
for kind, lab, w, opts, i0 in rows:
    for k, v in opts[i0][1].items(): ft[k] += w * v
keys = sorted({k for r in rows for _, cf in r[3] for k in cf})
negL = sorted((k for k in ft if ft[k] > 0), key=lambda k: -ft[k])
P('\nfy keys touched by cert rows: %d.  label-only pricing: %d fy columns with rc < 0' % (len(keys), len(negL)))
for k in negL[:25]: P('  rc = %s = %.6f  %s' % (-ft[k] / tco, float(-ft[k] / tco), k[1]))
minL = min([-ft[k] / tco for k in keys] + [Fraction(0)])
# ---- lifting LP: minimise e = max_K tot_K over convex mixes of same-coef contexts
kix = {k: i for i, k in enumerate(keys)}; var = [(r_, c_) for r_, r in enumerate(rows) for c_ in range(len(r[3]))]
A = np.zeros((len(keys), len(var))); Aeq = np.zeros((len(rows), len(var))); beq = np.array([float(abs(r[2])) for r in rows])
for v_, (r_, c_) in enumerate(var):
    Aeq[r_, v_] = 1
    for k, val in rows[r_][3][c_][1].items(): A[kix[k], v_] += val * (1 if rows[r_][0] == 'S' else -1)
nv = len(var); cobj = np.zeros(nv + 1); cobj[-1] = 1
res = linprog(cobj, A_ub=np.hstack([A, -np.ones((len(keys), 1))]), b_ub=np.zeros(len(keys)),
              A_eq=np.hstack([Aeq, np.zeros((len(rows), 1))]), b_eq=beq, bounds=[(0, None)] * nv + [(None, None)], method='highs')
assert res.status == 0
e = res.x[-1]; lam = res.x[:-1]; tv = A @ lam
P('\nlifting LP: min over liftings of max_K tot_K = %.9f, i.e. most negative fy rc = %.9f (%s)' % (
    e, -e / float(tco), 'old cert valid with fy: null' if e <= 1e-12 else 'some fy column has rc < 0 under every lifting'))
P('columns with rc < 0 at the best lifting: %d' % int((tv > 1e-12).sum()))
for i in np.argsort(-tv)[:15]:
    if tv[i] <= 1e-12: break
    who = [(rows[r_][1], rows[r_][3][c_][0], round(lam[v_], 6), int(A[i, v_])) for v_, (r_, c_) in enumerate(var) if A[i, v_] and lam[v_] > 1e-12]
    P('  NEG fy', keys[i][1], 'rc = %.6f' % (-tv[i] / float(tco)), who[:8])
P('\nSUMMARY: label-only most negative fy rc = %.6f; with lifting = %.6f; gate (re-solve if <= -0.002): %s' % (
    float(minL), -e / float(tco), 'RE-SOLVE' if -e / float(tco) <= -0.002 else 'NO RE-SOLVE'))
OUT.close()
