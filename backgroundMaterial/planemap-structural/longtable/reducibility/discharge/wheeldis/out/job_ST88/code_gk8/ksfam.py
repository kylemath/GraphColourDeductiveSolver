# W17 (swarm round 6, 5 Nov 2026): K* and the generic EDGE(7->P) family for the Studio-side upper checker.
# Written from Team D's REPORT section 1 (family statement only) and W6's grammar.py (EPOS / edge_vec / slots / match), with no
# Opus code. One module, used by st21_w17.py (rows, window bound, separator tables) and by w17_blocks.py (W17GRAM orientation test, W17ST self-test, KSDUMP).
#
# Arrangement of a receiver row of degree d: link w[0..d-1], apex s[0..d-1], s[i] = apex of the face beyond link edge (w_i, w_{i+1}).
# Letters 5..9 (9 = 9+). B = {7, 8, 9}, S = {5, 6}. ab(a, b) = the apex between consecutive link positions a, b (b = a +- 1).
#
# Grammar positions (grammar.EPOS index): S.L+k (k = 1..3) = u's k-th link vertex from v; S.L-k mirrored; S.A+1 = apex of
# (S.L+1, S.L+2) away from u; S.A-1 = apex of (S.L-2, S.L-1) away from u; R.L+2 / R.L-2 = v's link two steps from u through
# S.L+1 / S.L-1. Only these ten are allowed (the payer's 2-ball): R.L+-3, R.A+-1 are refused.
#
# PAYER row (centre u of degree 7, d = 7 only), payee v = w_j with letter in P, orientation sg = +-1 (S.L+1 = w_{j+sg}):
#   S.L+-k = w_{j +- k sg}; S.A+1 = ab(j+sg, j+2sg); S.A-1 = ab(j-sg, j-2sg); R.L+2 = ab(j, j+sg); R.L-2 = ab(j, j-sg).
#   Every letter is exact: coefficient -1 per orientation whose conditions all hold (grammar 'out' slot, SURE).
# PAYEE row (centre v of letter U = min(d, 9) in P), payer u = w_j = 7, orientation e = +-1 (S.L+1 = w_{j+e}):
#   S.L+-1 = w_{j+-e}; S.L+-2 = ab(j, j+-e); S.L+-3 = u's private next to ab(j, j+-e) (priv7, sides sg = +-e);
#   S.A+-1 = the vertex of w_k's link (k = j+-e) next to ab(j, k) other than u: w_k = 5 -> ab(k, k+-e) (exact apex),
#   w_k = 6 -> w_k's private (priv6), w_k >= 7 -> w_k's private (free); R.L+-2 = w_{j+-2e}.
#   Coefficient +1 per orientation whose conditions are all POSSIBLE (grammar 'in' slot), with the picture of certpics.recv_pic:
#   priv7 at d = 7 = L3T(sg, c, a, w2, w3, w4, o) & ~extra7 when c = w_{j+sg} and a = ab(j, j+sg) are in {5, 6}, else free;
#   priv7 at d >= 8 free; priv6 = amask(U, ...) & ~extra6 (extra6 at d <= 9 only; amask at every d unless KSA10=grammar).
import re, collections
LET = (5, 6, 7, 8, 9)
SYM = {'5': 1, '6': 2, '7': 4, '8': 8, '9': 16, 'S': 3, 'B': 28, '*': 31}
EPOS = ['S.L+1', 'S.L+2', 'S.L+3', 'S.L-1', 'S.L-2', 'S.L-3', 'S.A+1', 'S.A-1', 'R.L+2', 'R.L+3', 'R.L-2', 'R.L-3', 'R.A+1', 'R.A-1']
EMIRROR = [3, 4, 5, 0, 1, 2, 7, 6, 10, 11, 8, 9, 13, 12]
ALLOWED = {0, 1, 2, 3, 4, 5, 6, 7, 8, 10}
KSTAR_LINE = 'K1 EDGE(7->7)[S.L+1=B S.L-1=S S.L-2=5 S.L-3=5 S.A-1=B]'
def symmask(t):
    if t in SYM: return SYM[t]
    m_ = re.match(r'^\{([5-9]+)\}$', t)
    if m_: return sum(1 << (int(ch) - 5) for ch in m_.group(1))
    raise ValueError('bad symbol %r' % t)
def parse_key(line):
    """'NAME EDGE(7->P)[POS=SYM ...]' -> (name, P mask, ((pos index, mask), ...)) ; refuses anything outside the 2-ball"""
    f = line.split(None, 1)
    if len(f) != 2: raise ValueError('bad key line %r' % line)
    name, rule = f[0], f[1].strip()
    m_ = re.match(r'^EDGE\(([^-]+)->([^)]+)\)(?:\[(.*)\])?$', rule)
    if not m_: raise ValueError('bad rule %r' % rule)
    if m_.group(1) != '7': raise ValueError('%s: payer must be exactly 7 (got %s)' % (name, m_.group(1)))
    P = symmask(m_.group(2))
    if P & 3 or not P: raise ValueError('%s: payee letters must be a nonempty subset of B (got %s)' % (name, m_.group(2)))
    conds = []
    for t in (m_.group(3) or '').split():
        p_, s_ = t.split('=')
        if p_ not in EPOS: raise ValueError('%s: unknown position %s' % (name, p_))
        pi = EPOS.index(p_)
        if pi not in ALLOWED: raise ValueError('%s: position %s is outside the payer 2-ball (refused)' % (name, p_))
        if any(q == pi for q, _ in conds): raise ValueError('%s: position %s given twice' % (name, p_))
        conds.append((pi, symmask(s_)))
    return name, P, tuple(sorted(conds))
def load_keys(ks_on, egk_file):
    keys = []
    if ks_on: keys.append(parse_key(KSTAR_LINE))
    if egk_file:
        for l_ in open(egk_file):
            l_ = l_.split('#', 1)[0].strip()
            if l_: keys.append(parse_key(l_))
    names = [k[0] for k in keys]
    if len(set(names)) != len(names): raise ValueError('duplicate key names %s' % names)
    return keys
def key_str(k):
    name, P, conds = k
    inv = {v: kk for kk, v in SYM.items()}
    ms = lambda m: inv.get(m, '{' + ''.join(str(l) for l in LET if m >> (l - 5) & 1) + '}')
    return '%s EDGE(7->%s)[%s]' % (name, ms(P), ' '.join('%s=%s' % (EPOS[p], ms(m)) for p, m in conds))
def mirror_key(k, name=None):
    n_, P, conds = k
    return (name or n_ + 'm', P, tuple(sorted((EMIRROR[p], m) for p, m in conds)))

class Ctx:
    """the masks of one checker stack: l3t(sg, c, a, w2, w3, w4, o) -> 5-bit mask (only called with c, a in {5, 6});
    amask(U, wm2, wm1, wp1, wp2, sm2, sm1, s0, sp1); extra7(d, w, s, j, sg) and extra6(d, w, s, k) -> bits to remove"""
    def __init__(self, l3t, amask, extra7, extra6, a10='amask'):
        self.l3t, self.amask, self.extra7, self.extra6, self.a10 = l3t, amask, extra7, extra6, a10

def _ab(s, d, a, b):   # apex between consecutive link positions a and b = a +- 1
    a %= d; b %= d
    return s[a] if b == (a + 1) % d else s[b]
def payer_letter(pi, w, s, j, sg):
    d = len(w); W = lambda k: w[k % d]
    if pi == 0: return W(j + sg)
    if pi == 1: return W(j + 2 * sg)
    if pi == 2: return W(j + 3 * sg)
    if pi == 3: return W(j - sg)
    if pi == 4: return W(j - 2 * sg)
    if pi == 5: return W(j - 3 * sg)
    if pi == 6: return _ab(s, d, j + sg, j + 2 * sg)
    if pi == 7: return _ab(s, d, j - sg, j - 2 * sg)
    if pi == 8: return _ab(s, d, j, j + sg)
    if pi == 10: return _ab(s, d, j, j - sg)
    raise ValueError(pi)
def payer_counts(keys, w, s, plant=''):
    """d = 7 centre: {name: number of SURE oriented matches} (the row coefficient is minus this)"""
    out = collections.Counter(); d = len(w)
    if d != 7: return out
    for name, P, conds in keys:
        for j in range(d):
            if not (P >> (w[j] - 5)) & 1: continue
            for sg in (1, -1):
                if all((m >> (payer_letter(pi, w, s, j, sg) - 5)) & 1 for pi, m in conds): out[name] += 1
    return out
def priv7(ctx, d, w, s, j, sg):
    W = lambda k: w[k % d]
    c, a, o = W(j + sg), _ab(s, d, j, j + sg), _ab(s, d, j, j - sg)
    if d != 7 or c > 6 or a > 6: return 31
    return ctx.l3t(sg, c, a, W(j + 2 * sg), W(j + 3 * sg), W(j + 4 * sg), o) & ~ctx.extra7(d, w, s, j % d, sg) & 31
def priv6(ctx, d, w, s, k):
    if d >= 10 and ctx.a10 == 'grammar': return 31
    W = lambda q: w[q % d]; S = lambda q: s[q % d]; U = min(d, 9)
    m_ = ctx.amask(U, W(k - 2), W(k - 1), W(k + 1), W(k + 2), S(k - 2), S(k - 1), S(k), S(k + 1))
    if d <= 9: m_ &= ~ctx.extra6(d, w, s, k % d)
    return m_ & 31
def far(ctx, d, w, s, j, e):   # the vertex of w_k's link (k = j + e) next to ab(j, k), other than w_j
    k = j + e; wk = w[k % d]
    if wk == 5: return 1 << (_ab(s, d, k, k + e) - 5)
    if wk == 6: return priv6(ctx, d, w, s, k)
    return 31
def payee_set(ctx, pi, d, w, s, j, e):
    W = lambda k: w[k % d]
    if pi == 0: return 1 << (W(j + e) - 5)
    if pi == 3: return 1 << (W(j - e) - 5)
    if pi == 1: return 1 << (_ab(s, d, j, j + e) - 5)
    if pi == 4: return 1 << (_ab(s, d, j, j - e) - 5)
    if pi == 2: return priv7(ctx, d, w, s, j, e)
    if pi == 5: return priv7(ctx, d, w, s, j, -e)
    if pi == 6: return far(ctx, d, w, s, j, e)
    if pi == 7: return far(ctx, d, w, s, j, -e)
    if pi == 8: return 1 << (W(j + 2 * e) - 5)
    if pi == 10: return 1 << (W(j - 2 * e) - 5)
    raise ValueError(pi)
def payee_counts(ctx, keys, w, s):
    """centre letter U = min(d, 9): {name: number of POSSIBLE oriented matches}"""
    out = collections.Counter(); d = len(w); U = min(d, 9)
    js = [j for j in range(d) if w[j] == 7]
    if not js: return out
    for name, P, conds in keys:
        if not (P >> (U - 5)) & 1: continue
        for j in js:
            for e in (1, -1):
                if all(payee_set(ctx, pi, d, w, s, j, e) & m for pi, m in conds): out[name] += 1
    return out
def payee_dirs(ctx, keys, w, s):   # for dumps: per name the list of (j, e) that fire
    out = collections.defaultdict(list); d = len(w); U = min(d, 9)
    for name, P, conds in keys:
        if not (P >> (U - 5)) & 1: continue
        for j in range(d):
            if w[j] != 7: continue
            for e in (1, -1):
                if all(payee_set(ctx, pi, d, w, s, j, e) & m for pi, m in conds): out[name].append((j, e))
    return out

# ---- window bound: the payee credit of one link 7 at position j from the separator window (w_{j-1}, s_{j-1}, 7, s_j, w_{j+1}).
# Each position's letter set is replaced by the union of its exact set over every letter outside the window, and the f2b extras
# are dropped (they only remove letters), so the bound set contains the exact set for every completion; a condition possible on
# the exact sets is possible on the bound sets, hence bound count >= exact count for every arrangement with this window.
def bound_sets(ctx, U, wm1, sm1, sp0, wp1, e):
    """per allowed position, the bound set for payer w_j = 7 (window letters as given), orientation e, centre letter U"""
    L = {1: wp1, -1: wm1}; A = {1: sp0, -1: sm1}   # w_{j+-1}, ab(j, j+-1)
    out = {0: 1 << (L[e] - 5), 3: 1 << (L[-e] - 5), 1: 1 << (A[e] - 5), 4: 1 << (A[-e] - 5), 8: 31, 10: 31}
    for pi, sg in ((2, e), (5, -e)):   # priv7 on side sg: c = L[sg], a = A[sg], o = A[-sg]; outside: w2, w3, w4
        c, a, o = L[sg], A[sg], A[-sg]
        if U != 7 or c > 6 or a > 6: out[pi] = 31
        else:
            m_ = 0
            for w2 in LET:
                for w3 in LET:
                    for w4 in LET: m_ |= ctx.l3t(sg, c, a, w2, w3, w4, o)
            out[pi] = m_ & 31
    for pi, sg in ((6, e), (7, -e)):   # far vertex beside k = j + sg
        wk = L[sg]
        if wk == 5: out[pi] = 31            # the far apex ab(k, k + sg) lies outside the window
        elif wk == 6:
            if U == 9 and ctx.a10 == 'grammar': out[pi] = 31; continue   # the U = 9 table also serves d >= 10
            if getattr(ctx, 'amask_or', None) is not None: out[pi] = ctx.amask_or(min(U, 9), sg, wm1, sm1, sp0, wp1) & 31; continue
            m_ = 0
            for x1 in LET:
                for x2 in LET:
                    for y1 in LET:
                        for y2 in LET:
                            # amask(U, w_{k-2}, w_{k-1}, w_{k+1}, w_{k+2}, s_{k-2}, s_{k-1}, s_k, s_{k+1}) with the window letters fixed
                            if sg == 1:   # k = j+1: w_{k-2} = w_{j-1}, w_{k-1} = 7, w_{k+1} = x1, w_{k+2} = x2, s_{k-2} = s_{j-1}, s_{k-1} = s_j, s_k = y1, s_{k+1} = y2
                                m_ |= ctx.amask(min(U, 9), wm1, 7, x1, x2, sm1, sp0, y1, y2)
                            else:         # k = j-1: w_{k-2} = x2, w_{k-1} = x1, w_{k+1} = 7, w_{k+2} = w_{j+1}, s_{k-2} = y2, s_{k-1} = y1, s_k = s_{j-1}, s_{k+1} = s_j
                                m_ |= ctx.amask(min(U, 9), x2, x1, 7, wp1, y2, y1, sm1, sp0)
            out[pi] = m_ & 31
        else: out[pi] = 31
    return out
def bound_count(ctx, key, U, wm1, sm1, sp0, wp1, cache=None):
    name, P, conds = key
    if not (P >> (U - 5)) & 1: return 0
    n = 0
    for e in (1, -1):
        ck = (U, wm1, sm1, sp0, wp1, e)
        if cache is not None and ck in cache: bs = cache[ck]
        else:
            bs = bound_sets(ctx, U, wm1, sm1, sp0, wp1, e)
            if cache is not None: cache[ck] = bs
        if all(bs[pi] & m for pi, m in conds): n += 1
    return n
