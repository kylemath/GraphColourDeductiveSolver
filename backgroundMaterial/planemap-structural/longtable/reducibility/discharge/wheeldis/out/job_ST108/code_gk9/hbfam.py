# code_gk9 (W17, 10 Nov 2026): HATBB keys HAT(u->b)[ctx], u, b in {7, 8, 9} (9 = 9+), written from W6b's HATBB_SPEC.md (round 7,
# md5 a36ce8d2) only; no Opus / W6b code read. A big payer u pays a big apex b across one of u's link edges (diamond u x b y).
# Rows: receiver rows only (sender / cons2 / mrows have no slot with both endpoints big). Coefficient IN - OUT, where
#   OUT = slots where the row's centre (letter U = min(d, 9)) pays the apex s_i, counted on a SURE match,
#   IN  = slots where the apex s_i pays the centre, counted on a POSSIBLE match.
# Every link edge (w_i, w_{i+1}) of the centre with apex s_i >= 7 gives two oriented slots, (x, y) = (w_i, w_{i+1}) (o = +1) and
# (w_{i+1}, w_i) (o = -1). With a = index of x, b = index of y (b = a + o), A(p, q) = apex between link positions p, q, and
# pv(k, f) = the private of link vertex w_k next to A(k, k + f) (a 5: the other apex A(k, k - f); a 6: its picture set; a 7: its
# picture set on that side; 8+: all):
#   OUT (HATBB_SPEC 3.1): X = w_a, Y = w_b, U-1 = w_{a-o}, U+1 = w_{b+o}, XA = A(a, a-o), YA = A(b, b+o), V-1 = pv(a, o),
#       V+1 = pv(b, -o), U+2 = w_{b+2o}, U+3 = w_{b+3o}, U-2 = w_{a-2o}, U-3 = w_{a-3o}, UA+2 = A(b+o, b+2o), UA+3 = A(b+2o, b+3o),
#       UA-2 = A(a-o, a-2o), UA-3 = A(a-2o, a-3o); all exact letters except V-+1 (picture sets).
#   IN (HATBB_SPEC 3.2): X = w_a, Y = w_b, U-1 = pv(a, o), U+1 = pv(b, -o), XA = far(a, o), YA = far(b, -o) with far(k, f) =
#       w_{k-f} if w_k = 5, A(k, k-f) if w_k = 6, pv(k, -f) if w_k >= 7; V-1 = w_{a-o}, V+1 = w_{b+o}; extended positions wildcard.
# Picture sets (HATBB_SPEC 3, r5lib.recv_pic as for EDGE keys): a link 6's private = pmask & ~f2b extra6 at d <= 9, all at d >= 10;
# a link 7's private on side f = MASK (d = 7) / MASK8 (d = 8) & ~extra7 when w_{k+f} <= 6 and A(k, k+f) <= 6, else all; 8+ all.
import re, collections
HPOS = ['X', 'Y', 'U-1', 'U+1', 'XA', 'YA', 'V-1', 'V+1', 'U+2', 'U+3', 'U-2', 'U-3', 'UA+2', 'UA+3', 'UA-2', 'UA-3']
NPOS = 16
BIGM = 28   # {7, 8, 9}
SYM = {'5': 1, '6': 2, '7': 4, '8': 8, '9': 16, 'S': 3, 'B': 28, '*': 31}
def bit(l): return 1 << (min(l, 9) - 5)
def symmask(t):
    if t in SYM: return SYM[t]
    m_ = re.match(r'^\{([5-9]+)\}$', t)
    if m_: return sum(1 << (int(ch) - 5) for ch in set(m_.group(1)))
    raise ValueError('bad symbol %r' % t)
def msym(m):
    inv = {v: k for k, v in SYM.items()}
    return inv.get(m, '{' + ''.join(str(l) for l in (5, 6, 7, 8, 9) if m >> (l - 5) & 1) + '}')
def is_hat_line(line):
    f = line.split(None, 1)
    return len(f) == 2 and f[1].strip().startswith('HAT(')
def parse_key(line):
    """'NAME HAT(u->b)[POS=SYM ...]' -> (name, payer mask, payee mask, ((pos, mask), ...)); u, b nonempty subsets of {7, 8, 9}"""
    f = line.split(None, 1)
    if len(f) != 2: raise ValueError('bad key line %r' % line)
    name, rule = f[0], f[1].strip()
    m_ = re.match(r'^HAT\(([^-]+)->([^)]+)\)(?:\[(.*)\])?$', rule)
    if not m_: raise ValueError('bad HAT rule %r' % rule)
    U, V = symmask(m_.group(1)), symmask(m_.group(2))
    if not U or U & ~BIGM: raise ValueError('%s: HATBB payer letters must be a nonempty subset of {7, 8, 9} (got %s)' % (name, m_.group(1)))
    if not V or V & ~BIGM: raise ValueError('%s: HATBB payee letters must be a nonempty subset of {7, 8, 9} (got %s)' % (name, m_.group(2)))
    conds = []
    for t in (m_.group(3) or '').split():
        p_, s_ = t.split('=')
        if p_ not in HPOS: raise ValueError('%s: unknown HAT position %s' % (name, p_))
        pi = HPOS.index(p_)
        if any(q == pi for q, _ in conds): raise ValueError('%s: position %s given twice' % (name, p_))
        mk = symmask(s_)
        if not mk or mk & ~31: raise ValueError('%s: empty / bad set at %s' % (name, p_))
        conds.append((pi, mk))
    return name, U, V, tuple(sorted(conds))
def load_keys(fn):
    """the HAT lines of a GK key file (EDGE lines are gkfam's)"""
    keys = []
    for l_ in open(fn):
        l_ = l_.split('#', 1)[0].strip()
        if l_ and is_hat_line(l_): keys.append(parse_key(l_))
    names = [k[0] for k in keys]
    if len(set(names)) != len(names): raise ValueError('duplicate HAT key names')
    return keys
def key_str(k):
    n_, U, V, cd = k
    return '%s HAT(%s->%s)[%s]' % (n_, msym(U), msym(V), ' '.join('%s=%s' % (HPOS[p], msym(m)) for p, m in cd))

class RPic:
    """receiver picture: d, centre letter U, link w (letters), apex s (letters), P6[k] / P7[(k, f)] picture masks (missing = all)"""
    __slots__ = ('d', 'U', 'w', 's', 'P6', 'P7')
    def __init__(self, d, w, s, P6=None, P7=None):
        self.d, self.U, self.w, self.s, self.P6, self.P7 = d, min(d, 9), [min(x, 9) for x in w], [min(x, 9) for x in s], P6 or {}, P7 or {}
    def W(self, k): return self.w[k % self.d]
    def A(self, p, q):   # apex between consecutive link positions p, q
        d = self.d; p %= d; q %= d
        if q == (p + 1) % d: return self.s[p]
        if p == (q + 1) % d: return self.s[q]
        raise ValueError('not adjacent')
    def pv(self, k, f):
        k %= self.d; x = self.w[k]
        if x == 5: return bit(self.A(k, k - f))
        if x == 6: return self.P6.get(k, 31)
        if x == 7: return self.P7.get((k, f), 31)
        return 31
    def far(self, k, f):
        k %= self.d; x = self.w[k]
        if x == 5: return bit(self.W(k - f))
        if x == 6: return bit(self.A(k, k - f))
        return self.pv(k, -f)
    def out_vec(self, i, o):
        a = i if o == 1 else i + 1; b = a + o; W, A = self.W, self.A
        return (bit(W(a)), bit(W(b)), bit(W(a - o)), bit(W(b + o)), bit(A(a, a - o)), bit(A(b, b + o)), self.pv(a, o), self.pv(b, -o),
                bit(W(b + 2 * o)), bit(W(b + 3 * o)), bit(W(a - 2 * o)), bit(W(a - 3 * o)),
                bit(A(b + o, b + 2 * o)), bit(A(b + 2 * o, b + 3 * o)), bit(A(a - o, a - 2 * o)), bit(A(a - 2 * o, a - 3 * o)))
    def in_vec(self, i, o):
        a = i if o == 1 else i + 1; b = a + o; W = self.W
        return (bit(W(a)), bit(W(b)), self.pv(a, o), self.pv(b, -o), self.far(a, o), self.far(b, -o), bit(W(a - o)), bit(W(b + o)),
                31, 31, 31, 31, 31, 31, 31, 31)

def sure(key, ub, vb, vec):
    n_, U, V, cd = key
    return not (ub & ~U) and not (vb & ~V) and all(not (vec[p] & ~m) for p, m in cd)
def poss(key, ub, vb, vec):
    n_, U, V, cd = key
    return bool(ub & U) and bool(vb & V) and all(vec[p] & m for p, m in cd)

def edge_counts(keys, P, i, plant=''):
    """(OUT Counter, IN Counter) by key name of the two oriented slots on the link edge (w_i, w_{i+1}); plant = a planted
    error for the controls only ('outposs': OUT counted on a possible match; 'nomirror': the mirror slot dropped;
    'inmirror': the IN slot's U-1 / U+1 read from the wrong side)"""
    o_, i_ = collections.Counter(), collections.Counter()
    sb = P.s[i % P.d]
    if sb < 7: return o_, i_
    cb, pb = bit(P.U), bit(sb)
    for o in ((1,) if plant == 'nomirror' else (1, -1)):
        ov = P.out_vec(i, o); iv = P.in_vec(i, o)
        if plant == 'inmirror': iv = (iv[0], iv[1], iv[3], iv[2]) + iv[4:]
        for k in keys:
            if (poss if plant == 'outposs' else sure)(k, cb, pb, ov): o_[k[0]] += 1
            if poss(k, pb, cb, iv): i_[k[0]] += 1
    return o_, i_
def row_counts(keys, P, plant=''):
    """IN - OUT by key name over every link edge of the receiver picture P"""
    out = collections.Counter()
    for i in range(P.d):
        o_, i_ = edge_counts(keys, P, i, plant)
        for n_, c_ in i_.items(): out[n_] += c_
        for n_, c_ in o_.items(): out[n_] -= c_
    return out

P6DMAX = 9   # HATBB_SPEC 3: the link-6 private is the picture set at d <= 9, all at d >= 10 (st21 may set it for a comparison run only)
def recv_pic(d, w, s, pmask=None, MASK=None, MASK8=None, extra6=None, extra7=None):
    """the HATBB_SPEC 3 receiver picture: pmask(U, w-2, w-1, w+1, w+2, s-2, s-1, s0, s+1) & ~extra6(k) at d <= 9 (all at d >= 10);
    link 7 side f at d = 7 / 8: MASK / MASK8[(f, c, a, w_{k+2f}, w_{k+3f}, w_{k+4f}, o)] & ~extra7(k, f) when c, a <= 6"""
    w = [min(x, 9) for x in w]; s = [min(x, 9) for x in s]; U = min(d, 9)
    W = lambda k: w[k % d]; S = lambda k: s[k % d]; P6, P7 = {}, {}
    for k in range(d):
        if w[k] == 6 and d <= P6DMAX and pmask is not None:
            m_ = pmask(U, W(k - 2), W(k - 1), W(k + 1), W(k + 2), S(k - 2), S(k - 1), S(k), S(k + 1))
            if extra6 is not None: m_ &= ~extra6(k)
            P6[k] = m_ & 31
        elif w[k] == 7 and d in (7, 8) and MASK is not None:
            for f in (1, -1):
                c_ = W(k + f); a_ = S(k) if f == 1 else S(k - 1); o_ = S(k - 1) if f == 1 else S(k)
                if c_ <= 6 and a_ <= 6:
                    m_ = (MASK if d == 7 else MASK8)[(f, c_, a_, W(k + 2 * f), W(k + 3 * f), W(k + 4 * f), o_)]
                    if extra7 is not None: m_ &= ~extra7(k, f)
                    P7[(k, f)] = m_ & 31
    return RPic(d, w, s, P6, P7)

# ---------------- the separator's per-edge bound (cell = (w_{i-1}, s_{i-1}, w_i) x (s_i, w_{i+1})) ----------------
def edge_bound_vecs(U, wm1, sm1, w0, s0, wp1, wp2, sp1, o):
    """(OUT vector, IN vector) of the slot on edge i with every position outside (w_{i-1}, s_{i-1}, w_i, s_i, w_{i+1}, w_{i+2}, s_{i+1})
    read as the wildcard 31 (OUT only under-credits, IN only over-charges: an upper bound on the exact edge term)"""
    # local letters: link L(-1) = wm1, L(0) = w0, L(1) = wp1, L(2) = wp2; apex A(-1, 0) = sm1, A(0, 1) = s0, A(1, 2) = sp1
    Lk = {-1: wm1, 0: w0, 1: wp1, 2: wp2}; Ak = {-1: sm1, 0: s0, 1: sp1}
    def L(k): return bit(Lk[k]) if k in Lk else 31
    def A(p, q):
        m = min(p, q)
        return bit(Ak[m]) if m in Ak else 31
    def pv(k, f):
        if k not in Lk: return 31
        x = Lk[k]
        if x == 5: return A(k, k - f)
        return 31
    def far(k, f):
        if k not in Lk: return 31
        x = Lk[k]
        if x == 5: return L(k - f)
        if x == 6: return A(k, k - f)
        return 31
    a = 0 if o == 1 else 1; b = a + o
    ov = (L(a), L(b), L(a - o), L(b + o), A(a, a - o), A(b, b + o), pv(a, o), pv(b, -o), L(b + 2 * o), L(b + 3 * o), L(a - 2 * o), L(a - 3 * o),
          A(b + o, b + 2 * o), A(b + 2 * o, b + 3 * o), A(a - o, a - 2 * o), A(a - 2 * o, a - 3 * o))
    iv = (L(a), L(b), pv(a, o), pv(b, -o), far(a, o), far(b, -o), L(a - o), L(b + o)) + (31,) * 8
    return ov, iv
def edge_bound(keys_amt, U, wm1, sm1, w0, s0, wp1):
    """max over (w_{i+2}, s_{i+1}) of the amount-weighted relaxed edge term (IN - OUT), at centre letter U"""
    if s0 < 7: return 0.0
    best = None; cb, pb = bit(U), bit(s0)
    for wp2 in (5, 6, 7, 8, 9):
        for sp1 in (5, 6, 7, 8, 9):
            v = 0.0
            for o in (1, -1):
                ov, iv = edge_bound_vecs(U, wm1, sm1, w0, s0, wp1, wp2, sp1, o)
                for k, a_ in keys_amt:
                    if sure(k, cb, pb, ov): v -= a_
                    if poss(k, pb, cb, iv): v += a_
            if best is None or v > best: best = v
    return best
