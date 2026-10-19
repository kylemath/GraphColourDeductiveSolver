# Stage 24 pricer (design only, no LP). Runs inside the pcheck namespace (exec'd after prelay2.py).
# New column families (RELAY_SPEC 19): D = big -> big across a diamond (the far tip is an apex s_i), O = big -> big
# opposite across a 6-spoke (the far tip is the 6's private).  Both move charge between bigs only, so they enter
# receiverR2 rows only (out: -1 in the payer's load, in: +1 in the payee's load); senderR2 / cons2 / mrow rows are untouched.
import json, collections, random
from fractions import Fraction
TAG = OPT.get('ptag', 'p'); OUT = open('pricer24_%s.log' % TAG, 'w')
def P(*a):
    s = ' '.join(str(x) for x in a); print(s); OUT.write(s + '\n'); OUT.flush()
cap9 = lambda d: min(d, 9)
def canon2(a, b): return min(a + b, b + a)
# ---- keys -------------------------------------------------------------------------------------------------------
def keyD(lf, lt, sx, sy): return ('D', lf, lt, canon2(sx, sy))
def side_view(z, link_nb, apex_nb, out):
    """read at a receiver centre T with spoke z, z's other T-adjacent link nbr link_nb and the apex apex_nb across
    (link_nb, z).  out = T is the from-tip.
      z = 5: z's nbrs are (T, other spoke, far tip, C, X) with X = link_nb (adjacent to T) and C = apex_nb (adjacent to the far tip)
      z = 6: (T, other spoke, far tip, A, B, X): link_nb = X, apex_nb = B, which the far tip also reads as an apex
      z >= 7: letter only"""
    if z == 5: return ((5, link_nb, apex_nb),) if out else ((5, apex_nb, link_nb),)
    if z == 6: return ((6, apex_nb),)
    return ((z,),)
def D_terms(d, w, s, broken=False):
    """D columns of receiver row (d, link w, apexes s): for every i with s_i big, out u -> s_i (coef -1), in s_i -> u (+1)"""
    cf = collections.Counter(); n = len(w); U = cap9(d)
    for i in range(n):
        if s[i] < 7: continue
        wm1, wi, wi1, wi2 = w[(i - 1) % n], w[i], w[(i + 1) % n], w[(i + 2) % n]; sm1, sp1 = s[(i - 1) % n], s[(i + 1) % n]
        for out in (True, False):
            sx = side_view(wi, wm1, sm1, out if not broken else True); sy = side_view(wi1, wi2, sp1, out)
            k = keyD(U, s[i], sx, sy) if out else keyD(s[i], U, sx, sy)
            cf[k] += -1 if out else 1
    return cf
def keyO(px, py): return ('O', canon2(px, py))
def O_terms(d, w, s):
    """O columns: for every 6-spoke w_j whose private A may be big. Hexagon of w_j: (u, w_{j+1}, s_j, A, s_{j-1}, w_{j-1}).
    out u -> A: coef -1 only if every allowed private is big (the row must hold for each private, the minimum counts);
    in A -> u: coef +1 if some allowed private is big (the maximum counts).  Pairs are (from-adjacent, to-adjacent)."""
    cf = collections.Counter(); n = len(w); U = cap9(d)
    for j in range(n):
        if w[j] != 6: continue
        am = amask(U, w[(j - 2) % n], w[(j - 1) % n], w[(j + 1) % n], w[(j + 2) % n], s[(j - 2) % n], s[(j - 1) % n], s[j], s[(j + 1) % n]) if F16 else 31
        forced_big = am != 0 and (am & 3) == 0; big_ok = (am & 28) != 0
        if forced_big: cf[keyO((w[(j - 1) % n], s[(j - 1) % n]), (w[(j + 1) % n], s[j]))] -= 1
        if big_ok: cf[keyO((s[(j - 1) % n], w[(j - 1) % n]), (s[j], w[(j + 1) % n]))] += 1
    return cf
# ---- physical test of key visibility (both ends) -----------------------------------------------------------------
def selftest(N=100000, broken=False):
    rng = random.Random(24); bad = 0
    for _ in range(N):
        # diamond (u, x, s, y): x, y consecutive spokes of u, s = the other apex of xy. Explicit rotations of x, y.
        dx, dy = rng.choice((5, 6, 7)), rng.choice((5, 6, 7))
        rot = {'x': ['u', 'y', 's'] + ['x%d' % i for i in range(dx - 4)] + ['Xu'],
               'y': ['u', 'x', 's'] + ['y%d' % i for i in range(dy - 4)] + ['Yu']}
        deg = {nm: rng.choice(LET) for nm in rot['x'] + rot['y']}
        deg['x'] = dx; deg['y'] = dy; du = rng.choice(range(7, 13)); ds = rng.choice(range(7, 13))
        deg['u'] = cap9(du); deg['s'] = cap9(ds)
        def nb(c, p, other):   # neighbour of p in c's rotation that is not `other`
            r = rot[c]; i = r.index(p); a1, a2 = r[(i - 1) % len(r)], r[(i + 1) % len(r)]
            return a2 if a1 == other else a1
        def view(T, F):   # T's receiver window around (x, y) with far tip F: (w_{i-1}, x, y, w_{i+2}, s_{i-1}, F, s_{i+1})
            Xl = nb('x', T, 'y'); Xa = nb('x', Xl, T); Yl = nb('y', T, 'x'); Ya = nb('y', Yl, T)
            return Xl, Xa, Yl, Ya
        Xl, Xa, Yl, Ya = view('u', 's')
        ku = keyD(cap9(du), deg['s'], side_view(dx, deg[Xl], deg[Xa], True), side_view(dy, deg[Yl], deg[Ya], True))
        Xl2, Xa2, Yl2, Ya2 = view('s', 'u')
        # s reads the same diamond with x, y in the opposite rotational order; it is the to-tip
        sx2 = side_view(dx, deg[Xl2], deg[Xa2], False if not broken else True); sy2 = side_view(dy, deg[Yl2], deg[Ya2], False)
        ks = keyD(deg['u'], cap9(ds), sy2, sx2)
        if ku != ks: bad += 1
        # O: hexagon of a 6 z: (u, p1, q1, A, q2, p2); u reads link p1/p2 + apexes q1/q2, A reads link q1/q2 + apexes p1/p2
        p1, q1, q2, p2 = (rng.choice(LET) for _ in range(4))
        kuo = keyO((p2, q2), (p1, q1)); kao = keyO((p1, q1), (p2, q2)) if not broken else keyO((q1, p1), (q2, p2))
        if kuo != kao: bad += 1
    return N, bad
n_, b_ = selftest(); P('physical test: %d diamonds + %d hexagons, %d key mismatches' % (n_, n_, b_))
n_, bb_ = selftest(broken=True); P('broken-key control (s reads a five side as from-tip / A swaps pairs): %d mismatches' % bb_)
# ---- pricing ------------------------------------------------------------------------------------------------------
load_patterns(); xon = 'xon' in FLAGS
C = json.load(open(OPT['cert']))
SR = {(wd, tuple(map(str, b))): cf for wd, cf, b in R2_sender_rows()}
tco = Fraction(0); D = Fraction(0); tot = collections.defaultdict(Fraction); touch = collections.defaultdict(list)
for c in C:
    w = Fraction(c['w']).limit_denominator(10 ** 7); row = c['row']
    if row[0] == 'senderR2': tco += w; D += w
    elif row[0] == 'receiverR2':
        d, lk, sv = int(row[1]), row[2], row[3]; tco -= w; D += w * (d - 6)
        wl = [int(ch) for ch in lk]; sl = [int(ch) for ch in sv]
        for k, v in list(D_terms(d, wl, sl).items()) + list(O_terms(d, wl, sl).items()):
            if v: tot[k] += w * v; touch[k].append((float(w), v, '%d %s %s' % (d, lk, sv)))
P('cert', OPT['cert'], 'rows', len(C), 'tco', tco, 'objective', D / tco, '=', float(D / tco))
rc = {k: -v / tco for k, v in tot.items()}
for fam in ('D', 'O'):
    ks = [k for k in rc if k[0] == fam]
    neg = sorted((k for k in ks if rc[k] < 0), key=lambda k: rc[k])
    P('\nfamily %s: %d columns touched by the cert (all others have rc = 0); rc < 0: %d, rc = 0: %d, rc > 0: %d' % (
        fam, len(ks), len(neg), sum(1 for k in ks if rc[k] == 0), sum(1 for k in ks if rc[k] > 0)))
    for k in neg[:40]:
        P('  NEG', k, 'rc', rc[k], '=', '%.6f' % float(rc[k]), 'rows:', touch[k][:4])
json.dump({str(k): str(v) for k, v in rc.items()}, open('rc24_%s.json' % TAG, 'w'), indent=0)
OUT.close()
