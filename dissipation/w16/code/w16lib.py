# W16: rows of a periodic (torus) triangulation in the Studio-side engine (st21_w10, W10 copy fa40e97f), fast admissibility,
# and the per-pattern LP (min t over the pattern's own rows + mrow closure).
import sys, os, collections, itertools, time
import numpy as np
sys.path.insert(0, '/tmp/swarm-W16/code')
import torus as TT
NS = None
def init(cert='/mnt/project-files/swarm/round6/W12-studio-K/from_opus/cert_floor_t0.json', extra=None):
    global NS, PATA
    import load21
    import io, contextlib
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf): NS = load21.load(cert, '0', fam=True, extra=extra)
    lines = buf.getvalue().splitlines()
    print('\n'.join(l[:200] for l in lines if l.startswith(('LOWER', 'VERDICT', 'patterns distinct', 'cert rows', 'R5 ', '[load21]'))), flush=True)
    assert not NS['FAIL'], NS['FAIL']
    _r5, _r6 = NS['isR5'], NS['isR6']; C5, C6 = {}, {}
    def isR5c(w):
        w = tuple(w); v = C5.get(w)
        if v is None: v = C5[w] = _r5(w)
        return v
    def isR6c(w):
        w = tuple(w); v = C6.get(w)
        if v is None: v = C6[w] = _r6(w)
        return v
    NS['isR5'] = isR5c; NS['isR6'] = isR6c
    # vectorised pattern table: A[d] (npat, 2d) uint8 allowed-letter masks, 31 = free
    PATA = {}
    if os.environ.get('NOA111') == '1':   # drop every C pattern of the tierA k3x_C_A111 file (non-Lean C) from the matcher
        import re
        fn = '/tmp/swarm-W10/pat/loop__studio__opus_check__f2b041__tierA__k3x_C_A111.cfast'; lines = open(fn).read().splitlines(); drop = set()
        for k, l in enumerate(lines):
            if ' r=' in l and not l.startswith(' '):
                for l2 in lines[k + 1:]:
                    if ' r=' in l2 and not l2.startswith(' '): break
                    if 'C-REDUCIBLE' in l2:
                        nm = l.split()[0]
                        if re.match(r'^[epf]\d+_', nm): drop.add(NS['parse_name'](nm))
                        break
        for d in list(NS['PATL']):
            before = len(NS['PATL'][d]); NS['PATL'][d] = [P for P in NS['PATL'][d] if (d, frozenset(P)) not in drop]
            print('NOA111: d=%d patterns %d -> %d' % (d, before, len(NS['PATL'][d])), flush=True)
    for d, L in NS['PATL'].items():
        A = np.full((len(L), 2 * d), 31, dtype=np.uint8)
        for k, P in enumerate(L):
            for kd, i, S in P:
                m = sum(1 << (x - 5) for x in S); A[k, i if kd == 'w' else d + i] &= m
        # prefilter: required counts per letter class in w and in s (a pattern position whose set lies inside the class)
        REQ = np.zeros((len(L), 2, len(CLASSES)), dtype=np.int16)
        for ci, cm in enumerate(CLASSES):
            inside = (A & ~np.uint8(cm)) == 0   # allowed set within the class
            REQ[:, 0, ci] = inside[:, :d].sum(1); REQ[:, 1, ci] = inside[:, d:].sum(1)
        PATA[d] = (A, REQ)
    return NS
CLASSES = [1, 2, 4, 8, 16, 28]   # {5}, {6}, {7}, {8}, {9}, {7,8,9}

def patmatch_fast(d, w, s):
    if d not in PATA: return False
    A, REQ = PATA[d]
    cw = [sum(1 for x in w if (1 << (x - 5)) & cm) for cm in CLASSES]; cs = [sum(1 for x in s if (1 << (x - 5)) & cm) for cm in CLASSES]
    ok = (REQ[:, 0, :] <= np.array(cw)).all(1) & (REQ[:, 1, :] <= np.array(cs)).all(1)
    A = A[ok]
    if not len(A): return False
    O = np.array([list(a) + list(b) for a, b in TT.dihedral(w, s)], dtype=np.uint8)   # (2d orient, 2d pos)
    bits = (1 << (O - 5)).astype(np.uint8)
    hit = ((A[:, None, :] & bits[None, :, :]) != 0).all(axis=2)
    return bool(hit.any())
_ADM = {}
def admissible_fast(d, w, s):
    key = (d,) + TT.canon_ws(w, s)
    if key in _ADM: return _ADM[key]
    U = min(d, 9); isR5, isR6, canon, RBIG = NS['isR5'], NS['isR6'], NS['canon'], NS['RBIG']; why = None
    for i in range(d):
        if w[i] == 5 and isR5((U, w[(i + 1) % d], s[i], s[(i - 1) % d], w[(i - 1) % d])): why = 'R5'; break
        if w[i] == 6 and all(isR6((U, w[(i + 1) % d], s[i], p, s[(i - 1) % d], w[(i - 1) % d])) for p in NS['LET']): why = 'R6'; break
    if why is None and d in (7, 8) and canon(w) in RBIG: why = 'RBIG'
    if why is None and patmatch_fast(d, w, s): why = 'PAT'
    _ADM[key] = why; return why

def c2(l): return 1 if l >= 7 else 0
def cv(l): return l if l < 7 else 7

def vertex_row(T, v):
    """the LP row label of vertex v: ('S', w, H, F) for a 5, ('C', L, s) for a 6, ('R', d, lk, sv) for d >= 7; canonical."""
    w, s, r, ap = TT.words(T, v); d = len(w)
    if d == 5:
        H = [c2(x) for x in s]; F = []
        for k in range(5):
            if w[k] == 6:
                x = r[k]; rx = T.rot(x); j = rx.index(v); F.append(c2(TT.letter(T.deg[rx[(j + 3) % 6]])))
            else: F.append(-1)
        # canonical over the dihedral group (H like s, F like w)
        best = min(((tuple(a), tuple(b), tuple(f)) for (a, b), f in zip(TT.dihedral(w, H), [o[0] for o in TT.dihedral(F, F)])))
        return ('S',) + best
    if d == 6:
        sc = [cv(x) for x in s]
        return ('C',) + TT.canon_ws(w, sc)
    return ('R', d) + TT.canon_ws(w, s)

def row_status(lab):
    """None if the row is admissible (present in the LP), else the reason."""
    if lab[0] == 'S':
        w, H, F = lab[1], lab[2], lab[3]
        if NS['isR5'](w): return 'R5'
        if max(w) < 7: return 'nobig'
        if sender_coef(lab) is None: return 'R6fan'
        return None
    if lab[0] == 'C':
        return 'R6' if NS['isR6'](lab[1]) else None
    d, w, s = lab[1], lab[2], lab[3]
    return admissible_fast(d, w, s)

_SC = {}
def sender_coef(lab):
    if lab in _SC: return _SC[lab]
    w, H, F = lab[1], lab[2], lab[3]
    sixes = [k for k in range(5) if w[k] == 6]
    r = NS['sender_row'](list(w), {k: H[k] for k in range(5)}, {k: F[k] for k in sixes})
    _SC[lab] = None if r is None else {k: v for k, v in r.items() if v}
    return _SC[lab]
_RC = {}
def recv_coef(lab):
    if lab not in _RC:
        d, w, s = lab[1], lab[2], lab[3]
        _RC[lab] = dict(NS['recv_spec'](d, ''.join(map(str, w)), ''.join(map(str, s))))
    return _RC[lab]
def cons_coef(lab): return dict(NS['cons2_row'](lab[1], lab[2]))

def pattern_rows(T):
    """per-vertex labels and the multiset of labels."""
    labs = [vertex_row(T, v) for v in range(T.n)]
    return labs, collections.Counter(labs)

def label_json(lab):
    """certificate label in the st21 / pcheck format."""
    if lab[0] == 'S':
        w, H, F = lab[1], lab[2], lab[3]
        # st21 requires the canonical word: find the dihedral image with w == canon(w)
        cw = NS['canon'](w)
        for (a, b), (f, _) in zip(TT.dihedral(w, H), TT.dihedral(F, F)):
            if a == cw:
                sixes = [k for k in range(5) if a[k] == 6]
                return ['senderR2', ''.join(map(str, a)), list(b) + ['|'] + [f[k] for k in sixes]]
    if lab[0] == 'C': return ['cons2', list(lab[1]), list(lab[2])]
    return ['receiverR2', lab[1], ''.join(map(str, lab[2])), ''.join(map(str, lab[3]))]

# ---------------- LP ----------------
FAMS = {'base': set(), 'rrz': {'rr', 'z', 'zr'}, 'all': {'rr', 'z', 'zr', 'q', 'Q7'}}
NEWFAM = {'rr', 'z', 'zr', 'q', 'Q7'}
CAP = {'x': 3.0, 'lq': 3.0, 'z': 3.0, 'zr': 3.0, 'rr': 3.0, 'q': 3.0}
def coef_of(lab):
    if lab[0] == 'S': return sender_coef(lab)
    if lab[0] == 'C': return cons_coef(lab)
    return recv_coef(lab)
def closure(keys):
    """mrow rows (h - M <= 0, lq - lQ <= 0, q - Q7 <= 0) for every credit key in keys."""
    out = []
    for k in sorted(keys, key=str):
        if k[0] == 'M':
            for hk in sorted(NS['cand2'](k[1])): out.append((('mrowR2', k[1], hk), {('h', hk): 1, k: -1}))
        elif k[0] == 'lQ':
            sg = k[1]
            if len(sg) == 4: V, c_, a_, m = (8,), sg[1], sg[2], sg[3]
            else: V, c_, a_, m = (), sg[0], sg[1], sg[2]
            for a2 in NS['LET']:
                if (m >> (a2 - 5)) & 1: out.append((('mrowL', sg, V + (c_, a_, a2)), {('lq', V + (c_, a_, a2)): 1, k: -1}))
        elif k[0] == 'Q7':
            for qk in NS['q7cands'](k[1]): out.append((('mrowQ', k[1], qk), {('q', qk): 1, k: -1}))
    return out

def build_lp(labs, fam='all', drop_fam=None):
    """rows of the given labels (only admissible ones), with closure; returns (rowlist, varindex)."""
    off = NEWFAM - FAMS[fam]
    rows = []
    for lab in labs:
        cf = coef_of(lab)
        if cf is None: continue
        cf = {k: v for k, v in cf.items() if k[0] not in off and v != 0}
        if lab[0] == 'S': rows.append((lab, cf, 'ge', 1.0))          # sum + t >= 1
        elif lab[0] == 'C': rows.append((lab, cf, 'eq', 0.0))
        else: rows.append((lab, cf, 'le', float(lab[1] - 6)))     # sum - t <= d - 6
    keys = {k for _, cf, _, _ in rows for k in cf}
    for lab, cf in closure(keys):
        cf = {k: v for k, v in cf.items() if k[0] not in off}
        if len(cf) == 2: rows.append((lab, cf, 'mrow', 0.0))
    return rows

def solve_lp(rows, fix_t=None, obj_extra=None):
    from scipy.optimize import linprog
    from scipy.sparse import coo_matrix
    keys = sorted({k for _, cf, _, _ in rows for k in cf}, key=str); idx = {k: i + 1 for i, k in enumerate(keys)}   # 0 = t
    nv = len(keys) + 1
    Ai, Aj, Av, b = [], [], [], []; Ei, Ej, Ev, be = [], [], [], []; rmap = []
    for lab, cf, kind, rhs in rows:
        if kind == 'ge':   # -(sum) - t <= -1
            r = len(b); rmap.append(('ub', r)); b.append(-rhs); Ai.append(r); Aj.append(0); Av.append(-1.0)
            for k, v in cf.items(): Ai.append(r); Aj.append(idx[k]); Av.append(-float(v))
        elif kind == 'le':
            r = len(b); rmap.append(('ub', r)); b.append(rhs); Ai.append(r); Aj.append(0); Av.append(-1.0)
            for k, v in cf.items(): Ai.append(r); Aj.append(idx[k]); Av.append(float(v))
        elif kind == 'mrow':
            r = len(b); rmap.append(('ub', r)); b.append(0.0)
            for k, v in cf.items(): Ai.append(r); Aj.append(idx[k]); Av.append(float(v))
        else:
            r = len(be); rmap.append(('eq', r)); be.append(0.0)
            for k, v in cf.items(): Ei.append(r); Ej.append(idx[k]); Ev.append(float(v))
    A = coo_matrix((Av, (Ai, Aj)), shape=(len(b), nv)).tocsr() if b else None
    E = coo_matrix((Ev, (Ei, Ej)), shape=(len(be), nv)).tocsr() if be else None
    bounds = [(None, None) if fix_t is None else (fix_t, fix_t)] + [(0.0, CAP.get(k[0])) for k in keys]
    c = np.zeros(nv); c[0] = 1.0
    if fix_t is not None:
        c[0] = 0.0
        if obj_extra:
            for k, v in obj_extra.items():
                if k in idx: c[idx[k]] = v
    res = linprog(c, A_ub=A, b_ub=np.array(b) if b else None, A_eq=E, b_eq=np.array(be) if be else None, bounds=bounds, method='highs')
    return res, keys, rmap

# ---------------- kills of true hidden letters at a payee (pattern-level reducibility through the kill / l3q / f2b masks) ----------------
def privates(T, v):
    """per link position of v: the true hidden letters the payee v cannot see: for a link 6 X, X's neighbour opposite v;
    for a link 7 A, A's letters 3 steps from v on the + side (toward w_{i+1}) and the - side."""
    r = T.rot(v); d = len(r); out = []
    for i in range(d):
        x = r[i]; dx = T.deg[x]
        if dx == 6:
            rx = T.rot(x); j = rx.index(v); out.append((TT.letter(T.deg[rx[(j + 3) % 6]]),))
        elif dx == 7:
            rx = T.rot(x); j = rx.index(v)
            dirp = 1 if rx[(j + 1) % 7] == r[(i + 1) % d] else -1   # direction in A's rotation toward w_{i+1}
            assert rx[(j - dirp) % 7] == r[(i - 1) % d]
            out.append((TT.letter(T.deg[rx[(j + 3 * dirp) % 7]]), TT.letter(T.deg[rx[(j - 3 * dirp) % 7]])))
        else: out.append(())
    return tuple(out)

def payee_kills(d, w, s, pv):
    """list of (position, kind) where a true hidden letter is outside the payee's mask (the arrangement is killed there)."""
    U = min(d, 9); W_ = lambda k: w[k % d]; S_ = lambda k: s[k % d]; out = []
    for i in range(d):
        if w[i] == 6 and d <= 9 or (w[i] == 6):
            p = pv[i][0]
            mk = NS['pmask'](U, W_(i - 2), W_(i - 1), W_(i + 1), W_(i + 2), S_(i - 2), S_(i - 1), S_(i), S_(i + 1))
            if NS['F2BR'] and d <= 9: mk &= ~NS['f2b_extra'](d, w, s, i, ('w6', d))
            if not (mk >> (p - 5)) & 1: out.append((i, 'k6'))
        if w[i] == 7 and d in (7, 8):
            for sg, p in ((1, pv[i][0]), (-1, pv[i][1])):
                c_ = W_(i + sg); a_ = S_(i) if sg == 1 else S_(i - 1); o_ = S_(i - 1) if sg == 1 else S_(i)
                if c_ in (5, 6) and a_ in (5, 6):
                    m_ = (NS['MASK'] if d == 7 else NS['MASK8'])[(sg, c_, a_, W_(i + 2 * sg), W_(i + 3 * sg), W_(i + 4 * sg), o_)]
                    if NS['F2BR']: m_ &= ~NS['f2b_extra'](d, w, s, i, ('w7', d, sg), True)
                    if not (m_ >> (p - 5)) & 1: out.append((i, 'l3q%+d' % sg))
    return out

# ---------------- K* (W6 round 3 deep key, [M] pointer only; not an engine family) ----------------
# K* = EDGE(7->7)[S.L+1=B S.L-1=S S.L-2=5 S.L-3=5 S.A-1=B]; payer pays a per surely-firing oriented slot, payee gets a per
# possibly-firing slot; hidden S.L-3 masked by the l3q V7 table (and not f2b extra7), hidden S.A-1 (c- a 6) by pmask (and not f2b extra6).
FAMS['allK'] = FAMS['all'] | {'K'}; NEWFAM.add('K'); CAP['K'] = 3.0
def kstar_terms(d, w, s):
    if d != 7: return 0, 0
    W_ = lambda k: w[k % d]; S_ = lambda k: s[k % d]; B = lambda x: x >= 7; Sm = lambda x: x <= 6
    pay = get = 0
    for i in range(d):
        if w[i] != 7: continue
        for sg in (1, -1):
            # payer = this centre, payee = w_i
            sa = S_(i - 2) if sg == 1 else S_(i + 1)
            if B(W_(i + sg)) and Sm(W_(i - sg)) and W_(i - 2 * sg) == 5 and W_(i - 3 * sg) == 5 and B(sa): pay += 1
            # payee = this centre, payer = w_i (u); u's frame toward c+ = w_{i+sg}
            cm = W_(i - sg); l2 = S_(i - 1) if sg == 1 else S_(i)
            if not (B(W_(i + sg)) and Sm(cm) and l2 == 5): continue
            sgl = -sg   # engine side of c-
            c_, a_ = W_(i + sgl), (S_(i) if sgl == 1 else S_(i - 1)); o_ = S_(i - 1) if sgl == 1 else S_(i)
            m = NS['MASK'][(sgl, c_, a_, W_(i + 2 * sgl), W_(i + 3 * sgl), W_(i + 4 * sgl), o_)]
            if NS['F2BR']: m &= ~NS['f2b_extra'](d, w, s, i, ('w7', 7, sgl), True)
            if not m & 1: continue                       # S.L-3 = 5 impossible
            if cm == 5:
                X = S_(i - 2) if sg == 1 else S_(i + 1)
                if not B(X): continue
            else:
                j = (i - sg) % d; U = 7
                mk = NS['pmask'](U, W_(j - 2), W_(j - 1), W_(j + 1), W_(j + 2), S_(j - 2), S_(j - 1), S_(j), S_(j + 1))
                if NS['F2BR']: mk &= ~NS['f2b_extra'](d, w, s, j, ('w6', d))
                if not mk & 28: continue
            get += 1
    return pay, get
_coef_base = coef_of
def coef_of(lab):
    cf = _coef_base(lab)
    if cf is not None and lab[0] == 'R' and lab[1] == 7:
        pay, get = kstar_terms(7, lab[2], lab[3])
        if get - pay: cf = dict(cf); cf[('K', 0)] = get - pay
    return cf
