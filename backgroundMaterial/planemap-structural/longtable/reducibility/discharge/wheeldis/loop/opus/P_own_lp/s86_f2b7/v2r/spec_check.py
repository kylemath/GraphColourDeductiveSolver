# s86 v2r: re-derive the V2ROW_SPEC.md test vectors from the SPEC TEXT alone (sections 2, 4.2, 4.3), without the engine:
# key OUT / IN counts from the two position tables, the 6 / 7 copy terms from the h2_of / qkey / lq formulas, and the row as
# fixed + copies + keys.  Checks the spec's tables against the engine's output (v2rshow json).  Pure python, no stack tables.
# usage: python3 -I spec_check.py <v2show.json> <gkeys file>
import sys, json, re
V, KF = sys.argv[1], sys.argv[2]
SETS = {'5': {5}, '6': {6}, '7': {7}, '8': {8}, '9': {9}, 'S': {5, 6}, 'B': {7, 8, 9}, '*': {5, 6, 7, 8, 9}}
def lset(tok): return set().union(*[SETS[c] for c in tok[1:-1]]) if tok.startswith('{') else SETS[tok]
KEYS = []
for line in open(KF):
    if not line.strip() or line.lstrip().startswith('#'): continue
    m = re.match(r'^\s*(\S+)\s+EDGE\(([^)]*?)->([^)]*)\)(?:\[([^\]]*)\])?', line)
    KEYS.append((m.group(1), lset(m.group(2)), lset(m.group(3)), {p.split('=')[0]: lset(p.split('=')[1]) for p in (m.group(4) or '').split()}))
def counts(d, w, s, X, Y):
    W = lambda k: min(w[k % d], 9); S = lambda k: min(s[k % d], 9); x = lambda k: X[k % d]; y = lambda k: Y[k % d]
    out = {}; inn = {}
    for nm, U, Vp, pos in KEYS:
        o = n = 0
        for i in range(d):
            for sg in (1, -1):
                # OUT: payer c (letter d), payee w_i (spec 4.3 first table)
                P = {'S.L+1': W(i + sg), 'S.L+2': W(i + 2 * sg), 'S.L+3': W(i + 3 * sg), 'S.L-1': W(i - sg), 'S.L-2': W(i - 2 * sg), 'S.L-3': W(i - 3 * sg),
                     'S.A+1': S(i + 1) if sg == 1 else S(i - 2), 'S.A-1': S(i - 2) if sg == 1 else S(i + 1), 'R.L+2': S(i) if sg == 1 else S(i - 1), 'R.L-2': S(i - 1) if sg == 1 else S(i)}
                if d in U and W(i) in Vp and all(P[p] in st for p, st in pos.items()): o += 1
                # IN: payer w_i, payee c (spec 4.3 second table)
                if sg == 1: P = {'S.L+1': W(i - 1), 'S.L+2': S(i - 1), 'S.L+3': y(i), 'S.L-1': W(i + 1), 'S.L-2': S(i), 'S.L-3': x(i), 'S.A+1': x(i - 1), 'S.A-1': y(i + 1), 'R.L+2': W(i - 2), 'R.L-2': W(i + 2)}
                else: P = {'S.L+1': W(i + 1), 'S.L+2': S(i), 'S.L+3': x(i), 'S.L-1': W(i - 1), 'S.L-2': S(i - 1), 'S.L-3': y(i), 'S.A+1': y(i + 1), 'S.A-1': x(i - 1), 'R.L+2': W(i + 2), 'R.L-2': W(i - 2)}
                if W(i) in U and d in Vp and all(P[p] in st for p, st in pos.items()): n += 1
        if o or n: out[nm] = o; inn[nm] = n
    return out, inn
ap = lambda z: 7 if z >= 7 else 5
def h2_of(m, ar, al): return min(tuple(m) + (ap(ar), ap(al)), (m[0],) + tuple(reversed(m[1:])) + (ap(al), ap(ar)))
def qkey(m): return min(tuple(m), (m[0],) + tuple(reversed(m[1:])))
def copy(d, w, s, j, x_, y_):
    U = d; W = lambda k: w[k % d]; S = lambda k: s[k % d]; t = {}
    if w[j] == 6: t[('h', h2_of((U, W(j + 1), S(j), x_, S(j - 1), W(j - 1)), W(j + 2), W(j - 2)))] = 1
    if w[j] == 7:
        t[('q', qkey((U, W(j + 1), S(j), x_, y_, S(j - 1), W(j - 1))))] = 1
        Vv = () if d == 7 else (8,)
        for c_, a_, l_ in ((W(j + 1), S(j), x_), (W(j - 1), S(j - 1), y_)):
            if c_ <= 6 and a_ <= 6: k_ = ('lq', Vv + (c_, a_, l_)); t[k_] = t.get(k_, 0) + 1
    return t
def jk(c): return json.dumps(c)
bad = 0
for e in json.load(open(V)):
    _, d, lk, sv, rho = e['id']; w = [int(c) for c in lk]; s = [int(c) for c in sv]
    X = [int(rho[2 * j]) for j in range(d)]; Y = [int(rho[2 * j + 1]) for j in range(d)]
    for j in range(d):   # section 2: a 5's letters are its apexes, a 6 has x = y
        if w[j] == 5 and (X[j], Y[j]) != (s[(j - 1) % d], s[j]): bad += 1; print('  5 at %d: rho %d%d != (s_{j-1}, s_j)' % (j, X[j], Y[j]))
        if w[j] == 6 and X[j] != Y[j]: bad += 1; print('  6 at %d: x != y' % j)
    out, inn = counts(d, w, s, X, Y)
    eng = {k['key']: (k['OUT'], k['IN']) for k in e['keys_nonzero_IN_or_OUT']}
    mine = {nm: (out[nm], inn[nm]) for nm in out}
    if mine != eng: bad += 1; print('  %s: key counts differ: spec-only %s engine-only %s' % (e['id'], sorted(set(mine.items()) - set(eng.items()))[:6], sorted(set(eng.items()) - set(mine.items()))[:6]))
    row = {}
    for c, v in e['fixed']: row[jk(c)] = row.get(jk(c), 0) + v
    for j in range(d):
        t = copy(d, w, s, j, X[j], Y[j]); tj = {jk([k_[0], list(k_[1])]): v for k_, v in t.items()}
        ge = {jk(c): v for c, v in e['groups'][j]['terms']}
        if tj != ge: bad += 1; print('  %s group %d: copy terms differ: spec %s engine %s' % (e['id'], j, tj, ge))
        for k_, v in tj.items(): row[k_] = row.get(k_, 0) + v
    for nm in out:
        if inn[nm] != out[nm]: k_ = jk(['ks', nm]); row[k_] = row.get(k_, 0) + inn[nm] - out[nm]
    row = {k_: v for k_, v in row.items() if v}
    if row != {jk(c): v for c, v in e['row']}: bad += 1; print('  %s: row differs' % (e['id'],))
    print('%s %s/%s rho %s: %d keys with IN or OUT, row %d entries: %s' % (d, lk, sv, rho, len(mine), len(row), 'ok' if not bad else 'MISMATCH'))
print('SPEC-CHECK: %s (%d mismatches)' % ('PASS' if bad == 0 else 'FAIL', bad))
