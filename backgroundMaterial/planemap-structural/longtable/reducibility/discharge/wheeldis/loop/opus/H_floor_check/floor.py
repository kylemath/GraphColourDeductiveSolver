"""H_floor_check: rule-T floor at R*(6,6) from w2's (and mirror w4's) rows, with self-pairing and a one-step chain.
usage: python3 -I floor.py WHEELDIS_DIR [KILLFILE] [no37] [nopair] [nochain]
  WHEELDIS_DIR: copy of the branch's wheeldis tree with bin/sep3 built (sep3 `c` = k36's acceptance check).
  KILLFILE: one kill per line, first token a window name f7_<link>_<s> (dfast/kc/cfast line or bare name), letters 5-8
            exact, B = any big (7, 8, 9+), '.' = free; or two 7-letter tokens LINK SWORD in frame coordinates.
            A frame (w2 frame, w4 mirror or s2 chain frame, all degree 7) is killed if some dihedral image of the
            window agrees with it at every fixed letter (s_i between w_i, w_i+1; gen.py canon_key convention).
            Lines starting '#' and windows of degree != 7 are ignored.  Round 37's f7_5566757_...5... is always added
            unless no37.
Model (rule T, no L2): fives send Y to big neighbours and T across a 6 x next to their big B to z = third(B, x) when z
is big; Y, T keyed by rooted word + z letters (option F).  Bar of a 7 = 1 + t.  Sender shares (units of 1 - t) a link
five v of a centre C (letter 7) is guaranteed to pay C, for every feasible (Y, T, t):
  lone (only big C), no T route                                   -> 1
  lone, each T route (via 6 y = lk[i+d] to z = lk[i+2d] >= 7) self-paired: the slot five x between y and z (sv)
     is 5, z = 7 and y's 6-wheel (7, 5, a, a, 5, 7) (a = slot between v and y) is non-R: x, rooted at z, can carry v's
     word and z letters, so T_x (inflow at C) = T_v (outflow) and they cancel             -> 1
  lone with one unpaired route to z = s2 (index 5)                 -> chain: 1 - T_v, T_v <= 1 + t - c2 (1 - t)
  all bigs carry the same rooted word, no 6 next to a big          -> 1/#bigs
  otherwise                                                        -> 0
Per side: T <= alpha + beta t with (alpha, beta) = (1 - c, 1 + c) (no chain) or (1 - c - c2, 3 + c + c2) (chain, c
without the chained five).  R*(6,6): 2.7 t >= 0.7 - T0 - T6, so t >= (0.7 - a0 - a6) / (2.7 + b0 + b6), best frames."""
import sys, os, re, itertools, collections
from fractions import Fraction as F
WD = os.path.abspath(sys.argv[1]); MYOPT = set(sys.argv[2:])
KF = next((a for a in sys.argv[2:] if a not in ('no37', 'nopair', 'nochain', 'debug')), None)
os.chdir(WD)
YF = os.path.join(WD, 'out', 'wlp3_j28_13.txt'); hdr = open(YF).readline().split()
args = [a for a in hdr[2:] if a == 'w7plus' or (a.startswith(('pat=', 'cpat=')) and os.path.exists(a.split('=', 1)[1]))]
args += ['pat=loop/n9/win%s.out' % x for x in ('9', '25', '25b', '27', '29', '31')] + ['tag=hfloor']
src = open(os.path.join(WD, 'wlp3.py')).read(); __file__ = os.path.join(WD, 'wlp3.py'); sys.argv = ['wlp3'] + args
_so = sys.stdout; sys.stdout = open(os.devnull, 'w')
exec(src[:src.index('A_ub, b_ub = [], []')])
sys.stdout = _so
CC = {}
def check(lk, sv):
    k = (tuple(lk), tuple(sv))
    if k not in CC:
        SEP.stdin.write('c 7 %s %s\n' % (''.join(map(str, lk)), ''.join(map(str, sv)))); SEP.stdin.flush()
        CC[k] = SEP.stdout.readline().strip() == '1'
    return CC[k]
assert check([5, 6, 7, 5, 7, 6, 5], [6, 6, 7, 7, 6, 7, 5]), 'R*(6,6) rejected by c'
L5 = (5, 6, 7, 8, 9); d = 7
# ---- kills
def images(L, S):
    out = []
    for refl in (0, 1):
        l2, s2 = (L[::-1], ''.join(S[(-i - 2) % d] for i in range(d))) if refl else (L, S)
        for k in range(d): out.append((l2[k:] + l2[:k], s2[k:] + s2[:k]))
    return out
def ok(ch, x): return ch == '.' or (ch == 'B' and x >= 7) or (ch in '5678' and int(ch) == x)
KILLS = [] if 'no37' in MYOPT else [('f7_5566757_...5...', images('5566757', '...5...'))]
if KF:
    for line in open(KF):
        f = line.split()
        if not f or f[0].startswith('#'): continue
        if re.match(r'^[5-9B.]{7}$', f[0]) and len(f) > 1 and re.match(r'^[5-9B.]{7}$', f[1]):
            KILLS.append((f[0] + '/' + f[1], [(f[0].replace('9', 'B'), f[1].replace('9', 'B'))])); continue
        m = re.match(r'^f(\d+)_([5-8B.]+)_([5-8B.]+)$', f[0])
        if not m: print('# skipped kill line:', line.strip()[:80]); continue
        if int(m.group(1)) != 7: continue
        KILLS.append((f[0], images(m.group(2), m.group(3))))
def killer(lk, sv):
    for nm, ims in KILLS:
        for L, S in ims:
            if all(ok(L[j], lk[j]) and ok(S[j], sv[j]) for j in range(d)): return nm
    return None
print('# kills applied:', [k for k, _ in KILLS])
# ---- shares
def lone_routes(lk, sv, i):
    """routes of lone five lk[i]: list of (d, paired?)"""
    out = []
    for dd in (1, -1):
        y, z = lk[(i + dd) % d], lk[(i + 2 * dd) % d]
        if y == 6 and z >= 7:
            sx = sv[(i + 1) % d] if dd == 1 else sv[(i - 2) % d]
            a = sv[i] if dd == 1 else sv[(i - 1) % d]
            paired = ('nopair' not in MYOPT and sx == 5 and z == 7 and not isR6([7, 5, a, a, 5, 7]))
            out.append((dd, paired))
    return out
def share(lk, sv, i):
    nl = [7, lk[(i + 1) % d], sv[i], sv[(i - 1) % d], lk[(i - 1) % d]]
    bigs = [j for j in range(5) if nl[j] >= 7]
    if bigs == [0]:
        rt = lone_routes(lk, sv, i); up = [r for r in rt if not r[1]]
        if not up: return F(1), 'lone' + (' (routes self-paired)' if rt else '')
        if len(up) == 1 and (i + 2 * up[0][0]) % d == 5 and 'nochain' not in MYOPT: return None, 'chain'
        return F(0), 'lone, unpaired route'
    if any(nl[(j + q) % 5] == 6 for j in bigs for q in (1, -1)): return F(0), 'multi-big, 6 next to a big'
    return (F(1, len(bigs)), 'symmetric') if len({root(nl, j) for j in bigs}) == 1 else (F(0), 'multi-big')
def cshare(lk, sv):
    c, ch = F(0), None
    for i in range(d):
        if lk[i] == 5:
            s, why = share(lk, sv, i)
            if s is None: ch = i
            else: c += s
    return c, ch
# ---- chain: s2 frame (w3 5, w2 7, y 6, x4, q1, q2, s3 7) / (u 7, v 5, pi, r1, r2, r3, w4 7), y = lk[4], v = lk[3]
C2 = {}
def c2best(x3, x4):
    if (x3, x4) in C2: return C2[(x3, x4)]
    best = (F(-1), None)
    for q1, q2, pi, r1, r2, r3 in itertools.product(L5, repeat=6):
        if isR6([7, 5, x3, pi, x4, 7]): continue
        lk = [5, 7, 6, x4, q1, q2, 7]; sv = [7, 5, pi, r1, r2, r3, 7]
        c2, ch = cshare(lk, sv)
        if c2 <= best[0] or killer(lk, sv) or not check(lk, sv): continue
        best = (c2, (''.join(map(str, lk)), ''.join(map(str, sv))))
    C2[(x3, x4)] = best; return best
# ---- w2 / w4 frames at s1 (s4) = 6
def side(X):
    cand = []; cnt = collections.Counter()
    for e, e2, p, x2, x3, x4 in itertools.product(L5, repeat=6):
        lk = [7, 6, 6, e, e2, 7, 5]; sv = [5, p, x2, x3, x4, 7, 7]
        if any(isR5([7, lk[(i + 1) % d], sv[i], sv[(i - 1) % d], lk[(i - 1) % d]]) for i in range(d) if lk[i] == 5): continue
        if isR6([7, 6, p, X, 5, 7]): continue
        c, ch = cshare(lk, sv)
        if ch is None: a, b, info = 1 - c, 1 + c, 'c = %s' % c
        else:
            c2, fr = c2best(x3, x4)
            if fr is None: continue
            a, b, info = 1 - c - c2, 3 + c + c2, 'c = %s + chain c2 = %s at s2 frame %s/%s' % (c, c2, fr[0], fr[1])
        cand.append((a, b, ''.join(map(str, lk)), ''.join(map(str, sv)), info))
    # keep only non-dominated (a, b), then test acceptance in order of usefulness at t ~ 0.15
    cand.sort(key=lambda r: r[0] + r[1] * F(3, 20))
    out = []
    for r in cand:
        lk = [int(ch) for ch in r[2]]; sv = [int(ch) for ch in r[3]]
        if any(o[0] <= r[0] and o[1] <= r[1] for o in out): continue
        k = killer(lk, sv)
        if k: cnt['killed'] += 1; continue
        if not check(lk, sv): cnt['c rej'] += 1; continue
        out.append(r)
    return out, cnt
res = {}
for nm, X in (('w2', 6), ('w4', 7)):
    res[nm], cnt = side(X)
    print('## %s: %d non-dominated surviving frames (%s)' % (nm, len(res[nm]), dict(cnt)))
    for r in res[nm][:5]: print('   T <= %s + %s t   link %s s %s   %s' % r)
best = None
for A in res['w2']:
    for Bq in res['w4']:
        fl = (F(7, 10) - A[0] - Bq[0]) / (F(27, 10) + A[1] + Bq[1])
        if best is None or fl > best[0]: best = (fl, A, Bq)
fl, A, Bq = best
print('\nfloor t >= (0.7 - a0 - a6) / (2.7 + b0 + b6) = %s = %.5f' % (fl, float(fl)) if fl > 0 else '\nno positive floor (%s)' % fl)
print('  w2 frame %s / %s: T0 <= %s + %s t (%s)' % (A[2], A[3], A[0], A[1], A[4]))
print('  w4 frame %s / %s: T6 <= %s + %s t (%s)' % (Bq[2], Bq[3], Bq[0], Bq[1], Bq[4]))
SEP.stdin.close(); SEP.wait()
