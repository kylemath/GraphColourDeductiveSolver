"""Dump one maximal R0-planar open window: per state the components of M_{t-1} u M_t, whether E - M_t is a
connected figure-eight, DL pairing, A5v."""
import sys
import sat_planar
from sat_t1v import Enc, to_line
from pysat.solvers import Cadical153
sys.path.insert(0, '..')
from ax_lib import G5, parse_line, planar_rot
n, W = int(sys.argv[1]), int(sys.argv[2])
Enc._eager_loops = lambda self: None
enc = sat_planar.PEnc(n, W, 0, closed=False)
s = Cadical153(bootstrap_with=enc.cl)
cnt = 0
while s.solve() and cnt < int(sys.argv[3] if len(sys.argv) > 3 else 1):
    E, M, fv = enc.decode(s.get_model()); cnt += 1
    line = to_line(enc, E, fv); g = G5(*parse_line(line)); idx = {e: i for i, e in enumerate(E)}
    print('graph', line, 'planar_rot', planar_rot(g))
    for t in range(W):
        Mt = frozenset(idx[e] for e in M[t])
        k = g.kidx(Mt); d = g.dl(Mt); lp = g.loops(Mt)
        kh = g.ncomp(frozenset(idx[e] for e in M[t - 1]) | Mt) if t > 0 else '-'
        info = 'DL' if d else ('conn-fig8-nonDL' if lp else 'Q disconnected')
        a5 = ''
        if d:
            p = g.other(g.fv[k], g.v); a5 = 'A5v' if p in d[1]['X'][2] else 'anti'
        print(f'  t={t} k={k} k(M_t-1 u M_t)={kh} {info} {a5}')
    s.add_clause([-enc.X[e] for e in E if enc.X[e] is not None])
