# W17 round 4 (swarm round 6, 6 Nov 2026): W6's generic 2-ball keys ("KS keys", EDGE(u->v)[...] with u, v letters or letter sets)
# for the Studio-side upper checker. Written from W6's KEYSPEC.md (round7) and Opus's DUAL_EXPORT.md (gkwin paragraph) only;
# no Opus code (eng/edge56.py, jsepf_gk.cpp not read). Used by st21_w17.py (rows, window tables) in code_gk/.
#
# Semantics (KEYSPEC 2-5). A key moves DEBT from the payer u to the payee v. It is matched on every oriented pair (u, v) with
# both chiralities; each match counts once. A row is the constraint of one centre c, read on a PICTURE (letter set per vertex):
#   OUT slot (c pays, c -> link vertex): counts iff it SURELY matches (every set inside the key's set, endpoints included);
#   IN slot (link vertex pays c): counts iff it POSSIBLY matches (every set meets the key's set).
#   coefficient: sender (c = 5) OUT - IN (row >= 1 - t); receiver and cons2 (c = 7+, 6) IN - OUT (rows <= d - 6 + t, <= t).
# Positions (indices mod n, A(a, b) = apex between consecutive link positions a, b; priv(k, f) = the private of link vertex k
# next to A(k, k + f): link 5 -> the other apex A(k, k - f); link 6 -> its one private; link 7 -> the private on that side;
# link 8+ -> wildcard):
#   OUT c -> L_i, chirality sg: S.L+k = L_{i+k sg}, S.L-k = L_{i-k sg} (k = 1..3), S.A+1 = A(i+sg, i+2sg), S.A-1 = A(i-sg, i-2sg),
#       R.L+2 = A(i, i+sg), R.L-2 = A(i, i-sg).
#   IN L_i -> c, chirality e (S.L+1 = L_{i+e}): S.L+-1 = L_{i+-e}, S.L+-2 = A(i, i+-e), S.L+-3 = priv(i, +-e),
#       S.A+1 = priv(i+e, -e) (L_{i+e}'s vertex next to A(i, i+e) other than L_i), S.A-1 = priv(i-e, +e), R.L+-2 = L_{i+-2e}.
# Pictures: sender (w, H, F): apex S / B by H, link 6 private S / B by F, 7+ privates wildcard. cons2 (L, s): apex S (s <= 6) /
# B (s >= 7), every private wildcard. Receiver d = 7 (KEYSPEC 5): apex exact; link 6 private pmask(7, window) & ~f2b extra6;
# link 7 private on side f: l3q MASK & ~f2b extra7 when L_{k+f} <= 6 and A(k, k+f) <= 6, else wildcard.
# Receiver d >= 8 (DUAL_EXPORT gkwin, a bound): IN per link position j (payer W[j] in {5, ..., 9}) from the window
# (w_{j-2..j+2}, s_{j-2..j+1}) only: payer 6 private pmask(U, window) (no extra6), payer 7+ privates wildcard, neighbour 6 private
# pmask OR-ed over its two letters outside the window, neighbour 7+ private wildcard, neighbour 5 -> the apex beyond (exact).
# code_gk8 (W17, 9 Nov 2026, from W6b's PAYER8SPEC.md, W5 reading; no Opus code): payer letters 8 / 9 (exactly {8} or exactly {9};
# S.L+-3 refused for them). OUT at d >= 8 (centre U = min(d, 9) pays w_i; payer-8 keys only at U = 8, payer-9 keys at U = 9): SURE
# match on the window W_i = (w_{i-2..i+2}, s_{i-2..i+1}): sg = +1: S.L+-1 = w_{i+-1}, S.L+-2 = w_{i+-2}, S.A+1 = s_{i+1},
# S.A-1 = s_{i-2}, R.L+2 = s_i, R.L-2 = s_{i-1}, S.L+-3 wildcard; sg = -1 mirrors. Window rows: IN - OUT.
import re, collections
LET = (5, 6, 7, 8, 9)
SYM = {'5': 1, '6': 2, '7': 4, '8': 8, '9': 16, 'S': 3, 'B': 28, '*': 31}
EPOS = ['S.L+1', 'S.L+2', 'S.L+3', 'S.L-1', 'S.L-2', 'S.L-3', 'S.A+1', 'S.A-1', 'R.L+2', 'R.L+3', 'R.L-2', 'R.L-3', 'R.A+1', 'R.A-1']
EMIRROR = [3, 4, 5, 0, 1, 2, 7, 6, 10, 11, 8, 9, 13, 12]
ALLOWED = (0, 1, 2, 3, 4, 5, 6, 7, 8, 10)
P8BAD = (2, 5, 9, 11, 12, 13)   # code_gk8: S.L+3, S.L-3, R.L+3, R.L-3, R.A+1, R.A-1 refused for a payer 8 / 9
S_, B_ = 3, 28
def bit(l): return 1 << (min(l, 9) - 5)
def symmask(t):
    if t in SYM: return SYM[t]
    m_ = re.match(r'^\{([5-9]+)\}$', t)
    if m_: return sum(1 << (int(ch) - 5) for ch in set(m_.group(1)))
    raise ValueError('bad symbol %r' % t)
def msym(m):
    inv = {v: k for k, v in SYM.items()}
    return inv.get(m, '{' + ''.join(str(l) for l in LET if m >> (l - 5) & 1) + '}')
def parse_key(line):
    """'NAME EDGE(U->V)[POS=SYM ...]' -> (name, payer mask, payee mask, ((pos, mask), ...)); refuses positions outside the payer
    2-ball; payer letters must be a nonempty subset of {5, 6, 7}, or exactly {8}, or exactly {9} (code_gk8, PAYER8SPEC); a payer-8/9
    key may not constrain S.L+3 / S.L-3 (wildcard for a payer >= 8, W5 reading)"""
    f = line.split(None, 1)
    if len(f) != 2: raise ValueError('bad key line %r' % line)
    name, rule = f[0], f[1].strip()
    m_ = re.match(r'^EDGE\(([^-]+)->([^)]+)\)(?:\[(.*)\])?$', rule)
    if not m_: raise ValueError('bad rule %r' % rule)
    U, V = symmask(m_.group(1)), symmask(m_.group(2))
    if not U or (U & ~7 and U not in (8, 16)):
        raise ValueError('%s: payer letters must be a nonempty subset of {5, 6, 7}, or exactly {8}, or exactly {9} (got %s; split a mixed '
                         'payer set into single-letter keys)' % (name, m_.group(1)))
    if not V: raise ValueError('%s: empty payee set' % name)
    conds = []
    for t in (m_.group(3) or '').split():
        p_, s_ = t.split('=')
        if p_ not in EPOS: raise ValueError('%s: unknown position %s' % (name, p_))
        pi = EPOS.index(p_)
        if pi not in ALLOWED: raise ValueError('%s: position %s is outside the payer 2-ball (refused)' % (name, p_))
        if U in (8, 16) and pi in P8BAD: raise ValueError('%s: position %s is the wildcard for a payer 8 / 9 (PAYER8SPEC W5: refused)' % (name, p_))
        if any(q == pi for q, _ in conds): raise ValueError('%s: position %s given twice' % (name, p_))
        mk = symmask(s_)
        if not mk: raise ValueError('%s: empty set at %s' % (name, p_))
        conds.append((pi, mk))
    return name, U, V, tuple(sorted(conds))
def load_keys(fn):
    keys = []
    for l_ in open(fn):
        l_ = l_.split('#', 1)[0].strip()
        if l_: keys.append(parse_key(l_))
    names = [k[0] for k in keys]
    if len(set(names)) != len(names): raise ValueError('duplicate key names')
    return keys
def key_str(k):
    n_, U, V, cd = k
    return '%s EDGE(%s->%s)[%s]' % (n_, msym(U), msym(V), ' '.join('%s=%s' % (EPOS[p], msym(m)) for p, m in cd))
def mirror_key(k, name=None):
    n_, U, V, cd = k
    return (name or n_ + 'm', U, V, tuple(sorted((EMIRROR[p], m) for p, m in cd)))

class Pic:
    """n = centre degree, C = centre letter mask, L = link letters (ints), A = apex masks (A[i] between L[i], L[i+1]),
    P6[k] = mask of the private of a link 6, P7[(k, f)] = mask of a link 7's private next to A(k, k+f); missing = wildcard"""
    __slots__ = ('n', 'C', 'L', 'A', 'P6', 'P7')
    def __init__(self, n, C, L, A, P6=None, P7=None):
        self.n, self.C, self.L, self.A, self.P6, self.P7 = n, C, list(L), list(A), P6 or {}, P7 or {}
    def ab(self, a, b):
        n = self.n; a %= n; b %= n
        if b == (a + 1) % n: return self.A[a]
        if a == (b + 1) % n: return self.A[b]
        raise ValueError('not adjacent')
    def lk(self, k): return bit(self.L[k % self.n])
    def priv(self, k, f):
        k %= self.n; x = self.L[k]
        if x == 5: return self.ab(k, k - f)
        if x == 6: return self.P6.get(k, 31)
        if x == 7: return self.P7.get((k, f), 31)
        return 31
    def out_vec(self, i, sg):
        lk, ab = self.lk, self.ab
        return (lk(i + sg), lk(i + 2 * sg), lk(i + 3 * sg), lk(i - sg), lk(i - 2 * sg), lk(i - 3 * sg),
                ab(i + sg, i + 2 * sg), ab(i - sg, i - 2 * sg), ab(i, i + sg), 0, ab(i, i - sg))
    def in_vec(self, i, e):
        lk, ab, pv = self.lk, self.ab, self.priv
        return (lk(i + e), ab(i, i + e), pv(i, e), lk(i - e), ab(i, i - e), pv(i, -e),
                pv(i + e, -e), pv(i - e, e), lk(i + 2 * e), 0, lk(i - 2 * e))

class Engine:
    """key list + memoised slot evaluation: slot context -> tuple of key indices that count"""
    def __init__(self, keys):
        self.keys = keys; self.names = [k[0] for k in keys]; self.memo_out = {}; self.memo_in = {}
    def out_hits(self, ub, vb, vec):   # SURE: payer ub inside U, payee vb inside V, each position inside the key's set
        ck = (ub, vb, vec); r = self.memo_out.get(ck)
        if r is None:
            r = tuple(q for q, (n_, U, V, cd) in enumerate(self.keys)
                      if not (ub & ~U) and not (vb & ~V) and all(not (vec[p] & ~m) for p, m in cd))
            if len(self.memo_out) > 2000000: self.memo_out.clear()
            self.memo_out[ck] = r
        return r
    def in_hits(self, ub, vb, vec):    # POSSIBLE: every set meets the key's set
        ck = (ub, vb, vec); r = self.memo_in.get(ck)
        if r is None:
            r = tuple(q for q, (n_, U, V, cd) in enumerate(self.keys)
                      if (ub & U) and (vb & V) and all(vec[p] & m for p, m in cd))
            if len(self.memo_in) > 2000000: self.memo_in.clear()
            self.memo_in[ck] = r
        return r
    def pic_counts(self, P, out_on=True):
        """(out Counter, in Counter) over key names"""
        o, i_ = collections.Counter(), collections.Counter()
        for i in range(P.n):
            for sg in (1, -1):
                if out_on:
                    for q in self.out_hits(P.C, P.lk(i), P.out_vec(i, sg)): o[self.names[q]] += 1
                for q in self.in_hits(P.lk(i), P.C, P.in_vec(i, sg)): i_[self.names[q]] += 1
        return o, i_

def sender_pic(w, H, F):
    """KEYSPEC 5 sender label (w, H, F): apex h_k between w_k, w_{k+1} = S (H_k = 0) / B (H_k = 1); a link 6's private S / B by F_k"""
    return Pic(5, bit(5), w, [B_ if H[k] else S_ for k in range(5)], {k: (B_ if F[k] else S_) for k in range(5) if w[k] == 6})
def cons2_pic(L, s):
    """KEYSPEC 5 cons2 label (L, s): apex S if s_i <= 6 (5 and 6 are the ap witness of {5, 6}), B if s_i >= 7; privates wildcard"""
    return Pic(6, bit(6), L, [B_ if x >= 7 else S_ for x in s])
def recv7_pic(w, s, pmask, MASK, extra6, extra7):
    """KEYSPEC 5 receiver picture, d = 7 (exact apexes, l3q MASK and pmask with the f2b extras removed)"""
    d = 7; W = lambda k: w[k % d]; S = lambda k: s[k % d]
    P6, P7 = {}, {}
    for k in range(d):
        if w[k] == 6:
            P6[k] = pmask(7, W(k - 2), W(k - 1), W(k + 1), W(k + 2), S(k - 2), S(k - 1), S(k), S(k + 1)) & ~extra6(k) & 31
        elif w[k] == 7:
            for f in (1, -1):
                c_ = W(k + f); a_ = S(k) if f == 1 else S(k - 1); o_ = S(k - 1) if f == 1 else S(k)
                if c_ <= 6 and a_ <= 6:
                    P7[(k, f)] = MASK[(f, c_, a_, W(k + 2 * f), W(k + 3 * f), W(k + 4 * f), o_)] & ~extra7(k, f) & 31
    return Pic(d, bit(7), w, [bit(x) for x in s], P6, P7)

# ---------------- gkwin (d >= 8 rows; the window bound everywhere) ----------------
class Win:
    """payee credit of one link position j from its window (wm2, wm1, w0, wp1, wp2, sm2, sm1, s0, sp1) = (w_{j-2..j+2},
    s_{j-2..j+1}) at centre letter U: per key the number of chiralities in which the IN slot w_j -> c possibly matches"""
    def __init__(self, eng, pmask):
        self.eng = eng; self.pmask = pmask; self.orp = {}; self.orm = {}; self.memo = {}
    def or_plus(self, U, wm1, w0, wp2, sm1, s0, sp1):   # the link 6 at j+1: OR over w_{j+3}, s_{j+2}
        k_ = (U, wm1, w0, wp2, sm1, s0, sp1); r = self.orp.get(k_)
        if r is None:
            r = 0
            for x in LET:
                for y in LET: r |= self.pmask(U, wm1, w0, wp2, x, sm1, s0, sp1, y)
            self.orp[k_] = r
        return r
    def or_minus(self, U, wm2, w0, wp1, sm2, sm1, s0):  # the link 6 at j-1: OR over w_{j-3}, s_{j-3}
        k_ = (U, wm2, w0, wp1, sm2, sm1, s0); r = self.orm.get(k_)
        if r is None:
            r = 0
            for x in LET:
                for y in LET: r |= self.pmask(U, x, wm2, w0, wp1, y, sm2, sm1, s0)
            self.orm[k_] = r
        return r
    def vecs(self, U, wm2, wm1, w0, wp1, wp2, sm2, sm1, s0, sp1):
        """the two IN-slot vectors (e = +1, -1)"""
        if w0 == 5: pv = {1: bit(sm1), -1: bit(s0)}          # priv(j, f) = the other apex
        elif w0 == 6: m6 = self.pmask(U, wm2, wm1, wp1, wp2, sm2, sm1, s0, sp1); pv = {1: m6, -1: m6}
        else: pv = {1: 31, -1: 31}
        if wp1 == 5: fp = bit(sp1)
        elif wp1 == 6: fp = self.or_plus(U, wm1, w0, wp2, sm1, s0, sp1)
        else: fp = 31
        if wm1 == 5: fm = bit(sm2)
        elif wm1 == 6: fm = self.or_minus(U, wm2, w0, wp1, sm2, sm1, s0)
        else: fm = 31
        vp = (bit(wp1), bit(s0), pv[1], bit(wm1), bit(sm1), pv[-1], fp, fm, bit(wp2), 0, bit(wm2))
        vm = (bit(wm1), bit(sm1), pv[-1], bit(wp1), bit(s0), pv[1], fm, fp, bit(wm2), 0, bit(wp2))
        return vp, vm
    def counts(self, U, *win):
        """tuple of key indices, with multiplicity (one entry per chirality that possibly matches); code_gk8: payer w_j any letter
        (5..9; payers 7, 8, 9 have wildcard own privates)"""
        k_ = (U,) + win; r = self.memo.get(k_)
        if r is None:
            vp, vm = self.vecs(U, *win)
            r = self.eng.in_hits(bit(win[2]), bit(U), vp) + self.eng.in_hits(bit(win[2]), bit(U), vm)
            if len(self.memo) > 3000000: self.memo.clear()
            self.memo[k_] = r
        return r
    @staticmethod
    def out_vecs(wm2, wm1, w0, wp1, wp2, sm2, sm1, s0, sp1):
        """code_gk8 (PAYER8SPEC 3.1): the two OUT-slot vectors (sg = +1, -1) of centre -> w_i on the window W_i; S.L+-3 wildcard"""
        op = (bit(wp1), bit(wp2), 31, bit(wm1), bit(wm2), 31, bit(sp1), bit(sm2), bit(s0), 0, bit(sm1))
        om = (bit(wm1), bit(wm2), 31, bit(wp1), bit(wp2), 31, bit(sm2), bit(sp1), bit(sm1), 0, bit(s0))
        return op, om
    def out_counts(self, U, *win):
        """code_gk8: tuple of key indices, one entry per chirality whose OUT slot (centre U pays w_i) SURELY matches; only at U >= 8
        (a d = 7 centre's OUT is read on the exact picture, not here)"""
        if U < 8: return ()
        k_ = ('o', U) + win; r = self.memo.get(k_)
        if r is None:
            op, om = self.out_vecs(*win)
            r = self.eng.out_hits(bit(U), bit(win[2]), op) + self.eng.out_hits(bit(U), bit(win[2]), om)
            if len(self.memo) > 3000000: self.memo.clear()
            self.memo[k_] = r
        return r
    def row(self, d, w, s):
        """Counter over key names: the gkwin IN - OUT count of a receiver of degree d (letters capped at 9); code_gk8: every link
        position is a possible payer (5..9), and OUT (PAYER8SPEC 3.1) is subtracted at U >= 8"""
        U = min(d, 9); W = lambda k: min(w[k % d], 9); S = lambda k: min(s[k % d], 9); out = collections.Counter()
        for j in range(d):
            win = (W(j - 2), W(j - 1), W(j), W(j + 1), W(j + 2), S(j - 2), S(j - 1), S(j), S(j + 1))
            for q in self.counts(U, *win): out[self.eng.names[q]] += 1
            for q in self.out_counts(U, *win): out[self.eng.names[q]] -= 1
        return out
