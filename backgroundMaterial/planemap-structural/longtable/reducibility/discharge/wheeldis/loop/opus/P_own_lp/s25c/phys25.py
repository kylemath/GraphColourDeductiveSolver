# Stage 25 physical key test (RELAY_SPEC_s20 2.3).  exec'd in the pcheck namespace: python3 pcheck.py price25 pfile=phys25.py fy
# A random planar 2-ball around a five v is built as an explicit rotation system; every reading is made by ONE generic
# rule (the common neighbour of two adjacent vertices, other than a given third, taken from a rotation list).
#  - the five's end: v's link and hat classes from rotations, canonicalised exactly as SENDERS/R2_sender_rows do, then
#    fy_sender_key(w, H, j) at the big spoke u;
#  - the big's end: u's link word and apex word of length d (random letters away from v), the letters next to v read
#    from rotations, in a random orientation of u, then fy_recv_key at v's position.
# broken = the big reads s_{i+2} where it should read s_{i+1} (control).
import random
def phys(N=200000, broken=False, seed=25):
    rng = random.Random(seed); bad = 0; n_ = 0
    L = lambda: rng.choice(LET)
    for _ in range(N):
        d = rng.choice((7, 8, 9, 10)); U = min(d, 9)
        x = [U] + [rng.choice((5, 5, 6, 7, 8, 9)) for _ in range(4)]   # v's spokes, x0 = u (letter min(deg, 9))
        if isR5(x): continue
        rot = {}
        rot['v'] = ['x%d' % k for k in range(5)]
        deg = {'v': 5}
        for k in range(5): deg['x%d' % k] = x[k]
        for k in range(5): deg['t%d' % k] = L()                       # hats: t_k common nbr of x_k, x_{k+1} (not v)
        # rotation of each small spoke x_k (k >= 1): v, x_{k+1}, t_k, [privates], t_{k-1}, x_{k-1}
        for k in range(1, 5):
            pv = ['P%d_%d' % (k, m) for m in range(x[k] - 5)] if x[k] <= 6 else ['P%d_%d' % (k, m) for m in range(2)]
            for z in pv: deg[z] = L()
            rot['x%d' % k] = ['v', 'x%d' % ((k + 1) % 5), 't%d' % k] + pv + ['t%d' % ((k - 1) % 5), 'x%d' % ((k - 1) % 5)]
        # u = x0: link of length d around u: v, x1, t0, (others ...), t4, x4 ; its apexes are read from the link vertices' rotations
        mid = ['O%d' % m for m in range(d - 5)]
        for z in mid: deg[z] = L()
        rot['x0'] = ['v', 'x1', 't0'] + mid + ['t4', 'x4']
        def common(a, b, excl):
            """common nbr of a and b other than excl, from a's rotation (the rotation neighbour of b in a's list)"""
            r = rot[a]; i = r.index(b); c1, c2_ = r[(i - 1) % len(r)], r[(i + 1) % len(r)]
            return c2_ if c1 == excl else c1
        # ---- five's end
        H = [c2(deg['t%d' % k]) for k in range(5)]
        w_ = min(min(tuple(x[(s0 + m) % 5] for m in range(5)), tuple(x[(s0 - m) % 5] for m in range(5))) for s0 in range(5))
        # the canonical word may be symmetric: every reading with the same word must give the same key at u
        ks = set()
        for refl in (False, True):
            for s0 in range(5):
                idx = [(s0 + m) % 5 for m in range(5)] if not refl else [(s0 - m) % 5 for m in range(5)]
                ww = tuple(x[i] for i in idx)
                if ww != w_: continue
                HH = [H[idx[m]] for m in range(5)] if not refl else [H[(idx[m] - 1) % 5] for m in range(5)]
                ks.add(fy_sender_key(list(ww), HH, idx.index(0)))
        # ---- big's end: read u's link in a random orientation, v at position i
        link = rot['x0'] if rng.random() < 0.5 else [rot['x0'][0]] + list(reversed(rot['x0'][1:]))
        i = rng.randrange(d); link = [link[(m - i) % d] for m in range(d)]          # link[i] = v
        def apex(m):   # s_m = common nbr of w_m, w_{m+1} other than u, read from whichever of the two has a rotation
            a, b = link[m % d], link[(m + 1) % d]
            if a in rot: return deg[common(a, b, 'x0')]
            if b in rot: return deg[common(b, a, 'x0')]
            return None
        wl = [deg[z] for z in link]; sl = [apex(m) for m in range(d)]
        sl = [z if z is not None else L() for z in sl]
        kr = fy_recv_key(U, wl[(i - 2) % d], wl[(i - 1) % d], wl[(i + 1) % d], wl[(i + 2) % d], sl[(i - 2) % d],
                         sl[(i - 1) % d], sl[i], sl[(i + 2) % d] if broken else sl[(i + 1) % d])
        # the sender word is read with u's letter as U = min(deg u, 9): the five sees u's letter, which is min(d, 9)
        n_ += 1
        if len(ks) != 1 or kr not in ks: bad += 1
    return n_, bad
for br in (False, True):
    n_, b_ = phys(broken=br)
    log('stage 25 fy physical test%s: %d (five, big) pairs, %d key mismatches' % (' [BROKEN-KEY CONTROL]' if br else '', n_, b_))
