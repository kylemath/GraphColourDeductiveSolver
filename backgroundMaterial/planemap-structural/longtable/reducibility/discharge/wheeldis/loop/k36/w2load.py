"""EXPLORE round 36 (H-W2): w2's load under the 7/27 y (out/wlp3_j28_13.txt) over every arrangement of w2 that is
consistent with R* at an open filling (s1 >= 6).  R = d7 link 5675765 s 6577575 at u; w2 as a receiver of degree 7:
link (u 7, w1 6, s1 a, e, e2, s2 7, w3 5), s-word (w0 5, p, x2, x3, x4, s3 7, w4 7).  Filters: sep3's `c` check
(j28_13 patterns + loop/n9/win9-31) and w1's 6-wheel (w2, a, p, s0 = 6, w0, u) not in R6.
k = T inflows (s-slot 5 between a big and a 6 link vertex), m = T outflow routes of w2's own link fives
(6-spoke then a big z in w2's link).  usage: python3 w2load.py > w2load.txt"""
import sys, os, re, itertools, collections
H = os.path.dirname(os.path.abspath(__file__)); WD = os.path.normpath(os.path.join(H, '..', '..'))
os.chdir(WD)
YF = os.path.join(WD, 'out', 'wlp3_j28_13.txt')
hdr = open(YF).readline().split()
args = [a for a in hdr[2:] if a == 'w7plus' or (a.startswith(('pat=', 'cpat=')) and os.path.exists(a.split('=', 1)[1]))]
miss = [a for a in hdr[2:] if a.startswith(('pat=', 'cpat=')) and not os.path.exists(a.split('=', 1)[1])]
args += ['pat=loop/n9/win%s.out' % x for x in ('9', '25', '25b', '27', '29', '31')] + ['tag=k36']
print('# missing pattern files (d = 10 only in the j28_13 header):', ' '.join(miss), flush=True)
src = open(os.path.join(WD, 'wlp3.py')).read(); __file__ = os.path.join(WD, 'wlp3.py')
sys.argv = ['wlp3'] + args
exec(src[:src.index('A_ub, b_ub = [], []')])
def check(d, lk, sv):                 # as wlp3.py's check (defined there after the LP rows)
    SEP.stdin.write('c %d %s %s\n' % (d, lk, sv)); SEP.stdin.flush(); return SEP.stdout.readline().strip() == '1'
yv = [0.0] * len(roots); ny = 0
for line in open(YF):
    m = re.match(r'^\s+(\d)\|(\d{4})\s+([\d.]+)\s*$', line)
    if m:
        r = (int(m.group(1)),) + tuple(int(c) for c in m.group(2)); yv[ix[r]] = float(m.group(3)); ny += 1
T27 = 7 / 27; BAR = 1 + T27
print('# y entries read', ny, flush=True)
# check 1: the 7/27 file's own d = 7 max, by sep3's separation
res_, nodes = sep(7, yv, BAR - 0.01, 20)
print('# check: d = 7 arrangements above %.4f: %d, max %.5f (bar %.5f; y has 4 decimals)' %
      (BAR - 0.01, len(res_), max(v for v, *_ in res_) if res_ else float('nan'), BAR), flush=True)
print('# check: R at u allowed by c:', check(7, '5675765', '6577575'), flush=True)
def load(lk, sv):
    out = 0.0
    for i in range(7):
        if lk[i] == 5:
            w = [7, lk[(i + 1) % 7], sv[i], sv[(i - 1) % 7], lk[(i - 1) % 7]]
            out += yv[ix[root(w, 0)]]
    return out
def tin(lk, sv):
    return sum(1 for j in range(7) if sv[j] == 5 and sorted((lk[j], lk[(j + 1) % 7]))[0] == 6 and max(lk[j], lk[(j + 1) % 7]) >= 7)
def tout(lk):
    m = 0
    for i in range(7):
        if lk[i] != 5: continue
        for dd in (1, -1):
            if lk[(i + dd) % 7] == 6 and lk[(i + 2 * dd) % 7] >= 7: m += 1
    return m
print('# check: R at u: load %.4f, k %d, m %d' % (load([5, 6, 7, 5, 7, 6, 5], [6, 5, 7, 7, 5, 7, 5]),
      tin([5, 6, 7, 5, 7, 6, 5], [6, 5, 7, 7, 5, 7, 5]), tout([5, 6, 7, 5, 7, 6, 5])), flush=True)
L5 = (5, 6, 7, 8, 9)
def enum(X):
    """X = the 6-spoke's far s letter fixed by R: s0 = 6 (w2's spoke w1), s5 = 7 (w4's spoke w5)."""
    rows = []; cnt = collections.Counter()
    for a in (6, 7, 8, 9):
        for e, e2, p, x2, x3, x4 in itertools.product(L5, repeat=6):
            lk = [7, 6, a, e, e2, 7, 5]; sv = [5, p, x2, x3, x4, 7, 7]
            cnt['all'] += 1
            if isR6([7, a, p, X, 5, 7]): cnt['spoke R6'] += 1; continue
            if not check(7, ''.join(map(str, lk)), ''.join(map(str, sv))): cnt['c rejects'] += 1; continue
            cnt['kept'] += 1
            rows.append((load(lk, sv), tin(lk, sv), tout(lk), ''.join(map(str, lk)), ''.join(map(str, sv))))
    return rows, cnt
FMT = '%.4f k=%d m=%d link %s s %s'
CAP = {}
for side, X in (('w2', 6), ('w4', 7)):
    rows, cnt = enum(X); rows.sort(reverse=True)
    print('\n## %s (spoke far letter %d): %s' % (side, X, dict(cnt)), flush=True)
    print('# top 8 by yload (yload, k, m, link, s):')
    for r in rows[:8]: print('  ' + FMT % r)
    bk = min(rows, key=lambda r: (BAR - r[0]) / r[1])
    print('T_max (y, t fixed; outflow of w2-side fives ignored) = %.4f at  %s' % ((BAR - bk[0]) / bk[1], FMT % bk))
    net = [r for r in rows if r[1] - r[2] > 0]
    bn = min(net, key=lambda r: (BAR - r[0]) / (r[1] - r[2]))
    print('T_max_net (outflow counted, k - m > 0) = %.4f at  %s' % ((BAR - bn[0]) / (bn[1] - bn[2]), FMT % bn))
    for a in '6789':
        sub = [r for r in rows if r[3][2] == a]
        b = min(sub, key=lambda r: (BAR - r[0]) / r[1]); CAP[(side, a)] = (BAR - b[0]) / b[1]
        print('  filling letter %s: %d arrangements, max yload %.4f, T_max %.4f at  %s' % (a, len(sub), max(sub)[0], CAP[(side, a)], FMT % b))
    print('k distribution:', dict(sorted(collections.Counter(r[1] for r in rows).items())))
    for kk in sorted(set(r[1] for r in rows)):
        sub = [r for r in rows if r[1] == kk]; mx = max(sub)
        print('  k=%d: %d arrangements, max yload %.4f, bound %.4f  (%s %s)' % (kk, len(sub), mx[0], (BAR - mx[0]) / kk, mx[3], mx[4]))
print('\n## first-order R row per open filling (s1, s4): t >= (0.7 - cap_w2(s1) - cap_w4(s4)) / 2.7')
for a in '6789':
    print('  s1=%s: ' % a + '  '.join('s4=%s %.4f' % (b, (0.7 - CAP[('w2', a)] - CAP[('w4', b)]) / 2.7) for b in '6789'))
SEP.stdin.close(); SEP.wait()
