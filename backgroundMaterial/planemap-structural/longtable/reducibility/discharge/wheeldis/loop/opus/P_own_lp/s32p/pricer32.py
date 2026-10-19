# Stage 32 pricer (Opus s32p). Design only, no solve. Prices candidate column families against an lowerR2 certificate
# (default s28q/eng/cert_s28A60L.json, t >= 47/320 on 7360eb92) using the s28q engine's own row builders.
# rc(column) = -(sum over cert rows of dual * coefficient) / tco, as lowerR2 (t's reduced cost normalised to 0).
# Families (every key readable at both ends at the resolution each row has; sender rows see hats / fans as classes):
#   EX  existing columns (y, r, x, g, h, M, lq, lQ): their rc, as a check (all >= 0 iff the cert is valid at 47/320)
#   YR  big -> adjacent five, key = the five's rooted link (the reverse of y)                      [our own; RSST rule-1 shape reversed]
#   Z / ZR  five <-> adjacent big, key = rooted link + classes of the two hats beside the big    [engine 'zh' key, stage 13]
#   RR  big hat -> five across a diamond (reverse hat channel, engine 'hatrr' key, stage 23)
#   O5 / O5F  big -> five / five -> big opposite across a 6-spoke (key: the two (apex, class) pairs) [our own]
#   D / O  big -> big across a diamond / opposite across a 6 (pricer24 keys, RELAY_SPEC 19)
#   LG  big u -> adjacent big v, l3q shape, key (U, V, c, a, a2) read along u's link (drule9 shape, generalised to any U, V)
#       payee credit Q(U, V, c, a, mask); here priced with the mask from mask32 (or 31 = no kill, conservative)
import os, sys, json, collections, itertools
from fractions import Fraction
B = '/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp'
sys.path.insert(0, os.path.join(B, 's28q')); import eng_exec
M = '/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad/P/m/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis'
ARGS = ['root=' + M, 'args=' + B + '/s29/argsA60.txt', 'rpat=' + B + '/rpatD.txt', 'xon', 'apexcls', 'filt16',
        'killtab=' + B + '/s29/f/kill/kill6', 'hat5', 'consall', 'l3q', 'l3qtab=' + B + '/s28q/tab60_1.json,' + B + '/s28q/tab60_-1.json',
        'lqcap=3', 'xcap=3', 'work=/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad/P/w32p']
CERT = os.environ.get('CERT', B + '/s28q/eng/cert_s28A60L.json')
MASKF = os.environ.get('MASKS', '')        # json from mask32.py: {"d LK SV j sg": mask}
G = {}; eng_exec.engine(ARGS, G); globals().update({k: v for k, v in G.items() if not k.startswith('__')})
OUT = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), os.environ.get('OUTLOG', 'pricer32.log')), 'w')
def P(*a):
    s = ' '.join(str(x) for x in a); print(s, flush=True); OUT.write(s + '\n'); OUT.flush()
load_patterns(); xon = True
C = json.load(open(CERT))
SRL = R2_sender_rows(); SR = {(wd, tuple(map(str, b))): (cf, b) for wd, cf, b in SRL}
cap9 = lambda d: min(d, 9)
# ---------------------------------------------------------------- cert rows
rows = []   # (kind, w, data)
tco = Fraction(0); Dn = Fraction(0); tot = collections.defaultdict(Fraction)
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
P('cert', CERT, 'rows', len(C), 'tco', tco, 'bound before column pricing', bound, '=', float(bound))
rcE = {k: -v / tco for k, v in tot.items()}
negE = sorted((k for k in rcE if rcE[k] < 0), key=lambda k: rcE[k])
P('EX existing columns touched: %d; rc < 0: %d %s' % (len(rcE), len(negE), [(k, rcE[k]) for k in negE[:5]]))
for fam in ('y', 'r', 'x'):
    ks = sorted((k for k in rcE if k[0] == fam), key=lambda k: rcE[k])
    P('  %s: %d keys, %d at rc 0, %d at rc > 0; largest rc: %s' % (fam, len(ks), sum(1 for k in ks if rcE[k] == 0), sum(1 for k in ks if rcE[k] > 0),
      [(k[1], str(rcE[k])) for k in ks[::-1][:6]]))
def rname_(r): return '%d|%s' % (r[0], ''.join(map(str, r[1:])))
# ---------------------------------------------------------------- generic family accumulation
FAM = collections.defaultdict(lambda: collections.defaultdict(Fraction))
TOUCH = collections.defaultdict(list)
def add(fam, key, w, coef, tag):
    if coef: FAM[fam][key] += w * coef; TOUCH[(fam, key)].append('%s %+d @%.5f' % (tag, coef, float(w)))
def stag(wd, b): return 'S %s %s' % (wd, ''.join(map(str, b)))
def rtag(d, w, s): return 'R%d %s/%s' % (d, ''.join(map(str, w)), ''.join(map(str, s)))
for kind, w, data in rows:
    if kind == 'C': continue
    if kind == 'S':
        wd, b = data; wl = [int(ch) for ch in wd]; n = 5
        sixes = [k for k in range(n) if wl[k] == 6]
        H = dict(zip(range(n), b[:5])); Fn = dict(zip(sixes, b[6:])); tg = stag(wd, b)
        for j in range(n):
            if wl[j] >= 7:
                rt = root(wl, j); zk = zkey(tuple(wl[(j + i) % n] for i in range(5)), H[j], H[(j - 1) % n])
                add('YR', rt, w, -1, tg)                    # five gains: inflow is -1 in the 'sends >= 1 - t' row
                add('Z', zk, w, +1, tg); add('ZR', zk, w, -1, tg)
            if H[j]: add('RR', h5_sender(wl, H, Fn, j), w, -1, tg)
        for k in sixes:
            if Fn[k]:
                key = tuple(sorted([(wl[(k + 1) % n], H[k]), (wl[(k - 1) % n], H[(k - 1) % n])]))
                add('O5', key, w, -1, tg); add('O5F', key, w, +1, tg)
    else:
        d, wl, sl = data; U = cap9(d); tg = rtag(d, wl, sl)
        for i in range(d):
            W_ = lambda k: wl[k % d]; S_ = lambda k: sl[k % d]
            if wl[i] == 5:
                rt = root([U, W_(i + 1), S_(i), S_(i - 1), W_(i - 1)], 0)
                zk = zkey((U, W_(i + 1), S_(i), S_(i - 1), W_(i - 1)), c2(W_(i + 2)), c2(W_(i - 2)))
                add('YR', rt, w, -1, tg)                    # big pays out: load -1
                add('Z', zk, w, +1, tg); add('ZR', zk, w, -1, tg)
            if sl[i] == 5:
                add('RR', h5_recv(W_(i - 1), W_(i), W_(i + 1), W_(i + 2), S_(i - 1), S_(i + 1)), w, -1, tg)
            if wl[i] == 6:
                am = amask(U, W_(i - 2), W_(i - 1), W_(i + 1), W_(i + 2), S_(i - 2), S_(i - 1), S_(i), S_(i + 1))
                key = tuple(sorted([(S_(i), c2(W_(i + 1))), (S_(i - 1), c2(W_(i - 1)))]))
                if am == 1: add('O5', key, w, -1, tg)       # pays only when the private is forced to be a five
                if am & 1: add('O5F', key, w, +1, tg)       # receives whenever a five private is possible (max)
        # D / O (pricer24 keys, engine d_keys / O as pricer24)
        for i in range(d):
            if sl[i] >= 7:
                ko, ki = d_keys(U, wl[(i - 1) % d], wl[i], wl[(i + 1) % d], wl[(i + 2) % d], sl[(i - 1) % d], sl[i], sl[(i + 1) % d])
                add('D', ko, w, -1, tg); add('D', ki, w, +1, tg)
        for j in range(d):
            if wl[j] != 6: continue
            am = amask(U, wl[(j - 2) % d], wl[(j - 1) % d], wl[(j + 1) % d], wl[(j + 2) % d], sl[(j - 2) % d], sl[(j - 1) % d], sl[j], sl[(j + 1) % d])
            if am != 0 and (am & 3) == 0: add('O', ('O', d_canon2((wl[(j - 1) % d], sl[(j - 1) % d]), (wl[(j + 1) % d], sl[j]))), w, -1, tg)
            if am & 28: add('O', ('O', d_canon2((sl[(j - 1) % d], wl[(j - 1) % d]), (sl[j], wl[(j + 1) % d]))), w, +1, tg)
# ---------------------------------------------------------------- LG: l3q-shape big -> adjacent big, all U, V
MKV = os.environ.get('MASKVAR', 'win'); MKF = os.environ.get('MASKFIELD', 'mask')
MK = {k.split(' ', 1)[1]: v[MKF] for k, v in json.load(open(MASKF)).items() if k.split(' ', 1)[0] == MKV} if MASKF else {}
LGq = collections.defaultdict(Fraction); LGQ = collections.defaultdict(list)   # payer (U,V,c,a,a2) -> sum w*coef ; payee (U,V,c,a) -> [(w, mask, tag)]
for kind, w, data in rows:
    if kind != 'R': continue
    d, wl, sl = data; U = cap9(d); tg = rtag(d, wl, sl)
    for i in range(d):
        if wl[i] < 7: continue
        for sg in (1, -1):
            c, a, a2 = wl[(i + sg) % d], wl[(i + 2 * sg) % d], wl[(i + 3 * sg) % d]
            LGq[(U, wl[i], c, a, a2)] += -w; TOUCH[('LGq', (U, wl[i], c, a, a2))].append('%s payer @%.5f' % (tg, float(w)))   # -1 * w
            ap_ = sl[i] if sg == 1 else sl[(i - 1) % d]
            m = MK.get('%d %s %s %d %d' % (d, ''.join(map(str, wl)), ''.join(map(str, sl)), i, sg), 31)
            LGQ[(wl[i], U, c, ap_)].append((w, m, tg))           # payee v = centre (V = U here), payer letter wl[i]
def lg_price():
    """composite (q on a set S of a2 letters for (U, V, c, a); Q(mask) = 1 for each payee mask meeting S): exact min over S"""
    res = []
    sigs = {k[:4] for k in LGq} | set(LGQ)
    for sg in sigs:
        best = None
        for r in range(1, 6):
            for S in itertools.combinations(LET, r):
                gain = sum(LGq.get(sg + (a2,), Fraction(0)) for a2 in S)       # sum of (-w) over payer rows: >= 0
                cost = sum(-w for w, m, tg in LGQ.get(sg, []) if any((m >> LI[a2]) & 1 for a2 in S))
                rc = (cost - gain) / tco
                if best is None or rc < best[0]: best = (rc, S, gain, cost)
        res.append((best[0], sg, best[1], best[2], best[3]))
    return sorted(res)
# ---------------------------------------------------------------- report
P('\nfamily  keys touched  rc<0  rc=0  rc>0   most negative')
summary = {}
for fam in ('YR', 'Z', 'ZR', 'RR', 'O5', 'O5F', 'D', 'O'):
    rc = {k: -v / tco for k, v in FAM[fam].items()}
    neg = sorted((k for k in rc if rc[k] < 0), key=lambda k: rc[k])
    summary[fam] = {str(k): str(rc[k]) for k in neg}
    P('%-6s %6d %6d %6d %6d   %s' % (fam, len(rc), len(neg), sum(1 for k in rc if rc[k] == 0), sum(1 for k in rc if rc[k] > 0),
      '%s = %.6f' % (rc[neg[0]], float(rc[neg[0]])) if neg else '-'))
    for k in neg[:8]:
        P('    NEG %s %s rc %s = %.6f  rows: %s' % (fam, k, rc[k], float(rc[k]), TOUCH[(fam, k)][:8]))
lg = lg_price(); negL = [x for x in lg if x[0] < 0]
P('LG     %6d %6d   (mask source: %s %s %s)' % (len(lg), len(negL), MASKF or 'none = 31, conservative', MKV if MASKF else '', MKF if MASKF else ''))
for rc, sg, S, gain, cost in negL[:12]:
    P('    NEG LG (U,V,c,a)=%s a2 in %s rc %s = %.6f gain %s cost %s payer rows %s payee rows %s' % (sg, S, rc, float(rc), gain, cost,
      sorted({t for a2 in S for t in TOUCH[('LGq', sg + (a2,))]})[:6], [(t, m) for w, m, t in LGQ.get(sg, [])][:6]))
summary['LG'] = [[str(r), list(s), list(S)] for r, s, S, g_, c_ in negL]
json.dump(summary, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), os.environ.get('OUTJSON', 'rc32.json')), 'w'), indent=0)
pass
# ---------------------------------------------------------------- per-target-row view: every candidate column touching it
P('\nper receiver row: candidate columns with a nonzero coefficient there (rc, coefficient)')
RCALL = {}
for fam in ('YR', 'Z', 'ZR', 'RR', 'O5', 'O5F', 'D', 'O'):
    for k, v in FAM[fam].items(): RCALL[(fam, k)] = -v / tco
for kind, w, data in rows:
    if kind != 'R': continue
    tg = rtag(*data); hits = []
    for (fam, k), rc in RCALL.items():
        cs = [t for t in TOUCH[(fam, k)] if t.startswith(tg + ' ')]
        if cs: hits.append((rc, fam, k, cs[0].split(' ')[2]))
    P('  %s dual %.5f: %s' % (tg, float(w), sorted(hits)[:10]))
P('\nLG signatures (U payer, V payee, c, a): best composite')
for rc, sg, S, gain, cost in lg:
    P('  %s S=%s rc %s gain %s cost %s' % (sg, S, rc, gain, cost))
P('LG payer keys:', {k: str(v) for k, v in LGq.items()})
P('LG payee sigs:', {k: [(float(w), m, t) for w, m, t in v] for k, v in LGQ.items()})
pass

# ---------------------------------------------------------------- VG: big u -> adjacent 6 -> relayed by the 6's h (v6 generalised to U = 7, 8, 9)
# key at the 6 (cons2 row, L[j] >= 7): vkey(L from j, s_j, s_{j-1}); payer receiver row: signature (U, w_{j+1}, s_j, s_{j-1}, w_{j-1},
# w_{j+2}, w_{j-2}, private mask) pays V(sig) <= min over allowed privates p of v(vkey((U, w_{j+1}, s_j, p, s_{j-1}, w_{j-1}), w_{j+2}, w_{j-2})).
def vkey(m, ar, al):
    a = tuple(m) + (ap(ar), ap(al)); b = (m[0],) + tuple(reversed(m[1:])) + (ap(al), ap(ar)); return min(a, b)
VC = collections.defaultdict(Fraction); VSIG = collections.defaultdict(Fraction); VKEYS = {}
for kind, w, data in rows:
    if kind == 'C':
        L, s_ = data
        for j in range(6):
            if L[j] >= 7: VC[vkey(tuple(L[(j + i) % 6] for i in range(6)), s_[j], s_[(j - 1) % 6])] += -w   # rc numerator of v: -w * (+1)
    elif kind == 'R':
        d, wl, sl = data; U = cap9(d)
        for j in range(d):
            if wl[j] != 6: continue
            W_ = lambda k: wl[k % d]; S_ = lambda k: sl[k % d]
            am = amask(U, W_(j - 2), W_(j - 1), W_(j + 1), W_(j + 2), S_(j - 2), S_(j - 1), S_(j), S_(j + 1))
            sg = (U, W_(j + 1), S_(j), S_(j - 1), W_(j - 1), W_(j + 2), W_(j - 2), am)
            ks = frozenset(vkey((U, W_(j + 1), S_(j), p, S_(j - 1), W_(j - 1)), W_(j + 2), W_(j - 2)) for p in LET
                           if (am >> LI[p]) & 1 and not isR6((U, W_(j + 1), S_(j), p, S_(j - 1), W_(j - 1))))
            if not ks: continue
            VKEYS[sg] = ks; VSIG[sg] += w                    # rc numerator of V: -w * (-1) = w  (<= 0)
            TOUCH[('VG', sg)].append(rtag(d, wl, sl))
negv = sorted((k for k in VC if VC[k] < 0), key=lambda k: VC[k])
P('\nVG: %d v keys in cert cons2 rows; v alone with rc < 0 (should be none): %s' % (len(VC), [(k, VC[k] / tco) for k in negv[:5]]))
def vg_rc(sigs):
    K = set().union(*[VKEYS[s] for s in sigs])
    cost = sum(VC.get(k, Fraction(0)) for k in K); gain = sum(VSIG[s] for s in VKEYS if VKEYS[s] <= K)
    return (cost + gain) / tco, cost, gain
sl_ = sorted(VKEYS); res = []
for s in sl_: res.append((vg_rc([s]), (s,)))
for a, b in itertools.combinations(sl_, 2): res.append((vg_rc([a, b]), (a, b)))
res.sort(key=lambda x: x[0][0])
P('VG: %d payer signatures in cert receiver rows; singles + pairs priced; min rc %s' % (len(sl_), res[0][0][0] if res else None))
for (rc, cost, gain), ss in res[:10]:
    P('   VG %s rc %s = %.6f cost %s gain %s rows %s' % (ss, rc, float(rc), cost, gain, [TOUCH[('VG', s)][:3] for s in ss]))
OUT.close()
