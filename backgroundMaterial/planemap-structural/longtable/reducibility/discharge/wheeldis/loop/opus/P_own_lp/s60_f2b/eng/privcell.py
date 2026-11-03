# privcell.py (Opus s36g): private-cell names (PRIVCELL_SPEC.md part 1) and their absorption as masks (part 2).
# Standalone (python3 privcell.py canon|g7|pattern NAME...) or exec'd by prelay2.py when OPT has pcell=FILE.
# Absorbed here: (A) filt16 amask bits, (L) l3q mask bits, (F) receiver f-patterns (PATS).  Everything else is logged
# with the reason it is not absorbed (part 2's kill line).
import re, itertools, collections
PC_LET = (5, 6, 7, 8, 9)
PC_CH = {'5': frozenset((5,)), '6': frozenset((6,)), '7': frozenset((7,)), '8': frozenset((8,)),
         'B': frozenset((7, 8, 9)), '9': frozenset((9,))}
PC_INV = {v: k for k, v in PC_CH.items()}
def pc_exact(S):
    """the exact degree a slot set pins (5..8), else None ('B', '9', free)"""
    return next(iter(S)) if S is not None and len(S) == 1 and next(iter(S)) <= 8 else None

class PCName:
    """d, cu (centre in X with exact degree d), W[i], S[i] (frozenset or None), P {(i, side, k): set} (side 'L' from
    s_{i-1}, 'R' from s_i; exact parent -> always 'L'), T {chain: set}; chain = tuple of ring-2 labels in forward order,
    or ('#', label, k) for the k-th ring-3 neighbour of label counted from its ring-2 predecessor's side.
    Ring-2 label: ('s', i) or ('p', i, side, k)."""
    def __init__(s, d, cu, W, S, P, T): s.d, s.cu, s.W, s.S, s.P, s.T = d, cu, list(W), list(S), dict(P), dict(T)
    def npriv(s, i):
        e = pc_exact(s.W[i]); return None if e is None else e - 5

def _lab_parse(t):
    m = re.fullmatch(r's(\d+)', t)
    if m: return ('s', int(m.group(1)))
    m = re.fullmatch(r'p(\d+)([LR])(\d+)', t)
    if m: return ('p', int(m.group(1)), m.group(2), int(m.group(3)))
    raise ValueError('bad ring-2 label %r' % t)
def _lab_str(l): return 's%d' % l[1] if l[0] == 's' else 'p%d%s%d' % l[1:]

def pc_parse(name):
    m = re.fullmatch(r'q(\d+)([u-])_([^_]+)_([^_]+)_([^_]*)(?:_([^_]+))?', name)
    if not m: raise ValueError('not a q-name: %r' % name)
    d = int(m.group(1)); cu = m.group(2) == 'u'; lk, sw, pv, r3 = m.group(3), m.group(4), m.group(5), m.group(6)
    if len(lk) != d or len(sw) != d: raise ValueError('LINK/SWORD length != d in %r' % name)
    rd = lambda ch: None if ch == '.' else PC_CH[ch]
    for ch in lk + sw:
        if ch != '.' and ch not in PC_CH: raise ValueError('bad char %r in %r' % (ch, name))
    W = [rd(c) for c in lk]; S = [rd(c) for c in sw]
    gr = pv.split(':')
    if len(gr) != d: raise ValueError('PRIV needs %d groups in %r' % (d, name))
    N = PCName(d, cu, W, S, {}, {})
    for i, g in enumerate(gr):
        n = N.npriv(i)
        if g == '': continue
        if n is not None:
            if '*' in g or len(g) != n: raise ValueError('group %d of %r: exact parent %d needs %d chars, no *' % (i, name, n + 5, n))
            for k, ch in enumerate(g):
                if ch != '.': N.P[(i, 'L', k + 1)] = PC_CH[ch]
        else:
            if g.count('*') != 1: raise ValueError('group %d of %r: parent not exact, needs one *' % (i, name))
            L, R = g.split('*')
            for k, ch in enumerate(L):
                if ch != '.': N.P[(i, 'L', k + 1)] = PC_CH[ch]
            for k, ch in enumerate(reversed(R)):
                if ch != '.': N.P[(i, 'R', k + 1)] = PC_CH[ch]
    if r3:
        for it in r3.split(','):
            ch, v = it.split('=')
            if '#' in ch:
                a, k = ch.split('#'); key = ('#', _lab_parse(a), int(k))
            else:
                key = tuple(_lab_parse(x) for x in ch.split('/'))
                if len(key) < 2: raise ValueError('chain needs 2+ labels or #k: %r' % it)
            N.T[key] = PC_CH[v]
    return pc_norm(N)

def pc_norm(N):
    """exact parent: R k -> L n+1-k; labels inside chains likewise; validity of k <= n"""
    def fix(l):
        if l[0] != 'p': return ('s', l[1] % N.d)
        i = l[1] % N.d; n = N.npriv(i)
        if n is None: return ('p', i, l[2], l[3])
        k = l[3] if l[2] == 'L' else n + 1 - l[3]
        if not 1 <= k <= n: raise ValueError('private index out of range')
        return ('p', i, 'L', k)
    P = {}
    for (i, sd, k), v in N.P.items():
        l = fix(('p', i, sd, k)); P[l[1:]] = v
    T = {}
    for ch, v in N.T.items():
        T[('#', fix(ch[1]), ch[2]) if ch[0] == '#' else tuple(fix(l) for l in ch)] = v
    N.P, N.T = P, T
    return N

def _r2_order(N, l):
    """position of a ring-2 label in forward ring-2 order (for orienting chains): s_{i-1} < p_{i,L1} < .. < p_{i,R1} < s_i"""
    if l[0] == 's': return (l[1] % N.d, 3, 0)
    i, sd, k = l[1:]; return ((i - 1) % N.d, 1, k) if sd == 'L' else ((i - 1) % N.d, 2, -k)

def pc_render(N):
    ch = lambda S: '.' if S is None else PC_INV[S]
    gr = []
    for i in range(N.d):
        n = N.npriv(i); ks = {(sd, k): v for (j, sd, k), v in N.P.items() if j == i}
        if not ks: gr.append(''); continue
        if n is not None: gr.append(''.join(ch(ks.get(('L', k))) for k in range(1, n + 1)))
        else:
            mL = max([k for sd, k in ks if sd == 'L'], default=0); mR = max([k for sd, k in ks if sd == 'R'], default=0)
            gr.append(''.join(ch(ks.get(('L', k))) for k in range(1, mL + 1)) + '*' + ''.join(ch(ks.get(('R', k))) for k in range(mR, 0, -1)))
    its = []
    for c, v in N.T.items():
        its.append(('%s#%d' % (_lab_str(c[1]), c[2]) if c[0] == '#' else '/'.join(_lab_str(l) for l in c)) + '=' + PC_INV[v])
    s = 'q%d%s_%s_%s_%s' % (N.d, 'u' if N.cu else '-', ''.join(ch(x) for x in N.W), ''.join(ch(x) for x in N.S), ':'.join(gr))
    return s + ('_' + ','.join(sorted(its)) if its else '')

def _outer_count(N, l):
    """number of ring-3 neighbours of ring-2 label l (needs its exact degree, read from S / P)"""
    e = pc_exact(N.S[l[1]] if l[0] == 's' else N.P.get(l[1:]))
    if e is None: raise ValueError('y#k needs the exact degree of y')
    return e - 4 if l[0] == 's' else e - 3

def pc_image(N, r, refl):
    """symmetry w_i -> w_{r+i} (refl False) or w_{r-i} (refl True); s_i -> s_{r+i} or s_{r-i-1}; p_{i,L/R,k} -> same / swapped side"""
    d = N.d
    wi = (lambda i: (r + i) % d) if not refl else (lambda i: (r - i) % d)
    si = (lambda i: (r + i) % d) if not refl else (lambda i: (r - i - 1) % d)
    sw = {'L': 'R', 'R': 'L'}
    def lab(l): return ('s', si(l[1])) if l[0] == 's' else ('p', wi(l[1]), sw[l[2]] if refl else l[2], l[3])
    W = [None] * d; S = [None] * d
    for i in range(d): W[wi(i)] = N.W[i]; S[si(i)] = N.S[i]
    M = PCName(d, N.cu, W, S, {}, {})
    for (i, sd, k), v in N.P.items(): M.P[lab(('p', i, sd, k))[1:]] = v
    for c, v in N.T.items():
        if c[0] == '#': M.T[('#', lab(c[1]), (_outer_count(N, c[1]) + 1 - c[2]) if refl else c[2])] = v
        else: M.T[tuple(reversed([lab(l) for l in c])) if refl else tuple(lab(l) for l in c)] = v
    return pc_norm(M)

def pc_images(N): return [pc_image(N, r, f) for r in range(N.d) for f in (False, True)]
def pc_canon(N): return min(pc_render(M) for M in pc_images(N))

def pc_touched(N):
    t = set(i for i in range(N.d) if N.W[i] is not None)
    for i in range(N.d):
        if N.S[i] is not None: t |= {i, (i + 1) % N.d}
    for (i, sd, k) in N.P: t.add(i)
    for c in N.T:
        for l in ([c[1]] if c[0] == '#' else c):
            if l[0] == 's': t |= {l[1], (l[1] + 1) % N.d}
            else: t.add(l[1])
    return t
def pc_arc(N):
    """minimal cyclic interval (start, length) containing the touched link positions"""
    t = sorted(pc_touched(N)); d = N.d
    if not t: return 0, 0
    best = None
    for a in t:
        ln = max((x - a) % d for x in t) + 1
        if best is None or ln < best[1]: best = (a, ln)
    return best
def pc_degrees(N):
    """centre degrees d' at which N can be placed: d' = d if the centre is in X; else d and every d' >= arc + 1 (>= 5)"""
    if N.cu: return lambda dd: dd == N.d
    a0, ln = pc_arc(N); return lambda dd: dd == N.d or dd >= max(5, ln + 1)

def pc_pattern(N):
    """containment pattern: (vertex -> letter set, edge list) of the named (constrained) vertices, edges = frame adjacencies"""
    d = N.d; V = {}
    if N.cu: V['u'] = frozenset((d,))
    for i in range(d):
        if N.W[i] is not None: V['w%d' % i] = N.W[i]
        if N.S[i] is not None: V['s%d' % i] = N.S[i]
    for (i, sd, k), v in N.P.items(): V['p%d%s%d' % (i, sd, k)] = v
    for c, v in N.T.items(): V['t(' + ('%s#%d' % (_lab_str(c[1]), c[2]) if c[0] == '#' else '/'.join(_lab_str(l) for l in c)) + ')'] = v
    E = set()
    def e(a, b):
        if a in V and b in V: E.add(tuple(sorted((a, b))))
    for i in range(d):
        j = (i + 1) % d; n = N.npriv(i)
        e('u', 'w%d' % i); e('w%d' % i, 'w%d' % j); e('w%d' % i, 's%d' % i); e('w%d' % j, 's%d' % i)
        for (i2, sd, k) in N.P:
            if i2 == i: e('w%d' % i, 'p%d%s%d' % (i, sd, k))
        if n is not None:   # ring-2 chain s_{i-1} - p_{i,L1} - .. - p_{i,Ln} - s_i is determined
            ch = ['s%d' % ((i - 1) % d)] + ['p%dL%d' % (i, k) for k in range(1, n + 1)] + ['s%d' % i]
        else:               # only the ends are determined: s_{i-1} - L1 - .. - Lk  and  R k - .. - R1 - s_i
            mL = max([k for (i2, sd, k) in N.P if i2 == i and sd == 'L'], default=0); mR = max([k for (i2, sd, k) in N.P if i2 == i and sd == 'R'], default=0)
            ch = ['s%d' % ((i - 1) % d)] + ['p%dL%d' % (i, k) for k in range(1, mL + 1)]
            for a, b in zip(ch, ch[1:]): e(a, b)
            ch = ['p%dR%d' % (i, k) for k in range(mR, 0, -1)] + ['s%d' % i]
        for a, b in zip(ch, ch[1:]): e(a, b)
    for c in N.T:
        t = 't(' + ('%s#%d' % (_lab_str(c[1]), c[2]) if c[0] == '#' else '/'.join(_lab_str(l) for l in c)) + ')'
        for l in ([c[1]] if c[0] == '#' else c): e(t, _lab_str(l))
    return V, sorted(E)


def pc_cons2_sites(N):
    """link positions i with w_i exact 6 whose 6-centred 2-ball (link u, w_{i-1}, s_{i-1}, p_i, s_i, w_{i+1} and the six
    apexes) holds every constrained slot, as far as the name's exact degrees determine those apexes (report only)"""
    d = N.d; out = []
    for i in range(d):
        if pc_exact(N.W[i]) != 6: continue
        a, b = (i - 1) % d, (i + 1) % d
        ball = {('w', a), ('w', b), ('s', a), ('s', i), ('p', i, 'L', 1), ('w', (i - 2) % d), ('w', (i + 2) % d)}
        if N.cu: ball.add(('u',))
        na, nb = N.npriv(a), N.npriv(b)
        ball.add(('s', (a - 1) % d) if na == 0 else ('p', a, 'L', na) if na else ('p', a, 'R', 1))
        ball.add(('s', b) if nb == 0 else ('p', b, 'L', 1))
        ts = {(('s', a), ('p', i, 'L', 1)), (('p', i, 'L', 1), ('s', i))}
        named = {('w', j) for j in range(d) if N.W[j] is not None and j != i} | {('s', j) for j in range(d) if N.S[j] is not None} | {('p',) + k for k in N.P}
        if N.cu: named.add(('u',))
        if named <= ball and all(c[0] != '#' and len(c) == 2 and tuple(c) in ts for c in N.T): out.append(i)
    return out

# ---------------- g7_ -> q conversion (names on the row 7 7665566/6765766, RELAY_SPEC_s20 s25c-g) ----------------
G7_FRAME_W = [7, 6, 6, 5, 5, 6, 6]
G7_SLOTS = ['p01', 'p02', 'p11', 'p21', 'p51', 'p61', 'tp21/s2', 'ts2/s3/s4', 'ts4', 'tp51/s4']
def g7_to_q(nm):
    f = nm.split('_'); lk, sw, sl = f[1], f[2], f[3]
    assert len(lk) == 8 and len(sw) == 7 and len(sl) == 10, nm
    W = [None if c == '.' else PC_CH[c] for c in lk[1:]]; S = [None if c == '.' else PC_CH[c] for c in sw]
    N = PCName(7, lk[0] == 'u', W, S, {}, {})
    named = {('s', i) for i in range(7) if S[i] is not None}
    for k, ch in enumerate(sl):   # apexes that share a ring-3 chain with a private count as its named neighbours
        x = G7_SLOTS[k]
        if ch != '.' and x[0] == 't': named |= {('s', int(y[1:])) for y in x[1:].split('/') if y[0] == 's'}
    def plab(I, K):
        """g7 private p_{I,K} (frame degree of w_I known).  Name pins w_I: L K.  Otherwise the label must keep the
        frame adjacency to a named apex: K = 1 next to s_{I-1} -> L1; K = n next to s_I -> R1; both named with n = 1
        cannot be written without pinning w_I (refused)."""
        n = G7_FRAME_W[I] - 5
        if N.npriv(I) is not None: return ('p', I, 'L', K)
        left = K == 1 and ('s', (I - 1) % 7) in named; right = K == n and ('s', I) in named
        if left and right: raise ValueError('%s: p%d%d touches two named apexes, parent not pinned' % (nm, I, K))
        if right: return ('p', I, 'R', n + 1 - K)
        if left: return ('p', I, 'L', K)
        return ('p', I, 'L', K) if K <= (n + 1) // 2 else ('p', I, 'R', n + 1 - K)
    def lab(x): return ('s', int(x[1:])) if x[0] == 's' else plab(int(x[1]), int(x[2]))
    for k, ch in enumerate(sl):
        if ch == '.': continue
        x = G7_SLOTS[k]; v = PC_CH[ch]
        if x[0] == 'p': N.P[lab(x)[1:]] = v
        else:
            ls = [lab(y) for y in x[1:].split('/')]
            if len(ls) == 1:   # t(s4) of the frame: the 2nd ring-3 neighbour of s4 from s3's side (t(s2/s3/s4), t(s4), t(s4/p51))
                N.T[('#', ls[0], 2)] = v
            else: N.T[tuple(sorted(ls, key=lambda l: _r2_order(N, l)))] = v
    return pc_norm(N)

# ---------------- absorption (part 2) ----------------
def _rel(N, j, i, dd=None):
    """offset of link position i from the anchor spoke j: along the arc for a centre-free name, mod d for a centred one"""
    d = N.d
    if N.cu:
        x = (i - j) % d; return x - d if x > d // 2 else x
    a0, ln = pc_arc(N); return (i - a0) % d - (j - a0) % d
def pc_classify(N):
    """-> ('F', None) f-pattern | ('A', (j, label)) one private of a 6-able spoke | ('L', (j, sg)) | (None, reason)"""
    if N.T: return None, 'ring-3 slot(s) %s: no row of the engine reads ring 3 except cons2/cluster rows' % len(N.T)
    if not N.P: return 'F', None
    if len(N.P) > 1: return None, '%d constrained privates: joint cell, not a product of per-spoke masks' % len(N.P)
    (j, sd, k), = N.P.keys()
    return 'P', (j, sd, k)
def pc_window_sets(N, j, wR, sR):
    """readable link offsets wR and apex offsets sR around anchor spoke j -> (offset -> set for w, for s), or None if a
    constrained slot falls outside (strict rule: an unknown is never matched).  Centred name: offsets compared mod d
    (the context has degree d); centre-free name: offsets along its arc."""
    w = {}; s = {}
    def place(i, R):
        o = _rel(N, j, i)
        if not N.cu: return o if o in R else None
        hit = [r for r in R if (r - o) % N.d == 0]
        return hit[0] if len(hit) == 1 else None
    for i in range(N.d):
        if N.W[i] is not None:
            o = place(i, wR)
            if o is None: return None
            w[o] = N.W[i]
        if N.S[i] is not None:
            o = place(i, sR)
            if o is None: return None
            s[o] = N.S[i]
    return w, s
PC_LOG = []
def pc_build(names, kt_shape=(5,) * 8, dmax=17):
    """names (q-form strings) -> (AM {U: uint8 array of extra kill bits}, L3 {(sg,c,w2,w3,w4,a,o): bits}, PATS {d: set})"""
    import numpy as np
    AM = {U: np.zeros(kt_shape, dtype=np.uint8) for U in (7, 8, 9)}; L3 = collections.defaultdict(int)
    PT = collections.defaultdict(set); idx = lambda S: [PC_LET.index(x) for x in (S if S is not None else PC_LET)]
    for nm in names:
        N0 = pc_parse(nm); cn = pc_canon(N0); kind, info = pc_classify(N0); sites = collections.Counter()
        okd = pc_degrees(N0)
        if kind == 'F':
            for dd in range(7, dmax + 1):
                if not okd(dd): continue
                for M in pc_images(N0):
                    if dd == M.d: sl = [(('w', i), M.W[i]) for i in range(dd) if M.W[i]] + [(('s', i), M.S[i]) for i in range(dd) if M.S[i]]
                    else:
                        a0, ln = pc_arc(M)
                        sl = [(('w', (i - a0) % M.d), M.W[i]) for i in range(M.d) if M.W[i]] + [(('s', (i - a0) % M.d), M.S[i]) for i in range(M.d) if M.S[i]]
                    PT[dd].add(tuple(sorted(sl))); sites['F%d' % dd] += 1
        elif kind == 'P':
            for M in pc_images(N0):
                (j, sd, k), = M.P.keys(); pset = M.P[(j, sd, k)]; bits = sum(1 << PC_LET.index(x) for x in pset)
                par = M.W[j]
                # (A) filt16 amask: 6 at w_j, its single private (L1 = R1), window w_{j-2..j+2}, s_{j-2..j+1}
                if k == 1 and (par is None or 6 in par):
                    ws = pc_window_sets(M, j, (-2, -1, 0, 1, 2), (-2, -1, 0, 1))
                    Us = [U for U in (7, 8, 9) if (okd(U) if U < 9 else (not M.cu and max(5, pc_arc(M)[1] + 1) <= 9))]   # U = 9 is 'd >= 9': a centre-free name placeable at every d >= 9
                    if M.cu and M.d >= 9: Us = []
                    if ws is not None and Us:
                        w, s = ws
                        if 0 not in w or 6 in w[0]:
                            ax = [idx(w.get(-2)), idx(w.get(-1)), idx(w.get(1)), idx(w.get(2)), idx(s.get(-2)), idx(s.get(-1)), idx(s.get(0)), idx(s.get(1))]
                            for U in Us:
                                AM[U][np.ix_(*ax)] |= bits
                                sites['A%d' % U] += 1
                # (L) l3q: payer 7 at w_j (in the payee v's frame, d = 7), private adjacent to apex a; L1 -> sg = -1, R1 (= L2 of a 7) -> +1
                if okd(7) and (par is None or 7 in par):
                    # in a 7-context the parent has 2 privates: L1 = R2 (adjacent s_{j-1}) -> sg = -1; L2 = R1 (adjacent s_j) -> sg = +1
                    sg = {('L', 1): -1, ('R', 2): -1, ('L', 2): 1, ('R', 1): 1}.get((sd, k), 0)
                    if sg and not (M.cu and M.d != 7):
                        ws = pc_window_sets(M, j, tuple(sg * t_ for t_ in range(5)), (-1, 0))
                        if ws is not None:
                            w, s = ws
                            if 0 not in w or 7 in w[0]:
                                a_ = s.get(0 if sg == 1 else -1); o_ = s.get(-1 if sg == 1 else 0)
                                for c, w2, w3, w4, a, o in itertools.product(*[sorted(w.get(sg * t_) or PC_LET) for t_ in (1, 2, 3, 4)], sorted(a_ or PC_LET), sorted(o_ or PC_LET)):
                                    if c <= 6 and a <= 6: L3[(sg, c, w2, w3, w4, a, o)] |= bits; sites['L'] += 1
        why = info if kind is None else ('' if sites else 'single private but no window holds every constrained slot (strict rule): needs a wider window / new separator state')
        c2s = pc_cons2_sites(N0)
        if c2s: why += ' [cons2-row skip possible at 6 w%s; not applied]' % c2s
        PC_LOG.append((nm, cn, kind, dict(sites), why))
    return AM, dict(L3), PT

if __name__ == '__main__':
    import sys
    cmd = sys.argv[1]
    for a in sys.argv[2:]:
        if cmd == 'g7':
            q = g7_to_q(a); print(a, pc_canon(q))
        elif cmd == 'canon': print(a, pc_canon(pc_parse(a)))
        elif cmd == 'pattern':
            N = pc_parse(a); V, E = pc_pattern(N); print(a); print('  V', {k: sorted(v) for k, v in V.items()}); print('  E', E); print('  arc', pc_arc(N))
