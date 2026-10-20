"""Private-cell (q-name) admission guard, Studio, written from PRIVCELL_SPEC.md (Opus s36g, a9da7812) Parts 1 and 3 only;
no Opus code (framecheck.py, privcell.py, eng/) was read.
Part 1: q-name parser, well-formedness (1.5 determinacy), the 2D images and canonical form (1.4), the containment pattern
(vertex list, edges, faces; 1.5) and the g7_ -> q converter (1.6).
Part 3: guard G0..G6 for a two-engine name with its kc line:
  G0 form (parses, well formed, canonical); G1 two engines (D: kc D + dfast18 D; C: kc X + cfast --fixed X leftover 0);
  G2 ring-merge (X merges interior vertices only); G3 interior = named (a bijection kc interior <-> constrained slots
  with equal exact degrees; every constrained char an exact 5..8; a 'u' centre has degree exactly D);
  G4 frame = induced (kc interior edges equal the pattern edges under that bijection);
  G5 faces (every interior triangle of the kc configuration is a frame face of 1.5);
  G6 placement (a '-' name's arc |A| <= D - 1, else 'D only').
G3-G5 are decided by an exhaustive search over all degree-preserving bijections (the name is admitted iff one bijection
passes all three), so the check does not rely on any given frame map.
Admitted names go to out/job30/k3p_D.out / k3p_C.cfast (never k3x); held names to out/job30/privguard_held.log.
Updated for PRIVCELL_SPEC 7ce95033 section 1.9 (points 1 and 2; points 3-6 were already Studio's reading; point 7's
class= hint is optional and ignored, so k3p lines carry none).
Usage: python3 out/job30/privguard.py check  ENTRIES   (lines: g7-or-q-name  kc-line-fields(r m ringadj intadj)  verdict  [X])
       python3 out/job30/privguard.py g7 NAME..      (print the canonical q-name)
       python3 out/job30/privguard.py canon NAME..   (print the canonical form)"""
import sys, os, re, itertools, collections

EXACT = set('5678'); CHARS = set('.5678B9')

# ---------------- parse ----------------
class Name:
    """D, C, link[D], sword[D], priv[D] (exact parent: list of n_i chars; non-exact: ('NX', Lchars, Rchars) with Rchars
    listed R1 first), r3: list of (kind, labels-or-(lab,k), char); labels are ('s', i) / ('p', i, 'L'|'R', k)."""
    pass

def nprivs(ch):
    return int(ch) - 5 if ch in EXACT else None

def parse_lab(t):
    m = re.fullmatch(r's(\d+)', t)
    if m: return ('s', int(m.group(1)))
    m = re.fullmatch(r'p(\d+)([LR])(\d+)', t)
    if m: return ('p', int(m.group(1)), m.group(2), int(m.group(3)))
    raise ValueError('bad label %s' % t)

def parse(s):
    m = re.fullmatch(r'q(\d+)([u-])_([^_]*)_([^_]*)_([^_]*)(?:_([^_]*))?', s)
    if not m: raise ValueError('syntax')
    N = Name(); N.D = int(m.group(1)); N.C = m.group(2); N.link = list(m.group(3)); N.sword = list(m.group(4))
    if N.D < 5 or len(N.link) != N.D or len(N.sword) != N.D: raise ValueError('length')
    if not set(N.link) | set(N.sword) <= CHARS: raise ValueError('chars')
    groups = m.group(5).split(':')
    if len(groups) != N.D: raise ValueError('PRIV groups %d != D' % len(groups))
    N.priv = []
    for i, g in enumerate(groups):
        n = nprivs(N.link[i])
        if n is not None:
            if '*' in g: raise ValueError('* group on exact parent w%d' % i)
            if g and len(g) != n: raise ValueError('group w%d has %d chars, n = %d' % (i, len(g), n))
            if not set(g) <= CHARS: raise ValueError('chars')
            N.priv.append(list(g) if g else ['.'] * n)
        else:
            if g == '': N.priv.append(('NX', [], [])); continue
            if g.count('*') != 1: raise ValueError('non-exact group w%d needs one *' % i)
            L, R = g.split('*')
            if not set(L + R) <= CHARS: raise ValueError('chars')
            N.priv.append(('NX', list(L), list(R)[::-1]))   # R written c'_b..c'_1: store R1 first
    N.r3 = []
    if m.group(6):
        for it in m.group(6).split(','):
            ch, c = it.rsplit('=', 1)
            if c not in CHARS: raise ValueError('chars')
            if '#' in ch:
                lab, k = ch.split('#'); N.r3.append(('hash', (parse_lab(lab), int(k)), c))
            else:
                N.r3.append(('chain', tuple(parse_lab(t) for t in ch.split('/')), c))
    return N

# ---------------- labels, normalisation ----------------
def n_of(N, i): return nprivs(N.link[i % N.D])
def norm_lab(N, lab):
    """exact parent: p_{i,Rk} -> p_{i,L(n+1-k)}"""
    if lab[0] == 'p':
        i = lab[1] % N.D; n = n_of(N, i)
        if n is not None and lab[2] == 'R': return ('p', i, 'L', n + 1 - lab[3])
        return ('p', i, lab[2], lab[3])
    return ('s', lab[1] % N.D)
def lab_str(l): return 's%d' % l[1] if l[0] == 's' else 'p%d%s%d' % (l[1], l[2], l[3])

def priv_slots(N):
    """constrained private slots: label -> char"""
    out = {}
    for i, g in enumerate(N.priv):
        if isinstance(g, tuple):
            for k, c in enumerate(g[1]):
                if c != '.': out[('p', i, 'L', k + 1)] = c
            for k, c in enumerate(g[2]):
                if c != '.': out[('p', i, 'R', k + 1)] = c
        else:
            for k, c in enumerate(g):
                if c != '.': out[('p', i, 'L', k + 1)] = c
    return out

# ---------------- render / images / canonical ----------------
def fwd_sort(N, labs):
    """1.9 point 1: a chain in forward ring-2 order, cyclically: s_{i-1}, p_{i,L1}, .., p_{i,R1}, s_i; the start goes after
    the largest cyclic gap of the positions"""
    D = N.D
    def key(l):
        if l[0] == 's': return ((l[1] + 1) % D, 0)
        return (l[1] % D, l[3] if l[2] == 'L' else 1000 - l[3])
    ks = sorted(set(key(l) for l in labs)); idx = sorted({k[0] for k in ks})
    if len(idx) > 1:
        gaps = [((idx[(j + 1) % len(idx)] - idx[j]) % D, idx[(j + 1) % len(idx)]) for j in range(len(idx))]
        start = max(gaps)[1]
    else: start = idx[0]
    return tuple(sorted(labs, key=lambda l: (((key(l)[0] - start) % D), key(l)[1])))
def render(N):
    gs = []
    for i, g in enumerate(N.priv):
        if isinstance(g, tuple):
            L = ''.join(g[1]).rstrip('.'); R = ''.join(g[2]).rstrip('.')[::-1]   # R stored R1 first; written c'_b..c'_1
            gs.append('' if not L and not R else L + '*' + R)
        else:
            gs.append('' if all(c == '.' for c in g) else ''.join(g))
    items = []
    for kind, x, c in N.r3:
        if kind == 'chain': items.append('/'.join(lab_str(l) for l in fwd_sort(N, [norm_lab(N, l_) for l_ in x])) + '=' + c)
        else: items.append('%s#%d=%s' % (lab_str(x[0]), x[1], c))
    s = 'q%d%s_%s_%s_%s' % (N.D, N.C, ''.join(N.link), ''.join(N.sword), ':'.join(gs))
    return s + ('_' + ','.join(sorted(items)) if items else '')

def r3count(N, lab):
    """ring-3 count m of an exact vertex: deg - 4 for an apex, deg - 3 for a private (1.5); None if not exact"""
    if lab[0] == 's': c = N.sword[lab[1] % N.D]; return int(c) - 4 if c in EXACT else None
    c = priv_slots(N).get(norm_lab(N, lab)); return int(c) - 3 if c in EXACT else None

def image(N, r, refl):
    D = N.D; M = Name(); M.D = D; M.C = N.C
    wi = (lambda i: (r - i) % D) if refl else (lambda i: (i + r) % D)
    si = (lambda i: (r - i - 1) % D) if refl else (lambda i: (i + r) % D)
    M.link = ['.'] * D; M.sword = ['.'] * D; M.priv = [None] * D
    for i in range(D):
        M.link[wi(i)] = N.link[i]; M.sword[si(i)] = N.sword[i]
        g = N.priv[i]
        if isinstance(g, tuple): M.priv[wi(i)] = ('NX', g[2], g[1]) if refl else ('NX', g[1], g[2])
        else: M.priv[wi(i)] = g[::-1] if refl else list(g)
    def ml(l):
        if l[0] == 's': return ('s', si(l[1]))
        side = ({'L': 'R', 'R': 'L'}[l[2]]) if refl else l[2]
        return ('p', wi(l[1]), side, l[3])
    M.r3 = []
    for kind, x, c in N.r3:
        if kind == 'chain':
            labs = [ml(l) for l in x]
            if refl: labs = labs[::-1]
            M.r3.append(('chain', tuple(norm_lab(M, l) for l in labs), c))
        else:
            lab, k = x; m = r3count(N, lab)
            M.r3.append(('hash', (norm_lab(M, ml(lab)), (m + 1 - k) if refl else k), c))
    return M

def canon(N):
    return min(render(image(N, r, f)) for r in range(N.D) for f in (False, True))

# ---------------- well-formedness (1.5 determinacy) ----------------
def ring2_chain(N, i):
    """the ring-2 sequence of w_i when its degree is exact: s_{i-1}, p_{i,L1..Ln}, s_i"""
    n = n_of(N, i); D = N.D
    return [('s', (i - 1) % D)] + [('p', i, 'L', k) for k in range(1, n + 1)] + [('s', i)]

def consecutive(N, a, b):
    """True iff a, b (normalised) are fixed consecutive ring-2 vertices (a then b, forward order)"""
    D = N.D
    if a[0] == 's' and b[0] == 's': return b[1] == (a[1] + 1) % D and N.link[b[1]] == '5'
    if a[0] == 's' and b[0] == 'p': return b[1] == (a[1] + 1) % D and b[2] == 'L' and b[3] == 1
    if a[0] == 'p' and b[0] == 's':
        if b[1] != a[1]: return False
        n = n_of(N, a[1])
        return (a[2] == 'L' and n is not None and a[3] == n) or a[2] == 'R' and a[3] == 1
    if a[0] == 'p' and b[0] == 'p':
        if a[1] != b[1]: return False
        if a[2] == 'L' and b[2] == 'L': return b[3] == a[3] + 1
        if a[2] == 'R' and b[2] == 'R': return a[3] == b[3] + 1
        return False
    return False

def wellformed(N):
    errs = []
    for i, g in enumerate(N.priv):
        if isinstance(g, tuple) and N.link[i] in EXACT: errs.append('w%d exact but group not exact' % i)
    for kind, x, c in N.r3:
        if kind == 'chain':
            labs = [norm_lab(N, l) for l in x]
            for l in labs:
                if l[0] == 'p':
                    n = n_of(N, l[1])
                    if n is not None and not (1 <= l[3] <= n): errs.append('private %s beyond n' % lab_str(l))
            if len(labs) < 2: errs.append('chain of one label')
            for a, b in zip(labs, labs[1:]):
                if not consecutive(N, a, b): errs.append('chain %s/%s not fixed consecutive in ring 2' % (lab_str(a), lab_str(b)))
        else:
            lab, k = x; m = r3count(N, lab)
            if m is None: errs.append('%s#%d needs %s exact' % (lab_str(lab), k, lab_str(lab)))
            elif not 1 <= k <= m: errs.append('%s#%d beyond its ring-3 count %d' % (lab_str(lab), k, m))
    for (_, i, _, k), c in priv_slots(N).items():
        n = n_of(N, i)
        if n is not None and k > n: errs.append('private p%d k=%d > n=%d' % (i, k, n))
    return errs

# ---------------- pattern (1.5) ----------------
def pattern(N):
    """vertex dict {vertex: char}, edge set, face set; vertices: ('u',), ('w', i), ('s', i), private labels, ('t', item)"""
    D = N.D; V = {}
    if N.C == 'u': V[('u',)] = str(N.D)
    for i in range(D):
        if N.link[i] != '.': V[('w', i)] = N.link[i]
        if N.sword[i] != '.': V[('s', i)] = N.sword[i]
    for l, c in priv_slots(N).items(): V[norm_lab(N, l)] = c
    T = []
    for idx, (kind, x, c) in enumerate(N.r3):
        t = ('t', idx); V[t] = c; T.append((t, kind, x))
    def has(v): return v in V
    E = set(); F = set()
    def e(a, b):
        if has(a) and has(b): E.add(frozenset((a, b)))
    def f(a, b, c):
        if has(a) and has(b) and has(c): F.add(frozenset((a, b, c)))
    for i in range(D):
        wi, wj = ('w', i), ('w', (i + 1) % D)
        e(('u',), wi); e(wi, wj); e(wi, ('s', (i - 1) % D)); e(wi, ('s', i))
        f(('u',), wi, wj); f(wi, wj, ('s', i))
        for l in [v for v in V if v[0] == 'p' and v[1] == i]: e(wi, l)
        n = n_of(N, i)
        if n is not None:
            ch = ring2_chain(N, i)
            for a, b in zip(ch, ch[1:]): e(a, b); f(wi, a, b)
        else:
            g = N.priv[i]
            Lch = [('s', (i - 1) % D)] + [('p', i, 'L', k) for k in range(1, len(g[1]) + 1)]
            Rch = [('p', i, 'R', k) for k in range(len(g[2]), 0, -1)] + [('s', i)]
            for part in (Lch, Rch):
                for a, b in zip(part, part[1:]): e(a, b); f(wi, a, b)
    for t, kind, x in T:
        if kind == 'chain':
            labs = [norm_lab(N, l) for l in x]
            for l in labs: e(t, l)
            for a, b in zip(labs, labs[1:]): f(t, a, b)
        else:
            e(t, norm_lab(N, x[0]))
    return V, E, F

def arc(N):
    """minimal cyclic interval of touched link positions (1.4); returns its size"""
    D = N.D; P = set()
    for i in range(D):
        if N.link[i] != '.': P.add(i)
        if N.sword[i] != '.': P |= {i, (i + 1) % D}
    for l in priv_slots(N): P.add(l[1] % D)
    for kind, x, c in N.r3:
        for l in (x if kind == 'chain' else [x[0]]):
            l = norm_lab(N, l); P |= {l[1]} if l[0] == 'p' else {l[1], (l[1] + 1) % D}
    if not P: return 0
    best = D
    for st in range(D):
        L = next(L for L in range(1, D + 1) if P <= {(st + k) % D for k in range(L)})
        best = min(best, L)
    return best

# ---------------- g7 -> q (1.6) ----------------
G7W = [7, 6, 6, 5, 5, 6, 6]
G7SLOTS = [('p', 0, 1), ('p', 0, 2), ('p', 1, 1), ('p', 2, 1), ('p', 5, 1), ('p', 6, 1),
           ('t', (('p', 2, 1), ('s', 2))), ('t', (('s', 2), ('s', 3), ('s', 4))), ('t', 's4'), ('t', (('s', 4), ('p', 5, 1)))]
def g7_to_q(g):
    """returns (q-name string before canonicalisation, map g7 slot label -> q vertex) or raises"""
    m = re.fullmatch(r'g7_([u-])(.{7})_(.{7})_(.{10})', g)
    if not m: raise ValueError('not a g7 name')
    C, W, S, Tt = m.groups(); D = 7
    named_s = {i for i in range(D) if S[i] != '.'}
    tchains = [sl[1] for sl, c in zip(G7SLOTS[6:], Tt[6:]) if c != '.' and isinstance(sl[1], tuple)]
    def named_for(I, k, apex):   # 1.9 point 2
        return apex in named_s or any(('p', I, k) in ch and ('s', apex) in ch for ch in tchains)
    def plab(I, k, constrained_privs):
        """q label of g7 private p_{I,k} (frame n = G7W[I] - 5)"""
        n = G7W[I] - 5
        if W[I] != '.': return ('p', I, 'L', k)
        first, last = k == 1, k == n
        L = first and named_for(I, k, (I - 1) % D)
        R = last and named_for(I, k, I)
        if L and R and n == 1: raise ValueError('p%d%d: both sides apply with n = 1' % (I, k))
        if L: return ('p', I, 'L', 1)
        if R: return ('p', I, 'R', 1)
        raise ValueError('p%d%d: parent free and no named neighbouring apex' % (I, k))
    privs = {}
    cp = [(sl[1], sl[2]) for sl, c in zip(G7SLOTS[:6], Tt[:6]) if c != '.']
    groups = []
    for I in range(D):
        n = G7W[I] - 5
        if W[I] != '.': groups.append([Tt[G7SLOTS.index(('p', I, k))] if ('p', I, k) in G7SLOTS else '.' for k in range(1, n + 1)])
        else: groups.append(('NX', [], []))
    lmap = {}
    for sl, c in zip(G7SLOTS[:6], Tt[:6]):
        I, k = sl[1], sl[2]
        if c == '.' : continue
        lab = plab(I, k, cp); lmap['p%d%d' % (I, k)] = lab
        if W[I] == '.':
            g = groups[I]; side = 1 if lab[2] == 'L' else 2
            while len(g[side]) < lab[3]: g[side].append('.')
            g[side][lab[3] - 1] = c
    r3 = []; tnames = ['t(p21/s2)', 't(s2/s3/s4)', 't(s4)', 't(p51/s4)']
    for sl, c, tn in zip(G7SLOTS[6:], Tt[6:], tnames):
        if c == '.': continue
        if sl[1] == 's4': r3.append(('hash', (('s', 4), 2), c)); continue
        labs = []
        for l in sl[1]:
            if l[0] == 's': labs.append(('s', l[1]))
            else: labs.append(plab(l[1], l[2], cp))
        r3.append(('chain', tuple(labs), c))
    N = Name(); N.D = D; N.C = C; N.link = list(W); N.sword = list(S); N.priv = groups; N.r3 = r3
    return N

# ---------------- kc line ----------------
def kc_graph(fields):
    """fields: r m ringadj intadj -> (m, degree list, interior edge set, interior triangles)"""
    r, m = int(fields[0]), int(fields[1]); rp = fields[2].split(';'); ip = fields[3].split(';')
    E = {u: set() if ip[u] == '-' else {int(x) for x in ip[u].split(',')} for u in range(m)}
    g = [len(E[u]) + (0 if rp[u] == '-' else len(rp[u].split(','))) for u in range(m)]
    ed = {frozenset((a, b)) for a in range(m) for b in E[a]}
    tri = {frozenset((a, b, c)) for a in range(m) for b in E[a] for c in E[a] & E[b] if a < b < c}
    return m, g, ed, tri

def degree_of(v, c): return int(c)

def match(N, kcf):
    """all bijections kc interior -> pattern vertices with equal degrees (G3); for each, G4 (edges equal) and G5 (triangles
    are frame faces). Returns (n_deg_bijections, n_G4, n_G45, example)."""
    V, E, F = pattern(N); m, g, ked, ktri = kc_graph(kcf)
    pv = list(V)
    if len(pv) != m: return 0, 0, 0, None
    cand = {u: [v for v in pv if V[v] in EXACT | set('0123456789') and int(V[v]) == g[u]] for u in range(m)}
    order = sorted(range(m), key=lambda u: len(cand[u]))
    nb = {u: {w for w in range(m) if frozenset((u, w)) in ked} for u in range(m)}
    res = [0, 0, 0, None]; phi = {}
    def rec(k):
        if k == m:
            res[0] += 1
            img = {frozenset(phi[a] for a in e_) for e_ in ked}
            if img == E:
                res[1] += 1
                if all(frozenset(phi[a] for a in t) in F for t in ktri):
                    res[2] += 1
                    if res[3] is None: res[3] = dict(phi)
            return
        u = order[k]
        for v in cand[u]:
            if v in phi.values(): continue
            if any((frozenset((v, phi[w])) in E) != (w in nb[u]) for w in phi): continue   # induced, prune early
            phi[u] = v; rec(k + 1); del phi[u]
    # degree-only count first (G3), without the edge pruning
    deg_count = [0]
    def rec0(k, used):
        if k == m: deg_count[0] += 1; return
        u = order[k]
        for v in cand[u]:
            if v not in used: used.add(v); rec0(k + 1, used); used.discard(v)
    rec0(0, set()); rec(0)
    return deg_count[0], res[1], res[2], res[3]

def ringmerge(x):
    par = {}
    def fd(a):
        while par.setdefault(a, a) != a: a = par[a]
        return a
    for e_ in x:
        a, b = e_.split('-'); par[fd(a)] = fd(b)
    comp = collections.Counter(fd(v) for v in par if v.startswith('R'))
    return max(comp.values(), default=0) >= 2

def guard(name, kcf, verdict, X):
    """returns (admitted?, canonical q-name, per-rule results dict)"""
    R = collections.OrderedDict()
    try:
        N = g7_to_q(name) if name.startswith('g7_') else parse(name)
        q0 = render(N); qc = canon(N); Nc = parse(qc)
        wf = wellformed(Nc); rt = canon(parse(qc)) == qc
        incanon = name.startswith('g7_') or name == qc
        R['G0'] = (not wf and rt and incanon, 'canonical %s; round-trip %s%s%s' % (qc, rt, '' if incanon else '; input not canonical', '; ' + '; '.join(wf) if wf else ''))
    except ValueError as ex:
        R['G0'] = (False, 'parse/convert: %s' % ex); return False, None, R
    R['G1'] = (verdict in ('D', 'C'), verdict)
    R['G2'] = (True, 'n/a (D)') if verdict == 'D' else ((not ringmerge(X.split(',')), 'X={%s}' % X))
    V, E, F = pattern(Nc)
    bad = [c for c in V.values() if c not in EXACT and not (c.isdigit())]
    ok3 = not bad and (Nc.C != 'u' or V[('u',)] == str(Nc.D))
    nd, n4, n45, ex_ = match(Nc, kcf)
    R['G3'] = (ok3 and nd > 0, '%d constrained slots, kc m = %s; degree bijections %d%s' % (len(V), kcf[1], nd, '; open/9 chars %s' % bad if bad else ''))
    R['G4'] = (n4 > 0, 'pattern edges %d; bijections with kc interior edges = pattern edges: %d' % (len(E), n4))
    R['G5'] = (n45 > 0, 'frame faces %d, kc interior triangles %d; bijections also mapping every triangle onto a face: %d' % (len(F), len(kc_graph(kcf)[3]), n45))
    A = arc(Nc)
    R['G6'] = (True, ('u name: placed at d = %d only' % Nc.D) if Nc.C == 'u' else ('|A| = %d <= D - 1 = %d' % (A, Nc.D - 1) if A <= Nc.D - 1 else '|A| = %d: D only' % A))
    return all(v[0] for v in R.values()), qc, R, ex_

if __name__ == '__main__':
    cmd = sys.argv[1]
    if cmd in ('g7', 'canon'):
        for nm in sys.argv[2:]:
            N = g7_to_q(nm) if cmd == 'g7' else parse(nm); print(canon(N))
    elif cmd == 'check':
        HERE = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
        okD, okC, held = [], [], []
        for line in open(sys.argv[2]):
            if not line.strip() or line.startswith('#'): continue
            f = line.split(); nm, kcf, verdict = f[0], f[1:5], f[5]; X = f[6] if len(f) > 6 else ''
            adm, qc, R, ex_ = guard(nm, kcf, verdict, X)
            print('%s -> %s: %s' % (nm, qc, 'ADMITTED' if adm else 'HELD'))
            for k, (ok, why) in R.items(): print('   %s %s  %s' % (k, 'pass' if ok else 'FAIL', why))
            if ex_: print('   bijection: %s' % ', '.join('I%d=%s' % (u, v if isinstance(v, str) else (lab_str(v) if v[0] in 'sp' and len(v) > 2 or v[0] == 's' else ('u' if v == ('u',) else ('w%d' % v[1] if v[0] == 'w' else 't%d' % v[1])))) for u, v in sorted(ex_.items())))
            if adm: (okD if verdict == 'D' else okC).append((qc, nm, kcf, X))
            else: held.append((nm, qc, [k for k, (ok, _) in R.items() if not ok]))
        OUT = os.path.join(HERE, 'out', 'job30')
        with open(os.path.join(OUT, 'k3p_D.out'), 'w') as fo:
            for qc, nm, kcf, X in okD: fo.write('%s %s D=true (two engines; from %s)\n' % (qc, ' '.join(kcf), nm))
        with open(os.path.join(OUT, 'k3p_C.cfast'), 'w') as fo:
            for qc, nm, kcf, X in okC: fo.write('%s %s (from %s)\n  fixed X={%s}: C-REDUCIBLE, leftover bad classes extending after contraction = 0\n' % (qc, ' '.join(kcf), nm, X))
        with open(os.path.join(OUT, 'privguard_held.log'), 'a') as fo:
            for nm, qc, rules in held: fo.write('%s %s held: %s\n' % (nm, qc, ','.join(rules)))
        print('admitted %d D, %d C to k3p (not k3x); held %d' % (len(okD), len(okC), len(held)))
