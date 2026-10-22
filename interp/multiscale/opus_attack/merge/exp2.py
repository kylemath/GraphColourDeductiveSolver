# E2: twisted seams.  A (chordless rectangle, or a necklace) hangs from the top edge of U, B wraps around it.
# The seam is cut into consecutive stretches of length ell; stretch pair j is forced conflict-free for renaming
# pi_j with two DIFFERENT offsets.  Then every renaming carries a monodromy obstruction of size ~ell/2.
import sys, json, time, math, pickle, os
sys.dont_write_bytecode = True
from lat import Lat, disc_info, bfs, PERMS
from heights import ball_pts
from mergecheck import pockets, tau, min_R, glue, conflicts
import twist

def rect(H, M, ms, mb):
    X0 = 0.0; W = M + ms
    pts = []; Ap = set(); Up = set()
    for j in range(-2, H + mb + 3):
        for i in range(math.floor(X0 - W - 4 - j/2.0), math.ceil(X0 + W + 4 - j/2.0) + 1):
            x = i + j/2.0
            pts.append((i, j))
            if 0 <= j <= H + mb and abs(x - X0) <= W + 1e-9:
                Up.add((i, j))
                if j <= H and abs(x - X0) <= M + 1e-9: Ap.add((i, j))
    g = Lat(pts)
    A = set(g.id[p] for p in Ap); U = set(g.id[p] for p in Up)
    return g, A, U - A, U

def seam_sequence(g, A, B, U):
    """A-side seam vertices in boundary order (walk of A, keep vertices having a B neighbour), as one arc."""
    walk = disc_info(g, A)['walk']
    on = [v for v in walk if any(w in B for w in g.adj[v])]
    m = len(walk); pos = {v: i for i, v in enumerate(walk)}
    # rotate so that the arc starts after the largest gap
    idx = sorted(pos[v] for v in on)
    gaps = [((idx[(t+1) % len(idx)] - idx[t]) % m, t) for t in range(len(idx))]
    _, t = max(gaps)
    order = idx[t+1:] + idx[:t+1]
    return [walk[i] for i in order]

def design(g, A, B, U, ell, gap, renamings, margin):
    seq = seam_sequence(g, A, B, U)
    stretches = []; pos = margin; j = 0; meta = []
    for pi in renamings:
        sig, Tc = twist.ALL[pi]
        for side in (0, 1):
            if pos + ell > len(seq) - margin: return None, seq
            vs = seq[pos:pos+ell]
            edges = [(a, b) for a in vs for b in g.adj[a] if b in B]
            stretches.append((edges, sig, Tc, j)); meta.append(dict(pi=pi, j=j, start=pos, verts=vs))
            pos += ell + gap
        j += 1
    return (stretches, meta), seq

def run(H, M, ms, mb, ell, gap, nren, margin=3, seed=0, cA=(0, 0), order_seed=0):
    import random
    g, A, B, U = rect(H, M, ms, mb)
    PA = pockets(g, A); PB = pockets(g, B)
    consA = {}
    for W in PA:
        for x in W['walk']: consA[x] = set(ball_pts(cA, 1.0))
    consB = {x: set(ball_pts((0, 0), 1.0)) for W in PB for x in W['walk']}
    rens = list(PERMS); random.Random(order_seed).shuffle(rens); rens = rens[:nren]
    d, seq = design(g, A, B, U, ell, gap, rens, margin)
    if d is None: return dict(err='seam too short', seam=len(seq))
    stretches, meta = d
    t0 = time.time()
    h, Ts = twist.build(g, A, B, consA, consB, stretches, seed=seed)
    return dict(g=g, A=A, B=B, U=U, PA=PA, PB=PB, h=h, Ts=Ts, meta=meta, rens=rens, sec=time.time()-t0, seam=len(seq))

if __name__ == '__main__':
    H, M, ms, mb, ell, gap, nren = [int(x) for x in sys.argv[1:8]]
    r = run(H, M, ms, mb, ell, gap, nren)
    if 'err' in r: print(r); sys.exit()
    print('seam', r['seam'], 'nA', len(r['A']), 'nB', len(r['B']), 'build', r['h'] is not None and r['h'] != 'UNK', round(r['sec'], 1))
