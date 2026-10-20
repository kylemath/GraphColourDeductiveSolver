"""jcheck2.py -- jcheck.py with the jsep2 separator (rotation symmetry break, 5-letter-state bound, bitset
pattern matching, threads=N; ref = use the original bin/jsep).  upper also reports the max admissible load per d.

jcheck.py -- independent two-sided checker for the wheel-level discharging LP (Opus J_lp_checker).

Written from the row definitions (wheeldis README s0, s1, s6; JOB28.md; wlp3x/G_ruleT_lp docs for the x / T
column semantics).  Only the INPUT FORMATS of Studio's files were taken from their code (pattern names, cfast blocks,
wheel verdict files, solution JSON keys, tau integer codes); no separation / DP code was ported.

Model (letters 5,6,7,8,9; 9 = degree >= 9; receiver letter U = min(d,9)):
  sender rows   : every cyclic 5-word w, not R5, with a letter >= 7:  sum_{j: w_j>=7} y[root(w,j)] (+T) >= 1 - t
  receiver rows : u of exact degree d, arrangement (w_i, s_i), s_i = apex of w_i w_{i+1}; admissible iff
                  every w_i=5 has non-R5 word (U, w_{i+1}, s_i, s_{i-1}, w_{i-1}), every w_i=6 has a private p with
                  non-R6 word (U, w_{i+1}, s_i, p, s_{i-1}, w_{i-1}), d in {7,8} => link not in RBIG, and no
                  forbidden pattern (rotation/reflection) matches.
                  load = sum_{w_i=5} y[root(...)] + sum_{w_j>=7} (x[tau_in] - x[tau_out]) (+T) <= d - 6 + t.
Commands:
  python3 jcheck.py solve  [opts]           LP by row generation with jsep (x = 0), prints t*, writes sol + cert JSON
  python3 jcheck.py upper  sol=FILE [opts]  every receiver row at d = 7..DMAX by exhaustive jsep, + Karp tail
  python3 jcheck.py lower  cert=FILE [opts] exact rational check of a dual certificate (rows re-derived and re-checked)
  python3 jcheck.py maxload sol=FILE [opts] max admissible load per d (branch and bound), for comparison
Options: root=DIR (wheeldis dir to read data from), args=FILE (pattern-arg file, space separated, as Studio's
  .args) or argsjson=FILE (a solution JSON with an 'args' list), excl=out/def_,hr1_or1 (drop pattern files by name),
  dmax=17 (exhaustive separation up to this d), dtail=30 (relaxed DP up to here, then Karp), eps=1e-9,
  nf=FILE (Job 30 whole-arrangement kill patterns, format in FINDINGS.md), nox (ignore x in the solution).
"""
import sys, os, re, json, itertools, collections, subprocess, time
from fractions import Fraction
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
CMD = sys.argv[1] if len(sys.argv) > 1 else 'help'
OPT = {}
FLAGS = set()
for a in sys.argv[2:]:
    if '=' in a: k, v = a.split('=', 1); OPT[k] = v
    else: FLAGS.add(a)
ROOT = OPT.get('root', os.path.normpath(os.path.join(HERE, '..', '..', '..')))
DIS = os.path.dirname(ROOT)
DMAX = int(OPT.get('dmax', '17')); DTAIL = int(OPT.get('dtail', '30')); EPS = float(OPT.get('eps', '1e-9'))
LET = (5, 6, 7, 8, 9); LI = {l: i for i, l in enumerate(LET)}
BIN = os.path.join(HERE, 'bin', 'jsep' if 'ref' in FLAGS else 'jsep3')
BIN4 = os.path.join(HERE, 'bin', 'jsep4'); BONUSF = [None]; BIN5 = os.path.join(HERE, 'bin', 'jsep5')
NTH = OPT.get('threads', '3'); SYMF = '0' if 'nosym' in FLAGS else '1'
WORK = OPT.get('work', '/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad/P/work'); os.makedirs(WORK, exist_ok=True)
def log(*a): print(*a, flush=True)

# ---------------- reducible wheels ----------------
def canon(w):
    w = tuple(w); n = len(w)
    return min(min(s[k:] + s[:k] for k in range(n)) for s in (w, w[::-1]))
R5, R6 = set(), set()
EXCL6 = {'565667', '565676', '565677', '565757', '565767', '565777'}   # README s0: not certified, not used
for line in open(os.path.join(DIS, 'studio17', 'wheels17_verdicts.txt')):
    if line.startswith('#') or not line.strip(): continue
    f = line.split(); fam, wd = f[0].split('_'); v = f[2]
    if v == 'D' or (v == 'C' and wd not in EXCL6 and 'noCw' not in FLAGS):   # s33z (from s30t): noCw drops C wheel verdicts
        (R5 if fam == 'c5' else R6).add(canon(map(int, wd)))
FANS = []
for line in open(os.path.join(ROOT, 'out', 'fans_dfast.out')):
    if 'D=true' in line: FANS.append(tuple(None if c == 'F' else int(c) for c in line.split()[0][2:]))
def fanhit(w):
    for f in FANS:
        for s in (tuple(w), tuple(w)[::-1]):
            for k in range(5):
                r = s[k:] + s[:k]
                if all(p is None or p == q for p, q in zip(f, r)): return True
    return False
_r5 = {}
def isR5(w):
    w = tuple(w)
    if w not in _r5: _r5[w] = canon(w) in R5 or fanhit(w)
    return _r5[w]
def isR6(w):
    w = tuple(w)
    return canon(w) in R6 or any(w[i] == w[(i + 1) % 6] == w[(i + 2) % 6] == 5 for i in range(6))   # 2.122
RBIG = set()
def addbig(word):
    RBIG.add(''.join(map(str, canon(map(int, word)))))
for fn in ('bigwheels_dfast.out',):
    for line in open(os.path.join(ROOT, 'out', fn)):
        if 'D=true' in line: addbig(line.split()[0].split('_')[1])
if 'now7plus' not in FLAGS:   # R_opt+ (README s7.3): later D 7/8-wheels and cfast C-candidate 7-wheels
    import glob
    for fn in [os.path.join(ROOT, 'out', 'bigwheels1516_dfast_partial.out')] + glob.glob(os.path.join(ROOT, 'out', 'def_*.out')):
        for line in open(fn):
            f = line.split()
            if f and re.match(r'^c[78]_\d+$', f[0]) and 'D=true' in line: addbig(f[0][3:])
    for fn in ([] if 'noC' in FLAGS else glob.glob(os.path.join(ROOT, 'out', 'def_*.cfast'))):   # s33z (from s30t): noC drops cfast C 7-wheels
        cur = None
        for line in open(fn):
            if ' r=' in line and not line.startswith(' '):
                m = re.match(r'^(?:c7_|\S*_w7_\d+_)(\d{7}) ', line); cur = m.group(1) if m else None
            elif 'C-REDUCIBLE' in line and cur: addbig(cur)

# ---------------- variables ----------------
def root(w, j):   # rooted word read from position j, up to reflection of the link
    a = tuple(w[j:] + w[:j]); b = (a[0],) + tuple(reversed(a[1:])); return min(a, b)
W5 = sorted({canon(w) for w in itertools.product(LET, repeat=5)})
SENDERS = [w for w in W5 if not isR5(w) and max(w) >= 7]
ROOTS = sorted({root(list(w), j) for w in SENDERS for j in range(5) if w[j] >= 7})
RIX = {r: i for i, r in enumerate(ROOTS)}
def rname(r): return '%d|%s' % (r[0], ''.join(map(str, r[1:])))
def sender_coef(w):
    c = collections.Counter()
    for j in range(5):
        if w[j] >= 7: c[root(list(w), j)] += 1
    return c
# tau (Job 29 L2 transfer type) -- integer code as in Studio's solution JSON (format only)
def side(c, a, b): return LI[c] * 25 + LI[a] * 5 + LI[b]
def tau(fl, tl, s1, s2):
    lo, hi = min(s1, s2), max(s1, s2); return (((LI[fl] - 2) * 3 + (LI[tl] - 2)) * 125 + lo) * 125 + hi

# ---------------- patterns ----------------
SETS = {'5': (5,), '6': (6,), '7': (7,), '8': (8,), 'B': (7, 8, 9)}
def pname(name):
    """pattern name -> (d, [(slot, set)]) with slot ('w', i) / ('s', i).  Every specified letter is kept."""
    f = name.split('_'); kind = f[0][0]; d = int(f[0][1:]); lk, sv = f[1], f[2]
    assert len(lk) == d and len(sv) == d, name
    out = []
    for typ, word in (('w', lk), ('s', sv)):
        for i, ch in enumerate(word):
            if ch == '.': continue
            if kind == 'p' and ((typ == 'w' and ch == '9') or (typ == 's' and ch == '0')): continue
            assert ch in SETS, name
            if kind != 'f': assert ch in '56B', name
            out.append(((typ, i), frozenset(SETS[ch])))
    return d, tuple(sorted(out))
PATS = collections.defaultdict(set); PSRC = collections.Counter()
OFFREG = []   # s39o offc: (src, name, d, P, r, m) of every registry entry read (filled only under the offc flag)
def addpat(nm, src, rm=None):
    d, P = pname(nm)
    if 'offc' in FLAGS: OFFREG.append((src, nm, d, P) + (rm or (None, None)))
    if P not in PATS[d]: PATS[d].add(P); PSRC[src] += 1
def _rm(line):
    m_ = re.search(r' r=(\d+) m=(\d+)', line); return (int(m_.group(1)), int(m_.group(2))) if m_ else None
def load_patterns():
    if 'argsjson' in OPT: args = json.load(open(OPT['argsjson']))['args']
    elif 'args' in OPT: args = open(OPT['args']).read().split()
    else: args = []
    excl = [e for e in OPT.get('excl', '').split(',') if e]
    EXN = set(l.split()[0] for l in open(OPT['exname']) if l.strip() and not l.startswith('#')) if 'exname' in OPT else set(); EXHIT = collections.Counter()
    nf = 0; missing = []
    for a in args:
        if not a.startswith(('pat=', 'cpat=')) or any(e in a for e in excl) or ('noC' in FLAGS and a.startswith('cpat=')): continue   # s33z (from s30t): noC drops every cpat= file
        fn = a.split('=', 1)[1]; allf = fn.endswith(':all'); fn = fn[:-4] if allf else fn
        p = fn if os.path.isabs(fn) else os.path.join(ROOT, fn)
        if not os.path.exists(p): missing.append(fn); continue
        nf += 1
        if a.startswith('pat='):
            for line in open(p):
                if line.strip() and (allf or 'D=true' in line) and re.match(r'^[epf]\d+_', line): addpat(line.split()[0], 'D', _rm(line))
        else:
            cur = None
            for line in open(p):
                if ' r=' in line and not line.startswith(' '): cur = line.split()[0]; currm = _rm(line)
                elif 'C-REDUCIBLE' in line and cur and re.match(r'^[epf]\d+_', cur):
                    if cur in EXN: EXHIT[(fn, cur)] += 1; continue   # s40f exname=: C entry held out by name (ring-merge sweep FAILs)
                    addpat(cur, 'C', currm)
    if EXN: log('exname: %d names held out; %d C entries dropped (%d distinct names) in %s' % (len(EXN), sum(EXHIT.values()), len(set(n for _, n in EXHIT)), dict(collections.Counter(f_ for f_, _ in EXHIT))))
    if 'nf' in OPT:   # Job 30 part A: whole-arrangement kill patterns, one per line: d LINK SWORD  (or a name f<d>_...)
        for line in open(OPT['nf']):
            f = line.split()
            if not f or f[0].startswith('#'): continue
            if re.match(r'^[epf]\d+_', f[0]): addpat(f[0], 'NF')
            else: addpat('f%s_%s_%s' % (f[0], f[1], f[2]), 'NF')
    for fn in [f for f in OPT.get('rpat', '').split(',') if f]:   # raw sep3 patterns: d k (pos mask)*k ; mask 4x5 bits over (w_{i+1}, s_i, s_{i-1}, w_{i-1})
        for line in open(fn):
            f = line.split('#')[0].split()
            if not f: continue
            d, k = int(f[0]), int(f[1]); slots = {}
            for j in range(k):
                i, m = int(f[2 + 2 * j]), int(f[3 + 2 * j])
                rd = [('w', (i + 1) % d), ('s', i), ('s', (i - 1) % d), ('w', (i - 1) % d)]
                ent = [(('w', i), frozenset((5,)))] + [(rd[t], frozenset(LET[b] for b in range(5) if (m >> (5 * t + b)) & 1)) for t in range(4)]
                for sl, S_ in ent: slots[sl] = slots.get(sl, frozenset(LET)) & S_
            P = tuple(sorted(slots.items()))
            if 'offc' in FLAGS: OFFREG.append(('RPAT', line.split('#')[1].strip() if '#' in line else 'rpat', d, P, None, None))
            if P not in PATS[d]: PATS[d].add(P); PSRC['RPAT'] += 1
    for fn in [f for f in OPT.get('rpatN', '').split(',') if f]:   # s39o (OFFC_SPEC 3): whole-window patterns 'd LINK SWORD', chars 5-8 exact, N = {6,7,8,9}, . free
        for line in open(fn):
            f = line.split('#')[0].split()
            if not f: continue
            d, lk, sv = int(f[0]), f[1], f[2]; assert len(lk) == d and len(sv) == d, line
            P = tuple(sorted(((typ, i), frozenset((6, 7, 8, 9)) if ch == 'N' else frozenset((int(ch),)))
                             for typ, word in (('w', lk), ('s', sv)) for i, ch in enumerate(word) if ch != '.'))
            assert all(ch in '5678N.' for ch in lk + sv) and 'N' not in sv, line
            if 'offc' in FLAGS: OFFREG.append(('RPATN', line.split('#')[1].strip() if '#' in line else 'rpatN', d, P, None, None))
            if P not in PATS[d]: PATS[d].add(P); PSRC['RPATN'] += 1
    if 'offc' in FLAGS:   # s39o (OFFC_SPEC.md): every registry configuration also matched off-centre in the 1.5-ball
        exec(open(os.path.join(HERE, 'offc.py')).read(), globals()); offc_extend()
    log('patterns: %d files read, %d missing %s; distinct by d %s; by kind %s' % (
        nf, len(missing), missing, {d: len(v) for d, v in sorted(PATS.items())}, dict(PSRC)))
_INST = {}
def instances(d):
    if d not in _INST: _INST[d] = _instances(d)
    return _INST[d]
def _instances(d):
    """expand every pattern at degree d over the 2d rotations/reflections -> list of [(slotindex, mask)]"""
    out = set()
    for P in PATS.get(d, ()):
        for r in range(d):
            for refl in (False, True):
                inst = []
                for (typ, i), S in P:
                    if not refl: j = (i + r) % d
                    else: j = (r - i) % d if typ == 'w' else (r - i - 1) % d
                    slot = 2 * j + (0 if typ == 'w' else 1)
                    inst.append((slot, sum(1 << LI[x] for x in S)))
                # merge duplicate slots (intersection)
                m = {}
                for s, k in inst: m[s] = m.get(s, 31) & k
                out.add(tuple(sorted(m.items())))
    return sorted(out)

# ---------------- solution ----------------
def load_solution(fn):
    S = json.load(open(fn))
    y = np.zeros(len(ROOTS)); unk = 0
    for k, v in S['y'].items():
        u, rest = k.split('|'); r = (int(u),) + tuple(int(c) for c in rest)
        r = root(list(r), 0)
        if r in RIX: y[RIX[r]] = v
        else: unk += 1
    x = {}
    if 'nox' not in FLAGS and isinstance(S.get('x'), dict):
        for k, v in S['x'].items(): x[int(k)] = float(v)
    global TMODE
    if 'yT' in S:   # rule T solution (Job 30 part B): Y[root|fa fe], T[root|fa fe side]; keys canonical as tkey()
        TMODE = True
        for k, v in S['yT'].items():
            rw, fl = k.split('|'); YT[(tuple(int(c) for c in rw), int(fl[0]), int(fl[1]))] = float(v)
        for k, v in S.get('tau', {}).items():
            rw, fl = k.split('|'); TT[(tuple(int(c) for c in rw), int(fl[0]), int(fl[1]), fl[2])] = float(v)
    log('solution %s: t = %.12f, %d y (%d not a variable here), %d x, rule T %s (%d Y, %d T)' % (
        fn, S['t'], len(S.get('y', {})), unk, len(x), TMODE, len(YT), len(TT)))
    return float(S['t']), y, x, S
TMODE = False; YT = {}; TT = {}
BIGL = (7, 8, 9)
def rev5(r): return (r[0], r[4], r[3], r[2], r[1])
def ykey(raw, fa, fe):
    """Y key from a raw rooted word (B, a, b, c, e) read from the root; flags fa/fe = spoke a/e is 6 and the vertex
    beyond it (other common neighbour of the root and that 6) is big.  Reflection swaps a and e."""
    raw = tuple(raw); rv = rev5(raw)
    if rv < raw: raw, fa, fe = rv, fe, fa
    elif raw == rv: fa, fe = min(fa, fe), max(fa, fe)
    return (raw, fa, fe)
def tkey(raw, fa, fe, sd):
    raw = tuple(raw); rv = rev5(raw); sw = lambda x: 'e' if x == 'a' else 'a'
    if rv < raw: raw, fa, fe, sd = rv, fe, fa, sw(sd)
    elif raw == rv and (fe, fa, sw(sd)) < (fa, fe, sd): fa, fe, sd = fe, fa, sw(sd)
    return (raw, fa, fe, sd)
def T_inflow(b):
    """max T a five s_j can send to the receiver when s_j sits between a big b and a 6 (root b, toward the 6):
    raw word (b, 6, p, m, o), side a, fa = 1; fe free when o = 6.  Conservative: p, m, o maximised, the 6-wheel side
    condition dropped (G_ruleT_lp s2(ii))."""
    best = 0.0
    for p, m, o in itertools.product(LET, repeat=3):
        if isR5((b, 6, p, m, o)): continue
        for fe in ((0, 1) if o == 6 else (0,)):
            best = max(best, TT.get(tkey((b, 6, p, m, o), 1, fe, 'a'), 0.0))
    return best
def sender_rows_ok(t, y, x):
    """every sender row (with rule T: every admissible flag assignment), returns list of violations"""
    bad = []
    for w in SENDERS:
        if not TMODE:
            v = sum(c * y[RIX[r]] for r, c in sender_coef(w).items())
            if v < 1 - t - EPS: bad.append((''.join(map(str, w)), v))
            continue
        # flags: for each big root j and each spoke side (j+1 = 'a', j-1 = 'e') that is a 6, z = the 6's other
        # neighbour common with the root; z's bigness is a free choice, coupled through the 6's wheel
        n = 5; sixes = [k for k in range(n) if w[k] == 6]
        zs = {}   # (k, dir): z slot of the 6 at k on the side of neighbour k+dir
        for k in sixes:
            for dr in (1, -1):
                if w[(k + dr) % n] >= 7: zs[(k, dr)] = None
        keys = sorted(zs); worst = None
        for bits in itertools.product((0, 1), repeat=len(keys)):
            Z = dict(zip(keys, bits)); okc = True
            for k in sixes:   # 6-wheel (5, w_{k+1}, zR, q, zL, w_{k-1}) must be non-R6 for some letters
                zr = Z.get((k, 1)); zl = Z.get((k, -1))
                cand = lambda f: LET if f is None else (BIGL if f else (5, 6))
                if all(isR6((5, w[(k + 1) % n], a_, q, b_, w[(k - 1) % n])) for a_ in cand(zr) for b_ in cand(zl) for q in LET): okc = False; break
            if not okc: continue
            tot = 0.0
            for j in range(n):
                if w[j] < 7: continue
                raw = tuple(w[(j + i) % n] for i in range(5)); ka, ke = (j + 1) % n, (j - 1) % n
                fa = Z.get((ka, -1), 0) if w[ka] == 6 else 0; fe = Z.get((ke, 1), 0) if w[ke] == 6 else 0
                tot += YT.get(ykey(raw, fa, fe), 0.0)
                if fa: tot += TT.get(tkey(raw, fa, fe, 'a'), 0.0)
                if fe: tot += TT.get(tkey(raw, fa, fe, 'e'), 0.0)
            if worst is None or tot < worst: worst = tot
        if worst is not None and worst < 1 - t - EPS: bad.append((''.join(map(str, w)), worst))
    return bad

# ---------------- window table ----------------
def window_table(U, y, x):
    """WIN[a,b,c,e,f, p,q,r,s] for position i: w_{i-2..i+2} = a,b,c,e,f ; s_{i-2..i+1} = p,q,r,s (letter indices)."""
    W = np.zeros((5,) * 9)
    # w_i = 5 : depends on b, e (w_{i-1}, w_{i+1}), q, r (s_{i-1}, s_i)
    for b, e, q, r in itertools.product(range(5), repeat=4):
        wd = [U, LET[e], LET[r], LET[q], LET[b]]
        if isR5(wd): W[:, b, 0, e, :, :, q, r, :] = -np.inf
        elif not TMODE: W[:, b, 0, e, :, :, q, r, :] = y[RIX[root(wd, 0)]]
        else:   # outflow Y[r, fa, fe]: fa = (w_{i+1} = 6 and w_{i+2} big), fe = (w_{i-1} = 6 and w_{i-2} big)
            for a, f in itertools.product(range(5), repeat=2):
                fa = int(LET[e] == 6 and f >= 2); fe = int(LET[b] == 6 and a >= 2)
                W[a, b, 0, e, f, :, q, r, :] = YT.get(ykey(wd, fa, fe), 0.0)
        if all(isR6([U, LET[e], LET[r], p, LET[q], LET[b]]) for p in LET): W[:, b, 1, e, :, :, q, r, :] = -np.inf
    if TMODE:   # inflow: s_i = 5 between w_i and w_{i+1}, one big and one 6 -> T from s_i to u (u = z)
        for c, e in itertools.product(range(5), repeat=2):
            if LET[c] >= 7 and LET[e] == 6: W[:, :, c, e, :, :, :, 0, :] += T_inflow(LET[c])
            if LET[c] == 6 and LET[e] >= 7: W[:, :, c, e, :, :, :, 0, :] += T_inflow(LET[e])
    if x:
        for c in (2, 3, 4):
            for a, b, e, f, q, r in itertools.product(range(5), repeat=6):
                to = tau(U, LET[c], side(LET[b], LET[a], LET[q]), side(LET[e], LET[f], LET[r]))
                ti = tau(LET[c], U, side(LET[b], LET[q], LET[a]), side(LET[e], LET[r], LET[f]))
                W[a, b, c, e, f, :, q, r, :] += x.get(ti, 0.0) - x.get(to, 0.0)
    return W
def write_table(W, tag):
    p = os.path.join(WORK, 'win_%s.bin' % tag)
    np.ascontiguousarray(np.where(np.isfinite(W), W, -1e300), dtype=np.float64).tofile(p); return p

def run_sep(d, W, thr, K, mode, pats=True):
    hdr = os.path.join(WORK, 'hdr_%d.txt' % d)
    inst = instances(d) if pats else []
    big = sorted(b for b in RBIG if len(b) == d) if d in (7, 8) else []
    with open(hdr, 'w') as f:
        f.write('%d %.15f %d %d\n%d\n%s\n%d\n' % (d, thr, K, mode, len(big), '\n'.join(big), len(inst)))
        for I in inst: f.write('%d %s\n' % (len(I), ' '.join('%d %d' % sk for sk in I)))
    wp = write_table(W, 'd%d' % d)
    t0 = time.time()
    hdr2 = hdr.replace('.txt', '_m%d.txt' % mode); os.replace(hdr, hdr2); hdr = hdr2
    extra = [] if 'ref' in FLAGS else [NTH, SYMF]
    if mode == 2: extra.append(CLSFILE[0])
    if L3FILE[0] and d == 7:   # stage 28: jsep5 with the l3q leaf correction (RELAY_SPEC_s21 21.6)
        if mode != 2: extra.append('none')
        extra.append(BONUSF[0] or 'none'); extra.append(L3FILE[0])
        out = subprocess.run([BIN5, hdr, wp] + extra, capture_output=True, text=True, check=True).stdout.split('\n')
        return [l.split() for l in out if l], time.time() - t0, len(inst)
    if BONUSF[0] and d == 7:
        if mode != 2: extra.append('none')
        extra.append(BONUSF[0])
    out = subprocess.run([BIN4 if (BONUSF[0] and d == 7) else BIN, hdr, wp] + extra, capture_output=True, text=True, check=True).stdout.split('\n')
    return [l.split() for l in out if l], time.time() - t0, len(inst)

def karp(M):
    n = M.shape[0]; D = np.full((n + 1, n), -np.inf); D[0, :] = 0.0
    for k in range(1, n + 1): D[k] = (D[k - 1][:, None] + M).max(axis=0)
    best = -np.inf
    for v in range(n):
        if not np.isfinite(D[n, v]): continue
        q = min((D[n, v] - D[k, v]) / (n - k) for k in range(n) if np.isfinite(D[k, v]))
        best = max(best, q)
    return best
def relaxed_M(W):
    G = W.max(axis=(0, 4, 5, 8))          # b, c, e, q, r
    M = np.full((125, 125), -np.inf)
    for b, q, c, r, e in itertools.product(range(5), repeat=5):
        M[(b * 5 + q) * 5 + c, (c * 5 + r) * 5 + e] = G[b, c, e, q, r]
    return M
def closed_max(M, d):
    P = M.copy()
    for _ in range(d - 1): P = (P[:, :, None] + M[None, :, :]).max(axis=1)
    return np.diag(P).max()

def recv_coef(d, lk, sv, x_on):
    U = min(d, 9); w = [int(c) for c in lk]; s = [int(c) for c in sv]
    cy = collections.Counter(); cx = collections.Counter()
    for i in range(d):
        if w[i] == 5: cy[root([U, w[(i + 1) % d], s[i], s[(i - 1) % d], w[(i - 1) % d]], 0)] += 1
        elif w[i] >= 7 and x_on:
            W_ = lambda k: w[k % d]; S_ = lambda k: s[k % d]
            cx[tau(w[i], U, side(W_(i - 1), S_(i - 1), W_(i - 2)), side(W_(i + 1), S_(i), W_(i + 2)))] += 1
            cx[tau(U, w[i], side(W_(i - 1), W_(i - 2), S_(i - 1)), side(W_(i + 1), W_(i + 2), S_(i)))] -= 1
    return cy, cx
def admissible(d, lk, sv):
    """direct check of one arrangement (independent of the DFS)."""
    U = min(d, 9); w = [int(c) for c in lk]; s = [int(c) for c in sv]
    for i in range(d):
        wd = [U, w[(i + 1) % d], s[i], s[(i - 1) % d], w[(i - 1) % d]]
        if w[i] == 5 and isR5(wd): return 'R5 at w%d' % i
        if w[i] == 6 and all(isR6([U, w[(i + 1) % d], s[i], p, s[(i - 1) % d], w[(i - 1) % d]]) for p in LET): return 'R6 at w%d' % i
    if d in (7, 8) and ''.join(map(str, canon(w))) in RBIG: return 'RBIG link'
    if d not in _NPI:
        I = instances(d); m = max((len(x) for x in I), default=1)
        SL = np.zeros((len(I), m), dtype=np.int64); MK = np.full((len(I), m), 31, dtype=np.int64)
        for n, x in enumerate(I):
            for j, (sl, k) in enumerate(x): SL[n, j] = sl; MK[n, j] = k
        _NPI[d] = (SL, MK)
    SL, MK = _NPI[d]
    if len(SL) == 0: return None
    Larr = np.array([LI[v] for i in range(d) for v in (w[i], s[i])], dtype=np.int64)
    hit = np.all((MK >> Larr[SL]) & 1, axis=1)
    if hit.any(): return 'pattern %s' % (instances(d)[int(np.argmax(hit))],)
    return None
_NPI = {}

# ---------------- commands ----------------
def cmd_upper():
    load_patterns()
    t, y, x, S = load_solution(OPT['sol'])
    bad = 0; rep = []
    sb = sender_rows_ok(t, y, x)
    for w_, v in sb[:10]: log('  VIOLATED sender %s: %.9f < 1 - t' % (w_, v))
    log('sender rows: %d checked, %d violated' % (len(SENDERS), len(sb))); bad += len(sb)
    for d in range(7, DMAX + 1):
        U = min(d, 9); W = window_table(U, y, x); thr = d - 6 + t + EPS
        res, dt, ni = run_sep(d, W, thr, 20, 0)
        v = [r for r in res if r[0] == 'V']; end = [r for r in res if r[0] == 'END'][0]
        for r in v[:5]: log('  VIOLATED d=%d load %s > %.9f link %s s %s' % (d, r[1], d - 6 + t, r[2], r[3]))
        bad += len(v); rep.append((d, len(v), dt, int(end[2]), ni))
        log('d=%d exhaustive: %d violated (cap 20), %d pattern instances, %d DFS nodes, %.1fs' % (d, len(v), ni, int(end[2]), dt))
        if 'nomax' not in FLAGS:
            res, dt2, _ = run_sep(d, W, 0, 1, 1); r = res[0]
            log('d=%d max admissible load %s ; minus (d-6+t) = %+.3e  (link %s s %s; %.1fs)' % (d, r[1], float(r[1]) - (d - 6 + t), r[2], r[3], dt2))
    W9 = window_table(9, y, x); M = relaxed_M(W9)
    for d in range(DMAX + 1, DTAIL + 1):
        v = closed_max(M, d)
        if v > d - 6 + t + EPS:
            res, dt, ni = run_sep(d, W9, d - 6 + t + EPS, 20, 0, pats=False)
            nv = sum(1 for r in res if r[0] == 'V'); bad += nv
            log('d=%d relaxed DP %.6f > %.6f; exact pattern-free DFS: %d violated (%.1fs)' % (d, v, d - 6 + t, nv, dt))
        else: log('d=%d relaxed DP max %.6f <= %.6f' % (d, v, d - 6 + t))
    lam = karp(M); d0 = (6 - t) / (1 - lam) if lam < 1 else float('inf')
    log('Karp: letter-9 relaxed max cycle mean lambda = %.9f; d*lambda <= d-6+t for all d >= %.3f (need <= %d)' % (lam, d0, DTAIL + 1))
    if d0 > DTAIL + 1: bad += 1; log('TAIL NOT COVERED')
    log('UPPER: %s at t = %.12f' % ('FEASIBLE' if bad == 0 else 'INFEASIBLE (%d)' % bad, t))
    return rep

def cmd_maxload():
    load_patterns()
    t, y, x, S = load_solution(OPT['sol'])
    for d in range(7, DMAX + 1):
        W = window_table(min(d, 9), y, x)
        res, dt, ni = run_sep(d, W, 0, 1, 1)
        r = res[0]; log('d=%d max admissible load %s vs d-6+t = %.6f  (link %s s %s; %s nodes, %.1fs)' % (d, r[1], d - 6 + t, r[2], r[3], r[4], dt))

def cmd_solve():
    """LP min t over y in [0,1] (x = 0), receiver rows by jsep row generation at d = 7..DMAX (relaxed DP above)."""
    from scipy.optimize import linprog
    load_patterns()
    nv = len(ROOTS) + 1
    A, b, info = [], [], []
    for w in SENDERS:
        row = np.zeros(nv); row[-1] = -1
        for r, c in sender_coef(w).items(): row[RIX[r]] -= c
        A.append(row); b.append(-1.0); info.append(('sender', ''.join(map(str, w))))
    have = set()
    def addrow(d, lk, sv):
        cy, _ = recv_coef(d, lk, sv, False); key = (d, tuple(sorted(cy.items())))
        if key in have: return False
        have.add(key); row = np.zeros(nv); row[-1] = -1
        for r, c in cy.items(): row[RIX[r]] += c
        A.append(row); b.append(d - 6.0); info.append(('receiver', d, lk, sv)); return True
    if 'warm' in OPT:
        for line in open(OPT['warm']):
            m = re.search(r'receiver d=(\d+) link (\d+) s (\d+)', line)
            if m and int(m.group(1)) <= DMAX and admissible(int(m.group(1)), m.group(2), m.group(3)) is None: addrow(int(m.group(1)), m.group(2), m.group(3))
        log('warm rows admitted: %d' % (len(A) - len(SENDERS)))
    t = -1.0; y = np.ones(len(ROOTS)) * 0.5
    for it in range(400):
        res = linprog(np.eye(nv)[-1], A_ub=np.array(A), b_ub=np.array(b), bounds=[(0, 1)] * (nv - 1) + [(None, None)], method='highs')
        y, t = res.x[:-1], res.x[-1]; added = 0; tt = time.time()
        for d in range(7, DMAX + 1):
            W = window_table(min(d, 9), y, {})
            rr, dt, ni = run_sep(d, W, d - 6 + t + 1e-7, int(OPT.get("many", "3000")), 0)
            for r in rr:
                if r[0] == 'V' and addrow(d, r[2], r[3]): added += 1
        log('iter %d t=%.9f rows %d added %d (%.1fs)' % (it, t, len(A), added, time.time() - tt))
        if not added: break
    res = linprog(np.eye(nv)[-1], A_ub=np.array(A), b_ub=np.array(b), bounds=[(0, 1)] * (nv - 1) + [(None, None)], method='highs')
    y, t = res.x[:-1], res.x[-1]; duals = -res.ineqlin.marginals
    tag = OPT.get('tag', 'run')
    json.dump({'t': t, 'z9': 0.0, 'x': {}, 'y': {rname(r): float(y[i]) for i, r in enumerate(ROOTS) if y[i] > 0}},
              open(os.path.join(HERE, 'sol_%s.json' % tag), 'w'))
    cert = []
    for i, dv in enumerate(duals):
        if dv > 1e-10: cert.append({'w': float(dv), 'row': list(info[i])})
    json.dump(cert, open(os.path.join(HERE, 'cert_%s.json' % tag), 'w'), indent=0)
    log('LP t* = %.12f ; dual rows %d ; wrote sol_%s.json cert_%s.json' % (t, len(cert), tag, tag))
    for c in cert: log('  %.6f %s' % (c['w'], ' '.join(map(str, c['row']))))

def cmd_lower():
    """certificate: JSON list of {w: weight (float or 'p/q'), row: ['sender', WORD] | ['receiver', d, LINK, SWORD]}.
    Weights are rationalised (limit_denominator(10**6)) unless given as 'p/q'.  Rows are re-derived from their words
    and re-checked for genuineness; then the combination is checked in exact arithmetic."""
    load_patterns()
    C = json.load(open(OPT['cert']))
    tot = collections.defaultdict(Fraction); sw = Fraction(0); rhs = Fraction(0); ok = True
    for c in C:
        w = Fraction(c['w']) if isinstance(c['w'], str) else Fraction(c['w']).limit_denominator(10 ** 6)
        row = c['row']
        if row[0] == 'sender':
            wd = tuple(int(ch) for ch in row[1])
            if len(wd) != 5 or isR5(wd) or max(wd) < 7: log('  NOT A SENDER ROW', row); ok = False; continue
            for r, k in sender_coef(wd).items(): tot[('y', r)] -= w * k
            rhs -= w; sw += w
        else:
            d, lk, sv = int(row[1]), row[2], row[3]
            why = admissible(d, lk, sv)
            if why:
                alt = find_alternative(d, lk, sv)
                if alt is None: log('  RECEIVER ROW NOT GENUINE', row, why); ok = False; continue
                log('  representative %s/%s forbidden (%s); same row via admissible %s/%s' % (lk, sv, why, alt[0], alt[1])); lk, sv = alt
            cy, cx = recv_coef(d, lk, sv, 'nox' not in FLAGS)
            for r, k in cy.items(): tot[('y', r)] += w * k
            for r, k in cx.items(): tot[('x', r)] += w * k
            rhs += w * (d - 6); sw += w
        log('  w=%s %s' % (w, ' '.join(map(str, row))))
    neg = {k: v for k, v in tot.items() if v < 0}
    if neg: log('  combined coefficient negative on', len(neg), 'variables, e.g.', list(neg.items())[:5]); ok = False
    t0 = -rhs / sw
    log('LOWER: %s  t >= %s = %.9f  (sum of weights %s)' % ('VALID' if ok else 'INVALID', t0, float(t0), sw))
def find_alternative(d, lk, sv):
    """a forbidden representative: try every filling of the slots the y-row does not read (x = 0 rows only)."""
    w = [int(c) for c in lk]; s = [int(c) for c in sv]
    freeS = [i for i in range(d) if w[i] != 5 and w[(i + 1) % d] != 5]
    freeW = [i for i in range(d) if w[i] != 5 and w[(i - 1) % d] != 5 and w[(i + 1) % d] != 5]
    target = recv_coef(d, lk, sv, False)[0]
    for wv in itertools.product(*[[ww for ww in LET if ww != 5] for _ in freeW]):
        for sv2 in itertools.product(LET, repeat=len(freeS)):
            w2 = list(w); s2 = list(s)
            for i, v in zip(freeW, wv): w2[i] = v
            for i, v in zip(freeS, sv2): s2[i] = v
            L2, S2 = ''.join(map(str, w2)), ''.join(map(str, s2))
            if recv_coef(d, L2, S2, False)[0] == target and admissible(d, L2, S2) is None: return L2, S2
    return None

exec(open(os.path.join(HERE, 'psolve.py')).read())
exec(open(os.path.join(HERE, 'pslite.py')).read())
exec(open(os.path.join(HERE, 'prelay.py')).read())
exec(open(os.path.join(HERE, 'prelay2.py')).read())
log('jcheck: %d R5, %d R6, %d fans, %d RBIG; %d senders, %d rooted vars' % (len(R5), len(R6), len(FANS), len(RBIG), len(SENDERS), len(ROOTS)))
{'pcellcheck': cmd_pcellcheck, 'binderR2': cmd_binderR2, 'rowR2': cmd_rowR2, 'consbasisR2': cmd_consbasisR2, 'ctxR2': cmd_ctxR2, 'solveR2': cmd_solveR2, 'lowerR2': cmd_lowerR2, 'upperR2': cmd_upperR2, 'orientR2': cmd_orientR2, 'structR2': cmd_structR2, 'solveR': cmd_solveR, 'lowerR': cmd_lowerR, 'upperR': cmd_upperR, 'orientR': cmd_orientR, 'solveS': cmd_solveS, 'upperS': cmd_upperS, 'lowerS': cmd_lowerS, 'orientS': cmd_orientS, 'lowerT': cmd_lowerT, 'solveT': cmd_solveT, 'solve2': cmd_solve2, 'upper': cmd_upper, 'lower': cmd_lower, 'solve': cmd_solve, 'maxload': cmd_maxload}.get(CMD, lambda: print(__doc__))()
