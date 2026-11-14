"""Build rules.sqlite + rules_graph.json for the 604 parts (beat_633_588 synth_rules_588.txt)."""
import sys, json, sqlite3, collections as C, numpy as np
sys.path.insert(0, 'code')
from parts import parse
from mir import mirror

RULES, OUTDB, OUTJSON, BEH58, BEH911 = sys.argv[1:6]
SCALE, P = parse(RULES)
T = 2
FULL = (5, 9)
GEN = (5, 9, 5, 9, ())


def rng_txt(lo, hi):
    if (lo, hi) == FULL:
        return '*'
    if lo == hi:
        return '=9+' if lo == 9 else f'={lo}'
    if hi == 9:
        return f'>={lo}'
    if lo == 5:
        return f'<={hi}'
    return f'in{lo}..{hi}'


def word(lo, hi):
    if lo == hi:
        return '9 or more' if lo == 9 else str(lo)
    if hi == 9:
        return f'{lo} or more'
    if lo == 5:
        return f'at most {hi}'
    return f'{lo} to {hi}'


def tmpl(p):
    return {'drule': 'RSST', 'SP_': 'push', 'STm_': 'tunnel', 'STp_': 'tunnel'}[p['pre']]


def constraints(p):
    out = []
    for j, s in enumerate(p['slots']):
        if (s[0], s[1]) != FULL:
            out.append((j, 'spoke', 0, s[0], s[1]))
        if (s[2], s[3]) != FULL:
            out.append((j, 'hat', 0, s[2], s[3]))
        for k, (lo, hi) in enumerate(s[4]):
            if (lo, hi) != FULL:
                out.append((j, 'fan', k + 1, lo, hi))
    return out


def lab(j, h):
    o = (j - T) % h
    if o > h // 2:
        o -= h
    return 'T' if o == 0 else (f'R{o}' if o > 0 else f'L{-o}')


def compact(p):
    h = p['hub']
    cs = constraints(p)
    w = p['w']
    head = f"H{h} {'+' if w > 0 else '-'}{abs(w)}/{SCALE} -> T"
    body = []
    for j, role, k, lo, hi in cs:
        name = lab(j, h)
        if role == 'hat':
            name = 'h(' + lab((j - 1) % h, h) + ',' + name + ')'
        elif role == 'fan':
            name = f'f{k}({name})'
        body.append(name + rng_txt(lo, hi))
    return head + ' | ' + ' '.join(body)


def english(p):
    h = p['hub']
    w = p['w']
    amt = f'{abs(w)}/{SCALE}'
    what = f'A degree-{h} vertex sends {amt} of charge to its target neighbour T' if w > 0 else \
        f'A degree-{h} vertex takes back {amt} of charge from its target neighbour T'
    conds = []
    for j, role, k, lo, hi in constraints(p):
        name = lab(j, h)
        nm = 'T' if name == 'T' else f'neighbour {name}'
        if role == 'spoke':
            conds.append(f'{nm} has degree {word(lo, hi)}')
        elif role == 'hat':
            a = lab((j - 1) % h, h)
            conds.append(f'the vertex beyond the edge {a}-{name} has degree {word(lo, hi)}')
        else:
            conds.append(f'fan vertex {k} of {name} has degree {word(lo, hi)}')
    return what + (' when ' + '; '.join(conds) if conds else ' always') + '.'


# ---- ids, mirrors
n = len(P)
key = {}
for i, p in enumerate(P):
    key.setdefault((p['pre'], p['hub'], p['w'], p['slots']), []).append(i)
mir = [None] * n
for i, p in enumerate(P):
    ms = mirror(p, T, 1, 'with_spoke')
    js = key.get((p['pre'], p['hub'], p['w'], ms), [])
    mir[i] = i if ms == p['slots'] else (js[0] if js else None)

# ---- edges
E = []
canon = [min(p['slots'], mirror(p, T, 1, 'with_spoke')) for p in P]
vari = [[p['slots'], mirror(p, T, 1, 'with_spoke')] for p in P]
for i in range(n):
    if mir[i] is not None and mir[i] > i:
        E.append((i, mir[i], 'mirror'))
by = C.defaultdict(list)
for i, p in enumerate(P):
    by[(p['pre'], p['hub'], p['w'])].append(i)
for g, idx in by.items():
    for a in range(len(idx)):
        for b in range(a + 1, len(idx)):
            i, j = idx[a], idx[b]
            if canon[i] == canon[j]:
                continue
            if any(sum(x != y for x, y in zip(si, P[j]['slots'])) == 1 for si in vari[i]):
                E.append((i, j, 'one-slot edit'))
rot = C.defaultdict(list)
for i, p in enumerate(P):
    cands = [s[r:] + s[:r] for s in vari[i] for r in range(len(s))]
    rot[(p['hub'], min(cands))].append(i)
for g, idx in rot.items():
    for a in range(len(idx)):
        for b in range(a + 1, len(idx)):
            i, j = idx[a], idx[b]
            if canon[i] != canon[j] and mir[i] != j:
                E.append((i, j, 'retarget'))
look = C.defaultdict(list)
for i, p in enumerate(P):
    look[(p['pre'], p['hub'], p['w'], p['slots'])].append(i)
for i, p in enumerate(P):
    s = p['slots']
    for r in range(len(s)):
        if r == T or s[r] != GEN:
            continue
        s2 = s[:r] + s[r + 1:]
        for j in look.get((p['pre'], p['hub'] - 1, p['w'], s2), []):
            E.append((j, i, 'lift (add free spoke)'))

# ---- behaviour (mirror-symmetrised, by where the 5s sit)
def load(a, b):
    rows, Ms = [], []
    for z in (np.load(a), np.load(b)):
        for d in range(5, 12):
            if f'M{d}' in z:
                Ms.append(z[f'M{d}'])
                rows += [(d, tuple(int(x) for x in w)) for w in z[f'W{d}']]
    return np.vstack(Ms).astype(np.float64), rows


def fivepat(w):
    b = tuple(1 if x == 5 else 0 for x in w)
    d = len(b)
    return min(min(b[r:] + b[:r], tuple(reversed(b[r:] + b[:r]))) for r in range(d))


M, rows = load(BEH58, BEH911)
Msym = np.stack([(M[:, i] + M[:, mir[i] if mir[i] is not None else i]) / 2 for i in range(n)], 1)
nrm = np.linalg.norm(Msym, axis=0)
Y = Msym / np.where(nrm > 0, nrm, 1)
G = Y.T @ Y
for i in range(n):
    for j in range(i + 1, n):
        if G[i, j] >= 0.999 and canon[i] != canon[j] and mir[i] != j:
            E.append((i, j, 'same job (behaviour cos>=0.999)'))
grp = C.defaultdict(list)
for r, (d, w) in enumerate(rows):
    grp[(d, fivepat(w))].append(r)
gkeys = list(grp)
X = np.vstack([Msym[grp[k]].sum(0) for k in gkeys])
Xn = X / np.where(np.linalg.norm(X, axis=0) > 0, np.linalg.norm(X, axis=0), 1)
U, S, Vt = np.linalg.svd(Xn, full_matrices=False)
NF = 6
def gname(k):
    d, b = k
    return f'd{d} ' + ''.join('5' if x else '+' for x in b)
factor_desc = []
for f in range(NF):
    top = np.argsort(-np.abs(U[:, f]))[:3]
    factor_desc.append(', '.join(gname(gkeys[t]) for t in top))
topfac = [int(np.argmax(np.abs(Vt[:NF, i]))) + 1 for i in range(n)]

# components (schemas) over structural edges
par = list(range(n))
def fd(x):
    while par[x] != x:
        par[x] = par[par[x]]
        x = par[x]
    return x
for a, b, t in E:
    if t in ('mirror', 'one-slot edit', 'retarget', 'lift (add free spoke)'):
        par[fd(a)] = fd(b)
roots = {}
schema = [roots.setdefault(fd(i), len(roots) + 1) for i in range(n)]
par = list(range(n))
for a, b, t in E:
    par[fd(a)] = fd(b)
roots = {}
family = [roots.setdefault(fd(i), len(roots) + 1) for i in range(n)]

# ---- write sqlite
db = sqlite3.connect(OUTDB)
c = db.cursor()
c.executescript('''
DROP TABLE IF EXISTS parts; DROP TABLE IF EXISTS constraints; DROP TABLE IF EXISTS edges;
DROP TABLE IF EXISTS behaviour; DROP TABLE IF EXISTS factors; DROP TABLE IF EXISTS symbols;
CREATE TABLE parts(id INTEGER PRIMARY KEY, tag TEXT, template TEXT, hub INT, weight INT, scale INT,
  target_slot INT, mirror_id INT, self_mirror INT, schema_id INT, family_id INT, top_factor INT,
  n_pinned INT, compact TEXT, english TEXT);
CREATE TABLE constraints(part_id INT, slot INT, position TEXT, role TEXT, fan_index INT, lo INT, hi INT);
CREATE TABLE edges(a INT, b INT, kind TEXT);
CREATE TABLE behaviour(part_id INT, receiver_degree INT, five_pattern TEXT, charge REAL);
CREATE TABLE factors(factor INT, top_neighbourhoods TEXT);
CREATE TABLE symbols(symbol TEXT, meaning TEXT);
''')
for i, p in enumerate(P):
    cs = constraints(p)
    c.execute('INSERT INTO parts VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',
              (i, p['tag'], tmpl(p), p['hub'], p['w'], SCALE, T, mir[i], int(mir[i] == i), schema[i], family[i],
               topfac[i], len(cs), compact(p), english(p)))
    for j, role, k, lo, hi in cs:
        c.execute('INSERT INTO constraints VALUES (?,?,?,?,?,?,?)', (i, j, lab(j, p['hub']), role, k, lo, hi))
c.executemany('INSERT INTO edges VALUES (?,?,?)', E)
for gi, k in enumerate(gkeys):
    for i in np.nonzero(np.abs(X[gi]) > 1e-9)[0]:
        c.execute('INSERT INTO behaviour VALUES (?,?,?,?)', (int(i), k[0], gname(k).split(' ')[1], float(X[gi, i])))
for f in range(NF):
    c.execute('INSERT INTO factors VALUES (?,?)', (f + 1, factor_desc[f]))
SYM = [('H<d>', 'the hub: the vertex that sends charge; d = its degree (5..8)'),
       ('T', 'the target: the hub neighbour that receives (slot 2)'),
       ('L<k>, R<k>', 'the k-th hub neighbour counter-clockwise (L) or clockwise (R) of T'),
       ('h(X,Y)', 'hat: the second-ring vertex across the edge X-Y of two consecutive hub neighbours'),
       ('f<k>(X)', 'fan k of X: X\'s k-th neighbour outside the hub\'s 1-ball, between its two hats (only when X has exact degree 6..8; X has deg-5 fans)'),
       ('=k, >=k, <=k, ina..b, *', 'degree ranges over 5,6,7,8,9+ (9 means 9 or more); * = anything'),
       ('+w/M, -w/M', 'charge moved from H to T (positive) or taken back (negative), M = 60'),
       ('mirror', 'reflect the picture through the H-T axis'),
       ('retarget', 'the same picture read with a different neighbour as T'),
       ('lift', 'insert a neighbour with no condition, raising the hub degree by 1'),
       ('one-slot edit', 'change the conditions on one neighbour (its degree, hat or fans)')]
c.executemany('INSERT INTO symbols VALUES (?,?)', SYM)
db.commit()

# ---- json graph for the browser
nodes = []
for i, p in enumerate(P):
    nodes.append(dict(id=i, tag=p['tag'], t=tmpl(p), hub=p['hub'], w=p['w'], m=mir[i], s=schema[i], fam=family[i],
                      fac=topfac[i], np=len(constraints(p)), c=compact(p), e=english(p),
                      sl=[[s[0], s[1], s[2], s[3], [list(f) for f in s[4]]] for s in p['slots']]))
json.dump(dict(scale=SCALE, target=T, nodes=nodes, edges=[[a, b, t] for a, b, t in E],
               factors=factor_desc, symbols=SYM), open(OUTJSON, 'w'), separators=(',', ':'))
print('parts', n, 'edges', C.Counter(t for _, _, t in E), 'schemas', max(schema), 'families', max(family))
print('ranges used', C.Counter(rng_txt(lo, hi) for p in P for (_, _, _, lo, hi) in constraints(p)).most_common())
print(compact(P[0])); print(english(P[0])); print(compact(P[100])); print(english(P[100]))
print('factors', factor_desc)
