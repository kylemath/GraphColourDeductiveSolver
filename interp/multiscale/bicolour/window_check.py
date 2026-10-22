# Item 3: sliding-window circumradius adds nothing. [P] subset monotonicity of the minimal enclosing ball; here a numeric check
# on tube rows (walk H_0..H_L as in bf2.c; unit steps e1,e2,e3 at 120 deg), all windows of all lengths, incl. Hodge-detrended walk.
import random, math, itertools
S3 = math.sqrt(3); E = {1: (1, 0), 2: (-0.5, S3/2), 3: (-0.5, -S3/2)}
def mec(P):
    P = list(P); random.shuffle(P); c, r = P[0], 0.0
    inside = lambda c, r, p: math.dist(c, p) <= r + 1e-9
    for i, p in enumerate(P):
        if inside(c, r, p): continue
        c, r = p, 0.0
        for j, q in enumerate(P[:i]):
            if inside(c, r, q): continue
            c = ((p[0]+q[0])/2, (p[1]+q[1])/2); r = math.dist(p, q)/2
            for s in P[:j]:
                if inside(c, r, s): continue
                ax, ay = p; bx, by = q; cx, cy = s; d = 2*(ax*(by-cy)+bx*(cy-ay)+cx*(ay-by))
                ux = ((ax*ax+ay*ay)*(by-cy)+(bx*bx+by*by)*(cy-ay)+(cx*cx+cy*cy)*(ay-by))/d
                uy = ((ax*ax+ay*ay)*(cx-bx)+(bx*bx+by*by)*(ax-cx)+(cx*cx+cy*cy)*(bx-ax))/d
                c = (ux, uy); r = math.dist(c, p)
    return r
rng = random.Random(1); viol = 0; nwin = 0; nrows = 0; alt_max = 0
for L in range(8, 19):
    for _ in range(300):
        r = [rng.randrange(4)]
        for i in range(1, L): r.append(rng.choice([c for c in range(4) if c != r[-1] and (i < L-1 or c != r[0])]))
        if r[-1] == r[0]: continue
        H = [(0.0, 0.0)]
        for i in range(L):
            d = E[r[i] ^ r[(i+1) % L]]; H.append((H[-1][0]+d[0], H[-1][1]+d[1]))
        t = H[-1]; Hd = [(H[i][0]-i*t[0]/L, H[i][1]-i*t[1]/L) for i in range(L)]
        for walk in (H, Hd):
            R = mec(walk); nrows += 1
            for a in range(len(walk)):
                for b in range(a+1, len(walk)):
                    nwin += 1
                    if mec(walk[a:b+1]) > R + 1e-9: viol += 1
        # alternating run x,y,x,y..: labels constant -> H oscillates? no: constant label = straight line. check
print('rows', nrows, 'windows', nwin, 'violations', viol)
# The two-colour run x,y,x,y,... : the labels x^y are constant, so on the BOUNDARY walk of a tube row the height moves
# straight (m-1 equal steps); in the transversal (column) direction a cone vertex alternates x,y,x,... with heights
# oscillating between two points. Report both window radii.
for m in range(2, 8):
    line = [(k*1.0, 0.0) for k in range(m)]; osc = [((k % 2)*1.0, 0.0) for k in range(m)]
    print('run of', m, 'vertices: along-row window radius', mec(line), ' two-point oscillation radius', mec(osc))
