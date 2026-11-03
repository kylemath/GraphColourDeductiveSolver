# t3glue.py (s61_t3): the fy2 face-apex cells (RELAY_SPEC_s43) on the s60 hat5 + f2b stack, with an exact-window kill table.
# exec'd by pcheck.py after f2bglue.py.  Nothing here acts unless fy2 AND f2b= are both on (flags: fy fy2 f2b=...; f2boff = empty
# rule set).  Every other flag set (fy2 off, or the old s43 fy2 path without f2b) runs the s60 code and binaries unchanged.
#   tkill=FILE   exact-window kill table for the apex private t of a 5-5-5 face (format below); 'none' or absent = empty
#   toracle7     oracle: kill t in {5,6} at every face of every receiver row (d = 7..17 exhaustive part; tail d >= 18 keeps
#                the window upper bound, which is sound)
#   t3self=N     self-test: N random arrangements per d = 7..10 (half built with a face), exact python max over cells vs jsept eval
#   t3selftk     self-test with a random kill table built from the sample arrangements (tests the matcher and the drop rule)
#   zrand=SEED   self-test only: every z key gets a deterministic pseudo-random value in [0, 0.05) (the solutions here have no z)
# Face i of a receiver row (d, w, s): w_i = w_{i+1} = s_i = 5; t_i = the 4th neighbour of the apex five s_i (s43 Lemma 1).
# Allowed classes: K_i = OR of the kill letters of every entry that fires at face i (and {5,6} under toracle7).
#   K_i empty: A_i = fy2_allowed(s_{i+1}, s_{i-1}) (s43, with its fallback (0, 1)).
#   K_i not empty: A_i = {c : some x in CLS2[c] with x not in K_i and (5,5,s_{i+1},x,s_{i-1}) not R5}; A_i empty => the row
#   is excluded (every letter of t is R5 at s_i or killed by a configuration the table proves reducible).
# tkill FILE format (text, one entry per line, '#' comments):
#     D  w@OW=WPAT  s@OS=SPAT  kill=LETTERS
#   D = exact degree of u (7..17) or '*' (any d); WPAT / SPAT = letters for w_{i+OW}, w_{i+OW+1}, ... and s_{i+OS}, ...
#   relative to the face index i; each letter is 5..9 (9 = degree >= 9), '.' (any) or a set like [78]; either part may be
#   omitted; LETTERS = digits of the t letters removed (e.g. 56).  The two face fives (w@0=55, s@0=5) are implied.
#   Each entry is also applied to the mirror image (w offset o -> 1-o, s offset o -> -o): reducibility is reflection
#   invariant.  Example (SCOPE D11: u = 7, w_{j-1..j+2} = 6556, s_{j-1..j+1} = 657, t != 6):   7 w@-1=6556 s@-1=657 kill=6
import re as _re
T3_ON = FY2 and F2B_ON
TKE = []          # entries (d or 0, {off: frozenset}, {off: frozenset}, frozenset kill)
TKSTAT = collections.Counter()
def _tk_pat(off, pat):
    out = {}; k = 0; o = off
    while k < len(pat):
        ch = pat[k]
        if ch == '[':
            j = pat.index(']', k); st = frozenset(int(x) for x in pat[k + 1:j]); k = j + 1
        elif ch == '.': st = None; k += 1
        else: st = frozenset([int(ch)]); k += 1
        if st is not None:
            assert st <= set(LET), 'tkill: bad letter set %s' % pat
            out[o] = out[o] & st if o in out else st
        o += 1
    return out
def tk_parse(fn):
    ents = []
    for ln in open(fn):
        ln = ln.split('#')[0].strip()
        if not ln: continue
        f = ln.split(); dd = 0 if f[0] == '*' else int(f[0]); wc = {0: frozenset([5]), 1: frozenset([5])}; sc = {0: frozenset([5])}; kl = None
        for tok in f[1:]:
            m = _re.match(r'^([ws])@(-?\d+)=(.+)$', tok)
            if m:
                tgt = wc if m.group(1) == 'w' else sc
                for o, st in _tk_pat(int(m.group(2)), m.group(3)).items(): tgt[o] = tgt[o] & st if o in tgt else st
            elif tok.startswith('kill='): kl = frozenset(int(x) for x in tok[5:])
            else: raise Exception('tkill: bad token %r in %r' % (tok, ln))
        assert kl and kl <= set(LET), 'tkill: entry without kill letters: %r' % ln
        ents.append((dd, wc, sc, kl))
        ents.append((dd, {1 - o: st for o, st in wc.items()}, {-o: st for o, st in sc.items()}, kl))   # mirror
    return ents
if T3_ON:
    if OPT.get('tkill', 'none') != 'none': TKE += tk_parse(OPT['tkill'])
    if 'toracle7' in FLAGS: TKE.append((0, {}, {}, frozenset([5, 6])))
    log('t3: fy2 face cells on the f2b stack; tkill %s (%d entries incl. mirrors)%s' % (OPT.get('tkill', 'none'), len(TKE), '; ORACLE toracle7 (t >= 7 at every face)' if 'toracle7' in FLAGS else ''))
elif OPT.get('tkill') or 'toracle7' in FLAGS:
    raise SystemExit('tkill= / toracle7 need the flags fy fy2 and f2b= (f2boff for an empty rule set)')
def tk_fire(e, d, w, s, i):
    dd, wc, sc, kl = e
    if dd and dd != d: return False
    for o, st in wc.items():
        if w[(i + o) % d] not in st: return False
    for o, st in sc.items():
        if s[(i + o) % d] not in st: return False
    return True
def tk_letters(d, w, s, i):
    k = frozenset()
    if d > DMAX: return k
    for e in TKE:
        if tk_fire(e, d, w, s, i): k = k | e[3]
    return k
def tk_classes(sn, sp, k):
    if not k: return fy2_allowed(sn, sp)
    return tuple(c for c in (0, 1) if any(x not in k and not isR5([5, 5, sn, x, sp]) for x in CLS2[c]))
if T3_ON:
    def fy2_cells(d, w, s):
        """faces and cells of a receiver row, with the tkill classes (s61); [] = row excluded"""
        F = [i for i in range(d) if w[i] == 5 and w[(i + 1) % d] == 5 and s[i] == 5]
        for i in F: assert (i + 1) % d not in F, 'fy2: five in two faces (its link (U,5,5,5,5) is R5: row not admissible)'
        As = []
        for i in F:
            k = tk_letters(d, w, s, i); A = tk_classes(s[(i + 1) % d], s[(i - 1) % d], k)
            if k: TKSTAT['fire'] += 1
            As.append(A)
        return [(','.join('%d:%d' % (i, c) for i, c in zip(F, cb)), dict(zip(F, cb))) for cb in itertools.product(*As)]
    _t3_recv_coef_R2 = recv_coef_R2
    def recv_coef_R2(d, lk, sv, xon, tau=None):
        if tau is None:   # reporting callers: first cell; an excluded row reports its s43 first cell
            w = [int(ch) for ch in lk]; s = [int(ch) for ch in sv]; cl = fy2_cells(d, w, s)
            if not cl:
                F = [i for i in range(d) if w[i] == 5 and w[(i + 1) % d] == 5 and s[i] == 5]
                cl = [('', {i: fy2_allowed(s[(i + 1) % d], s[(i - 1) % d])[0] for i in F})]
            tau = cl[0][1]
        return _t3_recv_coef_R2(d, lk, sv, xon, tau)
    BINT = os.path.join(HERE, 'bin', 'jsept'); T3_EVAL = [None]
    def tk_write(d):
        """binary tkill file for jsept (layout in jsept.cpp)"""
        nr5 = bytearray(25)
        for sn, sp in itertools.product(range(5), repeat=2):
            nr5[sn * 5 + sp] = sum(1 << x for x in range(5) if not isR5([5, 5, LET[sn], LET[x], LET[sp]]))
        rows = []
        for dd, wc, sc, kl in TKE:
            if (dd and dd != d) or d > DMAX: continue
            offs = [o % d for o in list(wc) + list(sc)]
            fw = 0; fs = 0; ok = True; seenw = {}; seens = {}
            for o, st in wc.items():
                om = o % d; st2 = seenw[om] & st if om in seenw else st; seenw[om] = st2
            for o, st in sc.items():
                om = o % d; st2 = seens[om] & st if om in seens else st; seens[om] = st2
            if any(not v for v in list(seenw.values()) + list(seens.values())): continue   # contradictory after wrap: never fires
            for om, st in seenw.items(): fw |= (sum(1 << (x - 5) for x in LET if x not in st)) << (5 * om)
            for om, st in seens.items(): fs |= (sum(1 << (x - 5) for x in LET if x not in st)) << (5 * om)
            M64 = (1 << 64) - 1
            rows.append((fw & M64, fw >> 64, fs & M64, fs >> 64, sum(1 << (x - 5) for x in kl)))
        out = bytearray(np.array([d], dtype='<i4').tobytes()) + bytes(nr5) + np.array([len(rows)], dtype='<u4').tobytes()
        if rows: out += np.array(rows, dtype='<u8').tobytes()
        fn = os.path.join(WORK, 'tkill_d%d.bin' % d); open(fn, 'wb').write(bytes(out)); return fn
    _t3_run_sep = run_sep
    def run_sep(d, W, thr, K, mode, pats=True):
        """s61: every d through jsept (f2b leaf at d = 7..9 as jsepf, fy2 ZT coupling, tkill)"""
        hdr = os.path.join(WORK, 'hdr_%d.txt' % d)
        inst = instances(d) if pats else []
        big = sorted(b for b in RBIG if len(b) == d) if d in (7, 8) else []
        with open(hdr, 'w') as f:
            f.write('%d %.15f %d %d\n%d\n%s\n%d\n' % (d, thr, K, mode, len(big), '\n'.join(big), len(inst)))
            for I in inst: f.write('%d %s\n' % (len(I), ' '.join('%d %d' % sk for sk in I)))
        wp = write_table(W, 'd%d' % d)
        t0 = time.time()
        hdr2 = hdr.replace('.txt', '_m%d.txt' % mode); os.replace(hdr, hdr2); hdr = hdr2
        l3v = bool(LQVX and L3VFILE[0] and d in (7, 8))
        extra = [NTH, SYMF, CLSFILE[0] if mode == 2 else 'none', 'none', (L3FILE[0] or 'none') if d == 7 else 'none', ZTF[min(d, 9)],
                 L3VFILE[0] if l3v else 'none', f2b_write(d) if d in (7, 8, 9) else 'none', T3_EVAL[0] or 'none', tk_write(d) if TKE else 'none']
        pr = subprocess.run([BINT, hdr, wp] + extra, capture_output=True, text=True)
        if pr.returncode != 0: raise Exception('jsept exit %d: %s' % (pr.returncode, pr.stderr[-2000:]))
        for l in pr.stderr.split('\n'):
            if l.startswith('jsept: tkill face fires'): log('  ' + l)
        return [l.split() for l in pr.stdout.split('\n') if l], time.time() - t0, len(inst)
    class _ZRand(dict):
        def __init__(self, seed): super().__init__(); self.seed = seed
        def get(self, k, dflt=0.0):
            import hashlib
            h = hashlib.md5(('%s|%s' % (self.seed, k)).encode()).digest(); return 0.05 * int.from_bytes(h[:6], 'little') / 2 ** 48
    def t3_selftest(y, xd, MV2, N):
        """exact python value (max over the row's cells; DROP if no cell) vs jsept eval, d = 7..10"""
        global ZV, TKE
        if 'zrand' in OPT: ZV = _ZRand(OPT['zrand'])
        rng = random.Random(int(OPT.get('seed', '1'))); res = {}
        def val(k):
            if k[0] == 'y': return y[RIX[k[1]]]
            if k[0] == 'x': return xd.get(k[1], 0.0)
            if k[0] == 'M': v = MV2(k[1]); return 0.0 if v is None else v
            if k[0] == 'r': return RV.get(k[1], 0.0)
            if k[0] == 'rr': return RRV.get(k[1], 0.0)
            if k[0] == 'lq': return LQV.get(k[1], 0.0)
            if k[0] == 'lQ': return l3q_Qeff(*k[1]) if len(k[1]) == 3 else l3q_QeffV(*k[1])
            if k[0] == 'z': return ZV.get(k[1], 0.0)
            raise Exception('t3 selftest: unsupported key %s' % (k,))
        for d in (7, 8, 9, 10):
            arr = []; tries = 0
            while len(arr) < N and tries < 400 * N:
                tries += 1
                w = [rng.choice(LET) for _ in range(d)]; s = [rng.choice(LET) for _ in range(d)]
                if len(arr) % 4 != 3:   # plant one or two faces
                    for _ in range(rng.choice((1, 1, 2))):
                        i0 = rng.randrange(d); w[i0] = w[(i0 + 1) % d] = s[i0] = 5
                lk = ''.join(map(str, w)); sv = ''.join(map(str, s))
                if admissible(d, lk, sv) is not None: continue
                arr.append((lk, sv))
            if 't3selftk' in FLAGS:   # random kill table read off the sample: entries copy 2..6 letters around a face of a sample row
                TKE = [e for e in TKE if e[0] != d]
                for lk, sv in rng.sample(arr, min(len(arr), 40)):
                    w = [int(c) for c in lk]; s = [int(c) for c in sv]
                    F = [i for i in range(d) if w[i] == 5 and w[(i + 1) % d] == 5 and s[i] == 5]
                    if not F: continue
                    i = rng.choice(F); wc = {0: frozenset([5]), 1: frozenset([5])}; sc = {0: frozenset([5])}
                    for o in rng.sample([-2, -1, 2, 3], rng.randrange(1, 4)): wc[o] = frozenset([w[(i + o) % d]])
                    for o in rng.sample([-2, -1, 1, 2], rng.randrange(1, 4)): sc[o] = frozenset([s[(i + o) % d]])
                    kl = frozenset(rng.sample(LET, rng.choice((1, 1, 2, 2, 3, 5))))
                    TKE.append((d, wc, sc, kl)); TKE.append((d, {1 - o: st for o, st in wc.items()}, {-o: st for o, st in sc.items()}, kl))
            W = window_table_R2(min(d, 9), y, xd, MV2)
            ef = os.path.join(WORK, 't3_eval_d%d.txt' % d); open(ef, 'w').write(''.join('%s %s\n' % a for a in arr))
            T3_EVAL[0] = ef
            if d in (7, 8, 9): F2B_EVAL[0] = None
            rr, dt, ni = run_sep(d, W, 1e9, 1, 0); T3_EVAL[0] = None
            cpp = [r[1] for r in rr if r[0] == 'E']
            assert len(cpp) == len(arr), (len(cpp), len(arr))
            mx = 0.0; worst = None; nface = 0; ndrop = 0; dropbad = 0; ncell2 = 0; ndec = 0; nred = 0
            for (lk, sv), c in zip(arr, cpp):
                w = [int(ch) for ch in lk]; s = [int(ch) for ch in sv]
                cells = fy2_cells(d, w, s)
                if any(w[i] == 5 and w[(i + 1) % d] == 5 and s[i] == 5 for i in range(d)): nface += 1
                if not cells:
                    ndrop += 1
                    if c != 'DROP': dropbad += 1
                    continue
                if c == 'DROP': dropbad += 1; continue
                if TKE and len(cells) < len(list(itertools.product(*[fy2_allowed(s[(i + 1) % d], s[(i - 1) % d]) for i in range(d) if w[i] == 5 and w[(i + 1) % d] == 5 and s[i] == 5]))): nred += 1
                vals = [sum(v * val(k) for k, v in recv_coef_R2(d, lk, sv, 'xon' in FLAGS, tau).items()) for cl, tau in cells]
                pv = max(vals); ncell2 += len(cells) > 1
                if len(set(round(v, 12) for v in vals)) > 1: ndec += 1
                if abs(pv - float(c)) > mx: mx = abs(pv - float(c)); worst = (lk, sv, pv, c)
            log('T3-SELFTEST d=%d: %d arrangements (%d with a face, %d with >1 cell, %d whose cells differ in value, %d excluded by tkill, %d with cells reduced by tkill); max |python max over cells - C++ leaf| = %.3g; drop mismatches %d; tkill entries %d; worst %s'
                % (d, len(arr), nface, ncell2, ndec, ndrop, nred, mx, dropbad, sum(1 for e in TKE if e[0] in (0, d)), worst if mx > 1e-12 else '-'))
            res[d] = (mx, dropbad)
        log('T3-SELFTEST: %s' % ('PASS' if all(m < 1e-12 and b == 0 for m, b in res.values()) else 'FAIL'))
