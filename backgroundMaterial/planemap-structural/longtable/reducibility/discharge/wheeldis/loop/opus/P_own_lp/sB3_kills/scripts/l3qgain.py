# B3: for D/C windows that kill one private of a link 7 (route.py routes L / L' / X7), list every (row, link 7 at w_j, side s)
# where the window embeds with that private = the side's l3q a2 (the private of w_j next to the apex a; c = w_{j+s} <= 6,
# a <= 6), with the table mask m now and the payee credit Qeff(c, a, m) before / after removing the killed letter.
# Exact embedding test: same slot set under a rotation/reflection rebuilds the same canonical window code in that row.
# usage: python3 l3qgain.py OUT.tsv SOL.json ROWSFILE[,ROWSFILE..] route.tsv
import sys, json, re, collections
from gen3 import build, ringcycle, kcline
from kcanon import code
OUT, SOL, RF, RT = sys.argv[1:5]
P = '/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s77_k6patch/tab/'
L3T = {}
for fn in (P + 'tab_1.json', P + 'tab_-1.json'):
    for k, v in json.load(open(fn)).items():
        sg, wd, ao = k.split(); L3T[(int(sg),) + tuple(int(c) for c in wd) + tuple(int(c) for c in ao)] = v[0]
S = json.load(open(SOL)); LQ = {tuple(k): v for k, v in S['lQ']}; LQV = {tuple(k): v for k, v in S['lq']}
def Qeff(c, a, m): return max([LQ.get((c, a, m), 0.0)] + [LQV.get((c, a, a2), 0.0) for a2 in (5, 6, 7, 8, 9) if m >> (a2 - 5) & 1])
ROWS = []
for fn in RF.split(','):
    for l in open(fn):
        if not l.strip() or l.startswith('#'): continue
        f = l.split()
        if len(f[1]) == 7: ROWS.append((f[1], f[2], f[3] if len(f) > 3 else ''))
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
out = open(OUT, 'w'); out.write('# window\troute\trow\ttag\tj\tsigma\tl3q key (sg,c,w2,w3,w4,a,o)\ttable mask\tkilled\tQeff before\tQeff after\n')
tot = collections.defaultdict(float)
for l in open(RT):
    if l.startswith('#'): continue
    g = l.rstrip('\n').split('\t'); nm, rt, kl = g[3], g[6], g[9]
    d, uin, lk, sv, ex = parse_name(nm)
    if d != 7 or len(ex) != 1 or ex[0][0][0] != 'p' or lk[ex[0][0][1]] != '7': continue
    (p, L), = ex; target = code(kl)
    S0 = ({('u',)} if uin else set()) | {('w', j) for j in range(7) if lk[j] != '.'} | {('s', j) for j in range(7) if sv[j] != '.'}
    for LK, SV, tag in ROWS:
        w = [int(c) for c in LK]; s = [int(c) for c in SV]; sides = set()
        for r in range(7):
            for refl in (0, 1):
                pw = (lambda j: (j + r) % 7) if not refl else (lambda j: (r - j) % 7)
                ps = (lambda j: (j + r) % 7) if not refl else (lambda j: (r - j - 1) % 7)
                if any(LK[pw(x[1])] != lk[x[1]] for x in S0 if x[0] == 'w'): continue
                if any(SV[ps(x[1])] != sv[x[1]] for x in S0 if x[0] == 's'): continue
                j = pw(p[1]); k = p[2] if not refl else 3 - p[2]
                Sl = {x if x[0] == 'u' else (('w', pw(x[1])) if x[0] == 'w' else ('s', ps(x[1]))) for x in S0} | {('p', j, k)}
                if LK[j] != '7': continue
                if window_code(LK, SV, Sl, {('p', j, k): L}) != target: continue
                sg = 1 if k == 2 else -1
                c = w[(j + sg) % 7]; w2, w3, w4 = (w[(j + i * sg) % 7] for i in (2, 3, 4))
                ap, o = (s[j], s[(j - 1) % 7]) if sg == 1 else (s[(j - 1) % 7], s[j])
                if c > 6 or ap > 6: continue
                sides.add((j, sg, (sg, c, w2, w3, w4, ap, o)))
        for j, sg, key in sorted(sides):
            m = L3T[key]; b = Qeff(key[1], key[5], m); a = Qeff(key[1], key[5], m & ~(1 << (L - 5)))
            out.write('\t'.join(map(str, [nm, rt, '%s/%s' % (LK, SV), tag, j, sg, key, m, L, '%.6f' % b, '%.6f' % a])) + '\n')
            tot[('%s/%s' % (LK, SV), tag, j, sg)] = max(tot[('%s/%s' % (LK, SV), tag, j, sg)], b - a)
out.close()
per = collections.defaultdict(float); ns = collections.Counter()
for (row, tag, j, sg), v in tot.items(): per[(row, tag)] += v; ns[(row, tag)] += 1
for (row, tag), v in sorted(per.items(), key=lambda kv: -kv[1]):
    print('%-18s %-14s sides %d  credit removed at the in-point (fixed weights) %.4f' % (row, tag[:14], ns[(row, tag)], v))
