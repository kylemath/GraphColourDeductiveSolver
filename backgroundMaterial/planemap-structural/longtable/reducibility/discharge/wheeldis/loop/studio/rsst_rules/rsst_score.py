"""Studio (sealed task, 18 Oct): an independent scoring of R*'s centre u by the 32 discharging rules of Robertson,
Sanders, Seymour and Thomas, over the 250,000 round-42 cases (loop/k42: R* = d7 link 5675765, s 6.77.75 with s1, s4 in
{6,7,8,9} and the privates p1 p2a p2b p4a p4b p5 in 5..9).

Rule source: Gonthier's machine-checked encoding of the 32 rules (fourcolor, proof/discharge.v: drule1 .. drule32 and
base_drules with multiplicity, symmetrize_drules), read from the local opam install. Nothing from any other team.
Semantics, as part.v/discharge.v state them, in triangulation terms:
- a part is a list of subparts around a hub vertex h (in cyclic order); subpart j has a spoke (the j-th neighbour of
  h), a hat (the other common neighbour of spokes j-1 and j) and, when the spoke range is an exact N in 6..8, N-5 fans
  (the spoke's private neighbours, in order from the hat side);
- ranges: * = 5..9, M = [M,M], M?N, M+ = [M,9], N- = [5,N]; 9 means degree >= 9;
- a part fits at h (exact_fitp) if deg h = number of subparts and every range holds; each fit moves 1 unit from h to
  the third spoke (subpart index 2); charge(h) = 10 (6 - deg h) + inflow - outflow;
- the_drules = base_drules (38, with multiplicity) plus, for each, its reflection across the third spoke unless the
  reflection is a subset of it (symmetrize_drules).
Geometry: grow.py's build2 (u, link, second ring as named, a fresh third ring). Third-ring degrees are not part of a
case; a rule constraint on a third-ring vertex is evaluated as yes (holds for every degree), no, or maybe, and u's
charge is reported as an interval when a maybe occurs.
Containment: a case contains an RSST configuration if grow.py's embedding requirements (RSST's 633 only) cover it.
Usage: python3 rsst_score.py   -> rsst_score.txt"""
import os, re, sys, itertools, collections
H = os.path.dirname(os.path.abspath(__file__)); K = os.path.normpath(os.path.join(H, '..', '..', 'k42'))
G = {'__file__': os.path.join(K, 'grow.py'), '__name__': 'grow'}; exec(open(G['__file__']).read(), G)
DIS = os.path.expanduser('~/.opam/fourcolor/lib/coq/user-contrib/fourcolor/proof/discharge.v')

def rng(tok):
    if tok == '*': return (5, 9)
    m = re.fullmatch(r'(\d)\?(\d)', tok)
    if m: return (int(m.group(1)), int(m.group(2)))
    m = re.fullmatch(r'(\d)\+', tok)
    if m: return (int(m.group(1)), 9)
    m = re.fullmatch(r'(\d)-', tok)
    if m: return (5, int(m.group(1)))
    return (int(tok), int(tok))
def parse_part(txt):
    """'$ * $[5] 5 $ 7+ $' -> list of (spoke, hat, fans)"""
    body = txt.strip(); assert body.endswith('$'); body = body[:-1]
    subs = []
    for m in re.finditer(r'\$\s*(\[([^\]]*)\])?\s*([^\s$\[\]]+)', body):
        br, sp = m.group(2), rng(m.group(3))
        hat, fans = (5, 9), []
        if br is not None:
            t = br.split(); hat = rng(t[0]); fans = [rng(x) for x in t[1:]]
        if sp[0] == sp[1] and 6 <= sp[0] <= 8:
            fans = fans + [(5, 9)] * (sp[0] - 5 - len(fans))
        assert len(fans) <= max(0, sp[0] - 5) or not fans, txt
        subs.append((sp, hat, tuple(fans)))
    return subs
src = open(DIS).read()
DR = {m.group(1): parse_part(m.group(2)) for m in re.finditer(r"Definition (drule\d+'?)\s*:=\s*Part (.*?)\.\n", src)}
base_names = re.search(r'Definition base_drules : drules := @seqn part 38(.*?)\.\n', src, re.S).group(1).split()
assert len(base_names) == 38, len(base_names)
BASE = [DR[x] for x in base_names]
def mirror(p):
    """reflection across the third spoke: spoke k -> 4-k (mod n); hat j -> 5-j; fans reversed."""
    n = len(p); out = []
    for k2 in range(n):
        k = (4 - k2) % n; sp, _, fans = p[k]; hat = p[(5 - k2) % n][1]
        out.append((sp, hat, tuple(reversed(fans))))
    return out
def sub(a, b): return b[0] <= a[0] and a[1] <= b[1]
def part_subset(p, q):
    if len(p) != len(q): return False
    for (s1, h1, f1), (s2, h2, f2) in zip(p, q):
        if not (sub(s1, s2) and sub(h1, h2)): return False
        if f2 and not f1: return False
        if f1 and f2 and not all(sub(a, b) for a, b in zip(f1, f2)): return False
    return True
RULES = []
for p in BASE:
    pm = mirror(p)
    RULES.append(p)
    if not part_subset(p, pm): RULES.append(pm)

def score_cases():
    P, pa, pf = G['structure'](); fd = G['fixed_deg'](); VAR = G['VAR']; LET = G['LET']
    # RSST containment, as grow.py computes it (RSST's 633 only)
    pats = set()
    for c in G['rsst']():
        for e in G['embeddings'](c, P, pa, pf, fd):
            req = dict((v, c[3][u]) for u, v in e if v not in fd)
            pats.add(tuple(req.get(x, 0) for x in VAR))
    def contains(case): return any(all(k == 0 or k == x for k, x in zip(key, case)) for key in pats)
    res = collections.Counter(); ex = collections.defaultdict(list)
    for a in (6, 7, 8, 9):
        for b in (6, 7, 8, 9):
            for pv in itertools.product(LET, repeat=6):
                case = (a, b) + pv
                lo, hi, detail = charge_u(case)
                cr = contains(case)
                key = ('RSST' if cr else 'free', lo, hi)
                res[key] += 1
                if len(ex[key]) < 3: ex[key].append((case, detail))
    return res, ex

def charge_u(case):
    adj, name, faces = G['build2'](G['letters'](case[0], case[1], case[2:]))
    inv = {v: x for x, v in name.items()}
    deg = {}
    fd = G['fixed_deg']()
    for x, v in inv.items():
        nm = x
        if nm in fd: deg[v] = fd[nm]
        elif nm in dict(zip(G['VAR'], case)): deg[v] = dict(zip(G['VAR'], case))[nm]
    tri = set(faces)
    def rot(h):
        """neighbours of h in cyclic order (from its triangles); None if h's link is not a closed cycle in the patch."""
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
        """x's neighbours strictly between ha and hb, on the side away from h, in order from ha."""
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
        """yes / no / maybe for 'deg v in R'"""
        if v in deg:
            d = deg[v]; return 'yes' if R[0] <= d <= R[1] else 'no'
        return 'yes' if R == (5, 9) else 'maybe'
    def fits(h, S, a, p):
        """S = h's neighbours in cyclic order; anchor a; returns yes/no/maybe"""
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
    u = inv[('u',)]
    Su = rot(u); assert Su and len(Su) == 7
    out = collections.Counter(); inn_lo = collections.Counter(); inn_hi = collections.Counter(); det = []
    for a in range(7):
        for p in RULES:
            if len(p) != 7: continue
            f = fits(u, Su, a, p)
            assert f != 'maybe', ('u outflow depends on an unknown degree', case)
            if f == 'yes': out[Su[(a + 2) % 7]] += 1
    for w in Su:
        d = deg[w]; Sw = rot(w)
        if Sw is None or len(Sw) != d: det.append(('no rotation', name.get(w))); continue
        for a in range(d):
            if Sw[(a + 2) % d] != u: continue
            for p in RULES:
                if len(p) != d: continue
                f = fits(w, Sw, a, p)
                if f == 'yes': inn_lo[w] += 1; inn_hi[w] += 1
                elif f == 'maybe': inn_hi[w] += 1
    base = 10 * (6 - 7)
    lo = base + sum(inn_lo.values()) - sum(out.values()); hi = base + sum(inn_hi.values()) - sum(out.values())
    detail = ' '.join('%s:out%d/in%d..%d' % (''.join(map(str, name.get(w)[:2])), out[w], inn_lo[w], inn_hi[w]) for w in Su)
    return lo, hi, detail

if __name__ == '__main__':
    print('rules: base %d, after symmetrize %d; sizes %s' % (len(BASE), len(RULES), dict(collections.Counter(len(p) for p in RULES))), flush=True)
    res, ex = score_cases()
    lines = ['# u charge by the 32 RSST rules (Gonthier encoding), round-42 cases; key = (contains an RSST config?, lo, hi)']
    for k in sorted(res, key=lambda k: (k[0], k[1], k[2])):
        lines.append('%-5s charge %s: %d cases   e.g. %s' % (k[0], ('%d' % k[1]) if k[1] == k[2] else '[%d,%d]' % (k[1], k[2]), res[k],
                     ' ; '.join('%s %s' % (''.join(map(str, c)), d) for c, d in ex[k][:2])))
    open(os.path.join(H, 'rsst_score.txt'), 'w').write('\n'.join(lines) + '\n'); print('\n'.join(lines))
