# B3: for D/C windows that kill the private of a link 6 (route A / A'), list every (row, link 6 at w_j) where the window
# embeds with that private at the killed letter (exact: same canonical window code), the filt16 mask now (s77 kill6 table)
# and the receiver's M term before / after removing the letter, at an in-point solution.
# M = max over allowed p of h[h2_of((U, w_{j+1}, s_j, p, s_{j-1}, w_{j-1}), w_{j+2}, w_{j-2})] (apexcls on; R6 keys
# are not excluded here, they simply have no h value) -- an [M] estimate of the row's inflow cut at fixed weights.
# usage: python3 m6gain.py OUT.tsv SOL.json ROWSFILE[,..] route.tsv
import sys, json, re, collections
import numpy as np
from gen3 import build, ringcycle, kcline
from kcanon import code
OUT, SOL, RF, RT = sys.argv[1:5]
KTD = '/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s77_k6patch/tab/kill/kill6'
KT = {U: np.load(KTD + '_U%d.npy' % U) for U in (7, 8, 9)}
S = json.load(open(SOL)); HV = {tuple(k): v for k, v in S['h']}
ap = lambda x: 7 if x >= 7 else 5
def h2_of(m, ar, al):
    ar, al = ap(ar), ap(al); a = tuple(m) + (ar, al); b = (m[0],) + tuple(reversed(m[1:])) + (al, ar); return min(a, b)
def Mval(U, w, s, j, d, mask):
    vals = [HV.get(h2_of((U, w[(j + 1) % d], s[j], p, s[(j - 1) % d], w[(j - 1) % d]), w[(j + 2) % d], w[(j - 2) % d]), 0.0) for i, p in enumerate((5, 6, 7, 8, 9)) if mask >> i & 1]
    return max(vals) if vals else 0.0
ROWS = []
for fn in RF.split(','):
    for l in open(fn):
        if not l.strip() or l.startswith('#'): continue
        f = l.split(); ROWS.append((f[1], f[2], f[3] if len(f) > 3 else ''))
def parse_name(nm):
    m = re.match(r'b(\d+)_([u-])([0-9.]+)_([0-9.]+)((?:_[pt]\d+)*)$', nm)
    d = int(m.group(1)); uin = m.group(2) == 'u'; lk, sv = m.group(3), m.group(4); ex = []
    for e in m.group(5).split('_')[1:]:
        if e[0] == 'p': ex.append((('p', int(e[1]), int(e[2])), int(e[3])))
        else: ex.append((('t', int(e[1:-1])), int(e[-1])))
    return d, uin, lk, sv, ex
def window_code(LK, SV, Sl, pdeg):
    try: adj, rot, name, deg, Z3, inv = build(LK, SV, pdeg=pdeg)
    except (AssertionError, ValueError): return None
    if any(x not in inv for x in Sl): return None
    if any(deg.get(x, 9) >= 9 for x in Sl if x[0] in 'uws'): return None
    Is = set(inv[x] for x in Sl); order = ringcycle(adj, Is)
    if order is None: return None
    return code(kcline('x', adj, Is, order))
out = open(OUT, 'w'); out.write('# window\trow\ttag\tj\tkill6 key (a,b,e,f,s0..s3)\tmask now\tkilled\tM before\tM after\n')
tot = {}
for l in open(RT):
    if l.startswith('#'): continue
    g = l.rstrip('\n').split('\t'); nm, kl = g[3], g[9]
    d, uin, lk, sv, ex = parse_name(nm)
    if len(ex) != 1 or ex[0][0][0] != 'p' or lk[ex[0][0][1]] != '6': continue
    (p, L), = ex; target = code(kl)
    S0 = ({('u',)} if uin else set()) | {('w', j) for j in range(d) if lk[j] != '.'} | {('s', j) for j in range(d) if sv[j] != '.'}
    for LK, SV, tag in ROWS:
        if len(LK) != d: continue
        w = [int(c) for c in LK]; s = [int(c) for c in SV]; U = min(d, 9); js = set()
        for r in range(d):
            for refl in (0, 1):
                pw = (lambda j: (j + r) % d) if not refl else (lambda j: (r - j) % d)
                ps = (lambda j: (j + r) % d) if not refl else (lambda j: (r - j - 1) % d)
                if any(LK[pw(x[1])] != lk[x[1]] for x in S0 if x[0] == 'w'): continue
                if any(SV[ps(x[1])] != sv[x[1]] for x in S0 if x[0] == 's'): continue
                j = pw(p[1])
                if LK[j] != '6': continue
                Sl = {x if x[0] == 'u' else (('w', pw(x[1])) if x[0] == 'w' else ('s', ps(x[1]))) for x in S0} | {('p', j, 1)}
                if window_code(LK, SV, Sl, {('p', j, 1): L}) == target: js.add(j)
        for j in sorted(js):
            key = (w[(j - 2) % d], w[(j - 1) % d], w[(j + 1) % d], w[(j + 2) % d], s[(j - 2) % d], s[(j - 1) % d], s[j], s[(j + 1) % d])
            m = 31 & ~int(KT[U][tuple(x - 5 for x in key)])
            if not (m >> (L - 5)) & 1: continue   # already killed by the table
            b = Mval(U, w, s, j, d, m); a = Mval(U, w, s, j, d, m & ~(1 << (L - 5)))
            out.write('\t'.join(map(str, [nm, '%s/%s' % (LK, SV), tag, j, key, m, L, '%.6f' % b, '%.6f' % a])) + '\n')
            k = ('%s/%s' % (LK, SV), tag, j); tot[k] = tot.get(k, (m, 0.0, b)); tot[k] = (tot[k][0] & ~(1 << (L - 5)), 0.0, b)
out.close()
per = collections.defaultdict(float); ns = collections.Counter()
for (row, tag, j), (m2, _, b) in tot.items():
    U = min(len(row.split('/')[0]), 9); LK, SV = row.split('/'); d = len(LK)
    a = Mval(U, [int(c) for c in LK], [int(c) for c in SV], j, d, m2); per[(row, tag)] += b - a; ns[(row, tag)] += 1
for (row, tag), v in sorted(per.items(), key=lambda kv: -kv[1]):
    print('%-24s %-14s 6s %d  M inflow cut at the in-point (fixed weights) %.4f' % (row, tag[:14], ns[(row, tag)], v))
