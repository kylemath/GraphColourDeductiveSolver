# E4: chordless A (rectangle, one radius-1 ball) vs level B: all 24 renamings twisted on straight seam sides.
import sys, json, time, pickle; sys.dont_write_bytecode=True
import exp2 as E, twist
from lat import PERMS
from mergecheck import pockets
from heights import ball_pts

def make(H, M, ms, mb, ell, gap, rens, seed=0, cap=3, cA=(0, 0)):
    g, A, B, U = E.rect(H, M, ms, mb)
    PA = pockets(g, A); PB = pockets(g, B)
    consA = {x: set(ball_pts(cA, 1.0)) for W in PA for x in W['walk']}
    consB = {x: set(ball_pts((0, 0), 1.0)) for W in PB for x in W['walk']}
    seq = E.seam_sequence(g, A, B, U)
    ok = [v for v in seq if 3 <= g.pts[v][1] <= H - 4]
    # split into the two straight sides (consecutive in seq order)
    runs = []; cur = []
    for v in seq:
        if v in set(ok): cur.append(v)
        elif cur: runs.append(cur); cur = []
    if cur: runs.append(cur)
    sl = []
    for r in runs:
        p = 0
        while p + ell <= len(r): sl.append(r[p:p+ell]); p += ell + gap
    if len(sl) < 2*len(rens): return dict(err='need %d slots, have %d' % (2*len(rens), len(sl)))
    st = []; meta = []
    for j, pi in enumerate(rens):
        sig, Tc = twist.ALL[pi]
        for s in (sl[2*j], sl[2*j+1]):
            st.append(([(a, b) for a in s for b in g.adj[a] if b in B], sig, Tc, j)); meta.append(dict(pi=pi, verts=s))
    t0 = time.time()
    h, Ts = twist.build(g, A, B, consA, consB, st, seed=seed, cap=cap)
    return dict(g=g, A=A, B=B, U=U, PA=PA, PB=PB, h=h, Ts=Ts, meta=meta, sec=time.time()-t0, H=H, M=M, ms=ms, mb=mb, ell=ell, gap=gap)

if __name__ == '__main__':
    H, M, ms, mb, ell, gap = [int(x) for x in sys.argv[1:7]]; out = sys.argv[7]
    r = make(H, M, ms, mb, ell, gap, list(PERMS))
    if 'err' in r: print(r); sys.exit()
    print('nA', len(r['A']), 'nB', len(r['B']), 'feasible', isinstance(r['h'], dict), round(r['sec'], 1), flush=True)
    if isinstance(r['h'], dict):
        pickle.dump(dict(pts=r['g'].pts, A=sorted(r['A']), B=sorted(r['B']), h=r['h'], Ts=r['Ts'],
                         meta=r['meta'], params=[H, M, ms, mb, ell, gap]), open(out, 'wb'))
