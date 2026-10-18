"""Studio (sealed task, 18 Oct 23:36Z): independent RSST-rule scoring of the d = 7 receiver link 7665566, s 6675666
(reflection 6665766; canonical 5566766/5666667), as rsst_score.py did for R* (a3b52bb7).
Cases: the second ring is fixed by the s-word; the privates of the non-5 link vertices (d_i - 5 each: w0 x2, w1, w2, w5,
w6 x1) run over 5..9 (9 = degree >= 9): 5^6 = 15,625 cases; the third ring is free.
Geometry: grow.py's build2 (explore's round-42 builder, nothing from Team B) with this arrangement: a ring-2 vertex
adjacent to w_i and w_{i+1} is s_i (s_{D-1} between w_{D-1} and w_0); the others adjacent to one w_i are its privates.
Rules: rsst_score.py's Gonthier encoding (discharge.v, 71 parts after symmetrize) and its fit semantics, unchanged.
Containment: grow.py's embeddings over the 633 RSST configurations (interior onto the 2-ball's named vertices, exact
degrees, induced, interior triangles onto faces; a variable slot takes only degrees 5..8, so a private of degree 9+
never carries a configuration vertex).
Usage: python3 rsst_lt7.py   -> rsst_lt7.txt, rsst_lt7_cases.txt"""
import os, sys, itertools, collections
H = os.path.dirname(os.path.abspath(__file__))
SRC = open(os.path.join(H, 'rsst_score.py')).read()
RS = {'__file__': os.path.join(H, 'rsst_score.py'), '__name__': 'rsst_score_lib'}
exec(SRC[:SRC.index('def score_cases')], RS)          # rules (RULES), fit helpers, and grow.py loaded as RS['G']
G = RS['G']
D, LK, SW = 7, [7, 6, 6, 5, 5, 6, 6], [6, 6, 7, 5, 6, 6, 6]
G['D'] = D; G['LK'] = LK; G['SV'] = {i: SW[i] for i in range(D)}
VAR = [('p', i, k) for i in range(D) for k in range(1, LK[i] - 4)]
G['VAR'] = VAR
def letters(a, b, p):          # same signature as grow.py's; only p (the 6 privates, in VAR order) is used
    r2 = {('s', j): v for j, v in G['SV'].items()}
    for k, nm in enumerate(VAR): r2[nm] = p[k]
    return r2
G['letters'] = letters
assert len(VAR) == 6, VAR

def charge_u(pv):
    adj, name, faces = G['build2'](letters(None, None, pv))
    inv = {v: x for x, v in name.items()}
    fd = G['fixed_deg'](); var = dict(zip(VAR, pv)); deg = {}
    for x, v in inv.items():
        if x in fd: deg[v] = fd[x]
        elif x in var: deg[v] = var[x]
    # check the reading: each s_i is adjacent to exactly w_i and w_{i+1}; privates of w_i adjacent to w_i only
    for i in range(D):
        s = inv[('s', i)]; ws = sorted(name[y][1] for y in adj[s] if name.get(y, ('',))[0] == 'w')
        assert ws == sorted({i, (i + 1) % D}), (i, ws)
    tri = set(faces)
    rot, hat, fans, fits = make_fit(adj, tri, deg)
    u = inv[('u',)]; Su = rot(u); assert Su and len(Su) == 7
    out = collections.Counter(); inn_lo = collections.Counter(); inn_hi = collections.Counter()
    for a in range(7):
        for p in RS['RULES']:
            if len(p) != 7: continue
            f = fits(u, Su, a, p)
            assert f != 'maybe', ('u outflow depends on an unknown degree', pv)
            if f == 'yes': out[Su[(a + 2) % 7]] += 1
    for w in Su:
        d = deg[w]; Sw = rot(w)
        if Sw is None or len(Sw) != d: raise RuntimeError('no rotation at %s' % (name[w],))
        for a in range(d):
            if Sw[(a + 2) % d] != u: continue
            for p in RS['RULES']:
                if len(p) != d: continue
                f = fits(w, Sw, a, p)
                if f == 'yes': inn_lo[w] += 1; inn_hi[w] += 1
                elif f == 'maybe': inn_hi[w] += 1
    base = 10 * (6 - 7)
    lo = base + sum(inn_lo.values()) - sum(out.values()); hi = base + sum(inn_hi.values()) - sum(out.values())
    detail = ' '.join('%s:out%d/in%d..%d' % (''.join(map(str, name[w][:2])), out[w], inn_lo[w], inn_hi[w]) for w in Su)
    return lo, hi, detail

def make_fit(adj, tri, deg):
    """the fit test of rsst_score.charge_u, lifted out unchanged (rotation, hats, fans, yes/no/maybe)."""
    def rot(h):
        nb = adj[h]; nxt = collections.defaultdict(set)
        for t in tri:
            if h in t:
                a, b = sorted(t - {h}); nxt[a].add(b); nxt[b].add(a)
        if any(len(nxt[x]) != 2 for x in nb): return None
        start = min(nb); cyc = [start]; prev = None
        while True:
            c = sorted(nxt[cyc[-1]] - ({prev} if prev is not None else set()))
            c = [y for y in c if y not in cyc[1:]] or c
            y = c[0]
            if y == cyc[0]: break
            prev = cyc[-1]; cyc.append(y)
            if len(cyc) > len(nb): return None
        return cyc if len(cyc) == len(nb) else None
    def hat(h, x, y):
        c = [z for z in (adj[x] & adj[y]) if z != h and frozenset((x, y, z)) in tri]
        return c[0] if c else None
    def fans(h, x, ha, hb):
        r = rot(x)
        if r is None: return None
        n = len(r); i, j, k = r.index(ha), r.index(hb), r.index(h)
        for step in (1, -1):
            path = []; q = i
            while True:
                q = (q + step) % n
                if r[q] == hb: break
                path.append(r[q])
            if r[k] not in path: return path
        return None
    def test(v, R):
        if v in deg:
            d = deg[v]; return 'yes' if R[0] <= d <= R[1] else 'no'
        return 'yes' if R == (5, 9) else 'maybe'
    def fits(h, S, a, p):
        n = len(S); st = 'yes'
        for j, (sp, hr, fr) in enumerate(p):
            x = S[(a + j) % n]; xp = S[(a + j - 1) % n]; xn = S[(a + j + 1) % n]
            t = test(x, sp)
            if t == 'no': return 'no'
            if t == 'maybe': st = 'maybe'
            hv = hat(h, xp, x)
            t = 'maybe' if hv is None else test(hv, hr)
            if hr == (5, 9): t = 'yes'
            if t == 'no': return 'no'
            if t == 'maybe': st = 'maybe'
            if fr and any(r_ != (5, 9) for r_ in fr):
                hn = hat(h, x, xn)
                F = fans(h, x, hv, hn) if (hv is not None and hn is not None) else None
                if F is None or len(F) != len(fr):
                    if x in deg: return 'no' if F is not None else 'maybe'
                    st = 'maybe'; continue
                for fv, R in zip(F, fr):
                    t = test(fv, R)
                    if t == 'no': return 'no'
                    if t == 'maybe': st = 'maybe'
        return st
    return rot, hat, fans, fits

if __name__ == '__main__':
    print('rules: %d parts after symmetrize; privates %s' % (len(RS['RULES']), VAR), flush=True)
    P, pa, pf = G['structure'](); fd = G['fixed_deg']()
    keys = set(); nine = 0; percfg = collections.defaultdict(set)
    for c in G['rsst']():
        for e in G['embeddings'](c, P, pa, pf, fd):
            req = dict((v, c[3][u]) for u, v in e if v not in fd)
            if any(x >= 9 for x in req.values()): nine += 1
            key = tuple(req.get(x, 0) for x in VAR); keys.add(key); percfg[key].add(c[1])
    def contains(pv): return [k for k in keys if all(q == 0 or q == x for q, x in zip(k, pv))]
    res = collections.Counter(); rows = []
    for pv in itertools.product(G['LET'], repeat=6):
        lo, hi, det = charge_u(pv); ks = contains(pv)
        cfg = sorted(set().union(*[percfg[k] for k in ks])) if ks else []
        res[(lo, hi)] += 1
        rows.append('%s charge %s rsst %d %s %s' % (''.join(map(str, pv)), lo if lo == hi else '[%d,%d]' % (lo, hi), len(cfg), (cfg[0] if cfg else '-').replace(' ', '_'), det))
    nz = [r for r in rows if not r.split()[2] == '0']
    nofree = [r for r in nz if r.split()[4] == '0']
    lines = ['# d=7 receiver 7665566/6675666: u charge by the 32 RSST rules (Gonthier encoding); privates %s in 5..9' % VAR,
             'cases %d; charge histogram %s' % (len(rows), dict(sorted(res.items()))),
             'zero %d, non-zero %d, max %s' % (len(rows) - len(nz), len(nz), max(hi for (lo, hi) in res)),
             'non-zero cases with no RSST configuration: %d' % len(nofree),
             'RSST embeddings needing a 9+ private: %d (variable slots take 5..8 only)' % nine,
             'distinct containment requirement keys: %d' % len(keys)]
    open(os.path.join(H, 'rsst_lt7.txt'), 'w').write('\n'.join(lines) + '\n')
    open(os.path.join(H, 'rsst_lt7_cases.txt'), 'w').write('# privates (VAR order) charge rsst <n configs> <first> <per-neighbour in/out>\n' + '\n'.join(rows) + '\n')
    print('\n'.join(lines))
