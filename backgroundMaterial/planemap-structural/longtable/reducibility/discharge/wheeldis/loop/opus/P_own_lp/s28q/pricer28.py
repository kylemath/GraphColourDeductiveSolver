# Stage 28 pricer (Opus s28q): l3q family of BORROWED-CHANNEL-7FACE.md, priced against an exact dual (design only, no LP).
# Run: python3 run28.py  (execs the s24d engine pcheck.py + prelay2.py with the st24b flags, then this file).
# q[k], k = (U, V, c, a, a2): big u (U = min(d,9)) -> big link nbr v = w_i (V = letter), per side sg: c = w_{i+sg},
#   a = w_{i+2sg}, a2 = w_{i+3sg}. Payer row: -1 per (i, sg). First family: U = 7, V in 7..9, c, a in {5,6}, a2 in 5..9.
# Q[k', m], k' = (U, V, c, a), m = 5-bit mask of a2: payee row (centre v, V = min(d,9)) +1 per link 7 u = w_j and side sg:
#   c = w_{j+sg}, a = s_j (sg = +1) or s_{j-1} (sg = -1), m = mask28 'win' mask of u's private adjacent to a.
# mrowQ (new): Q[k', m] - q[(k', a2)] >= 0 for a2 in m. Old cert has no mrowQ rows (dual 0 there).
import json, collections, random, itertools
from fractions import Fraction
OUT = open(os.path.join(S28, 'pricer28.log'), 'w')
def P(*a):
    s = ' '.join(str(x) for x in a); print(s, flush=True); OUT.write(s + '\n'); OUT.flush()
MASKS = {}
for fn in ('masks_face.json', 'masks_side.json'):
    for k, v in json.load(open(os.path.join(S28, fn))).items(): MASKS[k] = v
def mask_of(lk, sv, j, sg, variant='win', swap=False):
    if swap: sg = -sg
    return MASKS['%s/%s %s' % (lk, sv, variant)]['%d %+d' % (j, sg)]['mask']
FIRST = [(7, V, c, a, a2) for V in (7, 8, 9) for c in (5, 6) for a in (5, 6) for a2 in LET]
assert len(FIRST) == 60
def payer_terms(d, w, Us=(7,)):
    cf = collections.Counter(); n = len(w); U = min(d, 9)
    if U not in Us: return cf
    for i in range(n):
        if w[i] < 7: continue
        for sg in (1, -1): cf[('q', (U, w[i], w[(i + sg) % n], w[(i + 2 * sg) % n], w[(i + 3 * sg) % n]))] -= 1
    return cf
def payee_terms(d, lk, sv, variant='win', maskoff=False, swap=False):
    cf = collections.Counter(); w = [int(c) for c in lk]; s = [int(c) for c in sv]; n = len(w); V = min(d, 9)
    for j in range(n):
        if w[j] != 7: continue
        for sg in (1, -1):
            a = s[j] if sg == 1 else s[(j - 1) % n]
            m = 31 if maskoff else mask_of(lk, sv, j, sg, variant, swap)
            cf[('Q', (7, V, w[(j + sg) % n], a), m)] += 1
    return cf
def l3q_terms(d, lk, sv, **kw):
    cf = payer_terms(d, [int(c) for c in lk]); cf.update(payee_terms(d, lk, sv, **kw)); return cf
def composite(cf, k):
    """coefficient of q^[k] = q[k] + every Q[(k[:4]), m] with k[4] in m (Q at its mrowQ minimum)"""
    v = cf.get(('q', k), 0)
    for kk, c in cf.items():
        if kk[0] == 'Q' and kk[1] == k[:4] and (kk[2] >> LET.index(k[4])) & 1: v += c
    return v
# ---- physical test of key visibility -----------------------------------------------------------------------
def phys(N=100000, broken=False):
    rng = random.Random(28); bad = 0
    for _ in range(N):
        # u (deg 7) clockwise rotation (v, n1..n6); v clockwise rotation (u, n6, x.., n1): faces (u, v, n1), (u, n6, v)
        dv = rng.choice(range(7, 12)); L = {x: rng.choice(LET) for x in ['n%d' % i for i in range(1, 7)] + ['x%d' % i for i in range(dv - 3)]}
        ru = ['v'] + ['n%d' % i for i in range(1, 7)]
        rv = ['u', 'n6'] + ['x%d' % i for i in range(dv - 3)] + ['n1']
        if rng.random() < .5: ru = ru[::-1]; rv = rv[::-1]          # mirror the whole embedding
        r0 = rng.randrange(7); ru = ru[r0:] + ru[:r0]; r1 = rng.randrange(dv); rv = rv[r1:] + rv[:r1]
        iv = ru.index('v'); V = min(dv, 9)
        pk = sorted((7, V, L[ru[(iv + sg) % 7]], L[ru[(iv + 2 * sg) % 7]], L[ru[(iv + 3 * sg) % 7]]) for sg in (1, -1))
        # v's row: link w' = rv read in rv's own order, apex s'_i = common nbr of w'_i, w'_{i+1} other than v (from u's rotation
        # for the two triangles at u). The payee knows s'_j, s'_{j-1}; a2 = u's private adjacent to that apex (truth).
        j = rv.index('u'); out = []
        for sg in (1, -1):
            c = rv[(j + sg) % dv]
            ic = ru.index(c); a = ru[(ic + 1) % 7] if ru[(ic - 1) % 7] == 'v' else ru[(ic - 1) % 7]   # apex across (u, c)
            if broken and sg == 1: c2 = rv[(j - 1) % dv]; ic2 = ru.index(c2); a = ru[(ic2 + 1) % 7] if ru[(ic2 - 1) % 7] == 'v' else ru[(ic2 - 1) % 7]
            ia = ru.index(a); a2 = ru[(ia + 1) % 7] if ru[(ia - 1) % 7] == c else ru[(ia - 1) % 7]
            out.append((7, V, L[c], L[a], L[a2]))
        if sorted(out) != pk: bad += 1
    return bad
P('physical test (u deg 7, v deg 7..11, random mirror/rotation, 100000 edges): %d key mismatches' % phys())
P('broken control (payee reads the + side apex across the - side edge): %d mismatches' % phys(broken=True))
# ---- engine regression: the cert is valid in the old class --------------------------------------------------
OPT['cert'] = CERT; cmd_lowerR2()
C = json.load(open(CERT)); tco = Fraction(0); D = Fraction(0); RR = []
for c in C:
    w = Fraction(c['w']).limit_denominator(10 ** 7); row = c['row']
    if row[0] == 'senderR2': tco += w; D += w
    elif row[0] == 'receiverR2':
        d, lk, sv = int(row[1]), row[2], row[3]; tco -= w; D += w * (d - 6)
        assert admissible(d, lk, sv) is None; base = recv_coef_R2(d, lk, sv, 'xon' in FLAGS)
        RR.append((w, d, lk, sv)); P('receiverR2 row', d, lk, sv, 'w', w, '| engine row builder: %d existing columns' % len(base))
P('cert', CERT, 'rows', len(C), 'tco', tco, 'objective', D / tco)
def price(tag, **kw):
    tot = collections.defaultdict(Fraction); touch = collections.defaultdict(list)
    for w, d, lk, sv in RR:
        cf = l3q_terms(d, lk, sv, **kw)
        for k, v in cf.items():
            if v: tot[k] += w * v; touch[k].append('%d %s/%s coef %+d' % (d, lk, sv, v))
        for k in FIRST:
            cc = composite(cf, k)
            if cc: tot[('qhat', k)] += w * cc; touch[('qhat', k)].append('%d %s/%s coef %+d' % (d, lk, sv, cc))
    rc = {k: -v / tco for k, v in tot.items()}
    P('\n[%s] l3q columns touched by the cert:' % tag)
    for k in sorted(rc, key=str):
        if k[0] != 'qhat': P('  %-34s rc %-6s = %+.6f  rows: %s' % (k, rc[k], float(rc[k]), touch[k]))
    P('[%s] composite q^ over the 60 first-family keys (Q at its mrowQ minimum):' % tag)
    for k in FIRST:
        r = rc.get(('qhat', k), Fraction(0))
        if r: P('  q^%s rc %s = %+.6f rows: %s' % (k, r, float(r), touch[('qhat', k)]))
    P('  all other first-family keys: rc = 0 (no cert row touches them)')
    # exact pricing with free mrowQ duals = min over a2-subsets S per signature of sum rc_q + sum rc_Q over masks meeting S
    worst = Fraction(0); arg = None
    for sig in sorted({k[:4] for k in FIRST}):
        for r_ in range(1, 6):
            for S in itertools.combinations(LET, r_):
                v = sum(rc.get(('q', sig + (a2,)), 0) for a2 in S) + sum(rc[k] for k in rc if k[0] == 'Q' and k[1] == sig and any((k[2] >> LET.index(a2)) & 1 for a2 in S))
                if v < worst: worst, arg = v, (sig, S)
    P('[%s] exact pricing (best mrowQ duals; min over a2-subsets per signature): min rc %s %s' % (tag, worst, arg))
    return rc
rcw = price('mask win'); rcf = price('mask full', variant='full'); rco = price('CONTROL mask off', maskoff=True)
rcs = price('CONTROL swapped side', swap=True)
k0 = ('qhat', (7, 7, 6, 6, 5))
P('\nHYPOTHESIS rc(q^(7,7,6,6,5)) = -6/13: got %s -> %s' % (rcw.get(k0), 'CONFIRMED' if rcw.get(k0) == Fraction(-6, 13) else 'REFUTED'))
P('CONTROL mask off: rc(q^(7,7,6,6,5)) = %s -> %s; min composite rc over family %s' % (rco.get(k0, 0), 'PASS' if rco.get(k0, 0) == 0 else 'FAIL', min([rco.get(('qhat', k), 0) for k in FIRST])))
P('with q capped at 3 (as x / D in lowerR2), the cert bound would be 2/13 + 3 * (-6/13) = %s' % (Fraction(2, 13) - 3 * Fraction(6, 13)))
# ---- side test on 7665567/6765756 (coefficients only, no dual) --------------------------------------------------
P('\nside test 7665567/6765756 (d = 7): payer + payee terms and composite coefficients, correct vs swapped mask side')
for tag, kw in (('correct', {}), ('swapped', {'swap': True})):
    cf = l3q_terms(7, '7665567', '6765756', **kw)
    P('  [%s] terms: %s' % (tag, dict(cf)))
    P('  [%s] composites: %s' % (tag, {k: composite(cf, k) for k in FIRST if composite(cf, k)}))
OUT.close()
