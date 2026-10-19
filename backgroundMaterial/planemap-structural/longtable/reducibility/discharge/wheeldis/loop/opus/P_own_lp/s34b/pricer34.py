# Stage 34b pricer (Opus). Pricing only, no solve. Spec: Long Table SolvingFrameworkPlan/docs/working/BORROWED-CHANNEL-2.md
# (origin/main 2417a735), families A (z6, flag l6r: 6 -> adjacent 6) and C (l3q extended to 7 -> 8).
# Cert: s28q/eng/cert_s28A60L.json (t >= 47/320, registry 7360eb92, args s29/argsA60.txt), rows rebuilt with the s28q engine's own
# builders exactly as s32p/pricer32.py. rc(column) = -(sum_rows dual * coef) / tco.
import os, sys, json, collections, itertools, random
from fractions import Fraction
B = '/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp'
sys.path.insert(0, os.path.join(B, 's28q')); import eng_exec
M = '/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad/P/m/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis'
ARGS = ['root=' + M, 'args=' + B + '/s29/argsA60.txt', 'rpat=' + B + '/rpatD.txt', 'xon', 'apexcls', 'filt16',
        'killtab=' + B + '/s29/f/kill/kill6', 'hat5', 'consall', 'l3q', 'l3qtab=' + B + '/s28q/tab60_1.json,' + B + '/s28q/tab60_-1.json',
        'lqcap=3', 'xcap=3', 'work=/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad/P/wr34b']
CERT = B + '/s28q/eng/cert_s28A60L.json'
MYDIR = '/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s34b'   # (pcheck defines HERE)
G = {}; eng_exec.engine(ARGS, G); globals().update({k: v for k, v in G.items() if not k.startswith('__')})
OUT = open(os.path.join(MYDIR, 'pricer34.log'), 'w')
def P(*a):
    s = ' '.join(str(x) for x in a); print(s, flush=True); OUT.write(s + '\n'); OUT.flush()
load_patterns(); xon = True
C = json.load(open(CERT))
SRL = R2_sender_rows(); SR = {(wd, tuple(map(str, b))): (cf, b) for wd, cf, b in SRL}
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
        tot[('h', tuple(row[2]))] += w; tot[('M', tuple(row[1]))] -= w
    elif row[0] == 'mrowL':
        tot[('lq', tuple(row[2]))] += w; tot[('lQ', tuple(row[1]))] -= w
    elif row[0] == 'receiverR2':
        d, lk, sv = int(row[1]), row[2], row[3]
        assert admissible(d, lk, sv) is None
        for k, v in recv_coef_R2(d, lk, sv, xon).items(): tot[k] += w * v
        tco -= w; Dn += w * (d - 6); rows.append(('R', w, (d, [int(ch) for ch in lk], [int(ch) for ch in sv])))
    else: raise SystemExit('row type ' + row[0])
bound = Dn / tco
rcE = {k: -v / tco for k, v in tot.items()}; negE = [k for k in rcE if rcE[k] < 0]
P('CONTROL flag off (l6r absent): cert %s rows %d tco %s bound %s = %.9f; existing columns touched %d, rc<0: %d' % (
    os.path.basename(CERT), len(C), tco, bound, float(bound), len(rcE), len(negE)))
assert bound == Fraction(47, 320) and not negE
ncons = sum(1 for r in rows if r[0] == 'C')
# ======================================================================== A. z6 (l6r)
def refl7(a): return (a[4], a[3], a[2], a[1], a[0], a[6], a[5])
def zkey6(L, s, j):
    a = (L[(j + 1) % 6], ap(L[(j + 2) % 6]), L[(j + 3) % 6], ap(L[(j + 4) % 6]), L[(j + 5) % 6], s[j], s[(j - 1) % 6])
    return min(a, refl7(a))
def refl6(g): return (g[3], g[2], g[1], g[0], g[5], g[4])
def sig_of_key(K):
    g = (K[0], K[1], K[3], K[4], K[5], K[6]); return min(g, refl6(g))
def sig_payee(L, s, k):
    g = (L[(k + 1) % 6], s[k], s[(k - 1) % 6], L[(k - 1) % 6], ap(L[(k + 2) % 6]), ap(L[(k - 2) % 6])); return min(g, refl6(g))
PAY = collections.defaultdict(Fraction); PAYR = collections.defaultdict(list); FIRST = {}
REC = collections.defaultdict(Fraction); RECR = collections.defaultdict(list)
for kind, w, data in rows:
    if kind != 'C': continue
    L, s = data; tg = 'cons2 %s/%s' % (''.join(map(str, L)), ''.join(map(str, s)))
    cnt = collections.Counter(zkey6(L, s, j) for j in range(6) if L[j] == 6)
    for K, n in cnt.items():
        PAY[K] += w * (-n); PAYR[K].append('%s w=%s x%d' % (tg, w, n)); FIRST[K] = FIRST.get(K, False) or (5 in L)
    cs = collections.Counter(sig_payee(L, s, k) for k in range(6) if L[k] == 6)
    for g, n in cs.items(): REC[g] += w * n; RECR[g].append('%s w=%s x%d' % (tg, w, n))
def rc_z6(K, sign=1): return -sign * (PAY[K] + REC.get(sig_of_key(K), Fraction(0))) / tco
keys = sorted(PAY); fk = [K for K in keys if FIRST[K]]
rcs = {K: rc_z6(K) for K in keys}
neg = sorted((K for K in fk if rcs[K] < 0), key=lambda K: (rcs[K], K))
P('\n== A. z6 / l6r: %d cert cons2 rows; payer keys touched %d (first family, payer L has a five: %d)' % (ncons, len(keys), len(fk)))
P('   first family: rc<0 %d, rc=0 %d, rc>0 %d' % (len(neg), sum(1 for K in fk if rcs[K] == 0), sum(1 for K in fk if rcs[K] > 0)))
P('   all payer keys: rc<0 %d' % sum(1 for K in keys if rcs[K] < 0))
for K in neg:
    g = sig_of_key(K)
    P('  NEG K=%s rc %s = %.6f | payer part %s, payee sigma=%s part %s' % (K, rcs[K], float(rcs[K]), -PAY[K] / tco, g, -REC.get(g, Fraction(0)) / tco))
    P('      payer rows: %s' % PAYR[K]); P('      payee rows: %s' % (RECR.get(g) or 'none'))
P('  all first-family keys with rc (sorted):')
for K in sorted(fk, key=lambda K: (rcs[K], K)): P('    %s rc %s' % (K, rcs[K]))
Ks = (5, 5, 5, 7, 5, 5, 5)
P('CONTROL wiring: K*=%s rc %s (decomposition: %s); sign flip rc %s' % (Ks, rc_z6(Ks), PAYR[Ks], rc_z6(Ks, -1)))
# composite per sigma: Z6[sigma] shared by several payer keys (z6[K] = Z6 for K in S): best S = all keys with negative payer part
bysig = collections.defaultdict(list)
for K in fk: bysig[sig_of_key(K)].append(K)
comp = []
for g, Kl in bysig.items():
    parts = [PAY[K] for K in Kl if PAY[K] > 0]          # -PAY/tco < 0 contributes negatively (PAY > 0 means rc part < 0)
    if parts: comp.append((-(sum(parts) + REC.get(g, Fraction(0))) / tco, g, sorted(K for K in Kl if PAY[K] > 0)))
comp.sort()
P('  composites per payee signature (best key set): %d sigma, min rc %s' % (len(comp), comp[0][0] if comp else None))
for r, g, Kl in comp[:8]: P('    sigma %s rc %s keys %s' % (g, r, Kl))
# ---- physical test: explicit 6-6 edge, payer view vs payee view
def phys(N, broken=False, seed=11):
    rng = random.Random(seed); bad = 0; badP = 0
    for _ in range(N):
        v = [rng.choice(LET) for _ in range(6)]; a_ = [rng.choice(LET) for _ in range(6)]; j = rng.randrange(6); v[j] = 6; Qv = rng.choice(LET)
        # vertices: x, V0..V5 (x's link), A0..A5 (A_i adjacent V_i, V_{i+1}), Q (y = V_j's vertex opposite x)
        tri = [('x', 'V%d' % i, 'V%d' % ((i + 1) % 6)) for i in range(6)] + [('V%d' % i, 'V%d' % ((i + 1) % 6), 'A%d' % i) for i in range(6)]
        y = 'V%d' % j; tri += [(y, 'A%d' % j, 'Q'), (y, 'Q', 'A%d' % ((j - 1) % 6))]
        let = {'x': 6, 'Q': Qv}; let.update({'V%d' % i: v[i] for i in range(6)}); let.update({'A%d' % i: a_[i] for i in range(6)})
        def cyc(c):   # cyclic link of c from the triangle list
            T = [t for t in tri if c in t]; nb = {}
            for t in T:
                o = [u for u in t if u != c]; nb.setdefault(o[0], []).append(o[1]); nb.setdefault(o[1], []).append(o[0])
            st = sorted(nb)[0]; seq = [st]; prev = None
            while True:
                nx = [u for u in nb[seq[-1]] if u != prev and u not in seq[-1:]]
                nx = [u for u in nx if u != (seq[-2] if len(seq) > 1 else None)]
                if not nx or nx[0] == st: break
                prev = seq[-1]; seq.append(nx[0])
            return seq
        def third(p, q, notv):
            for t in tri:
                if p in t and q in t and notv not in t: return [u for u in t if u not in (p, q)][0]
            return None
        def view(c, rot, rf):
            lk = cyc(c); assert len(lk) == 6
            if rf: lk = lk[::-1]
            lk = lk[rot:] + lk[:rot]
            ap_ = [third(lk[i], lk[(i + 1) % 6], c) for i in range(6)]
            return lk, ap_
        lx, axs = view('x', rng.randrange(6), rng.random() < .5)
        jj = lx.index(y); Lx = [let[u] for u in lx]; Sx = [ap(let[u]) for u in axs]
        K = zkey6(Lx, Sx, jj); Ptrue = let[lx[(jj + 3) % 6]]
        ly, ays = view(y, rng.randrange(6), rng.random() < .5)
        kk = ly.index('x'); Ly = [let[u] for u in ly]
        Sy = [ap(let[u]) if u is not None else 5 for u in ays]
        if broken: Sy[kk], Sy[(kk - 1) % 6] = Sy[(kk - 1) % 6], Sy[kk]
        if sig_payee(Ly, Sy, kk) != sig_of_key(K): bad += 1
        # P is x's vertex opposite y: not in y's closed 1-ball (y never sees it)
        if lx[(jj + 3) % 6] in ly or K[2] != Ptrue: badP += 1
    return bad, badP
b0 = phys(100000); b1 = phys(100000, broken=True)
P('CONTROL physical (100,000 random 6-6 edges, random rotation + reflection at both ends): sigma mismatches %d, P mismatches %d; broken (payee swaps s\'_k, s\'_k-1): %d' % (b0[0], b0[1], b1[0]))
# ---- non-vacuity of the negative keys: payer and payee 6-words (non-R6, incl. 2.122) that realise K / sigma(K)
A6 = all6_words()
def realise(K):
    g = sig_of_key(K); pay = set(); rec = set()
    for L in A6:
        for rot in range(6):
            for rf in (0, 1):
                Lr = list(L[::-1] if rf else L); Lr = Lr[rot:] + Lr[:rot]
                if Lr[0] != 6: continue
                for s0, s5 in itertools.product((5, 7), repeat=2):
                    s = [5] * 6; s[0], s[5] = s0, s5
                    if zkey6(Lr, s, 0) == K: pay.add((tuple(L), (s0, s5)))
                    if sig_payee(Lr, s, 0) == g: rec.add((tuple(L), (s0, s5)))
    return pay, rec
for K in neg[:6]:
    pay, rec = realise(K)
    P('NONVAC K=%s: payer (canonical non-R6 L, (s_j, s_j-1)) %d e.g. %s; payee sigma=%s words %d e.g. %s' % (
        K, len(pay), sorted(pay)[:4], sig_of_key(K), len(rec), sorted(rec)[:6]))
json.dump({'z6_rc': {str(K): str(rcs[K]) for K in keys}, 'z6_neg': [str(K) for K in neg]}, open(os.path.join(MYDIR, 'rc34_z6.json'), 'w'), indent=0)
# ======================================================================== C. l3q 7 -> 8 (LG of pricer32 restricted to U=7, V=8)
MK = json.load(open(B + '/s32p/masks32.json'))
LGq = collections.defaultdict(Fraction); LGQ = collections.defaultdict(list); TQ = collections.defaultdict(list)
for kind, w, data in rows:
    if kind != 'R': continue
    d, wl, sl = data; U = min(d, 9); tg = 'R%d %s/%s' % (d, ''.join(map(str, wl)), ''.join(map(str, sl)))
    for i in range(d):
        if wl[i] < 7: continue
        for sg in (1, -1):
            c_, a_, a2 = wl[(i + sg) % d], wl[(i + 2 * sg) % d], wl[(i + 3 * sg) % d]
            if (U, wl[i]) == (7, 8): LGq[(c_, a_, a2)] += -w; TQ[(c_, a_, a2)].append('%s w=%s' % (tg, w))
            if (wl[i], U) == (7, 8):
                ap_ = sl[i] if sg == 1 else sl[(i - 1) % d]
                kk = '%d %s %s %d %d' % (d, ''.join(map(str, wl)), ''.join(map(str, sl)), i, sg)
                LGQ[(c_, ap_)].append((w, kk, tg))
P('\n== C. l3q 7 -> 8: payer keys (c, a, a2) from d7 rows: %s' % {k: str(v) for k, v in LGq.items()})
P('   payee signatures (c, a) from d8 rows: %s' % {k: [(str(w), t) for w, kk, t in v] for k, v in LGQ.items()})
def mval(kk, var):
    if var == 'none': return 31
    if var == 'drop': return 0
    vv, fld = var.split(':'); e = MK.get(vv + ' ' + kk)
    return e[fld] if e else 31
for var in ('none', 'win:mask', 'full:mask', 'win:mask_without_suspect', 'full:mask_without_suspect', 'drop'):
    out = []
    for (c_, a_, a2), gain in sorted(LGq.items()):
        cost = sum(-w for w, kk, t in LGQ.get((c_, a_), []) if (mval(kk, var) >> LI[a2]) & 1)
        out.append('(%d,%d,%d): payer -sum w %s, payee cost %s, rc %s' % (c_, a_, a2, gain, cost, (cost - gain) / tco))
    P('  mask %-26s %s' % (var, ' | '.join(out)))
for k, v in TQ.items(): P('  payer rows %s: %s' % (k, v))
OUT.close()
