# ST-88 T3 / T4: an independent, deliberately simple set-based reading of PAYER8SPEC 3.1 / 3.2 (and the KEYSPEC section 5 pictures
# as PAYER8SPEC restates them), sharing no matcher or picture code with gkfam: Python sets of letters, slots built position by
# position from the text. Compared with code_gk8/gkfam.py on random rows x random keys. Stack masks (pmask, l3q MASK, f2b extras)
# are deterministic hash stubs handed to both sides as data (the change under test does not touch them).
# T4: planted gkfam variants 'outposs' (OUT on a possible match) and 'outmirror' (S.A+-1 not mirrored for sg = -1) must mismatch.
import sys, random, re, collections, hashlib
C = sys.argv[1] if len(sys.argv) > 1 else '/tmp/swarm-W17/code_gk8'; sys.path.insert(0, C)
import gkfam as G
ALL = frozenset((5, 6, 7, 8, 9)); SS = frozenset((5, 6)); BB = frozenset((7, 8, 9))
def hset(*a):   # a deterministic nonempty-or-empty letter set from any arguments (stub stack table)
    h = int(hashlib.md5(repr(a).encode()).hexdigest()[:8], 16); return frozenset(l for l in ALL if h >> (l - 5) & 1)
def tomask(S): return sum(1 << (l - 5) for l in S)
# stubs given to gkfam as masks
pmask_m = lambda *a: tomask(hset('pm', a) | {6})          # never empty, as a real pmask of an admissible window
class MASKD(dict):
    def __getitem__(self, k): return tomask(hset('l3', k) | {5})
MASK_m = MASKD()
def ex6_m(w, s): return lambda k: tomask(hset('x6', tuple(w), tuple(s), k) & {7, 9})
def ex7_m(w, s): return lambda k, f: tomask(hset('x7', tuple(w), tuple(s), k, f) & {8})
# ---------------- independent reference ----------------
POS = ['S.L+1', 'S.L+2', 'S.L+3', 'S.L-1', 'S.L-2', 'S.L-3', 'S.A+1', 'S.A-1', 'R.L+2', 'R.L-2']
class Key:
    def __init__(s, P, Q, X): s.P, s.Q, s.X = frozenset(P), frozenset(Q), dict(X)
def sure(k, payer, payee, pic):     # every set inside the key's set (endpoints exact letters)
    return payer in k.P and payee in k.Q and all(pic[p] <= k.X[p] for p in k.X)
def poss(k, payer, payee, pic):
    return payer in k.P and payee in k.Q and all(pic[p] & k.X[p] for p in k.X)
def ref_window(d, w, s, keys, plant=''):
    """receiver d >= 8: {key index: IN - OUT}"""
    U = min(d, 9); W = lambda i: min(w[i % d], 9); S = lambda i: min(s[i % d], 9); res = collections.Counter()
    def amask_or(k, free):   # OR of pmask(U, w_{k-2}, w_{k-1}, w_{k+1}, w_{k+2}, s_{k-2}, s_{k-1}, s_k, s_{k+1}) over the free arguments
        out = set()
        for x in ALL:
            for y in ALL:
                a = {'w-2': W(k - 2), 'w-1': W(k - 1), 'w+1': W(k + 1), 'w+2': W(k + 2), 's-2': S(k - 2), 's-1': S(k - 1), 's0': S(k), 's+1': S(k + 1)}
                if free == '+': a['w+2'], a['s+1'] = x, y        # neighbour j+1 = k: w_{j+3} = w_{k+2}, s_{j+2} = s_{k+1}
                elif free == '-': a['w-2'], a['s-2'] = x, y      # neighbour j-1 = k: w_{j-3} = w_{k-2}, s_{j-3} = s_{k-2}
                out |= {l for l in ALL if pmask_m(U, a['w-2'], a['w-1'], a['w+1'], a['w+2'], a['s-2'], a['s-1'], a['s0'], a['s+1']) >> (l - 5) & 1}
                if free == '': return frozenset(out)
        return frozenset(out)
    for j in range(d):
        # IN: payer w_j -> centre U, spec chirality sg = +1: S.L+1 = w_{j-1}
        for sg in (1, -1):
            a, b = j - sg, j + sg                     # S.L+1 / S.L-1 link positions
            sa = S(j - 1) if sg == 1 else S(j)          # apex between w_j and w_a
            sb = S(j) if sg == 1 else S(j - 1)
            pic = {'S.L+1': {W(a)}, 'S.L-1': {W(b)}, 'S.L+2': {sa}, 'S.L-2': {sb}, 'R.L+2': {W(j - 2 * sg)}, 'R.L-2': {W(j + 2 * sg)}}
            if W(j) == 5: pic['S.L+3'], pic['S.L-3'] = {sb}, {sa}
            elif W(j) == 6: m = amask_or(j, ''); pic['S.L+3'] = pic['S.L-3'] = m
            else: pic['S.L+3'] = pic['S.L-3'] = ALL   # payers 7, 8, 9: own privates wildcard
            def nb(n, side):   # the S.A position next to neighbour n (= w_{j-1} if side '-' else w_{j+1}), far apex / amask / wildcard
                if W(n) == 5: return {S(j - 2)} if side == '-' else {S(j + 1)}
                if W(n) == 6: return amask_or(n, side)
                return ALL
            nm, np_ = nb(j - 1, '-'), nb(j + 1, '+')
            pic['S.A+1'], pic['S.A-1'] = (nm, np_) if sg == 1 else (np_, nm)
            pic = {p: frozenset(v) for p, v in pic.items()}
            for q, k in enumerate(keys):
                if poss(k, W(j), U, pic): res[q] += 1
        # OUT: centre U pays w_j (PAYER8SPEC 3.1), S.L+-3 wildcard, SURE
        for sg in (1, -1):
            if plant == 'outmirror' or sg == 1: sap, sam = S(j + 1), S(j - 2)
            else: sap, sam = S(j - 2), S(j + 1)
            pic = {'S.L+1': {W(j + sg)}, 'S.L+2': {W(j + 2 * sg)}, 'S.L-1': {W(j - sg)}, 'S.L-2': {W(j - 2 * sg)}, 'S.A+1': {sap}, 'S.A-1': {sam},
                   'R.L+2': {S(j) if sg == 1 else S(j - 1)}, 'R.L-2': {S(j - 1) if sg == 1 else S(j)}, 'S.L+3': ALL, 'S.L-3': ALL}
            pic = {p: frozenset(v) for p, v in pic.items()}
            for q, k in enumerate(keys):
                if U in (8, 9) and (poss if plant == 'outposs' else sure)(k, U, W(j), pic): res[q] -= 1
    return res
def ref_picture(c, n, w, apex, priv, keys):
    """a picture row with centre letter c, degree n: link letters w, apex SETS apex[i] (between w_i, w_{i+1}), privates priv(k, side)
    = the set of link vertex k's private next to apex(k, k + side) (5: the other apex; given for 6 / 7; ALL for 8+).
    returns (OUT Counter, IN Counter)"""
    A = lambda i, side: apex[i % n] if side == 1 else apex[(i - 1) % n]   # apex between w_i and w_{i+side}
    L = lambda i: w[i % n]
    def pv(k, side):
        k %= n
        if L(k) == 5: return A(k, -side)
        if L(k) >= 8: return ALL
        return priv(k, side)
    o, i_ = collections.Counter(), collections.Counter()
    for j in range(n):
        for e in (1, -1):   # IN payer w_j -> c, S.L+1 = w_{j+e}
            pic = {'S.L+1': {L(j + e)}, 'S.L-1': {L(j - e)}, 'S.L+2': A(j, e), 'S.L-2': A(j, -e), 'S.L+3': pv(j, e), 'S.L-3': pv(j, -e),
                   'S.A+1': pv(j + e, -e), 'S.A-1': pv(j - e, e), 'R.L+2': {L(j + 2 * e)}, 'R.L-2': {L(j - 2 * e)}}
            pic = {p: frozenset(v) for p, v in pic.items()}
            for q, k in enumerate(keys):
                if poss(k, L(j), c, pic): i_[q] += 1
            # OUT c -> w_j, S.L+1 = w_{j+e}
            pic = {'S.L+1': {L(j + e)}, 'S.L+2': {L(j + 2 * e)}, 'S.L+3': {L(j + 3 * e)}, 'S.L-1': {L(j - e)}, 'S.L-2': {L(j - 2 * e)},
                   'S.L-3': {L(j - 3 * e)}, 'S.A+1': A(j + e, e), 'S.A-1': A(j - e, -e), 'R.L+2': A(j, e), 'R.L-2': A(j, -e)}
            pic = {p: frozenset(v) for p, v in pic.items()}
            for q, k in enumerate(keys):
                if sure(k, c, L(j), pic): o[q] += 1
    return o, i_
def ref_send(w, H, F, keys):
    apex = [BB if h else SS for h in H]
    o, i_ = ref_picture(5, 5, w, apex, lambda k, side: (BB if F[k] else SS) if w[k] == 6 else ALL, keys)
    return {q: o[q] - i_[q] for q in range(len(keys))}
def ref_cons(L, s, keys):
    o, i_ = ref_picture(6, 6, L, [BB if x >= 7 else SS for x in s], lambda k, side: ALL, keys)
    return {q: i_[q] - o[q] for q in range(len(keys))}
def ref_r7(w, s, keys):
    W = lambda k: w[k % 7]; S = lambda k: s[k % 7]; x6, x7 = ex6_m(w, s), ex7_m(w, s)
    def priv(k, side):
        msk = lambda m: frozenset(l for l in ALL if m >> (l - 5) & 1)
        if w[k] == 6: return msk(pmask_m(7, W(k - 2), W(k - 1), W(k + 1), W(k + 2), S(k - 2), S(k - 1), S(k), S(k + 1)) & ~x6(k))
        c_, a_ = W(k + side), (S(k) if side == 1 else S(k - 1)); o_ = S(k - 1) if side == 1 else S(k)
        if c_ <= 6 and a_ <= 6: return msk(MASK_m[(side, c_, a_, W(k + 2 * side), W(k + 3 * side), W(k + 4 * side), o_)] & ~x7(k, side))
        return ALL
    o, i_ = ref_picture(7, 7, w, [frozenset({x}) for x in s], priv, keys)
    return {q: i_[q] - o[q] for q in range(len(keys))}
# ---------------- random keys and rows ----------------
rr = random.Random(int(sys.argv[2]) if len(sys.argv) > 2 else 8808)
def rset(big=False):
    k = rr.choice((1, 2, 2, 3, 3, 4)) if not big else rr.choice((2, 3, 4, 4))
    return frozenset(rr.sample(sorted(ALL), k))
def rkey(p89, l3=False):
    if p89 and l3:   # a payer-8/9 key that constrains S.L+3 or S.L-3: refused by the code_gk8 parser, fed to the matcher raw (as in W6b's test)
        P = {rr.choice((8, 9))}; Q = rset(True); X = {p: rset() for p in rr.sample(POS, rr.choice((1, 2, 3)))}
        X[rr.choice(('S.L+3', 'S.L-3'))] = rset(); return Key(P, Q, X)
    if p89: P = {rr.choice((8, 9))}; poss_ = [p for p in POS if p not in ('S.L+3', 'S.L-3')]
    else: P = set(rr.sample((5, 6, 7), rr.choice((1, 1, 1, 2)))); poss_ = POS
    Q = rset(True) if rr.random() < 0.6 else frozenset({rr.choice(sorted(ALL))})
    X = {p: rset() for p in rr.sample(poss_, rr.choice((0, 1, 2, 2, 3, 3, 4, 5)))}
    return Key(P, Q, X)
NK89 = int(sys.argv[3]) if len(sys.argv) > 3 else 240; NK57 = int(sys.argv[4]) if len(sys.argv) > 4 else 60; NR = int(sys.argv[5]) if len(sys.argv) > 5 else 60
NKL3 = int(sys.argv[6]) if len(sys.argv) > 6 else 40
keys = [rkey(True) for _ in range(NK89)] + [rkey(False) for _ in range(NK57)] + [rkey(True, True) for _ in range(NKL3)]
def gkline(q, k): return 'k%03d EDGE(%s->%s)[%s]' % (q, G.msym(tomask(k.P)), G.msym(tomask(k.Q)), ' '.join('%s=%s' % (p, G.msym(tomask(v))) for p, v in k.X.items()))
def rawkey(q, k): return ('k%03d' % q, tomask(k.P), tomask(k.Q), tuple(sorted((G.EPOS.index(p), tomask(v)) for p, v in k.X.items())))
gk = [G.parse_key(gkline(q, k)) if q < NK89 + NK57 else rawkey(q, k) for q, k in enumerate(keys)]
for q in range(NK89 + NK57, len(keys)):   # these must be refused by the production parser
    try: G.parse_key(gkline(q, keys[q])); print('T3 parser: raw S.L+-3 key %s ACCEPTED (should be refused)' % gkline(q, keys[q])); sys.exit(1)
    except ValueError: pass
LW = (5, 5, 5, 6, 6, 7, 7, 8, 8, 9, 9)
rows = []
for d in (8, 9, 10):
    for _ in range(NR): rows.append(('recv', d, [rr.choice(LW) for _ in range(d)], [rr.choice(LW) for _ in range(d)]))
for _ in range(NR):
    w = [rr.choice(LW) for _ in range(7)]; w[rr.randrange(7)] = rr.choice((8, 9)); rows.append(('recv', 7, w, [rr.choice(LW) for _ in range(7)]))
for _ in range(NR):
    w = [rr.choice(LW) for _ in range(5)]; rows.append(('send', 5, w, ([rr.randrange(2) for _ in range(5)], [rr.randrange(2) for _ in range(5)])))
for _ in range(NR): rows.append(('cons', 6, [rr.choice(LW) for _ in range(6)], [rr.choice(LW) for _ in range(6)]))
# ---------------- gkfam side ----------------
def gk_row(typ, d, w, s, eng, win):
    if typ == 'recv' and d >= 8: c = win.row(d, w, s); return {q: c[gk[q][0]] for q in range(len(gk))}
    if typ == 'recv': o, i_ = eng.pic_counts(G.recv7_pic(w, s, pmask_m, MASK_m, ex6_m(w, s), ex7_m(w, s))); sgn = 1
    elif typ == 'send': o, i_ = eng.pic_counts(G.sender_pic(w, s[0], s[1])); sgn = -1
    else: o, i_ = eng.pic_counts(G.cons2_pic(w, s)); sgn = 1
    return {q: sgn * (i_[gk[q][0]] - o[gk[q][0]]) for q in range(len(gk))}
class OutPoss(G.Win):
    def out_counts(self, U, *win):
        if U < 8: return ()
        op, om = self.out_vecs(*win); return self.eng.in_hits(G.bit(U), G.bit(win[2]), op) + self.eng.in_hits(G.bit(U), G.bit(win[2]), om)
class OutMirror(G.Win):
    def out_counts(self, U, *win):
        if U < 8: return ()
        op, om = self.out_vecs(*win); om = om[:6] + (op[6], op[7]) + om[8:]
        return self.eng.out_hits(G.bit(U), G.bit(win[2]), op) + self.eng.out_hits(G.bit(U), G.bit(win[2]), om)
# parser refusals (rule 1, 2)
ref_ok = 0; ref_tests = ['EDGE({89}->5)', 'EDGE({78}->5)', 'EDGE(B->5)', 'EDGE(*->5)', 'EDGE(8->5)[S.L+3=5]', 'EDGE(9->6)[S.L-3={56}]',
                         'EDGE(8->5)[R.L+3=5]', 'EDGE(9->5)[R.A+1=5]', 'EDGE(8->5)[R.A-1=5]', 'EDGE(9->5)[R.L-3=5]']
for t in ref_tests:
    try: G.parse_key('x ' + t); print('T3 parser: %s ACCEPTED (should be refused)' % t)
    except ValueError as e: ref_ok += 1; print('T3 parser: %s refused: %s' % (t, e))
acc_tests = ['EDGE(8->{678})[S.L+1={57} S.L+2=S]', 'EDGE(9->B)', 'EDGE({567}->5)[S.L+3=5]', 'EDGE(7->7)[S.L-3=5]']
for t in acc_tests:
    try: G.parse_key('x ' + t); ref_ok += 1; print('T3 parser: %s accepted' % t)
    except ValueError as e: print('T3 parser: %s REFUSED (should be accepted): %s' % (t, e))
eng = G.Engine(gk); win = G.Win(eng, pmask_m)
variants = {'code_gk8': win, 'outposs': OutPoss(eng, pmask_m), 'outmirror': OutMirror(eng, pmask_m)}
stat = {v: collections.Counter() for v in variants}; ex = collections.defaultdict(list); nz = collections.Counter(); npairs = 0
for typ, d, w, s in rows:
    tag = 'recv d=%d' % d if typ == 'recv' else typ
    if typ == 'recv' and d >= 8: ref = ref_window(d, w, s, keys)
    elif typ == 'recv': ref = ref_r7(w, s, keys)
    elif typ == 'send': ref = ref_send(w, s[0], s[1], keys)
    else: ref = ref_cons(w, s, keys)
    for q in range(len(keys)): nz[tag] += ref.get(q, 0) != 0; nz[(tag, 'neg')] += ref.get(q, 0) < 0
    npairs += len(keys)
    for vn, wv in variants.items():
        if vn != 'code_gk8' and not (typ == 'recv' and d >= 8):
            continue
        mine = gk_row(typ, d, w, s, eng, wv)
        for q in range(len(keys)):
            if mine[q] != ref.get(q, 0):
                stat[vn][tag] += 1
                if len(ex[vn]) < 3: ex[vn].append('%s %s/%s %s: ref %d %s %d' % (tag, ''.join(map(str, w)), s if typ == 'send' else ''.join(map(str, s)), gkline(q, keys[q]), ref.get(q, 0), vn, mine[q]))
print('T3 rows %d (receiver d = 8, 9, 10, d = 7 with a link 8/9, senders, cons2: %d each) x keys %d (%d payer-8/9 W5, %d payer-5/6/7, %d payer-8/9 with an S.L+-3 condition: parser-refused, matcher fed raw) = %d pairs' % (len(rows), NR, len(keys), NK89, NK57, NKL3, npairs))
print('T3 nonzero reference coefficients by row type: %s' % dict(sorted((k, v) for k, v in nz.items() if isinstance(k, str))))
print('T3 negative (OUT-dominated) reference coefficients: %s' % {k[0]: v for k, v in nz.items() if not isinstance(k, str)})
for vn in variants:
    print('T%s %s vs independent reference: mismatches %d %s' % ('3' if vn == 'code_gk8' else '4', vn, sum(stat[vn].values()), dict(stat[vn])))
    for e in ex[vn]: print('    e.g. %s' % e)
ok = ref_ok == len(ref_tests) + len(acc_tests) and sum(stat['code_gk8'].values()) == 0
print('T3 %s; T4 %s' % ('PASS' if ok else 'FAIL', 'PASS (both controls fail)' if all(sum(stat[v].values()) > 0 for v in ('outposs', 'outmirror')) else 'FAIL'))
