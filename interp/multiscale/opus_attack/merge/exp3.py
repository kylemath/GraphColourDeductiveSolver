# E3: twisted seams on a NECKLACE A (weakly level: each pocket in its own radius-1 ball, centres differ), so that
# all 24 renamings can be defeated (a single chordless A admitted at most 13 of 24, see REPORT).
import sys, json, time, math, random, pickle
sys.dont_write_bytecode = True
from lat import disc_info, bfs, PERMS
from heights import ball_pts
from mergecheck import pockets
import twist, neck
from exp2 import seam_sequence

CENTRES = [(0, 0), (2, 0), (2, 2), (0, 2)]

def setup(k, h, M, ms, mb, centres=None):
    g, A, B, U, blob = neck.build(k, h, M, ms, mb)
    PA = pockets(g, A); PA.sort(key=lambda W: sum(g.pts[x][1] for x in W['walk'])/len(W['walk']))
    centres = centres or [CENTRES[n % 4] for n in range(len(PA))]
    consA = {}
    for n, W in enumerate(PA):
        bp = set(ball_pts(centres[n], 1.0))
        for x in W['walk']: consA[x] = consA[x] & bp if x in consA else set(bp)
    PB = pockets(g, B)
    consB = {x: set(ball_pts((0, 0), 1.0)) for W in PB for x in W['walk']}
    seq = seam_sequence(g, A, B, U)
    info = disc_info(g, A)
    chordv = set(x for e in info['chords'] for x in e)
    dch = bfs(g.adj, list(chordv), set(A) | set(B))
    return dict(g=g, A=A, B=B, U=U, PA=PA, PB=PB, consA=consA, consB=consB, seq=seq, dch=dch, centres=centres)

def slots(S, ell, gap, avoid):
    """consecutive runs of seam positions at distance > avoid from every chord endpoint, cut into stretches."""
    seq, dch = S['seq'], S['dch']; out = []; run = []
    for v in seq + [None]:
        if v is not None and dch.get(v, 99) > avoid: run.append(v); continue
        p = 1
        while p + ell <= len(run) - 1:
            out.append(run[p:p+ell]); p += ell + gap
        run = []
    return out

def greedy(S, ell, gap, avoid, rens, seed=0, log=print):
    sl = slots(S, ell, gap, avoid); g, B = S['g'], S['B']
    used = []          # list of (pi, slotL, slotR)
    free = list(range(len(sl)))
    def stretches(assign):
        st = []
        for j, (pi, a, b) in enumerate(assign):
            sig, Tc = twist.ALL[pi]
            for s in (a, b):
                st.append(([(x, y) for x in sl[s] for y in g.adj[x] if y in B], sig, Tc, j))
        return st
    h = None; Ts = None
    for pi in rens:
        placed = False
        for t in range(len(free) - 1):
            a, b = free[t], free[t+1]
            trial = used + [(pi, a, b)]
            hh, TT = twist.build(g, S['A'], B, S['consA'], S['consB'], stretches(trial), seed=seed)
            if isinstance(hh, dict):
                used = trial; free = free[:t] + free[t+2:]; h, Ts = hh, TT; placed = True; break
        log('renaming %s placed=%s (%d placed, %d free slots)' % (pi, placed, len(used), len(free)))
    return used, sl, h, Ts
