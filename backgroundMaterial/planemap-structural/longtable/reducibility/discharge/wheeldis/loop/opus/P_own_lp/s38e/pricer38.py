# Stage 38e pricer (Opus). Pricing only, no solve. Steinberger stage 2: an overcharged big (8, or any >= 8) pays an adjacent 7.
# Cert: s28q/eng/cert_s28A62L.json (lowerR2 VALID t >= 11/75, registry 3cfd7f18, args s31/argsA62.txt, s28q engine flags of
# cmd_s28.sh REG=A62). Rows rebuilt with the s28q engine's own builders, as s32p/pricer32.py. rc = -(sum dual * coef) / tco.
# Families (payer u = centre of a receiverR2 row of degree d >= 8 with a link 7 v = w_i; payee v = centre of a d = 7 row (L, t)
# with u = L_j, letter 8 or 9; payer reads exactly, payee reads exactly what it sees and a strict 14' mask on the rest):
#   E1  key (U, 7, {(c, a, b)} per side) = (w_{i+-1}, w_{i+-2}, s_i / s_{i-1}): exact at both ends. This is the engine's
#       x column tau(U, 7, ...) itself (control: must reproduce x's rc).
#   E2  E1 + e per side = the payer apex s_{i+1} / s_{i-2} (distance 2 from v; the payee's private of c, mask).  All of the 8's
#       link letters and apexes within distance 2 of the 7.
#   E3  E2 + a2 per side = w_{i+-3} (u's private at the payee, mask): adds the l3q/LG reach.
#   LG8 per-side l3q shape (U, 7, c, a, a2) with every letter in 5..9 (ask (A)), a2 masked.
# Composite pricing (exact): columns q_k >= 0 (cap 1/2), payee credit Q(sig, mask) >= max_{k in mask} q_k; the extreme rays are
# q = 1 on a key set S, Q = 1 on every payee item whose allowed set meets S: rc(S) = (cost(S) - gain(S)) / tco, minimised by
# enumeration over subsets of the keys with gain > 0 (and checked to be a closure problem: any S with gain 0 keys only adds cost).
import os, sys, json, collections, itertools, random
from fractions import Fraction
B = '/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp'
HERE38 = os.path.join(B, 's38e')
sys.path.insert(0, os.path.join(B, 's28q')); import eng_exec
M = '/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad/P/m/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis'
ARGS = ['root=' + M, 'args=' + B + '/s31/argsA62.txt', 'rpat=' + B + '/rpatD.txt', 'xon', 'apexcls', 'filt16',
        'killtab=' + B + '/s31/f/kill/kill6', 'hat5', 'consall', 'l3q', 'l3qtab=' + B + '/s28q/tab62_1.json,' + B + '/s28q/tab62_-1.json',
        'lqcap=3', 'xcap=3', 'work=/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad/P/w38e']
CERT = os.environ.get('CERT', B + '/s28q/eng/cert_s28A62L.json')
G = {}; eng_exec.engine(ARGS, G); globals().update({k: v for k, v in G.items() if not k.startswith('__')})
OUT = open(os.path.join(HERE38, os.environ.get('OUTLOG', 'pricer38.log')), 'w')
def P(*a):
    s = ' '.join(str(x) for x in a); print(s, flush=True); OUT.write(s + '\n'); OUT.flush()
load_patterns(); xon = True
C = json.load(open(CERT))
SRL = R2_sender_rows(); SR = {(wd, tuple(map(str, b))): (cf, b) for wd, cf, b in SRL}
cap9 = lambda d: min(d, 9)
rows = []; tco = Fraction(0); Dn = Fraction(0); tot = collections.defaultdict(Fraction)
for c in C:
    w = Fraction(c['w']).limit_denominator(10 ** 7); row = c['row']
    if row[0] == 'senderR2':
        cf, b = SR[(row[1], tuple(map(str, row[2])))]
        for k, v in cf.items(): tot[k] += w * v
        tco += w; Dn += w; rows.append(('S', w, (row[1], b)))
    elif row[0] == 'cons2':
        for k, v in cons2_coef(tuple(row[1]), tuple(row[2])).items(): tot[k] += w * v
        rows.append(('C', w, (tuple(row[1]), tuple(row[2]))))
    elif row[0] == 'mrowR2':
        tot[('h', tuple(row[2]))] += w; tot[('M', tuple(row[1]))] -= w; rows.append(('MR', w, (tuple(row[1]), tuple(row[2]))))
    elif row[0] == 'mrowL':
        tot[('lq', tuple(row[2]))] += w; tot[('lQ', tuple(row[1]))] -= w
    elif row[0] == 'receiverR2':
        d, lk, sv = int(row[1]), row[2], row[3]
        assert admissible(d, lk, sv) is None
        for k, v in recv_coef_R2(d, lk, sv, xon).items(): tot[k] += w * v
        tco -= w; Dn += w * (d - 6); rows.append(('R', w, (d, [int(ch) for ch in lk], [int(ch) for ch in sv])))
    else: raise SystemExit('row type ' + row[0])
rcE = {k: -v / tco for k, v in tot.items()}
bound = Dn / tco
CAPS = {'x': Fraction(3), 'D': Fraction(3), 'lq': Fraction(3)}
capadj = sum((rcE[k] * CAPS[k[0]] for k in rcE if rcE[k] < 0 and k[0] in CAPS), Fraction(0))
other_neg = [(k, rcE[k]) for k in rcE if rcE[k] < 0 and k[0] not in CAPS]
P('cert', CERT, 'rows', len(C), 'tco', tco)
P('CONTROL flag-off reproduction: bound Dn/tco = %s, capped-column adjustment %s, total %s = %.9f (target 11/75: %s); uncapped rc<0: %d'
  % (bound, capadj, bound + capadj, float(bound + capadj), bound + capadj == Fraction(11, 75), len(other_neg)))
xs = sorted((k for k in rcE if k[0] == 'x'), key=lambda k: rcE[k])
def untau(code):
    hi = code % 125; code //= 125; lo = code % 125; code //= 125; tl = LET[code % 3 + 2]; fl = LET[code // 3 + 2]
    dec = lambda s_: (LET[s_ // 25], LET[(s_ // 5) % 5], LET[s_ % 5]); return fl, tl, dec(lo), dec(hi)
P('EX x columns touched: %d; rc<0 (priced at cap 3): %s' % (len(xs), [(untau(k[1]), str(rcE[k])) for k in xs if rcE[k] < 0]))
P('   x keys into 7 from >= 8: %s' % [(untau(k[1]), str(rcE[k])) for k in xs if untau(k[1])[1] == 7 and untau(k[1])[0] >= 8])
P('   x keys 7 -> >= 8:        %s' % [(untau(k[1]), str(rcE[k])) for k in xs if untau(k[1])[0] == 7 and untau(k[1])[1] >= 8])
def rtag(d, w, s): return 'R%d %s/%s' % (d, ''.join(map(str, w)), ''.join(map(str, s)))
MK = json.load(open(os.path.join(HERE38, 'masks38.json')))
# ---------------------------------------------------------------- payer / payee readers (the physical test uses the same two)
def payer_sides(d, w, s, i):
    W_ = lambda k: w[k % d]; S_ = lambda k: s[k % d]
    return {+1: dict(c=W_(i + 1), a=W_(i + 2), b=S_(i), e=S_(i + 1), a2=W_(i + 3)),
            -1: dict(c=W_(i - 1), a=W_(i - 2), b=S_(i - 1), e=S_(i - 2), a2=W_(i - 3))}
def payee_sides(L, t, j, oracle=None):
    """payee v (d = 7 centre) reads (c, a, b) exactly; e exact when c = 5, else free ('e+'/'e-'); a2 always free"""
    D = len(L); L_ = lambda k: L[k % D]; T_ = lambda k: t[k % D]
    sp = dict(c=L_(j + 1), a=T_(j), b=L_(j + 2), e=T_(j + 1) if L_(j + 1) == 5 else 'e+', a2='a2+')
    sm = dict(c=L_(j - 1), a=T_(j - 1), b=L_(j - 2), e=T_(j - 2) if L_(j - 1) == 5 else 'e-', a2='a2-')
    if oracle:
        for sd, nm in ((sp, '+'), (sm, '-')):
            for f in ('e', 'a2'):
                if isinstance(sd[f], str): sd[f] = oracle(sd[f])
    return {+1: sp, -1: sm}
FIELDS = {'E1': ('c', 'a', 'b'), 'E2': ('c', 'a', 'b', 'e'), 'E3': ('c', 'a', 'b', 'e', 'a2')}
def keyE(fam, U, sides):
    t1 = tuple(sides[+1][f] for f in FIELDS[fam]); t2 = tuple(sides[-1][f] for f in FIELDS[fam])
    return (fam, U, 7) + tuple(sorted([t1, t2]))
def keyLG(U, sd): return ('LG8', U, 7, sd['c'], sd['a'], sd['a2'])
# ---------------------------------------------------------------- items
PAY = collections.defaultdict(Fraction); PAYT = collections.defaultdict(list)    # key -> gain (sum of -w), rows
PEE = collections.defaultdict(list)                                              # (fam, variant) -> [(cost, allowed keys, tag)]
def allowed(fam, variant, d, L, t, j, side_filter=None):
    """set of payer keys the payee item (row, j[, side]) must credit: completions of the free slots not killed by the mask"""
    U = L[j]; base = payee_sides(L, t, j)
    if fam.startswith('LG'):
        sg = +1 if fam == 'LG+' else -1; sd = base[sg]
        kills = [] if variant == 'none' else MK['%s %s %d %s %s %d' % (fam, variant, d, ''.join(map(str, L)), ''.join(map(str, t)), j)]['kills']
        out = set()
        for a2 in LET:
            if any(all(dict(a2=a2)[n[:-1]] == v for n, v in kl) for kl in kills): continue
            out.add(keyLG(U, dict(sd, a2=a2)))
        return out
    names = [n for sg in (+1, -1) for f in ('e', 'a2') if f in FIELDS[fam] for n in [base[sg][f]] if isinstance(n, str)]
    kills = [] if variant == 'none' or fam == 'E1' else MK['%s %s %d %s %s %d' % (fam, variant, d, ''.join(map(str, L)), ''.join(map(str, t)), j)]['kills']
    out = set()
    for vals in itertools.product(LET, repeat=len(names)):
        asg = dict(zip(names, vals))
        if any(all(asg.get(n) == v for n, v in kl) for kl in kills): continue
        sides = {sg: {f: (asg[x] if isinstance(x, str) else x) for f, x in base[sg].items() if f in FIELDS[fam]} for sg in (+1, -1)}
        out.add(keyE(fam, U, sides))
    return out
FAMS = [('E1', ['none']), ('E2', ['full', 'win', 'none']), ('E3', ['full', 'win', 'none']), ('LG8', ['full', 'win', 'none'])]
U8ONLY = os.environ.get('U8ONLY', '0') == '1'
for kind, w, data in rows:
    if kind != 'R': continue
    d, wl, sl = data; tg = rtag(d, wl, sl)
    if d >= 8 and not (U8ONLY and d != 8):
        for i in range(d):
            if wl[i] != 7: continue
            sides = payer_sides(d, wl, sl, i); U = cap9(d)
            for fam in ('E1', 'E2', 'E3'):
                k = keyE(fam, U, sides); PAY[k] += -w; PAYT[k].append('%s @w%d' % (tg, i))
            for sg in (+1, -1):
                k = keyLG(U, sides[sg]); PAY[k] += -w; PAYT[k].append('%s @w%d%+d' % (tg, i, sg))
    if d == 7:
        for j in range(7):
            if wl[j] < 8 or (U8ONLY and wl[j] != 8): continue
            for fam, vs in FAMS:
                for v in vs:
                    if fam == 'LG8':
                        for f2 in ('LG+', 'LG-'): PEE[(fam, v)].append((-w, allowed(f2, v, d, wl, sl, j), '%s @w%d%s' % (tg, j, f2[2])))
                    else: PEE[(fam, v)].append((-w, allowed(fam, v, d, wl, sl, j), '%s @w%d' % (tg, j)))
def price(fam, variant, sign=1, drop_payees=False):
    """exact best composite. sign=-1: every coefficient negated (the reverse transfer on the same keys)"""
    keys = [k for k in PAY if k[0] == fam]
    items = [] if drop_payees else PEE[(fam, variant)]
    if sign == 1:
        cand = [k for k in keys if PAY[k] > 0]; best = (Fraction(0), ())
        for r in range(1, len(cand) + 1):
            for S in itertools.combinations(cand, r):
                Ss = set(S); gain = sum(PAY[k] for k in S); cost = sum(cw for cw, A, tg in items if A & Ss)
                rc = (cost - gain) / tco
                if rc < best[0] or not best[1]: best = (rc, S) if (rc < best[0] or not best[1]) else best
        singles = sorted(((sum(cw for cw, A, tg in items if k in A) - PAY[k]) / tco, k) for k in keys)
        return best, singles
    # reverse direction: the 7 pays the big, each exact item now a payer (gain) and each payer occurrence a cost; for the
    # signed check only exact single keys are meaningful: rc_rev(k) = -rc(k) when every item touching k is exact (E1)
    singles = sorted((-(sum(cw for cw, A, tg in items if k in A) - PAY[k]) / tco, k) for k in keys)
    return None, singles
summary = {}
P('\nfamily variant  payer keys  payee items  best composite rc (key set)   single keys rc<0')
for fam, vs in FAMS:
    for v in vs:
        (rc, S), singles = price(fam, v)
        neg = [(str(r), k) for r, k in singles if r < 0]
        summary['%s %s' % (fam, v)] = {'best': str(rc), 'S': [list(map(str, k)) for k in S], 'neg_singles': [[r, list(map(str, k))] for r, k in neg]}
        P('%-4s %-5s %6d %6d   %s = %.6f  S=%s   neg singles %d' % (fam, v, len([k for k in PAY if k[0] == fam]), len(PEE[(fam, v)]), rc, float(rc), list(S), len(neg)))
        for r, k in singles[:4]:
            P('      single %s rc %s = %.6f payer rows %s payee rows %s' % (k, r, float(r), PAYT[k], [tg for cw, A, tg in PEE[(fam, v)] if k in A]))
# ---------------------------------------------------------------- controls
P('\nCONTROL E1 = engine x: every E1 key against x tau(U, 7, ...) rc')
bad = 0
for k in [k for k in PAY if k[0] == 'E1']:
    U = k[1]; (c1, a1, b1), (c2, a2, b2) = k[3], k[4]
    code = tau(U, 7, side(c1, a1, b1), side(c2, a2, b2)); rx = rcE.get(('x', code), Fraction(0))
    (r_, S), sing = price('E1', 'none'); rk = dict((kk, rr) for rr, kk in sing)[k]
    coderev = tau(7, U, side(c1, b1, a1), side(c2, b2, a2)); rrev = rcE.get(('x', coderev), Fraction(0))
    _, sing_rev = price('E1', 'none', sign=-1); rkrev = dict((kk, rr) for rr, kk in sing_rev)[k]
    P('   %s  E1 rc %s  x(U->7) rc %s  | sign flip %s  x(7->U) rc %s' % (k, rk, rx, rkrev, rrev))
    bad += (rk != rx) + (rkrev != rrev)
P('CONTROL E1/x agreement and sign flip: %d mismatches' % bad)
# sign flip on the richer families: the reverse column (7 pays the big, same keys) is exact at the 7 for E1 only; for E2/E3/LG8
# the reverse needs the big to see e/a2, which it does exactly, and the 7 to pay without seeing them -> singles negated
for fam, v in (('E2', 'full'), ('E3', 'full'), ('LG8', 'full')):
    _, s1 = price(fam, v); _, s2 = price(fam, v, sign=-1)
    P('CONTROL sign flip %s %s: singles rc+ %s / flipped %s (flipped = -original for each key: %s)' % (fam, v, [str(r) for r, k in s1], [str(r) for r, k in s2],
      all(dict((k, r) for r, k in s1)[k] == -r for r, k in s2)))
for fam, v in (('E2', 'full'), ('E3', 'full'), ('LG8', 'full')):
    (rc, S), _ = price(fam, v, drop_payees=True)
    P('CONTROL non-vacuity (payee rows dropped -> pure payer gain must price negative) %s %s: best %s = %.6f with %d keys' % (fam, v, rc, float(rc), len(S)))
for fam, v in (('E2', 'full'), ('E3', 'full'), ('LG8', 'full')):
    nk = sum(1 for cw, A, tg in PEE[(fam, v)]); nkill = sum(1 for cw, A, tg in PEE[(fam, v)] if len(A) < len([x for x in PEE[(fam, 'none')] if x[2] == tg][0][1]))
    P('CONTROL non-vacuity masks %s %s: %d payee items, %d with a strict kill (mask smaller than none)' % (fam, v, nk, nkill))
# payer / payee key overlap: which payer keys have any payee in the cert at all
for fam in ('E1', 'E2', 'E3', 'LG8'):
    for k in sorted(k for k in PAY if k[0] == fam):
        P('   %s payer key %s gain %s rows %s ; payee items (full/none) %s' % (fam, k, PAY[k], PAYT[k],
          [tg for cw, A, tg in PEE[(fam, 'full' if fam != 'E1' else 'none')] if k in A]))
# ---------------------------------------------------------------- physical both-end test
def phys(N, broken=False, seed=38):
    rng = random.Random(seed); bad = 0
    for _ in range(N):
        du = rng.choice(range(8, 13)); L = lambda: rng.choice(LET)
        deg = {'u': du, 'v': 7}
        U_ = ['v', 'A1', 'B1'] + ['U%d' % k for k in range(3, du - 2)] + ['B2', 'A2']       # u's cyclic link
        V_ = ['u', 'A1', 'C1', 'V3', 'V4', 'C2', 'A2']                                      # v's cyclic link (shares u, A1, A2)
        nb = {'u': U_, 'v': V_}
        def cyc(x, before, after, k, tag):     # x's cycle: before... then k middles ... after
            return before + ['%s_m%d' % (tag, m) for m in range(k)] + after
        dA1 = rng.choice((5, 6, 7, 8, 9)); dA2 = rng.choice((5, 6, 7, 8, 9))
        nb['A1'] = cyc('A1', ['v', 'u', 'B1'], ['C1'], dA1 - 4, 'A1')                       # v, u, B1, e1 = A1_m0, ..., C1
        nb['A2'] = cyc('A2', ['u', 'v', 'C2'], ['B2'], dA2 - 4, 'A2')                       # u, v, C2, ..., e2 = last middle, B2
        deg['A1'], deg['A2'] = dA1, dA2
        # B1 / B2 adjacency (u's link neighbours): B1 ~ A1, U3 ; v's apexes: across (A1, C1) = A1's last middle, across (C2, A2) = A2_m0
        allv = set(U_) | set(V_) | set(nb['A1']) | set(nb['A2'])
        for z in allv: deg.setdefault(z, L())
        def apex(x, y, centre):                # third vertex of the face (x, y, .) other than centre
            for z in (x, y):
                if z in nb:
                    cy = nb[z]; o = y if z == x else x; i_ = cy.index(o); cand = {cy[i_ - 1], cy[(i_ + 1) % len(cy)]} - {centre}
                    others = [q for q in cand if q != z]
                    if len(others) == 1: return others[0]
                    for q in others:          # the one also adjacent to the other endpoint (forced by our construction)
                        if q in nb.get(o, []) or (o in nb and q in nb[o]): return q
                    return sorted(others)[0]
            return 'X_%s_%s' % tuple(sorted((x, y)))
        # u's row: random offset + mirror
        def row(centre):
            cy = list(nb[centre])
            if rng.random() < 0.5: cy = cy[::-1]
            k0 = rng.randrange(len(cy)); cy = cy[k0:] + cy[:k0]
            d_ = len(cy); ap_ = [apex(cy[k], cy[(k + 1) % d_], centre) for k in range(d_)]
            for z in ap_: deg.setdefault(z, L())
            return cy, ap_
        cu, au = row('u'); cv, av = row('v')
        lt = lambda z: min(deg[z], 9)
        wu = [lt(z) for z in cu]; su = [lt(z) for z in au]; i = cu.index('v')
        k1 = keyE('E3', min(du, 9), payer_sides(du, wu, su, i))
        kl1 = sorted(keyLG(min(du, 9), sd) for sd in payer_sides(du, wu, su, i).values())
        Lv = [lt(z) for z in cv]; tv = [lt(z) for z in av]; j = cv.index('u')
        Dv = 7; Ln = lambda k: cv[k % Dv]
        def oracle_names(name):                # ground truth for a free slot, read off the explicit rotations
            sg = +1 if name.endswith('+') else -1
            if broken and name.startswith('e'): sg = -sg
            c = Ln(j + sg); a = apex('u', c, 'v')           # a = the face (u, c, a), a != v
            if name.startswith('e'):
                cy = nb[c]; i_ = cy.index(a); cand = [cy[i_ - 1], cy[(i_ + 1) % len(cy)]]
                return lt([q for q in cand if q != 'u'][0])
            cy = nb['u']; i_ = cy.index(a); cand = [cy[i_ - 1], cy[(i_ + 1) % len(cy)]]
            return lt([q for q in cand if q != c][0])
        s2 = payee_sides(Lv, tv, j, oracle=oracle_names)
        k2 = keyE('E3', Lv[j], s2); kl2 = sorted(keyLG(Lv[j], sd) for sd in s2.values())
        if k1 != k2 or kl1 != kl2: bad += 1
    return bad
b0 = phys(100000); b1 = phys(100000, broken=True)
P('\nCONTROL physical both-end test (100,000 random 8..12 - 7 edges, explicit rotations, random offset + mirror at both ends):'
  ' E3 (hence E2, E1) + LG8 key mismatches %d; broken control (payee reads e from the wrong side) %d' % (b0, b1))
# ---------------------------------------------------------------- ask (B): r67o, a 6 -> 7 relay paid only when the 7's outer contacts are all >= 9
# A cons2 6-type (L, s) splits by h; the r67o column at (L, s, j) (L_j = 7) has -1 in the h = all>=9 split (same dual w as the
# unsplit row), +1 on the payee 7's receiver row (a d = 7 row whose link has the 6, its two link neighbours and >= 9 letters on
# every outer contact: no cert d7 row has a 9), nothing else. h = all>=9 needs the apexes beside the 7 (s_{j-1}, s_j) >= 9,
# so class 7.  rc = w / tco per occurrence.
P('\nASK (B) r67o:')
negB = []
for kind, w, data in rows:
    if kind != 'C': continue
    L_, s_ = data
    for j in range(6):
        if L_[j] == 7:
            elig = s_[j] >= 7 and s_[(j - 1) % 6] >= 7
            if elig: negB.append((w / tco, L_, s_, j))
P('   cert cons2 rows with a 7 whose two flanking apexes are class 7 (eligible for h = all>=9): %s' % [(str(r), L_, s_, j) for r, L_, s_, j in negB])
Lw4 = (5, 6, 5, 7, 6, 7)
P('   w4 of 8666655/5677657 at p41 = 5: L = %s (L0 = p41, L3 = u, L5 = s3); cert cons2 rows with this L: %s' % (Lw4, [(str(w), s_) for kind, w, (L_, s_) in [r for r in rows if r[0] == 'C'] if L_ == Lw4]))
P('   (b) needs s4 = p31 >= 9 and s5 = the apex across (s3, p41) >= 9, i.e. s = (., ., 5, 5, 7, 7): not in the cert -> dual 0 -> rc(r67o) = 0')
hk = (7, 5, 6, 5, 7, 6, 5, 5)
P('   existing h key from w4 into u (p41 = 5): %s rc %s; its mrowR2 sig in the cert: %s' % (hk, rcE.get(('h', hk)), [(str(w), sg) for kind, w, (sg, k) in [r for r in rows if r[0] == 'MR'] if k == hk]))
json.dump(summary, open(os.path.join(HERE38, 'rc38.json'), 'w'), indent=0)
OUT.close()
