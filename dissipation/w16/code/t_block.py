import sys, collections; sys.path.insert(0, '/tmp/swarm-W16/code')
import w16lib as W, torus as TT
from lp_patterns import lab_str
ns = W.init()
def vid_fn(p, q, r):
    def vid(i, j):
        k, j2 = divmod(j, r); i2 = (i - q * k) % p; return j2 * p + i2
    return vid
def build(p, q, r, flips):
    T = TT.lattice_torus(p, q, r); vid = vid_fn(p, q, r)
    for (i1, j1, i2, j2) in flips:
        assert T.flip(vid(i1, j1), vid(i2, j2)), ('flip failed', i1, j1, i2, j2)
    T.rebuild(); T.check(); return T
def report(T, name):
    labs, cnt = W.pattern_rows(T)
    print('==', name, 'n', T.n, 'degs', dict(collections.Counter(T.deg)))
    for lab, m in sorted(cnt.items(), key=str): print('  %3d %-40s %s' % (m, lab_str(lab), W.row_status(lab)))
    for fam in ('base', 'rrz', 'all'):
        res, keys, rmap = W.solve_lp(W.build_lp(list(cnt), fam)); print('  LP', fam, res.status, res.fun)
# 2x2 blocks, anti-diagonal flips
fl = [(2*m+1, 2*n, 2*m, 2*n+1) for m in range(2) for n in range(2)]
report(build(4, 0, 4, fl), 'block2x2')
# brick offset: blocks shifted by 1 in alternate rows
fl = [(2*m+1 + (n % 2), 2*n, 2*m + (n % 2), 2*n+1) for m in range(2) for n in range(2)]
report(build(4, 0, 4, fl), 'brick')
