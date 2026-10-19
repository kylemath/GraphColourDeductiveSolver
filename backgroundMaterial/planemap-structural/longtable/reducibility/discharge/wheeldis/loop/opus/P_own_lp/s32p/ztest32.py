# Physical test of the Z / ZR key (zh key) at both ends, and of the RR key (engine hat5_selftest with hatrr) (Opus s32p).
# Z: a five v with an adjacent big b. Explicit rotation of v: (b, n1, n2, n3, n4). Hats of v are read off explicit rotations
# of b, n1, n4 (a hat = the common neighbour of two consecutive spokes of v other than v). The receiver row of b reads the
# five at link position i with w_{i+1} = n1 or n4 (random mirror), s_i / s_{i-1} = n2 / n3 accordingly, w_{i+2}, w_{i-2} =
# b's link neighbours beyond n1 / n4. Sender key: zkey((b, n1, n2, n3, n4), class(hat(b, n1)), class(hat(n4, b))).
# Broken control: the receiver swaps the two hat classes without mirroring the link.
import os, sys, random
B = '/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp'
sys.path.insert(0, os.path.join(B, 's28q')); import eng_exec
M = '/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad/P/m/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis'
G = {}; eng_exec.engine(['root=' + M, 'hat5', 'hatrr', 'ntest=100000', 'work=/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad/P/w32p'], G)
zkey, c2, root, LET = G['zkey'], G['c2'], G['root'], G['LET']
def ztest(N=100000, broken=False):
    rng = random.Random(32); bad = 0
    for _ in range(N):
        db = rng.choice(range(7, 13)); L = lambda: rng.choice(LET)
        # b's rotation: v, n1, h1, ..., h4, n4  (h1 = hat(b, n1), h4 = hat(n4, b)); v's rotation: b, n1, n2, n3, n4
        deg = {'v': 5, 'b': min(db, 9), 'n1': L(), 'n2': L(), 'n3': L(), 'n4': L(), 'h1': L(), 'h4': L()}
        rotb = ['v', 'n1', 'h1'] + ['x%d' % k for k in range(db - 5)] + ['h4', 'n4']
        if rng.random() < 0.5: rotb = rotb[::-1]                       # random mirror of b's rotation
        k0 = rng.randrange(len(rotb)); rotb = rotb[k0:] + rotb[:k0]       # random offset
        for z in rotb: deg.setdefault(z, L())
        nb = lambda x: {rotb[rotb.index(x) - 1], rotb[(rotb.index(x) + 1) % len(rotb)]}
        hat_of = lambda x: (nb(x) - {'v'}).pop()                         # common nbr of b and spoke x of v, other than v
        ks = zkey(tuple(deg[x] for x in ('b', 'n1', 'n2', 'n3', 'n4')), c2(deg[hat_of('n1')]), c2(deg[hat_of('n4')]))
        # receiver b: link = rotb, v = w_i; s_i = apex of (w_i, w_{i+1}) other than b, read off v's rotation (b, n1, n2, n3, n4)
        i = rotb.index('v'); d_ = len(rotb); W = lambda k: rotb[(i + k) % d_]
        rotv = ['b', 'n1', 'n2', 'n3', 'n4']
        apex = lambda x: [z for z in rotv if z not in ('b', x) and abs(rotv.index(z) - rotv.index(x)) in (1, 4)][0]  # nbr of x in v's rotation other than b
        wn, wp = W(1), W(-1); sn, sp = apex(wn), apex(wp)
        hr, hl = c2(deg[W(2)]), c2(deg[W(-2)])
        if broken: hr, hl = hl, hr
        kr = zkey((deg['b'], deg[wn], deg[sn], deg[sp], deg[wp]), hr, hl)
        if ks != kr: bad += 1
        if root([deg['b'], deg[wn], deg[sn], deg[sp], deg[wp]], 0) != root([deg[x] for x in ('b', 'n1', 'n2', 'n3', 'n4')], 0): bad += 1
    return N, bad
n, b = ztest(); print('Z/ZR key physical test: %d fives, %d mismatches' % (n, b))
n, b = ztest(broken=True); print('broken control (receiver swaps the hat classes): %d mismatches' % b)
n, b = G['hat5_selftest'](100000); print('RR (hat5 + hatrr) physical test: %d diamonds, %d mismatches (key or r/rr coefficient signs)' % (n, b))
n, b = G['hat5_selftest'](100000, broken=True); print('RR broken control: %d mismatches' % b)
