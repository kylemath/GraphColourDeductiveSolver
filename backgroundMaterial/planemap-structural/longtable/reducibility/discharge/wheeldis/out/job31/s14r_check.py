"""Standalone check of Opus's relay result s14r (sol_s14r.json / cert_s14r.json, 39f457ba), written by Studio from
P_own_lp/RELAY_SPEC.md (be66f349) alone. No Opus code is read or run.

Spec-side (implemented here from the spec text):
- reducible sets R5, R6, FANS, RBIG (spec 4.4) from the named source files, checked against the spec's listed values;
- sender words and senderR rows with hat/fan flag assignments (spec 3), checked at the solution;
- relay words and cons rows (spec 6); signatures, cand and M = max h (spec 2.5, 5); bounds (spec 7.1);
- receiverR rows rebuilt from labels (spec 4.2) with the x keys of spec 2.2; admissibility (spec 4.4) with a pattern
  loader and matcher written from spec 4.5;
- the exact lower check of spec 8 (Fractions, limit_denominator(10**7), reduced costs, x priced at its cap).
Studio-side (the exhaustive search the spec's own engine does with jsep3): receivers at d = 7..15 by Studio's sep3r
(SEP_NODELIMIT=0), whose window values are y for a five, max over the unseen private of y6b for a 6, and x_in - x_out
for a big. With y6b := h (889/889 keys map one-to-one, map_s14r.log) that is spec 4.2 with M = max h. Before the search
is trusted, the checker compares Studio's receiver rows with the spec rebuild (keys, values and admissibility) on the
4 cert labels, on the heaviest arrangements at each d, and on random arrangements. d = 16..30: Studio's relaxed DP with
z9 := the largest x into a 9 (x_in - x_out <= x_in <= z9), plus the Karp tail.
Usage: WLP3X_DEF=1 WLP_SEPF=1 python3 out/job31/s14r_check.py SOL CERT ARGSFILE"""
import sys, os, json, re, itertools, collections, random
from fractions import Fraction as Fr
HERE = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
DIS = os.path.dirname(HERE)
SOLF, CERTF, ARGF = sys.argv[1], sys.argv[2], sys.argv[3]
SOL = json.load(open(SOLF)); CERT = json.load(open(CERTF)); ARGS = open(ARGF).read().split()
EPS = 1e-9; FAIL = []
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

# ================= spec 2: keys =================
def root5(a):
    a = tuple(a); return min(a, (a[0], a[4], a[3], a[2], a[1]))
def rootw(w, j):
    return root5(tuple(w[(j + k) % 5] for k in range(5)))
def kh_of(L, j):
    a = tuple(L[(j + k) % 6] for k in range(6)); return min(a, (a[0], a[5], a[4], a[3], a[2], a[1]))
def kg_of(n1, n2, n3, n4, n5):
    a = (n1, c(n2), c(n3), c(n4), n5); return min(a, a[::-1])
def sig_of(U, wr, sr, sl, wl): return min((U, wr, sr, sl, wl), (U, wl, sl, sr, wr))
def cand(sig):
    U, wr, sr, sl, wl = sig; return {kh_of((U, wr, sr, p, sl, wl), 0) for p in LET if not isR6((U, wr, sr, p, sl, wl))}
def side(cc, a, b): return LI[cc] * 25 + LI[a] * 5 + LI[b]
def tau(fl, tl, s1, s2_): return (((LI[fl] - 2) * 3 + (LI[tl] - 2)) * 125 + min(s1, s2_)) * 125 + max(s1, s2_)

# ================= solution values =================
Y = {}
for k, v in SOL['y'].items():
    u, rest = k.split('|'); Y[(int(u),) + tuple(int(ch) for ch in rest)] = v
G = {tuple(k): v for k, v in SOL['g']}; H = {tuple(k): v for k, v in SOL['h']}; X = {int(k): v for k, v in SOL['x'].items()}
T = SOL['t']
print('solution t = %.15f (19/102 = %.15f), %d y, %d g, %d h, %d x' % (T, 19 / 102, len(Y), len(G), len(H), len(X)), flush=True)
neg = [v for v in list(Y.values()) + list(G.values()) + list(H.values()) + list(X.values()) if v < 0]
xmax = max(X.values()) if X else 0.0
print('bounds: %d negative values; max x = %.6f (cap 3)' % (len(neg), xmax))
if neg or xmax > 3 + EPS: fail('bounds')

# ================= spec 2.5 / 5: signatures and M =================
SIGS = {}
for U in (7, 8, 9):
    for wr, sr, sl, wl in itertools.product(LET, repeat=4):
        sg = sig_of(U, wr, sr, sl, wl); cd = cand(sg)
        if cd: SIGS[sg] = cd
Mv = {sg: max(H.get(k, 0.0) for k in cd) for sg, cd in SIGS.items()}
HCOLS = set().union(*SIGS.values())
print('signatures %d (spec 975), M rows %d (spec 4,760), h columns from M rows %d' % (len(SIGS), sum(len(v) for v in SIGS.values()), len(HCOLS)))
if len(SIGS) != 975 or sum(len(v) for v in SIGS.values()) != 4760: fail('signature counts')
badh = [k for k in H if k not in HCOLS]
if badh: fail('%d solution h keys are not h columns: %s' % (len(badh), badh[:3]))

# ================= spec 3: senders =================
W5 = sorted({canon(w) for w in itertools.product(LET, repeat=5)})
SENDERS = [w for w in W5 if not isR5(w) and max(w) >= 7]
print('sender words %d (spec 342)' % len(SENDERS))
if len(SENDERS) != 342: fail('sender count')
def sender_row(w, H_, F_):
    """coefficients (Counter over keys) of senderR(w, H, F), or None if the assignment is inadmissible."""
    sixes = [k for k in range(5) if w[k] == 6]
    for k in sixes:
        if not any(not isR6((5, w[(k + 1) % 5], a, q, b, w[(k - 1) % 5]))
                   for a in CLS2[H_[k]] for q in CLS2[F_[k]] for b in CLS2[H_[(k - 1) % 5]]): return None
    r = collections.Counter()
    for j in range(5):
        if w[j] >= 7: r[('y', rootw(w, j))] += 1
    for k in sixes:   # spec 3: a_k = (w_{k+1}, H[k], F[k], H[k-1], w_{k-1}); the bits are already classes
        a_ = (w[(k + 1) % 5], H_[k], F_[k], H_[(k - 1) % 5], w[(k - 1) % 5]); r[('g', min(a_, a_[::-1]))] += 1
    return r
def val(key):
    if key[0] == 'y': return Y.get(key[1], 0.0)
    if key[0] == 'g': return G.get(key[1], 0.0)
    if key[0] == 'h': return H.get(key[1], 0.0)
    if key[0] == 'M': return Mv.get(key[1], 0.0)
    if key[0] == 'x': return X.get(key[1], 0.0)
    raise KeyError(key)
nrows = nbad = 0; worst = 1e9; GCOLS = set()
for w in SENDERS:
    sixes = [k for k in range(5) if w[k] == 6]; hats = sorted({m for k in sixes for m in (k, (k - 1) % 5)})
    seen = set()
    for hb in itertools.product((0, 1), repeat=len(hats)):
        for fb in itertools.product((0, 1), repeat=len(sixes)):
            H_ = dict(zip(hats, hb)); F_ = dict(zip(sixes, fb)); r = sender_row(w, H_, F_)
            if r is None: continue
            key = tuple(sorted(r.items()))
            if key in seen: continue
            seen.add(key); nrows += 1; GCOLS.update(k[1] for k in r if k[0] == 'g')
            v = sum(cf * val(k) for k, cf in r.items()); worst = min(worst, v - (1 - T))
            if v < 1 - T - EPS: nbad += 1; nbad <= 5 and print('VIOLATED senderR %s H%s F%s: %.12f < %.12f' % (''.join(map(str, w)), H_, F_, v, 1 - T))
print('senderR rows %d (spec 6,915), violated %d, min slack %.3g; g columns %d (spec 102)' % (nrows, nbad, worst, len(GCOLS)), flush=True)
if nbad: fail('senderR violated')
if nrows != 6915 or len(GCOLS) != 102: fail('senderR/g counts differ from spec 10')
badg = [k for k in G if k not in GCOLS]
if badg: fail('%d solution g keys are not g columns' % len(badg))

# ================= spec 6: conservation =================
RW = sorted({canon(L) for L in itertools.product(LET, repeat=6) if 5 in L and not isR6(L)})
def cons_row(L):
    r = collections.Counter()
    for i in range(6):
        if L[i] == 5: r[('g', kg_of(*(L[(i + k) % 6] for k in range(1, 6))))] += 1
        elif L[i] >= 7: r[('h', kh_of(L, i))] -= 1
    return r
cbad = 0; cmax = 0.0
for L in RW:
    v = sum(cf * val(k) for k, cf in cons_row(L).items()); cmax = max(cmax, abs(v))
    if abs(v) > 1e-9: cbad += 1; cbad <= 5 and print('VIOLATED cons %s: %.3g' % (''.join(map(str, L)), v))
print('cons rows %d (spec 994), violated %d, max |g - h| %.3g' % (len(RW), cbad, cmax), flush=True)
if cbad: fail('cons violated')
if len(RW) != 994: fail('relay word count')

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
if (KIND['D'], KIND['C'], KIND['R']) != (15497, 1494, 158): fail('pattern counts differ from spec 4.5')
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

# ================= spec 4.2: receiver rows =================
def recv_spec(d, link, sword):
    U = min(d, 9); w = [int(ch) for ch in link]; s = [int(ch) for ch in sword]; r = collections.Counter()
    W = lambda k: w[k % d]; S = lambda k: s[k % d]
    for i in range(d):
        if w[i] == 5: r[('y', root5((U, W(i + 1), S(i), S(i - 1), W(i - 1))))] += 1
        elif w[i] == 6:
            sg = sig_of(U, W(i + 1), S(i), S(i - 1), W(i - 1))
            if sg in SIGS: r[('M', sg)] += 1
        else:
            ti = tau(w[i], U, side(W(i - 1), S(i - 1), W(i - 2)), side(W(i + 1), S(i), W(i + 2)))
            to = tau(U, w[i], side(W(i - 1), W(i - 2), S(i - 1)), side(W(i + 1), W(i + 2), S(i)))
            r[('x', ti)] += 1; r[('x', to)] -= 1
    return {k: v for k, v in r.items() if v != 0}

# ================= spec 8: exact lower check =================
tot = collections.defaultdict(Fr); tco = Fr(0); Dn = Fr(0); nlab = collections.Counter(); lbad = 0
for e in CERT:
    w = Fr(e['w']).limit_denominator(10 ** 7); lab = e['row']; kind = lab[0]; nlab[kind] += 1
    if kind == 'senderR':
        word = tuple(int(ch) for ch in lab[1]); bits = lab[2]; cut = bits.index('|')
        sixes = [k for k in range(5) if word[k] == 6]; hats = sorted({m for k in sixes for m in (k, (k - 1) % 5)})
        if word not in SENDERS or len(bits[:cut]) != len(hats) or len(bits[cut + 1:]) != len(sixes): fail('bad senderR label %s' % lab); lbad += 1; continue
        r = sender_row(word, dict(zip(hats, bits[:cut])), dict(zip(sixes, bits[cut + 1:])))
        if r is None: fail('senderR assignment inadmissible %s' % lab); lbad += 1; continue
        if w < 0: fail('senderR weight < 0'); lbad += 1
        tco += w; Dn += w
    elif kind == 'receiverR':
        d, lk, sv = lab[1], lab[2], lab[3]
        if not admissible(d, [int(ch) for ch in lk], [int(ch) for ch in sv]): fail('receiverR label not admissible %s' % lab); lbad += 1
        r = recv_spec(d, lk, sv)
        if w > 0: fail('receiverR weight > 0'); lbad += 1
        tco -= w; Dn += w * (d - 6)
    elif kind == 'cons':
        L = tuple(lab[1])
        if canon(L) != L or isR6(L): fail('cons label not canonical/non-R6 %s' % lab); lbad += 1
        r = cons_row(L)
    elif kind == 'mrowR':
        sg, hk = tuple(lab[1]), tuple(lab[2]); U, wr, sr, sl, wl = sg
        if hk not in cand(sg) and hk not in cand((U, wl, sl, sr, wr)): fail('mrowR key not in cand %s' % lab); lbad += 1
        if sg not in SIGS: fail('mrowR signature not canonical %s' % lab); lbad += 1
        r = {('h', hk): 1, ('M', sg): -1}
        if w > 0: fail('mrowR weight > 0'); lbad += 1
    else:
        fail('unknown label %s' % lab); lbad += 1; continue
    for k, cf in r.items(): tot[k] += w * cf
print('cert rows %d: %s' % (len(CERT), dict(nlab)))
if tco <= 0: fail('t coefficient %s <= 0' % tco)
D = Dn / tco; rc = {k: -v / tco for k, v in tot.items() if v != 0}
for k, v in list(rc.items()):
    if k[0] == 'x' and v < 0: D += v * 3
negrc = {k: v for k, v in rc.items() if k[0] != 'x' and v < 0}
print('lower: tco = %s, D = %s; nonzero reduced costs %s; negative (non-x) %d' % (
    tco, D, ', '.join('%s%s=%s' % (k[0], ''.join(map(str, k[1])) if isinstance(k[1], tuple) else k[1], v) for k, v in sorted(rc.items(), key=str)), len(negrc)))
for want in (('g', (5, 0, 0, 1, 6)), ('M', (7, 6, 6, 6, 7))):
    print('  residual %s%s: reduced cost %s' % (want[0], ''.join(map(str, want[1])), rc.get(want, Fr(0))))
if negrc: fail('negative reduced costs %s' % negrc)
if D != Fr(19, 102): fail('lower bound %s != 19/102' % D)
else: print('LOWER: VALID t >= %s' % D)

# ================= receivers: Studio sep3r, after checking it against the spec rebuild =================
os.environ['SEP_NODELIMIT'] = '0'
src = open(os.path.join(HERE, 'wlp3r6.py')).read().replace('os.path.abspath(__file__)', repr(os.path.join(HERE, 'wlp3r6.py')), 1)
sys.argv = ['wlp3r6', 'tag=s14rchk'] + ARGS
NS_ = {'__name__': 'studio_wlp3r6'}
exec(src[:src.index('DS, DSF = list(range(7, 13))')], NS_)   # own namespace: the spec-side sets above stay untouched
import numpy as np
NY, ix, V56, V6B, I6B, recv_row, sepx, check, dp9, DMAXP = (NS_[k] for k in ('NY', 'ix', 'V56', 'V6B', 'I6B', 'recv_row', 'sepx', 'check', 'dp9', 'DMAXP'))
NS, TRI, states, BIGSTATE, best6, SEPX = (NS_[k] for k in ('NS', 'TRI', 'states', 'BIGSTATE', 'best6', 'SEPX'))
yv = np.zeros(NY)
for k, v in Y.items(): yv[ix[k]] = v
V56[:] = 0.0; V6B[:] = 0.0
for k, v in H.items(): V6B[I6B[k]] = v
xv = dict(X)
def studio_val(d, lk, sv):
    r_ = recv_row(d, lk, sv)
    return sum(cf * (yv[k[1]] if k[0] == 'y' else xv.get(k[1], 0.0) if k[0] == 'x' else V6B[k[1]] if k[0] == 'y6b' else 0.0) for k, cf in r_.items() if k[0] != 't')
def spec_val(d, lk, sv): return sum(cf * val(k) for k, cf in recv_spec(d, lk, sv).items())
def xkeys_studio(d, lk, sv): return collections.Counter({k[1]: cf for k, cf in recv_row(d, lk, sv).items() if k[0] == 'x'})
def xkeys_spec(d, lk, sv): return collections.Counter({k[1]: cf for k, cf in recv_spec(d, lk, sv).items() if k[0] == 'x'})
cmp_n = cmp_bad = adm_n = adm_bad = 0
tests = [(e['row'][1], e['row'][2], e['row'][3]) for e in CERT if e['row'][0] == 'receiverR']
for d in range(7, 16):
    tests += [(d, lk, sv) for _, lk, sv in sepx(d, yv, xv, -1e9, 20)]
random.seed(7)
rnd = []
for d in (7, 8, 9, 10):
    for _ in range(150):
        rnd.append((d, ''.join(random.choice('5666777889') for _ in range(d)), ''.join(random.choice('5566677889') for _ in range(d))))
for d, lk, sv in tests + rnd:
    a_spec = admissible(d, [int(ch) for ch in lk], [int(ch) for ch in sv]); a_st = check(d, lk, sv); adm_n += 1
    if a_spec != a_st: adm_bad += 1; adm_bad <= 5 and print('ADMISSIBILITY MISMATCH d=%d %s %s: spec %s studio %s' % (d, lk, sv, a_spec, a_st))
    if a_spec and a_st:
        cmp_n += 1; v1, v2 = spec_val(d, lk, sv), studio_val(d, lk, sv)
        if abs(v1 - v2) > 1e-12 or xkeys_spec(d, lk, sv) != xkeys_studio(d, lk, sv):
            cmp_bad += 1; cmp_bad <= 5 and print('ROW MISMATCH d=%d %s %s: spec %.12f studio %.12f' % (d, lk, sv, v1, v2))
print('spec rebuild vs Studio rows: %d arrangements, admissibility mismatches %d; %d admissible rows compared, value/x-key mismatches %d'
      % (adm_n, adm_bad, cmp_n, cmp_bad), flush=True)
if adm_bad or cmp_bad: fail('Studio receiver rows differ from the spec; the exhaustive search below would not be the spec class')
rbad = 0
for d in range(7, DMAXP + 1):
    out = sepx(d, yv, xv, d - 6 + T + EPS, 20)
    for o in out[:5]: print('VIOLATED receiver d=%d load %.12f link %s s %s' % (d, o[0], o[1], o[2]))
    rbad += len(out); print('receivers d=%d: %d violated' % (d, len(out)), flush=True)
z9 = max([v for tq, v in X.items() if (tq // 15625) % 3 == 2] + [0.0])
for d in range(DMAXP + 1, 31):
    out = dp9(d, yv, z9, d - 6 + T + EPS, 5); rbad += len(out)
    for o in out[:3]: print('VIOLATED DP d=%d %.12f' % (d, o[0]))
print('DP d=%d..30 (z9 = %.6f): %s' % (DMAXP + 1, z9, 'clean' if rbad == 0 else 'see above'))
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
print('Karp tail: lambda = %.9f, covered for d >= %.3f (needs <= 31)' % (lam, d0))
if d0 > 31: rbad += 1
if rbad: fail('receiver side violated')
SEPX.stdin.close(); SEPX.wait()
print('UPPER: %s' % ('FEASIBLE at t = %.12f' % T if rbad == 0 and not [f for f in FAIL if 'violated' in f or 'bounds' in f] else 'NOT ESTABLISHED'))
print('VERDICT: %s' % ('PASS (upper FEASIBLE, lower VALID 19/102)' if not FAIL else 'FAIL: ' + ' | '.join(FAIL)))
