# E5: necklace A (weakly level, pocket centres chosen by the solver) vs level B; all 24 renamings twisted.
import sys, json, time, pickle; sys.dont_write_bytecode=True
import neck, twist, exp3
from lat import PERMS, disc_info, bfs
from mergecheck import pockets
from heights import ball_pts

COPTS = [(a, b) for a in range(-3, 4) for b in range(-3, 4) if (a*a + b*b - a*b)/4.0 <= 2.0 + 1e-9]

def make(k, h, M, ms, mb, ell, gap, avoid, rens, seed=0, cap=3, tcands=3.0, perrun=99, bfree=False):
    g, A, B, U, blob = neck.build(k, h, M, ms, mb)
    PA = pockets(g, A); PB = pockets(g, B)
    consB = {} if bfree else {x: set(ball_pts((0, 0), 1.0)) for W in PB for x in W['walk']}
    S = dict(g=g, A=A, B=B, U=U, seq=None)
    from exp2 import seam_sequence
    S['seq'] = seam_sequence(g, A, B, U)
    chordv = set(x for e in disc_info(g, A)['chords'] for x in e)
    S['dch'] = bfs(g.adj, list(chordv), U)
    # stretch pairs: both stretches of a pair inside the same run of seam positions far (> avoid) from all necks
    sl = []; run = []
    for v in S['seq'] + [None]:
        if v is not None and S['dch'].get(v, 99) > avoid: run.append(v); continue
        p = 1; npair = 0
        while p + 2*ell + gap <= len(run) - 1 and npair < perrun:
            npair += 1
            sl.append(run[p:p+ell]); sl.append(run[p+ell+gap:p+2*ell+gap]); p += 2*(ell + gap)
        run = []
    if len(sl) < 2*len(rens): return dict(err='need %d slots, have %d' % (2*len(rens), len(sl)))
    st = []; meta = []
    for j, pi in enumerate(rens):
        sig, Tc = twist.ALL[pi]
        for s in (sl[2*j], sl[2*j+1]):
            st.append(([(a, b) for a in s for b in g.adj[a] if b in B], sig, Tc, j)); meta.append(dict(pi=pi, verts=s))
    popts = [(W['walk'], COPTS) for W in PA]
    if bfree: popts += [(W['walk'], COPTS) for W in PB if len(W['walk']) > 3]
    t0 = time.time()
    hh, Ts = twist.build(g, A, B, {}, consB, st, seed=seed, cap=cap, pocket_opts=popts, tcands=tcands)
    cen = twist.build.centres if isinstance(hh, dict) else None
    return dict(g=g, A=A, B=B, U=U, PA=PA, PB=PB, h=hh, Ts=Ts, meta=meta, centres=cen, sec=time.time()-t0,
                params=dict(k=k, h=h, M=M, ms=ms, mb=mb, ell=ell, gap=gap, avoid=avoid), nslots=len(sl))

if __name__ == '__main__':
    k, h, M, ms, mb, ell, gap, avoid, nren, perrun = [int(x) for x in sys.argv[1:11]]; out = sys.argv[11] if len(sys.argv) > 11 else None
    r = make(k, h, M, ms, mb, ell, gap, avoid, list(PERMS)[:nren], perrun=perrun)
    if 'err' in r: print(r); sys.exit()
    print('nA', len(r['A']), 'nB', len(r['B']), 'slots', r['nslots'], 'feasible', isinstance(r['h'], dict), 'centres', r['centres'], round(r['sec'], 1), flush=True)
    if out and isinstance(r['h'], dict):
        pickle.dump(dict(pts=r['g'].pts, A=sorted(r['A']), B=sorted(r['B']), h=r['h'], Ts=r['Ts'], centres=r['centres'],
                         meta=r['meta'], params=r['params']), open(out, 'wb'))
