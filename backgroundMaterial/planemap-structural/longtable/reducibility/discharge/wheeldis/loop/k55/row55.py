"""EXPLORE round 55: which binder rows hold a configuration wholly inside their 1.5-ball (u, the link w_i and the second
ring s_i; exact vertices only, letter 9 never exact).  The frame is cen54's (loop/k53) with no slots; containment is
grow.embeddings (round 42/44 matcher: exact degrees, induced, interior triangles onto faces).  Configurations: the
registry (fam51.registry: RSST 582 + the twoeng names of TD/TC) and an extra kc file (the 2026 set), each extra hit
marked with its verdict in RES (loop/k53/N54_res.txt) if it has one.
usage: python3 row55.py TD TC XKC RES ROWS   (ROWS: lines 'w d link second-ring', e.g. Opus's cert receivers)
-> one line per row, then the totals"""
import sys, os, importlib, collections
TD, TC, XKC, RES, ROWS = sys.argv[1:6]
H = os.path.dirname(os.path.abspath(__file__)); K53 = os.path.join(H, '..', 'k53'); sys.path.insert(0, K53)
os.environ.update({'RING3': '0', 'J3S': '', 'FOCUS': ''})
rows = [l.split() for l in open(ROWS) if l.strip() and not l.startswith('#')]
sys.argv = ['cen54.py', rows[0][1], rows[0][2], rows[0][3]]
import cen54, grow
REG, miss = cen54.F.registry(TD, TC)
XL = [l.rstrip('\n') for l in open(XKC) if l.strip()]
XR = [grow.kcline(l, 'xreg') for l in XL]
ver = {}
if os.path.exists(RES):
    for l in open(RES):
        f = l.rstrip('\n').split(' ', 2)
        if len(f) == 3: ver[f[2]] = f[1]
XV = {l.split()[0]: ver.get(l.split(' ', 1)[1], 'unrun') for l in XL}
print('# registry %d (%d names not found), extra %d (%d with a verdict in %s), %d rows' % (len(REG), miss, len(XR),
      sum(v != 'unrun' for v in XV.values()), os.path.basename(RES), len(rows)), flush=True)
tot = collections.Counter(); allx = collections.Counter()
for w, d, lk, sv in rows:
    sys.argv = ['cen54.py', d, lk, sv]; importlib.reload(cen54)
    P, pa, pf = cen54.structure(dict(cen54.EX), [], {})
    def hits(confs):
        return sorted({c[0] for c in confs if grow.embeddings(c, P, pa, pf, cen54.EX)})
    hr, hx = hits(REG), hits(XR)
    tot['rows'] += 1; tot['registry hit'] += bool(hr); tot['2026 hit'] += bool(hx)
    tot['2026 hit, all D'] += bool(hx) and all(XV[n] == 'D' for n in hx)
    allx.update(hx)
    print('%s d%s %s/%s | registry %d %s | 2026 %d %s' % (w, d, lk, sv, len(hr), ' '.join(hr[:3]), len(hx),
          ' '.join('%s:%s' % (n, XV[n]) for n in hx[:6]) + (' +%d' % (len(hx) - 6) if len(hx) > 6 else '')), flush=True)
print('# %s; distinct 2026 configurations hit %d: %s' % (dict(tot), len(allx), ' '.join('%s:%s' % (n, XV[n]) for n in sorted(allx))))
