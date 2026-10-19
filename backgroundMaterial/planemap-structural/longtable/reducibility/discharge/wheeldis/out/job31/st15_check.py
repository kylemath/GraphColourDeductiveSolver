"""Stage 15 check ("s16 mode" = s12r mode + v6; RELAY_SPEC section 13, d3bc1f93), extending s12r_check.py from the
spec alone (no prelay2.py, pcheck.py, cmd_st15.sh, snap/st15 or cons2basis_v6.json). Section 13 additions:
- cv(l) = l if l < 7 else 7; v (6 -> 7 pass-on, 8-tuple, the h2 shape with cv) in cons2 at every L_j = 7;
- receivers of letter U = 7 (d = 7) subtract V[sigV] at each link 6 with candV nonempty; mrowV rows V - v[k] <= 0;
- V is not stored: it is rebuilt as min over candV of v (the largest value the mrowV rows allow; V enters receivers
  with a minus sign). This mirrors spec 7.1's M = max over cand of h.
Receivers d = 7..15: Studio sep3r_ak on the relaxation y6b[k6] := max over ap pairs of h2(k6), minus, for k6 rooted
at a 7, Vlow(k6) = min over the private and the cv apex pairs of v. Its six window is then >= M[sig2] - V[sigV]; every
reported arrangement is re-evaluated exactly with the spec row.
Cons2 runs over all 1,424 non-R6 6-words x 3^6 cv class words (every 5^6 apex word maps to one of them).
Usage: CAP=3000000 EXPECT_T=<t*> EXPECT_PAT=15550,1568,158 WLP3X_DEF=1 WLP_SEPF=1 python3 out/job31/st15_check.py SOL CERT ARGSFILE"""
import sys, os, json, re, itertools, collections, random
from fractions import Fraction as Fr
HERE = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
DIS = os.path.dirname(HERE)
SOLF, CERTF, ARGF = sys.argv[1], sys.argv[2], sys.argv[3]
SOL = json.load(open(SOLF)); CERT = json.load(open(CERTF)); ARGS = open(ARGF).read().split()
EPS = 1e-9; FAIL = []
# per-solve expectations (defaults: s14r): EXPECT_T = claimed t* as a fraction, EXPECT_PAT = 'D,C,RPAT' distinct pattern counts
EXPECT_T = Fr(os.environ.get('EXPECT_T', '19/102')); EXPECT_PAT = tuple(int(v) for v in os.environ.get('EXPECT_PAT', '15497,1494,158').split(','))
def fail(msg): FAIL.append(msg); print('FAIL: ' + msg, flush=True)
LET = (5, 6, 7, 8, 9); LI = {l: l - 5 for l in LET}
def c(l): return 1 if l >= 7 else 0
CLS2 = {0: (5, 6), 1: (7, 8, 9)}

# ================= spec 4.4: reducible sets =================
def canon(w):
    w = tuple(w); n = len(w); rots = [w[k:] + w[:k] for k in range(n)]; r = w[::-1]
    return min(rots + [r[k:] + r[:k] for k in range(n)])
UNC = {'565667', '565676', '565677', '565757', '565767', '565777'}
R5, R6 = set(), set()
for line in open(os.path.join(DIS, 'studio17', 'wheels17_verdicts.txt')):
    f = line.split()
    if not f or f[0].startswith('#'): continue
    fam, word = f[0].split('_', 1); v = f[2]
    if v == 'D' or (v == 'C' and word not in UNC):
        (R5 if fam == 'c5' else R6).add(canon(tuple(int(ch) for ch in word)))
FANS = []
for line in open(os.path.join(HERE, 'out', 'fans_dfast.out')):
    if 'D=true' in line:
        nm = line.split()[0].split('_', 1)[1]; FANS.append(tuple(None if ch == 'F' else int(ch) for ch in nm))
def fanmatch(w, p):
    n = len(w)
    for r in range(n):
        for refl in (False, True):
            if all(pc is None or pc == (w[(r - i) % n] if refl else w[(r + i) % n]) for i, pc in enumerate(p)): return True
    return False
def isR5(w): return canon(w) in R5 or any(fanmatch(tuple(w), p) for p in FANS)
def isR6(w):
    w = tuple(w); return canon(w) in R6 or any(w[i] == w[(i + 1) % 6] == w[(i + 2) % 6] == 5 for i in range(6))
RBIG = set()
for line in open(os.path.join(HERE, 'out', 'bigwheels_dfast.out')):
    if 'D=true' in line: RBIG.add(canon(tuple(int(ch) for ch in line.split()[0].split('_')[1])))
import glob
for fn in [os.path.join(HERE, 'out', 'bigwheels1516_dfast_partial.out')] + glob.glob(os.path.join(HERE, 'out', 'def_*.out')):
    for line in open(fn):
        f = line.split()
        if f and re.match(r'^c[78]_\d+$', f[0]) and 'D=true' in line: RBIG.add(canon(tuple(int(ch) for ch in f[0][3:])))
for fn in glob.glob(os.path.join(HERE, 'out', 'def_*.cfast')):
    cur = None
    for line in open(fn):
        if ' r=' in line and not line.startswith(' '):
            m = re.match(r'^(?:c7_|\S*_w7_\d+_)(\d{7}) ', line); cur = m.group(1) if m else None
        elif 'C-REDUCIBLE' in line and cur: RBIG.add(canon(tuple(int(ch) for ch in cur)))
SPEC_R5 = '55555 55556 55557 55558 55566 55567 55568 55577 55578 55588 55656 55657 55658 55666 56566 56567 56568 56577 56578 56588 56657 56658 56666 66666'.split()
SPEC_R6 = ('555555 555556 555557 555566 555567 555577 555656 555657 555666 555667 555676 555677 555757 555767 555777 556556 '
           '556557 556566 556567 556576 556577 556657 556666 565656 565657 565666 566566 566567 566577 566657 566666').split()
SPEC_FANS = 'F5565 F5656 F5555 F5665 FF555 F5556 FF565'.split()
s2 = lambda S: {''.join(map(str, w)) for w in S}
print('R5 %d (spec 24, same set: %s); R6 %d (spec 31, same: %s); FANS %d (spec 7, same: %s); RBIG %d (spec 104)' % (
    len(R5), s2(R5) == set(SPEC_R5), len(R6), s2(R6) == set(SPEC_R6), len(FANS),
    {''.join('F' if x is None else str(x) for x in p) for p in FANS} == set(SPEC_FANS), len(RBIG)), flush=True)
if s2(R5) != set(SPEC_R5) or s2(R6) != set(SPEC_R6) or len(FANS) != 7 or len(RBIG) != 104: fail('reducible sets differ from spec 4.4')

# ================= spec 2 / 12.1-12.2: keys =================
def root5(a):
    a = tuple(a); return min(a, (a[0], a[4], a[3], a[2], a[1]))
def rootw(w, j): return root5(tuple(w[(j + k) % 5] for k in range(5)))
def ap(l): return 7 if l >= 7 else 5
def kh_of(L, j):
    a = tuple(L[(j + k) % 6] for k in range(6)); return min(a, (a[0], a[5], a[4], a[3], a[2], a[1]))
def h2_of(m, ar, al):
    """h2 of a 6 with link m rooted at the big m0; ar = apex beyond edge (m0, m1), al = apex beyond (m5, m0)."""
    m = tuple(m); return min(m + (ap(ar), ap(al)), (m[0], m[5], m[4], m[3], m[2], m[1]) + (ap(al), ap(ar)))
def g2_raw(n1, c2, c3, c4, n5, ar, al):
    """g2 from letters n1, n5, classes c2..c4 and apex classes (already ap-ed)."""
    a = (n1, c2, c3, c4, n5, ar, al); b = (n5, c4, c3, c2, n1, al, ar); return min(a, b)
def sig2_of(U, wr, sr, sl, wl, ar, al): return min((U, wr, sr, sl, wl, ar, al), (U, wl, sl, sr, wr, al, ar))
def cand2(sig):
    U, wr, sr, sl, wl, ar, al = sig
    return {h2_of((U, wr, sr, p, sl, wl), ar, al) for p in LET if not isR6((U, wr, sr, p, sl, wl))}
def side(cc, a, b): return LI[cc] * 25 + LI[a] * 5 + LI[b]
def tau(fl, tl, s1, s2_): return (((LI[fl] - 2) * 3 + (LI[tl] - 2)) * 125 + min(s1, s2_)) * 125 + max(s1, s2_)
# apex classes enter only through ap(): the witnesses 5 and 7 stand for them (ap(5) = 5, ap(7) = 7)
AP = (5, 7)
# ---- section 13.1: cv, v, sigV, candV ----
def cv(l): return l if l < 7 else 7
CV = (5, 6, 7)
def v_of(m, ar, al):
    m = tuple(m); return min(m + (cv(ar), cv(al)), (m[0], m[5], m[4], m[3], m[2], m[1]) + (cv(al), cv(ar)))
def sigV_of(U, wr, sr, sl, wl, ar, al): return min((U, wr, sr, sl, wl, ar, al), (U, wl, sl, sr, wr, al, ar))
def candV(sig):
    U, wr, sr, sl, wl, ar, al = sig
    return {v_of((U, wr, sr, p, sl, wl), ar, al) for p in LET if not isR6((U, wr, sr, p, sl, wl))}

# ================= solution values =================
Y = {}
for k, v in SOL['y'].items():
    u, rest = k.split('|'); Y[(int(u),) + tuple(int(ch) for ch in rest)] = v
G = {tuple(k): v for k, v in SOL['g']}; H = {tuple(k): v for k, v in SOL['h']}; X = {int(k): v for k, v in SOL['x'].items()}
VV = {tuple(k): v for k, v in SOL.get('v', [])}
T = SOL['t']
print('solution t = %.15f (claimed %s = %.15f), model %s apex %s apexcls %s zh %s: %d y, %d g, %d h, %d x, z %s' % (
    T, EXPECT_T, float(EXPECT_T), SOL.get('model'), SOL.get('apex'), SOL.get('apexcls'), SOL.get('zh'), len(Y), len(G), len(H), len(X), SOL.get('z')), flush=True)
if SOL.get('model') != 'R6x2' or not SOL.get('apexcls') or SOL.get('zh') or not SOL.get('v6'): fail('solution is not s16 mode (model/apexcls/zh/v6)')
print('v values %d' % len(VV))
if abs(T - float(EXPECT_T)) > 1e-12: fail('solution t differs from the claimed value')
badlen = [k for k in G if len(k) != 7] + [k for k in H if len(k) != 8] + [k for k in VV if len(k) != 8]
if badlen: fail('%d g/h keys of the wrong length' % len(badlen))
neg = [v for v in list(Y.values()) + list(G.values()) + list(H.values()) + list(X.values()) + list(VV.values()) if v < 0]
xmax = max(X.values()) if X else 0.0
print('bounds: %d negative values; max x = %.6f (cap 3)' % (len(neg), xmax))
if neg or xmax > 3 + EPS: fail('bounds')
def Mval(sig): return max([H.get(k, 0.0) for k in cand2(sig)] + [0.0])
def Vval(sig): return min([VV.get(k, 0.0) for k in candV(sig)])
def val(key):
    if key[0] == 'y': return Y.get(key[1], 0.0)
    if key[0] == 'g': return G.get(key[1], 0.0)
    if key[0] == 'h': return H.get(key[1], 0.0)
    if key[0] == 'M': return Mval(key[1])
    if key[0] == 'v': return VV.get(key[1], 0.0)
    if key[0] == 'V': return Vval(key[1])
    if key[0] == 'x': return X.get(key[1], 0.0)
    raise KeyError(key)

# ================= 12.3: senderR2 =================
W5 = sorted({canon(w) for w in itertools.product(LET, repeat=5)})
SENDERS = [w for w in W5 if not isR5(w) and max(w) >= 7]
print('sender words %d (spec 342)' % len(SENDERS))
if len(SENDERS) != 342: fail('sender count')
def sender_row(w, H_, F_):
    sixes = [k for k in range(5) if w[k] == 6]
    for k in sixes:
        if not any(not isR6((5, w[(k + 1) % 5], a, q, b, w[(k - 1) % 5]))
                   for a in CLS2[H_[k]] for q in CLS2[F_[k]] for b in CLS2[H_[(k - 1) % 5]]): return None
    r = collections.Counter()
    for j in range(5):
        if w[j] >= 7: r[('y', rootw(w, j))] += 1
    for k in sixes:
        r[('g', g2_raw(w[(k + 1) % 5], H_[k], F_[k], H_[(k - 1) % 5], w[(k - 1) % 5], ap(w[(k + 2) % 5]), ap(w[(k - 2) % 5])))] += 1
    return r
nrows = nbad = 0; worst = 1e9; GSEND = set()
for w in SENDERS:
    sixes = [k for k in range(5) if w[k] == 6]; hats = sorted({m for k in sixes for m in (k, (k - 1) % 5)})
    seen = set()
    for hb in itertools.product((0, 1), repeat=len(hats)):
        for fb in itertools.product((0, 1), repeat=len(sixes)):
            H_ = dict(zip(hats, hb)); F_ = dict(zip(sixes, fb)); r = sender_row(w, H_, F_)
            if r is None: continue
            key = tuple(sorted(r.items()))
            if key in seen: continue
            seen.add(key); nrows += 1; GSEND.update(k[1] for k in r if k[0] == 'g')
            v = sum(cf * val(k) for k, cf in r.items()); worst = min(worst, v - (1 - T))
            if v < 1 - T - EPS: nbad += 1; nbad <= 5 and print('VIOLATED senderR2 %s H%s F%s: %.12f < %.12f' % (''.join(map(str, w)), H_, F_, v, 1 - T))
print('senderR2 rows %d (spec 7,074), violated %d, min slack %.3g; g2 keys in sender rows %d (spec 393)' % (nrows, nbad, worst, len(GSEND)), flush=True)
if nbad: fail('senderR2 violated')
if nrows != 7074: fail('senderR2 row count differs from spec 12.3')
if len(GSEND) != 393: print('WARN: %d g2 keys in sender rows, spec 12.3 says 393 (a descriptive count: neither a violation nor a rebuild mismatch; see README ambiguities)' % len(GSEND))

# ================= 12.4 / 12.7.2: cons2 over all non-R6 6-words x all apex class words =================
def cons2_row(L, s):
    r = collections.Counter()
    for i in range(6):
        if L[i] == 5:
            r[('g', g2_raw(L[(i + 1) % 6], c(L[(i + 2) % 6]), c(L[(i + 3) % 6]), c(L[(i + 4) % 6]), L[(i + 5) % 6], ap(s[i]), ap(s[(i - 1) % 6])))] += 1
        elif L[i] >= 7:
            m = tuple(L[(i + k) % 6] for k in range(6)); r[('h', h2_of(m, s[i], s[(i - 1) % 6]))] -= 1
            if L[i] == 7: r[('v', v_of(m, s[i], s[(i - 1) % 6]))] += 1
    return {k: v for k, v in r.items() if v != 0}
ALL6 = sorted({canon(L) for L in itertools.product(LET, repeat=6) if not isR6(L)})
cres = {'five': [0, 0, 0.0], 'nofive': [0, 0, 0.0]}
for L in ALL6:
    sub = 'five' if 5 in L else 'nofive'; cres[sub][0] += 1
    for s in itertools.product(CV, repeat=6):
        v = sum(cf * val(k) for k, cf in cons2_row(L, s).items())
        cres[sub][2] = max(cres[sub][2], abs(v))
        if abs(v) > 1e-9: cres[sub][1] += 1; cres[sub][1] <= 5 and print('VIOLATED cons2 %s s %s: %.3g' % (''.join(map(str, L)), ''.join(map(str, s)), v))
print('cons2: %d non-R6 6-words (spec 1,424) x 729 cv class words (= all 5^6 apex words through cv and ap)' % len(ALL6))
for sub in ('five', 'nofive'):
    print('  %-7s %d words (%s): violated %d, max |sum g2 - sum h2| %.3g' % (sub, cres[sub][0], 'spec 994' if sub == 'five' else 'spec 430', cres[sub][1], cres[sub][2]), flush=True)
if len(ALL6) != 1424 or cres['five'][0] != 994: fail('6-word counts')
if cres['five'][1] or cres['nofive'][1]: fail('cons2 violated')
hcan = [k for k in H if k != min(k, (k[0], k[5], k[4], k[3], k[2], k[1], k[7], k[6]))]
gcan = [k for k in G if k != g2_raw(*k)]
if hcan or gcan: fail('%d h2 / %d g2 solution keys not canonical' % (len(hcan), len(gcan)))

# ================= spec 4.5: pattern loader and matcher =================
CH = {'.': None, '5': {5}, '6': {6}, '7': {7}, '8': {8}, 'B': {7, 8, 9}}
odd = collections.Counter()
def parse_name(nm):
    f = nm.split('_'); K, d = f[0][0], int(f[0][1:]); lk, sw = f[1], f[2]; P = []
    for kind, word in (('w', lk), ('s', sw)):
        for i, ch in enumerate(word):
            if K == 'p' and ((kind == 'w' and ch == '9') or (kind == 's' and ch == '0')): continue
            if ch not in CH: odd[ch] += 1; S = {int(ch)}   # not in spec 4.5's table; read as the exact letter
            else: S = CH[ch]
            if S is not None: P.append((kind, i, frozenset(S)))
    return d, frozenset(P)
PAT = collections.defaultdict(set); KIND = collections.Counter(); seenp = {'D': set(), 'C': set(), 'R': set()}
for a in ARGS:
    if a.startswith(('pat=', 'cpat=')):
        fn = a.split('=', 1)[1]; allf = fn.endswith(':all'); fn = fn[:-4] if allf else fn
        p = fn if os.path.isabs(fn) else os.path.join(HERE, fn)
        if not os.path.exists(p): print('missing pattern file (skipped as in the run): %s' % fn); continue
        lines = open(p).read().splitlines()
        if a.startswith('pat='):
            names = [l.split()[0] for l in lines if l.strip() and (allf or 'D=true' in l)]; kind = 'D'
        else:
            names = []; kind = 'C'
            for k, l in enumerate(lines):
                if ' r=' in l and not l.startswith(' '):
                    for l2 in lines[k + 1:]:
                        if ' r=' in l2 and not l2.startswith(' '): break
                        if 'C-REDUCIBLE' in l2: names.append(l.split()[0]); break
        for nm in names:
            if not re.match(r'^[epf]\d+_', nm): continue
            d, P = parse_name(nm)
            if (d, P) not in seenp[kind]: seenp[kind].add((d, P)); KIND[kind] += 1
            PAT[d].add(P)
    elif a.startswith('rpat='):
        fn = a[5:]; p = fn if os.path.isabs(fn) else os.path.join(HERE, fn)
        for line in open(p):
            f = line.split('#')[0].split()
            if not f: continue
            d, k = int(f[0]), int(f[1]); slots = {}
            for e in range(k):
                i, m = int(f[2 + 2 * e]), int(f[3 + 2 * e])
                for sl, S in ((('w', i), {5}),) + tuple(((nm_, (ix_ % d)), {LET[b] for b in range(5) if (m >> (5 * t_)) >> b & 1})
                                                        for t_, (nm_, ix_) in enumerate((('w', i + 1), ('s', i), ('s', i - 1), ('w', i - 1)))):
                    slots[sl] = slots.get(sl, set(LET)) & S
            P = frozenset((kd, ix_, frozenset(S)) for (kd, ix_), S in slots.items() if S != set(LET))
            if (d, P) not in seenp['R']: seenp['R'].add((d, P)); KIND['R'] += 1
            PAT[d].add(P)
byd = {d: len(v) for d, v in sorted(PAT.items())}
print('patterns distinct by kind: D %d (spec 15,497), C %d (spec 1,494), RPAT %d (spec 158); by d %s; chars outside the spec table %s'
      % (KIND['D'], KIND['C'], KIND['R'], byd, dict(odd)), flush=True)
if (KIND['D'], KIND['C'], KIND['R']) != EXPECT_PAT: fail('pattern counts %s differ from expected %s' % ((KIND['D'], KIND['C'], KIND['R']), EXPECT_PAT))
PATL = {d: [tuple(P) for P in v] for d, v in PAT.items()}
def patmatch(d, w, s):
    for P in PATL.get(d, ()):
        for r in range(d):
            for refl in (False, True):
                ok = True
                for kd, i, S in P:
                    if kd == 'w': x_ = w[(r - i) % d] if refl else w[(i + r) % d]
                    else: x_ = s[(r - i - 1) % d] if refl else s[(i + r) % d]
                    if x_ not in S: ok = False; break
                if ok: return True
    return False
def admissible(d, w, s):
    U = min(d, 9)
    for i in range(d):
        if w[i] == 5 and isR5((U, w[(i + 1) % d], s[i], s[(i - 1) % d], w[(i - 1) % d])): return False
        if w[i] == 6 and all(isR6((U, w[(i + 1) % d], s[i], p, s[(i - 1) % d], w[(i - 1) % d])) for p in LET): return False
    if d in (7, 8) and canon(w) in RBIG: return False
    return not patmatch(d, w, s)

# ================= 12.5: receiverR2 rows =================
def recv_spec(d, link, sword):
    U = min(d, 9); w = [int(ch) for ch in link]; s = [int(ch) for ch in sword]; r = collections.Counter()
    W = lambda k: w[k % d]; S = lambda k: s[k % d]
    for i in range(d):
        if w[i] == 5: r[('y', root5((U, W(i + 1), S(i), S(i - 1), W(i - 1))))] += 1
        elif w[i] == 6:
            sg = sig2_of(U, W(i + 1), S(i), S(i - 1), W(i - 1), ap(W(i + 2)), ap(W(i - 2)))
            if cand2(sg): r[('M', sg)] += 1
            if U == 7:
                sv_ = sigV_of(U, W(i + 1), S(i), S(i - 1), W(i - 1), cv(W(i + 2)), cv(W(i - 2)))
                if candV(sv_): r[('V', sv_)] -= 1
        else:
            ti = tau(w[i], U, side(W(i - 1), S(i - 1), W(i - 2)), side(W(i + 1), S(i), W(i + 2)))
            to = tau(U, w[i], side(W(i - 1), W(i - 2), S(i - 1)), side(W(i + 1), W(i + 2), S(i)))
            r[('x', ti)] += 1; r[('x', to)] -= 1
    return {k: v for k, v in r.items() if v != 0}
def spec_val(d, lk, sv): return sum(cf * val(k) for k, cf in recv_spec(d, lk, sv).items())

# ================= 12.8: exact lower check =================
tot = collections.defaultdict(Fr); tco = Fr(0); Dn = Fr(0); nlab = collections.Counter(); noncanon = []
for e in CERT:
    w = Fr(e['w']).limit_denominator(10 ** 7); lab = e['row']; kind = lab[0]; nlab[kind] += 1
    if kind == 'senderR2':
        word = tuple(int(ch) for ch in lab[1]); bits = lab[2]; cut = bits.index('|')
        sixes = [k for k in range(5) if word[k] == 6]; hats = sorted({m for k in sixes for m in (k, (k - 1) % 5)})
        if word not in SENDERS or len(bits[:cut]) != len(hats) or len(bits[cut + 1:]) != len(sixes): fail('bad senderR2 label %s' % lab); continue
        r = sender_row(word, dict(zip(hats, bits[:cut])), dict(zip(sixes, bits[cut + 1:])))
        if r is None: fail('senderR2 assignment inadmissible %s' % lab); continue
        if w < 0: fail('senderR2 weight < 0 %s' % lab)
        tco += w; Dn += w
    elif kind == 'receiverR2':
        d, lk, sv = lab[1], lab[2], lab[3]
        if not admissible(d, [int(ch) for ch in lk], [int(ch) for ch in sv]): fail('receiverR2 label not admissible %s' % lab)
        r = recv_spec(d, lk, sv)
        if w > 0: fail('receiverR2 weight > 0 %s' % lab)
        tco -= w; Dn += w * (d - 6)
    elif kind == 'cons2':
        L, s = tuple(lab[1]), tuple(lab[2])
        if isR6(L) or not all(x in LET for x in L + s): fail('cons2 label not admissible %s' % lab)
        r = cons2_row(L, s)
    elif kind == 'mrowR2':
        sg, hk = tuple(lab[1]), tuple(lab[2])
        if sg != sig2_of(*sg): noncanon.append(lab)
        if hk not in cand2(sg): fail('mrowR2 key not in cand2 (stored orientation) %s' % lab)
        r = {('h', hk): 1, ('M', sg): -1}
        if w > 0: fail('mrowR2 weight > 0 %s' % lab)
    elif kind == 'mrowV':
        sg, vk = tuple(lab[1]), tuple(lab[2])
        if sg != sigV_of(*sg): noncanon.append(lab)
        if vk not in candV(sg): fail('mrowV key not in candV %s' % lab)
        r = {('V', sg): 1, ('v', vk): -1}
        if w > 0: fail('mrowV weight > 0 %s' % lab)
    else:
        fail('unknown label %s' % lab); continue
    for k, cf in r.items(): tot[k] += w * cf
print('cert rows %d: %s; mrowR2/mrowV not in canonical orientation: %d %s' % (len(CERT), dict(nlab), len(noncanon), noncanon[:3]))
if noncanon: fail('%d mrowR2/mrowV rows not in canonical orientation' % len(noncanon))
if tco <= 0: fail('t coefficient %s <= 0' % tco)
D = Dn / tco; rc = {k: -v / tco for k, v in tot.items() if v != 0}
for k, v in list(rc.items()):
    if k[0] == 'x' and v < 0: D += v * 3
negrc = {k: v for k, v in rc.items() if k[0] != 'x' and v < 0}
print('lower: tco = %s, D = %s; nonzero reduced costs: %s; negative (non-x) %d' % (
    tco, D, ', '.join('%s[%s] = %s' % (k[0], ''.join(map(str, k[1])) if isinstance(k[1], tuple) else k[1], v) for k, v in sorted(rc.items(), key=str)), len(negrc)))
if negrc: fail('negative reduced costs %s' % negrc)
if D != EXPECT_T: fail('lower bound %s != claimed %s' % (D, EXPECT_T))
elif negrc: print('LOWER: NOT ESTABLISHED (D = %s but negative reduced costs)' % D)
else: print('LOWER: VALID t >= %s' % D)

# ================= receivers: Studio sep3r on the apex relaxation, exact re-check of what it reports =================
os.environ['SEP_NODELIMIT'] = '0'
src = open(os.path.join(HERE, 'wlp3r6.py')).read().replace('os.path.abspath(__file__)', repr(os.path.join(HERE, 'wlp3r6.py')), 1)
sys.argv = ['wlp3r6', 'tag=s12rchk'] + ARGS
NS_ = {'__name__': 'studio_wlp3r6'}
exec(src[:src.index('DS, DSF = list(range(7, 13))')], NS_)
import numpy as np
NY, ix, V56, V6B, I6B, recv_row, sepx, check, dp9, DMAXP = (NS_[k] for k in ('NY', 'ix', 'V56', 'V6B', 'I6B', 'recv_row', 'sepx', 'check', 'dp9', 'DMAXP'))
NS, TRI, states, BIGSTATE, best6, SEPX = (NS_[k] for k in ('NS', 'TRI', 'states', 'BIGSTATE', 'best6', 'SEPX'))
# results keyed by arrangement (bin/sep3r_ak, SEP_ARRKEY=1): under the apex relaxation two arrangements with one Studio
# row can differ in their exact value, so sep3r's row-keyed dedupe could hide an exact violator
SEPX.stdin.close(); SEPX.wait()
import subprocess as _sp
SEPX = _sp.Popen([os.path.join(HERE, 'bin', 'sep3r_ak'), NS_['SF']], stdin=_sp.PIPE, stdout=_sp.PIPE, text=True,
                 env=dict(os.environ, SEP_NODELIMIT='0', SEP_ARRKEY='1'))
NS_['SEPX'] = SEPX
yv = np.zeros(NY)
for k, v in Y.items(): yv[ix[k]] = v
V56[:] = 0.0; V6B[:] = 0.0
def Vlow(k6):   # the least v over the private and the cv apex pairs, for the 5-signature of this rooted 6-link
    U, a1, b1, _, d1, e1 = k6
    if U != 7: return 0.0
    lst = [VV.get(v_of((U, a1, b1, p, d1, e1), ar, al), 0.0) for p in LET if not isR6((U, a1, b1, p, d1, e1)) for ar in CV for al in CV]
    return min(lst) if lst else 0.0
for k6, i6 in I6B.items():   # relaxation: the largest h2 over the apex pairs, minus (at a 7) the least possible V
    V6B[i6] = max(H.get(h2_of(k6, a, b), 0.0) for a in AP for b in AP) - Vlow(k6)
xv = dict(X)
def studio_val(d, lk, sv):
    r_ = recv_row(d, lk, sv)
    return sum(cf * (yv[k[1]] if k[0] == 'y' else xv.get(k[1], 0.0) if k[0] == 'x' else V6B[k[1]] if k[0] == 'y6b' else 0.0) for k, cf in r_.items() if k[0] != 't')
def xk(rr): return collections.Counter({k[1]: cf for k, cf in rr.items() if k[0] == 'x'})
tests = [(e['row'][1], e['row'][2], e['row'][3]) for e in CERT if e['row'][0] == 'receiverR2']
for d in range(7, 16): tests += [(d, lk, sv) for _, lk, sv in sepx(d, yv, xv, -1e9, 20)]
random.seed(7)
for d in (7, 8, 9, 10):
    for _ in range(150): tests.append((d, ''.join(random.choice('5666777889') for _ in range(d)), ''.join(random.choice('5566677889') for _ in range(d))))
adm_bad = low = xbad = ncmp = 0
for d, lk, sv in tests:
    a1 = admissible(d, [int(ch) for ch in lk], [int(ch) for ch in sv]); a2 = check(d, lk, sv)
    if a1 != a2: adm_bad += 1; adm_bad <= 5 and print('ADMISSIBILITY MISMATCH d=%d %s %s spec %s studio %s' % (d, lk, sv, a1, a2))
    if a1 and a2:
        ncmp += 1; v1, v2 = spec_val(d, lk, sv), studio_val(d, lk, sv)
        if v2 < v1 - 1e-12: low += 1; low <= 5 and print('RELAXATION BELOW EXACT d=%d %s %s spec %.12f studio %.12f' % (d, lk, sv, v1, v2))
        if xk(recv_spec(d, lk, sv)) != xk(recv_row(d, lk, sv)): xbad += 1
print('spec rows vs Studio relaxed rows: %d arrangements, admissibility mismatches %d; %d compared: relaxed below exact %d, x-key mismatches %d'
      % (len(tests), adm_bad, ncmp, low, xbad), flush=True)
if adm_bad or low or xbad: fail('Studio relaxed receiver rows are not an upper bound on the spec rows')
rbad = 0; CAP = int(os.environ.get('CAP', '5000')); import time as _tm
for d in range(7, DMAXP + 1):
    _t0 = _tm.time(); out = sepx(d, yv, xv, d - 6 + T + EPS, CAP)
    exact_bad = [(spec_val(d, lk, sv), lk, sv) for _, lk, sv in out if spec_val(d, lk, sv) > d - 6 + T + EPS]
    for v_, lk, sv in exact_bad[:5]: print('VIOLATED receiverR2 d=%d exact load %.12f link %s s %s' % (d, v_, lk, sv))
    full = len(out) < CAP
    if not full: fail('d=%d: relaxation reports >= %d arrangements; exact check incomplete' % (d, CAP))
    rbad += len(exact_bad)
    print('receivers d=%d: relaxation reports %d above threshold%s; exact violated %d (%.0fs)' % (d, len(out), '' if full else ' (CAP hit)', len(exact_bad), _tm.time() - _t0), flush=True)
z9 = max([v for tq, v in X.items() if (tq // 15625) % 3 == 2] + [0.0])
for d in range(DMAXP + 1, 31):
    out = dp9(d, yv, z9, d - 6 + T + EPS, 5)
    if out: rbad += len(out); print('DP d=%d relaxed bound %.12f > %.12f (not decided)' % (d, out[0][0], d - 6 + T))
print('DP d=%d..30 (apex relaxation, z9 = %.6f): %s' % (DMAXP + 1, z9, 'clean' if not any(True for _ in []) and rbad == 0 else 'see above'))
Mk = np.full((NS, NS), -np.inf)
for a_, b_, rr in TRI[9]:
    (wp, sp, wc), (_, sc, wn) = states[a_], states[b_]
    v_ = (yv[ix[rr]] if rr is not None else 0.0) + z9 * BIGSTATE[a_]
    if wc == 6: v_ += best6(9, wn, sc, sp, wp)[0]
    Mk[a_, b_] = max(Mk[a_, b_], v_)
n_ = NS; Dk = np.full((n_ + 1, n_), -np.inf); Dk[0, :] = 0.0
for k in range(1, n_ + 1): Dk[k] = (Dk[k - 1][:, None] + Mk).max(axis=0)
with np.errstate(invalid='ignore'):
    q = np.where(np.isfinite(Dk[n_]), np.min(np.where(np.isfinite(Dk[:n_]), (Dk[n_] - Dk[:n_]) / (n_ - np.arange(n_))[:, None], np.inf), axis=0), -np.inf)
lam = q.max(); d0 = (6 - T) / (1 - lam) if lam < 1 else float('inf')
print('Karp tail (apex relaxation): lambda = %.9f, covered for d >= %.3f (needs <= 31)' % (lam, d0))
if d0 > 31: rbad += 1
if rbad: fail('receiver side violated or undecided')
SEPX.stdin.close(); SEPX.wait()
print('UPPER: %s' % ('FEASIBLE at t = %.12f' % T if rbad == 0 and not [f for f in FAIL if 'violated' in f or 'bounds' in f or 'incomplete' in f] else 'NOT ESTABLISHED'))
print('VERDICT: %s' % ('PASS (upper FEASIBLE, lower VALID %s)' % EXPECT_T if not FAIL else 'FAIL: ' + ' | '.join(FAIL)))
