# ST-88 TV: W6b's p8_vectors (README.txt there) against code_gk8/gkfam.py.
# The harness builds every row picture with code_gk8's own constructors (gkfam.sender_pic, gkfam.cons2_pic, gkfam.Pic for d = 7,
# gkfam.Win for d >= 8 window rows) and counts with gkfam.Engine / gkfam.Win.row. The only data taken from the reference slots are
# the STACK masks it cannot recompute (no GS14 / A97+F tables here): a link 6's private (pmask & ~extra6, or amask in window rows),
# a link 7's two privates at d = 7 (MASK & ~extra7), and the window amask OR of a link 6 next to the payer (S.A+-1). They are read
# from the reference IN slots and injected; every other position, every letter, chirality, gate and the match rule are code_gk8's.
# Checks: (S) slot level: my slot vectors vs every reference slot (10 positions, payer -> payee letters);
#         (a), (b): coefficients of the 24 keys on all 1,132 GS14_01 rows vs a_*.txt / b_*.txt (unlisted (key, row) = 0);
#         (c): c_A / c_B slot level on W00..W62, c_C coefficients (W5) of 400 rows x 300 keys (payer sets mixing 8 / 9 skipped);
#         (d): the 8 planted controls (code_gk8 must give the correct value; the planted reading must give the stated wrong value).
import sys, re, collections
C = sys.argv[1] if len(sys.argv) > 1 else '/tmp/swarm-W17/code_gk8'; sys.path.insert(0, C)
import gkfam as G
V = sys.argv[2]
POS10 = ['S.L+1', 'S.L+2', 'S.L+3', 'S.L-1', 'S.L-2', 'S.L-3', 'S.A+1', 'S.A-1', 'R.L+2', 'R.L-2']
GI = [G.EPOS.index(p) for p in POS10]   # gkfam vector index of each of the 10 positions
def sm(t): return G.symmask(t)
def parse_sets(txt):
    d = dict(t.split('=', 1) for t in txt.split())
    return tuple(sm(d[p]) for p in POS10)
def vec10(v): return tuple(v[i] for i in GI)
SLOT = re.compile(r'(IN|OUT)\s+[ji]=(\d+) sg=([+-]1) (\d)->(\d)\s+(.*)$')
def rawkey(name, U, Vv, conds):   # a key tuple straight to the matcher (gkfam.parse_key would refuse S.L+-3 on a payer 8 / 9)
    return (name, U, Vv, tuple(sorted((G.EPOS.index(p), m) for p, m in conds)))
def key_from_edge(name, rule):
    m = re.match(r'^EDGE\(([^-]+)->([^)]+)\)(?:\[(.*)\])?$', rule)
    return rawkey(name, sm(m.group(1)), sm(m.group(2)), [(t.split('=')[0], sm(t.split('=')[1])) for t in (m.group(3) or '').split()])
def parse_attrs(toks):
    return dict(t.split('=', 1) for t in toks if '=' in t)
# ---------------- rows and slots ----------------
class Row:
    def __init__(self, rid, typ, a):
        self.id, self.typ = rid, typ; self.d = int(a['d']); self.w = [int(c) for c in a['link']]; self.a = a; self.slots = []
def load_gs14():
    rows = collections.OrderedDict()
    for l in open(V + '/rows_GS14_01.txt'):
        if l.startswith('#') or not l.strip(): continue
        f = l.split(); rows[f[0]] = Row(f[0], {'R': 'recv', 'S': 'send', 'C': 'cons'}[f[0][0]], parse_attrs(f[1:]))
    for l in open(V + '/slots_GS14_01.txt'):
        if l.startswith('#') or not l.strip(): continue
        rid, rest = l.split(None, 1); m = SLOT.match(rest.strip())
        rows[rid].slots.append(('W5', m.group(1), int(m.group(2)), int(m.group(3)), int(m.group(4)), int(m.group(5)), parse_sets(m.group(6))))
    return rows
def load_cC():
    rows = collections.OrderedDict(); cur = None
    for l in open(V + '/c_C_rows_slots.txt'):
        if l.startswith('#') or not l.strip(): continue
        if not l[0].isspace():
            f = l.split(); cur = Row(f[0], {'receiver': 'recv', 'sender': 'send', 'cons2': 'cons'}[f[1]], parse_attrs(f[2:])); rows[f[0]] = cur
        else:
            mode, rest = l.split(None, 1); m = SLOT.match(rest.strip())
            cur.slots.append((mode, m.group(1), int(m.group(2)), int(m.group(3)), int(m.group(4)), int(m.group(5)), parse_sets(m.group(6))))
    return rows
def load_cAB():
    rows = collections.OrderedDict()
    for fn, hasmode in (('c_A_out_slots.txt', True), ('c_B_window_in_slots.txt', False)):
        for l in open(V + '/' + fn):
            if l.startswith('#') or not l.strip(): continue
            f = l.split()
            mode = f.pop(0) if hasmode else 'W5'
            rid = f[0]; a = parse_attrs(f[1:4]); m = SLOT.match(' '.join(f[4:]))
            if rid not in rows: rows[rid] = Row(rid, 'recv', a)
            rows[rid].slots.append((mode, m.group(1), int(m.group(2)), int(m.group(3)), int(m.group(4)), int(m.group(5)), parse_sets(m.group(6))))
    return rows
# ---------------- my pictures (stack masks injected from the reference IN slots) ----------------
def inj_masks(r):
    """from the reference W5 IN slots (ref sg = +1: S.L+1 = w_{j-1}): P6[j] (payer 6's S.L+3), P7[(j, -1)] / P7[(j, +1)] (payer 7's
    S.L+3 / S.L-3, d = 7 pictures), window neighbour ORs: ORM[j] (S.A+1 when w_{j-1} = 6), ORP[j] (S.A-1 when w_{j+1} = 6)"""
    P6, P7, ORM, ORP = {}, {}, {}, {}; bad = []
    def put(D, k, v):
        if k in D and D[k] != v: bad.append((k, D[k], v))
        D[k] = v
    d, w = r.d, r.w
    for mode, role, j, sg, a_, b_, s10 in r.slots:
        if mode != 'W5' or role != 'IN' or sg != 1: continue
        if w[j] == 6: put(P6, j, s10[2]); put(P6, j, s10[5])
        if w[j] == 7 and r.typ == 'recv' and d == 7: put(P7, (j, -1), s10[2]); put(P7, (j, 1), s10[5])
        if w[(j - 1) % d] == 6: put(ORM, j, s10[6])
        if w[(j + 1) % d] == 6: put(ORP, j, s10[7])
    return P6, P7, ORM, ORP, bad
class InjWin(G.Win):
    """gkfam.Win with the stack-dependent masks of one row looked up from the reference (keyed by the window arguments gkfam passes)"""
    def __init__(self, eng, r):
        G.Win.__init__(self, eng, self._pm); d, w = r.d, r.w; s = [int(c) for c in r.a['apex']]; U = min(d, 9)
        P6, _, ORM, ORP, self.bad = inj_masks(r); self.t6, self.tp, self.tm = {}, {}, {}
        W = lambda k: min(w[k % d], 9); S = lambda k: min(s[k % d], 9)
        def put(D, k, v):
            if k in D and D[k] != v: self.bad.append(('window-collision', k))
            D[k] = v
        for j, m in P6.items(): put(self.t6, (U, W(j - 2), W(j - 1), W(j + 1), W(j + 2), S(j - 2), S(j - 1), S(j), S(j + 1)), m)
        for j, m in ORP.items(): put(self.tp, (U, W(j - 1), W(j), W(j + 2), S(j - 1), S(j), S(j + 1)), m)
        for j, m in ORM.items(): put(self.tm, (U, W(j - 2), W(j), W(j + 1), S(j - 2), S(j - 1), S(j)), m)
        self.U, self.W, self.S = U, W, S
    def _pm(self, *a): return self.t6[a]
    def or_plus(self, *a): return self.tp[a]
    def or_minus(self, *a): return self.tm[a]
    def win(self, j): W, S = self.W, self.S; return (W(j - 2), W(j - 1), W(j), W(j + 1), W(j + 2), S(j - 2), S(j - 1), S(j), S(j + 1))
def my_pic(r):
    d, w = r.d, r.w
    if r.typ == 'send':
        H = [1 if c == 'B' else 0 for c in r.a['apex_classes']]
        F = [0] * 5
        if r.a.get('six_private_classes', 'none') not in ('none', ''):
            for t in r.a['six_private_classes'].split(','): k, c = t.split(':'); F[int(k)] = 1 if c == 'B' else 0
        return G.sender_pic(w, H, F)
    if r.typ == 'cons': return G.cons2_pic(w, [7 if c == 'B' else 5 for c in r.a['apex_classes']])
    P6, P7, _, _, bad = inj_masks(r); assert d == 7 and not bad, (r.id, bad)
    return G.Pic(7, G.bit(7), w, [G.bit(int(c)) for c in r.a['apex']], P6, P7)
def my_slots(r, wn=None):
    """my slots as {(role, idx, ref sg): (payer letter, payee letter, 10 sets)}"""
    out = {}
    if r.typ == 'recv' and r.d >= 8:
        U = wn.U
        for j in range(r.d):
            win = wn.win(j); vp, vm = wn.vecs(U, *win); op, om = G.Win.out_vecs(*win)
            out[('IN', j, -1)] = (win[2], U, vec10(vp)); out[('IN', j, 1)] = (win[2], U, vec10(vm))
            out[('OUT', j, 1)] = (U, win[2], vec10(op)); out[('OUT', j, -1)] = (U, win[2], vec10(om))
    else:
        P = my_pic(r); c = {'send': 5, 'cons': 6, 'recv': 7}[r.typ]
        for j in range(r.d):
            for e in (1, -1):
                out[('IN', j, -e)] = (min(r.w[j], 9), c, vec10(P.in_vec(j, e)))
                out[('OUT', j, e)] = (c, min(r.w[j], 9), vec10(P.out_vec(j, e)))
    return out
def slot_check(rows, tag, modes=('W5',)):
    n = bad = 0; ex = []; wins = {}
    for r in rows.values():
        wn = InjWin(G.Engine([]), r) if (r.typ == 'recv' and r.d >= 8) else None
        if wn is not None and wn.bad: bad += 1; ex.append((r.id, 'mask collision', wn.bad[:2])); continue
        mine = my_slots(r, wn)
        for mode, role, i, sg, a_, b_, s10 in r.slots:
            if mode not in modes: continue
            n += 1; got = mine.get((role, i, sg))
            if got != (a_, b_, s10):
                bad += 1
                if len(ex) < 5: ex.append((r.id, role, i, sg, 'ref', (a_, b_, [G.msym(x) for x in s10]), 'mine', got and (got[0], got[1], [G.msym(x) for x in got[2]])))
    print('TV slots %-28s %6d reference slots compared, mismatches %d' % (tag, n, bad))
    for e in ex: print('   MISMATCH', e)
    return bad
# ---------------- coefficients ----------------
def coefs(rows, keys):
    """{(key name, row id): coefficient} for every key and row (code_gk8 rules)"""
    eng = G.Engine(keys); res = {}
    for r in rows.values():
        if r.typ == 'recv' and r.d >= 8:
            ct = InjWin(eng, r).row(r.d, r.w, [int(c) for c in r.a['apex']])
            for k in keys: res[(k[0], r.id)] = ct[k[0]]
        else:
            o, i = eng.pic_counts(my_pic(r))
            for k in keys: res[(k[0], r.id)] = (o[k[0]] - i[k[0]]) if r.typ == 'send' else (i[k[0]] - o[k[0]])
    return res
def load_ab(fn):
    exp = {}; keys = []; cur = None; ends = {}
    for l in open(V + '/' + fn):
        if l.startswith('#') or not l.strip(): continue
        if l.startswith('KEY '):
            m_ = re.match(r'^KEY (\S+) (EDGE\([^)]*\)(?:\[[^\]]*\])?)', l); cur = m_.group(1); keys.append(key_from_edge(cur, m_.group(2)))
        elif l.startswith('END '): ends[cur] = int(l.split()[2])
        elif not l[0].isspace():
            f = l.split(); exp[(cur, f[0])] = int(re.search(r'coef=([+-]?\d+)', l).group(1))
    for k in keys: assert ends[k[0]] == sum(1 for (kk, _) in exp if kk == k[0]), ('END count', k[0])   # file self-consistency
    return keys, exp
def compare(tag, mine, exp, rowids, keynames):
    n = bad = nz = 0; ex = []
    for k in keynames:
        for rid in rowids:
            n += 1; e = exp.get((k, rid), 0); m = mine[(k, rid)]; nz += e != 0
            if e != m:
                bad += 1
                if len(ex) < 8: ex.append('%s %s expected %d code_gk8 %d' % (k, rid, e, m))
    print('TV coef  %-28s %7d (key, row) pairs, %d nonzero expected, mismatches %d' % (tag, n, nz, bad))
    for e in ex: print('   MISMATCH', e)
    return bad
TOT = collections.Counter()
GS = load_gs14()
TOT['slots GS14'] = slot_check(GS, 'slots_GS14_01 (all 1,132 rows)')
k24 = G.load_keys(sys.argv[3])   # the production parser accepts all 24 keys
ka, ea = load_ab('a_receivers_GS14_01.txt'); kb, eb = load_ab('b_senders_cons2_GS14_01.txt')
assert [k[0] for k in ka] == [k[0] for k in k24] and [k[1:] for k in ka] == [k[1:] for k in k24], 'a-file keys differ from the 24-key file'
mine = coefs(GS, k24)
TOT['a'] = compare('a receivers GS14_01', mine, ea, [r for r in GS if GS[r].typ == 'recv'], [k[0] for k in k24])
TOT['b'] = compare('b senders+cons2 GS14_01', mine, eb, [r for r in GS if GS[r].typ != 'recv'], [k[0] for k in k24])
# (c)
AB = load_cAB()
TOT['c_A'] = slot_check({k: Row(r.id, r.typ, r.a) for k, r in AB.items()} if False else AB, 'c_A + c_B (W00..W62, W5)')
CC = load_cC()
TOT['slots c_C'] = slot_check(CC, 'c_C rows (400, W5)')
ckeys = []; skipped = []; refused = []
for l in open(V + '/c_C_keys.txt'):
    if l.startswith('#') or not l.strip(): continue
    f = l.split(); a = parse_attrs(f[1:3]); U, Vv = sm(a['U']), sm(a['V'])
    conds = [(t.split('=')[0], sm(t.split('=')[1])) for t in f[3:] if '=' in t]
    if (U & 24) and U not in (8, 16): skipped.append(f[0]); continue
    k = rawkey(f[0], U, Vv, conds)
    try: G.parse_key('%s EDGE(%s->%s)[%s]' % (f[0], G.msym(U), G.msym(Vv), ' '.join('%s=%s' % (p, G.msym(m)) for p, m in conds)))
    except ValueError: refused.append(f[0])
    ckeys.append(k)
exp = {}
for l in open(V + '/c_C_values.txt'):
    if l.startswith('#') or not l.strip(): continue
    r_, k_, w5, w7 = l.split(); exp[(k_, r_)] = int(w5)
cm = coefs(CC, ckeys)
print('TV c_C keys: %d evaluated, %d skipped (payer set mixing 8 / 9: %s), %d of the evaluated refused by the code_gk8 parser (payer 8/9 with S.L+-3; '
      'evaluated through the matcher directly)' % (len(ckeys), len(skipped), ' '.join(skipped), len(refused)))
TOT['c_C'] = compare('c_C W5 (all evaluated keys)', cm, exp, list(CC), [k[0] for k in ckeys])
acc = [k[0] for k in ckeys if k[0] not in refused]
compare('c_C W5 (parser-accepted keys)', cm, exp, list(CC), acc)
compare('c_C W5 (payer exactly 8 or 9)', cm, exp, list(CC), [k[0] for k in ckeys if k[1] in (8, 16)])
# (d) planted controls
class OutPoss(InjWin):
    def out_counts(self, U, *win):
        if U < 8: return ()
        op, om = self.out_vecs(*win); return self.eng.in_hits(G.bit(U), G.bit(win[2]), op) + self.eng.in_hits(G.bit(U), G.bit(win[2]), om)
class OutMirror(InjWin):
    def out_counts(self, U, *win):
        if U < 8: return ()
        op, om = self.out_vecs(*win); om = om[:6] + (op[6], op[7]) + om[8:]
        return self.eng.out_hits(G.bit(U), G.bit(win[2]), op) + self.eng.out_hits(G.bit(U), G.bit(win[2]), om)
dbad = 0
for l in open(V + '/d_controls.txt'):
    if l.startswith('#') or not l.strip(): continue
    m = re.match(r'^(\S+)\s+key (\S+) (EDGE\([^)]*\)(?:\[[^\]]*\])?)\s+row (\S+) .*correct coef=([+-]?\d+).*control \S+ gives ([+-]?\d+)', l)
    bug, kn, rule, rid, good, wrong = m.group(1), m.group(2), m.group(3), m.group(4), int(m.group(5)), int(m.group(6))
    k = key_from_edge(kn, rule); r = GS[rid]; s = [int(c) for c in r.a['apex']]
    try: G.parse_key('%s %s' % (kn, rule)); acc_ = 'accepted'
    except ValueError as e_: acc_ = 'REFUSED by the parser (%s)' % e_
    mine_ = InjWin(G.Engine([k]), r).row(r.d, r.w, s)[kn]
    pl = (OutPoss if bug == 'outposs' else OutMirror)(G.Engine([k]), r).row(r.d, r.w, s)[kn]
    ok = mine_ == good and mine_ != wrong and pl == wrong
    dbad += not ok
    print('TV d %-9s %-12s %s: correct %+d wrong %+d | code_gk8 %+d, planted %s reading %+d -> %s; key %s' % (bug, kn, rid, good, wrong, mine_, bug, pl, 'OK' if ok else 'FAIL', acc_))
TOT['d'] = dbad
print('TV summary (mismatch counts): %s -> %s' % (dict(TOT), 'PASS' if not sum(TOT.values()) else 'FAIL'))
