#!/usr/bin/env python3
"""RSST-1SHOT core (Studio, independent re-implementation of RSSTFP_SPEC 33338de6).
Built from the spec text only. Inputs: rsst_drules.v (Gonthier parts), unavoidable.conf (633 RSST configs),
rsst_verdicts.txt; the containment test follows rsst_rows.py c9f344bd (`prep`/`contains` logic, re-typed here
so that the parser does not depend on rsst_parse)."""
import os, re, collections, itertools

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..'))   # .../wheeldis
PS = os.path.abspath(os.path.join(ROOT, '..', '..', '..', '..'))                                          # planemap-structural
DRULES = os.path.join(ROOT, 'loop', 'pubrules', 'data', 'rsst_drules.v')
CONF = os.path.join(PS, 'studiointel', 'routeb', 'rsst', 'unavoidable.conf')
VERD = os.path.join(ROOT, 'loop', 'k44', 'rsst_verdicts.txt')
FULL = (5, 9)
CONTROL = os.environ.get('RSST_CONTROL', '')
U_HOST_ALWAYS = False   # set True by the §13 (d = 9..14) engine; CONTROL = planted mis-implementation switch (README)

# ---------------------------------------------------------------- parts (§3.1, §3.2)
def rng(tok):
    if tok == '*': return FULL
    m = re.fullmatch(r'(\d)\?(\d)', tok)
    if m: return (int(m.group(1)), int(m.group(2)))
    m = re.fullmatch(r'(\d)\+', tok)
    if m: return (int(m.group(1)), 9)
    m = re.fullmatch(r'(\d)-', tok)
    if m: return (5, int(m.group(1)))
    if re.fullmatch(r'\d', tok): return (int(tok), int(tok))
    raise ValueError(tok)

def parse_part(body):
    # body: text between 'Part' and final '.', i.e. "$ * $[5] 5 $ ... $"
    chunks = body.split('$')[1:-1]
    subs = []
    for ch in chunks:
        ch = ch.strip(); hat = FULL; fans = []
        m = re.match(r'\[([^\]]*)\]\s*(.*)', ch)
        if m:
            toks = m.group(1).split(); ch = m.group(2).strip()
            hat = rng(toks[0]); fans = [rng(t) for t in toks[1:]]
        sp = rng(ch)
        if sp[0] == sp[1] and 6 <= sp[0] <= 8:
            fans = fans + [FULL] * (sp[0] - 5 - len(fans))
        assert len(fans) <= max(0, sp[0] - 5) or not fans, (body, ch)
        subs.append((sp, hat, tuple(fans)))
    return subs

def mirror(p):
    n = len(p)
    return [(p[(4 - k) % n][0], p[(5 - k) % n][1], tuple(reversed(p[(4 - k) % n][2]))) for k in range(n)]

def rsub(a, b): return b[0] <= a[0] and a[1] <= b[1]
def psub(p, q):
    if len(p) != len(q): return False
    for (s1, h1, f1), (s2, h2, f2) in zip(p, q):
        if not (rsub(s1, s2) and rsub(h1, h2)): return False
        if f2:
            if len(f1) != len(f2): return False
            if not all(rsub(a, b) for a, b in zip(f1, f2)): return False
    return True

def load_parts():
    txt = open(DRULES).read()
    defs = {}
    for m in re.finditer(r'Definition\s+(\S+)\s*:=\s*Part(.*?)\.\s*\n', txt):
        defs[m.group(1)] = parse_part(m.group(2))
    m = re.search(r'base_drules\s*:\s*drules\s*:=\s*@seqn part (\d+)(.*?)\.', txt, re.S)
    names = m.group(2).split(); assert len(names) == int(m.group(1)) == 38
    seen = collections.Counter(); out = []
    for nm in names:
        seen[nm] += 1; tag = nm if seen[nm] == 1 else '%s#%d' % (nm, seen[nm])
        p = defs[nm]; out.append((tag, p))
        mp = mirror(p)
        if not psub(mp, p): out.append((tag + 'm', mp))
    return out

def fmt_r(r):
    if r == FULL: return '*'
    if r[0] == r[1]: return '=%d' % r[0]
    if r[1] == 9: return '>=%d' % r[0]
    if r[0] == 5: return '<=%d' % r[1]
    return 'in%d..%d' % r

def parts_text(parts):
    lines = []
    for tag, p in parts:
        lines.append('%s\t%d\t%s' % (tag, len(p), '  '.join('%s[%s|%s]' % (fmt_r(s), fmt_r(h), ','.join(fmt_r(f) for f in fs)) for s, h, fs in p)))
    return lines

PARTS = load_parts()
if CONTROL == 'nomirror':                      # planted control: drop all mirrors
    PARTS = [(t, p) for t, p in PARTS if not t.endswith('m') or t in ('drule1#2',)]

# ---------------------------------------------------------------- window (§2)
def npriv(L): return 0 if L == 5 else (3 if L >= 9 else L - 5)

class Window:
    """d, link letters (5..9; 9 = 9+), apex letters (5..9) or None (= variable 's<i>')."""
    def __init__(self, d, link, apex):
        self.d = d; self.link = list(link); self.apex = list(apex) if apex is not None else [None] * d
        self.seg = []
        for i in range(d):
            k = npriv(self.link[i])
            self.seg.append([('s', (i - 1) % d)] + [('p', i, j) for j in range(1, k + 1)] + [('s', i)])
        self.rot = {'u': [('w', i) for i in range(d)]}
        for i in range(d):
            self.rot[('w', i)] = ['u', ('w', (i - 1) % d)] + self.seg[i] + [('w', (i + 1) % d)]
        R2 = []
        for i in range(d): R2 += self.seg[i][:-1]
        self.R2 = R2; n = len(R2)
        self.r2prev = {R2[t]: R2[t - 1] for t in range(n)}; self.r2next = {R2[t]: R2[(t + 1) % n] for t in range(n)}

    def deg(self, v):
        """('dec', value) | ('var', name) | ('open',)"""
        if v == 'u': return ('dec', min(self.d, 9))
        if v == 'R': return ('open',)
        if v[0] == 'w': return ('dec', self.link[v[1]])
        if v[0] == 's':
            a = self.apex[v[1]]
            return ('dec', a) if a is not None else ('var', 's%d' % v[1])
        return ('var', 'p%d.%d' % (v[1], v[2]))

    def succ(self, x, y):
        """z with face (x, y, z)."""
        if x == 'R': return 'R'
        if x == 'u' or x[0] == 'w':
            L = self.rot[x]; return L[(L.index(y) + 1) % len(L)]
        prev, nxt = self.r2prev[x], self.r2next[x]
        if x[0] == 's':
            i = x[1]; w1, w0 = ('w', (i + 1) % self.d), ('w', i)
            if y == w1: return w0
            if y == w0: return prev
            if y == prev: return 'R'
            if y == nxt: return w1
            return 'R'
        wi = ('w', x[1])
        if y == wi: return prev
        if y == prev: return 'R'
        if y == nxt: return wi
        return 'R'

# ---------------------------------------------------------------- fits (§3.3-3.5)
class Fail(Exception): pass

def _test(W, v, r, conds, st):
    if r == FULL: return
    k = W.deg(v)
    if k[0] == 'dec':
        val = k[1]
        if CONTROL == 'nine10' and val == 9: val = 10
        if not (r[0] <= val <= r[1]): raise Fail
    elif k[0] == 'open':
        st['open'] = True
    else:
        nm = k[1]
        if nm.startswith('p'):
            _, i, j = v
            assert not (W.link[i] >= 9 and j == 2), 'a 9+ middle was read'
        lo, hi = conds.get(nm, FULL); lo, hi = max(lo, r[0]), min(hi, r[1])
        if lo > hi: raise Fail
        conds[nm] = (lo, hi)

def fit(W, h, part, a):
    S = W.rot[h]; n = len(part)
    if len(S) != n: return None
    conds = {}; st = {'open': False}
    try:
        for j in range(n):
            sp, hat, fans = part[j]
            x, xp, xn = S[(a + j) % n], S[(a + j - 1) % n], S[(a + j + 1) % n]
            _test(W, x, sp, conds, st)
            if hat != FULL:
                hvx = W.succ(xn, x) if CONTROL == 'hatside' else W.succ(x, xp)   # control: hat read across x-xn
                _test(W, hvx, hat, conds, st)
            if any(f != FULL for f in fans):
                if x == 'u' or x[0] == 'w':
                    hv = W.succ(x, xp); hn = W.succ(xn, x)
                    R = W.rot[x]; t = (R.index(hv) + 1) % len(R); F = []
                    while R[t] != hn: F.append(R[t]); t = (t + 1) % len(R)
                    if len(F) != len(fans): raise Fail
                    for f, v in zip(fans, F): _test(W, v, f, conds, st)
                else:
                    st['open'] = True
    except Fail:
        return None
    return conds, st['open']

def instances(W):
    """All fits that move u's charge: list of dicts tag, hub, target, dir (+1 into u, -1 out of u), conds, open."""
    d = W.d; out = []
    byn = collections.defaultdict(list)
    for tag, p in PARTS: byn[len(p)].append((tag, p))
    if 5 <= d <= 8:
        for tag, p in byn[d]:
            for a in range(d):
                r = fit(W, 'u', p, a)
                if r: out.append({'tag': tag, 'hub': 'u', 'target': 'w%d' % W.rot['u'][(a + 2) % d][1], 'dir': -1, 'conds': r[0], 'open': r[1], 'anchor': a})
    for i in range(d):
        L = W.link[i]
        if L > 8: continue
        for tag, p in byn[L]:
            a = (L - 2) % L
            assert W.rot[('w', i)][(a + 2) % L] == 'u'
            r = fit(W, ('w', i), p, a)
            if r: out.append({'tag': tag, 'hub': 'w%d' % i, 'target': 'u', 'dir': 1, 'conds': r[0], 'open': r[1], 'anchor': a})
    return out

def holds(inst, f):
    for nm, (lo, hi) in inst['conds'].items():
        v = f[nm]
        if not (lo <= v <= hi): return False
    return True

def ledger(d, insts, f):
    base = 10 * (6 - d); lo = hi = base; fired = []
    for I in insts:
        if not holds(I, f): continue
        sure = not I['open']
        fired.append((I, sure))
        if I['dir'] > 0:
            hi += 1; lo += sure
        else:
            lo -= 1; hi -= sure
    return lo, hi, fired

def cond_text(I):
    if not I['conds']: return 'always'
    def key(nm):
        a, b = nm[1:].split('.'); return (int(a), int(b))
    return ' & '.join(nm + fmt_r(I['conds'][nm]) for nm in sorted(I['conds'], key=key))

# ---------------------------------------------------------------- RSST configurations (§7)
def parse_conf():
    toks = open(CONF).read().split('\n')
    out = []; t = 0
    while t < len(toks):
        line = toks[t].strip()
        if not line: t += 1; continue
        name = line; t += 1
        n, r, _a, _b = [int(z) for z in toks[t].split()[:4]]; t += 1
        cl = [int(z) for z in toks[t].split()]; t += 1
        k = cl[0]
        adj = {}
        for _ in range(n):
            f = [int(z) for z in toks[t].split()]; t += 1
            v, dg = f[0], f[1]; adj[v] = f[2:]; assert len(adj[v]) == dg, (name, f)
        while t < len(toks) and toks[t].strip(): t += 1
        out.append({'name': name, 'n': n, 'r': r, 'adj': adj, 'k_contract': k})
    return out

def prep(c):
    r, n = c['r'], c['n']; U = list(range(r + 1, n + 1))
    deg = {u: len(c['adj'][u]) for u in U}; E = {u: set(x for x in c['adj'][u] if x > r) for u in U}
    order = [max(U, key=lambda u: (deg[u], len(E[u])))]; seen = set(order)
    while len(order) < len(U):
        b = max((u for u in U if u not in seen), key=lambda u: (len(E[u] & seen), deg[u])); order.append(b); seen.add(b)
    faces = set()
    for u in U:
        L = c['adj'][u]
        for i in range(len(L)):
            a, b = L[i], L[(i + 1) % len(L)]
            if a > r and b > r: faces.add(frozenset((u, a, b)))
    return {'deg': deg, 'E': E, 'order': order, 'dm': collections.Counter(deg.values()), 'faces': faces,
            'ring': r, 'name': c['name']}

def load_configs():
    C = parse_conf(); assert len(C) == 633
    V = []
    for line in open(VERD):
        f = line.split()
        if f and f[0].startswith('rsst') and len(f) > 2:
            vd = [z for z in f if z.startswith('verdict=')][0].split('=')[1]
            V.append((f[0], vd))
    assert len(V) == 633
    P = []
    for i, (c, (rid, vd)) in enumerate(zip(C, V)):
        assert int(rid[4:7]) == i and rid.split('_', 1)[1].replace('o', '.') == c['name'], (rid, c['name'])
        p = prep(c); p['verdict'] = vd; p['proved'] = vd in ('D2', 'C2cons'); P.append(p)
    return P

CONFIGS = load_configs()

def window_hostgraph(W, d9_u_host=None):
    """Potential hosts: u (if d<=8), w_i with exact letter, s_i with exact letter (or variable), privates
    except 9+ middles. Letter sets: fixed {L} or variable {5..8} (variable hosts produce requirements)."""
    d = W.d; host = {}; var = {}
    if d <= 8 or U_HOST_ALWAYS: host['u'] = {d}      # §7/§10.2: u not a host at d >= 9; §13 A.1: u is a host
    for i in range(d):
        if W.link[i] <= 8: host[('w', i)] = {W.link[i]}
        a = W.apex[i]
        if a is None: host[('s', i)] = {5, 6, 7, 8}; var[('s', i)] = 's%d' % i
        elif a <= 8: host[('s', i)] = {a}
        for j in range(1, npriv(W.link[i]) + 1):
            if W.link[i] >= 9 and j == 2: continue
            host[('p', i, j)] = {5, 6, 7, 8}; var[('p', i, j)] = 'p%d.%d' % (i, j)
    adj = {v: set() for v in host}
    def e(a, b):
        if a in host and b in host and a != b: adj[a].add(b); adj[b].add(a)
    for i in range(d):
        e('u', ('w', i)); e(('w', i), ('w', (i + 1) % d)); e(('s', i), ('w', (i + 1) % d))
        sg = W.seg[i]
        for t in range(len(sg)):
            e(('w', i), sg[t])
            if t + 1 < len(sg): e(sg[t], sg[t + 1])
    return host, adj, var

def all_embeddings(host, adj, p, var):
    """All injective induced face-preserving maps of p's interior into the host graph; returns the set of
    requirements (frozenset of (varname, letter)) on variable hosts."""
    order, deg, E = p['order'], p['deg'], p['E']; phi = {}; used = set(); reqs = set()
    def rec(k):
        if k == len(order):
            for f in p['faces']:
                a, b, c = (phi[x] for x in f)
                if not (b in adj[a] and c in adj[a] and c in adj[b]): return
            reqs.add(frozenset((var[phi[x]], deg[x]) for x in phi if phi[x] in var)); return
        x = order[k]; nb = [y for y in order[:k] if y in E[x]]
        for t in (adj[phi[nb[0]]] if nb else host.keys()):
            if t in used or deg[x] not in host[t]: continue
            if CONTROL != 'notinduced':
                if any((y in E[x]) != (phi[y] in adj[t]) for y in order[:k]): continue
            else:
                if any((y in E[x]) and not (phi[y] in adj[t]) for y in order[:k]): continue
            phi[x] = t; used.add(t); rec(k + 1); del phi[x]; used.discard(t)
    rec(0)
    # keep only minimal requirements
    rl = sorted(reqs, key=len); keep = []
    for r in rl:
        if not any(q <= r for q in keep): keep.append(r)
    return keep

def requirements(W):
    """config index -> list of minimal requirements (frozensets of (var, letter)); empty frozenset = always."""
    host, adj, var = window_hostgraph(W)
    hc = collections.Counter()
    for v, S in host.items():
        for x in S: hc[x] += 1
    out = {}
    for ci, p in enumerate(CONFIGS):
        if CONTROL == 'drop2122' and p['name'] in ('2.122', '0.7322'): continue   # planted kill-side control
        if len(p['deg']) > len(host): continue
        if any(hc[x] < m for x, m in p['dm'].items()): continue
        rq = all_embeddings(host, adj, p, var)
        if rq: out[ci] = rq
    return out

def contained(reqs, f):
    """f: var -> letter (9 = not a host). Returns list of config indices contained."""
    res = []
    for ci, rl in reqs.items():
        for r in rl:
            if all(f.get(nm) == L for nm, L in r): res.append(ci); break
    return res
