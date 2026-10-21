# s45 control (b): independent physical key check for l3qV (RELAY_SPEC_s45 45.1-45.4).  Explicit rotation systems around a
# 7 u (s44 phys44's builder; link degrees now up to 11 so the letter 9 covers d >= 9).  For every link vertex v of degree >= 8:
#   (I) an INDEPENDENT key from vertex identities, per side: c = a common nbr of u and v; a = the common nbr of u, c other
#       than v; a2 = the common nbr of u, a other than c; and v's window w2 = common(v, c) other than u, w3 = common(v, w2)
#       other than c, w4 = common(v, w3) other than w2, o = the common nbr of u and v's other common nbr c', other than v.
#   (P) the engine's payer terms l3q_terms(7, w, s) on u's row (random rotation and reflection): the lq (V, c, a, a2) multiset
#       must equal the independent one over all link 8/9s and sides.
#   (Q) the engine's payee terms l3q_terms_payeeV(n, L, t) on v's own row (random rotation and reflection, apexes from the
#       rotations, unknown apexes random letters); the mask table is replaced by a probe table whose value is a hash of
#       (c, w2, w3, w4, a, o), so the multiset {(V, c, a, hash)} must equal the independent one.  v's whose link holds a 7
#       other than u are skipped (their extra terms would mix in).
# Broken control: the payee read with the apex across the wrong edge (a and o swapped) must mismatch.
import sys, random, collections
NARG = int(sys.argv[1]) if len(sys.argv) > 1 else 50000
B = '/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp'
M = '/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad/P/m/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis'
E = B + '/s45/eng'; Q = B + '/s33z/reg_A78'
sys.argv = [E + '/pcheck.py', 'none', 'apexcls', 'hat5', 'l3q', 'l3qtab=%s/tab_1.json,%s/tab_-1.json' % (Q, Q), 'l3qV=7,8,9', 'root=' + M]
src = open(E + '/pcheck.py').read(); last = src.rstrip().rsplit('\n', 1)
G = {'__file__': E + '/pcheck.py', '__name__': 'pcheck_exec'}; exec(compile(last[0], E + '/pcheck.py', 'exec'), G)
assert G['LQVX'] == (8, 9)
def H(c, w2, w3, w4, a, o): return (((((c * 7 + w2) * 11 + w3) * 13 + w4) * 17 + a) * 19 + o) % 32
class Probe(dict):
    def __getitem__(self, k): return H(*k[1:])
G['L3TV'][8] = Probe(); G['L3TV'][9] = Probe()
LT = lambda x: min(x, 9)
def build(rng, d):
    L = lambda: rng.choice((5, 6, 7, 8, 9))
    deg = {}; rot = {}; deg['u'] = d
    w = [rng.choice((5, 5, 6, 6, 6, 7, 8, 8, 9, 10, 11)) for _ in range(d)]
    s = [rng.choice((5, 5, 6, 6, 7, 8, 9)) for _ in range(d)]
    W_ = ['w%d' % i for i in range(d)]; S_ = ['s%d' % i for i in range(d)]
    for i in range(d): deg[W_[i]] = w[i]; deg[S_[i]] = s[i]
    rot['u'] = list(W_)
    for i in range(d):
        pv = ['p%d_%d' % (i, k) for k in range(w[i] - 5)]
        for z in pv: deg[z] = L()
        rot[W_[i]] = ['u', W_[(i + 1) % d], S_[i]] + pv + [S_[(i - 1) % d], W_[(i - 1) % d]]
    for i in range(d):
        a = rot[W_[(i + 1) % d]][-3]; b = rot[W_[i]][3]
        fr = ['f%d_%d' % (i, k) for k in range(s[i] - 4)]
        for z in fr: deg[z] = L()
        rot[S_[i]] = [W_[i], W_[(i + 1) % d], a] + fr + [b]
    par = {}
    def fd(x):
        while par.get(x, x) != x: x = par[x]
        return x
    for i in range(d):
        if w[(i + 1) % d] == 5:
            x, y = fd(rot[S_[i]][3]), fd(rot[S_[(i + 1) % d]][-2])
            if x != y: par[y] = x
    for k in list(rot): rot[k] = [fd(z) for z in rot[k]]
    return d, w, s, deg, rot
def common(rot, x, y, excl):
    hs = set()
    for a, b in ((x, y), (y, x)):
        if a in rot and b in rot[a]:
            r = rot[a]; j = r.index(b); c1, c2_ = r[(j - 1) % len(r)], r[(j + 1) % len(r)]
            assert excl in (c1, c2_), (a, b, excl); hs.add(c2_ if c1 == excl else c1)
    assert len(hs) <= 1, hs
    return hs.pop() if hs else None
def orient(L, t, rng, track=None):
    n = len(L); r = rng.randrange(n); refl = rng.random() < 0.5; L2 = [None] * n; t2 = [None] * n; tr = None
    for i in range(n):
        j = (i + r) % n if not refl else (r - i) % n; L2[j] = L[i]
        if track is not None and i == track: tr = j
        j2 = (i + r) % n if not refl else (r - i - 1) % n; t2[j2] = t[i]
    return L2, t2, tr
def payee_broken(d, w, s):
    cf = collections.Counter(); V = min(d, 9)
    for i in range(d):
        if w[i] != 7: continue
        for sg in (1, -1):
            c, w2, w3, w4 = (w[(i + k * sg) % d] for k in (1, 2, 3, 4))
            o, ap = (s[i], s[(i - 1) % d]) if sg == 1 else (s[(i - 1) % d], s[i])   # BROKEN: apex across the wrong edge
            if c <= 6 and ap <= 6: cf[('lQ', (V, c, ap, H(c, w2, w3, w4, ap, o)))] += 1
    return cf
def run(N, seed=45):
    rng = random.Random(seed); st = collections.Counter()
    for _ in range(N):
        st_ = build(rng, 7); d, w, s, deg, rot = st_
        # (I) independent payer multiset
        ind_pay = collections.Counter()
        for i in range(d):
            v = 'w%d' % i
            if deg[v] < 8: continue
            for c in (rot['u'][(i + 1) % d], rot['u'][(i - 1) % d]):
                a = common(rot, 'u', c, v); a2 = common(rot, 'u', a, c)
                if deg[c] <= 6 and deg[a] <= 6: ind_pay[('lq', (LT(deg[v]), deg[c], deg[a], LT(deg[a2])))] += 1
        Wl, Sl, _ = orient([LT(x) for x in w], [LT(x) for x in s], rng)
        eng = G['l3q_terms'](7, Wl, Sl); eng_pay = collections.Counter({k: -v for k, v in eng.items() if k[0] == 'lq' and len(k[1]) == 4})
        st['rows'] += 1; st['payer terms'] += sum(ind_pay.values())
        if eng_pay != ind_pay: st['PAYER MISMATCH'] += 1
        for i in range(d):
            v = 'w%d' % i
            if deg[v] < 8: continue
            Lv = rot[v]; n = len(Lv); assert n == deg[v]
            if any(deg[z] == 7 for z in Lv if z != 'u'): st['payees skipped (other 7)'] += 1; continue
            ku = Lv.index('u'); ind_q = collections.Counter()
            for sgi in (1, -1):
                c = Lv[(ku + sgi) % n]; cp = Lv[(ku - sgi) % n]
                a = common(rot, 'u', c, v); o = common(rot, 'u', cp, v)
                w2 = Lv[(ku + 2 * sgi) % n]; w3 = Lv[(ku + 3 * sgi) % n]; w4 = Lv[(ku + 4 * sgi) % n]
                # independent re-derivation of w2 from identities where c's rotation is known (cross-check of the link walk)
                if c in rot and v in rot[c]: assert common(rot, v, c, 'u') == w2
                if deg[c] <= 6 and deg[a] <= 6: ind_q[('lQ', (LT(deg[v]), deg[c], deg[a], H(deg[c], LT(deg[w2]), LT(deg[w3]), LT(deg[w4]), deg[a], LT(deg[o]))))] += 1
            Lt = [LT(deg[z]) for z in Lv]; tt = []
            for m in range(n):
                a_ = common(rot, Lv[m], Lv[(m + 1) % n], v)
                tt.append(LT(deg[a_]) if a_ is not None else rng.choice((5, 6, 7, 8, 9)))
            L2, t2, _ = orient(Lt, tt, rng)
            got = collections.Counter({k: v_ for k, v_ in G['l3q_terms_payeeV'](n, L2, t2).items()})
            st['payees'] += 1; st['payees V=%d' % LT(deg[v])] += 1; st['payee terms'] += sum(ind_q.values())
            if got != ind_q: st['PAYEE MISMATCH'] += 1
            if ind_q:
                st['broken checked'] += 1; st['broken mismatches'] += payee_broken(n, L2, t2) != ind_q
    return st
st = run(NARG)
for k in sorted(st): print('%-26s %d' % (k, st[k]))
ok = not (st['PAYER MISMATCH'] or st['PAYEE MISMATCH']) and st['broken mismatches'] > 0.5 * st['broken checked'] > 0
print('PHYS45:', 'PASS' if ok else 'FAIL', '(broken payee apex: %d of %d payees mismatch)' % (st['broken mismatches'], st['broken checked']))
