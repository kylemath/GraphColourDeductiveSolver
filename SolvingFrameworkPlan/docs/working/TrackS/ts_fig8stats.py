#!/usr/bin/env python3
"""Track S: figure-eight statistics along Q-runs (DL, F13 connected) on spheres.
Per state t: |X|,|Y| (cubic vertices on the loops), chords of M_t inside D_X, inside D_Y, in O, and among the O-chords
how many join X to Y (xy).  Regions are computed in the primal (P2 chains): D_X = K_aA(x2), D_Y = K_aA(x0), O = mB.
usage: ts_fig8stats.py GRAPHFILE name:hole ..."""
import sys
from ts_lib import load_graphs, HoleData
from tl_lib import TaitState
from ts_qruns import longest


def stats(hd, i):
    St = TaitState(hd, i); E = St.E; T = St.T
    X = St.X; Y = St.Y
    vX = St.verts(X) - {0}; vY = St.verts(Y) - {0}
    M = [k for k, e in enumerate(E) if e[2] == 2]
    r = hd.info[i]; col = hd.col[i]; al, mu, A, B = r['roles']; x = r['x']
    KX = hd.Hh.comp(col, x[2], (al, A)); KY = hd.Hh.comp(col, x[0], (al, A))
    cnt = dict(inX=0, inY=0, inO=0, xy=0, xx=0, yy=0)
    for k in M:
        u, w = St.prim[k]
        reg = 'X' if u in KX else ('Y' if u in KY else 'O')
        cnt['in' + reg] += 1
        if reg == 'O':
            a, b = E[k][0], E[k][1]
            ta = 'x' if a in vX else ('y' if a in vY else 'v'); tb = 'x' if b in vX else ('y' if b in vY else 'v')
            key = ''.join(sorted(ta + tb))
            if key in ('xy', 'xx', 'yy'): cnt[key] += 1
    return len(vX), len(vY), cnt


G = load_graphs(sys.argv[1], {s.rsplit(':', 1)[0] for s in sys.argv[2:]})
for spec in sys.argv[2:]:
    nm, h = spec.rsplit(':', 1); h = int(h); hd = HoleData(G[nm], h); info = hd.info
    ok = lambda i: info[i]['kind'] == 'DL' and info[i]['c6'][2] + info[i]['c6'][3] == 3
    pre = {info[i]['pi'] for i in range(hd.S) if ok(i) and info[i]['pi'] is not None}
    for i in range(hd.S):
        if not ok(i) or i in [info[q]['pi'] for q in range(hd.S) if ok(q)]: continue
        run = [i]; x = info[i]['pi']
        while x is not None and ok(x) and x not in run: run.append(x); x = info[x]['pi']
        if len(run) < 5: continue
        print(nm, h, 'Q-run', len(run))
        for q in run:
            nx, ny, c = stats(hd, q)
            print('   N=%d |X|=%d |Y|=%d inX=%d inY=%d inO=%d  O: xy=%d xx=%d yy=%d' % (info[q]['N'], nx, ny, c['inX'], c['inY'], c['inO'], c['xy'], c['xx'], c['yy']))
