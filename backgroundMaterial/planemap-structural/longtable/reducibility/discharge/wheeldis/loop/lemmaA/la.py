"""Lemma A as a finite statement (16 Oct 2026; engine level, exploratory: dfast/cfast only, no Lean).

STATEMENT (written 07:47Z, before any computation in loop/lemmaA):
  A(k). u of degree exactly 7, link w0..w6 over {5,6,7,8,9+} with >= k fives (positions F); sigma_j = degree of s_j
  (common neighbour of w_j, w_{j+1} other than u) given in {5,6,7,8,9+} for j in F u (F-1); generic local disc (free
  completion).  If no wheel FORCED by these data is in R_opt (5-wheel Job 17 D/C + D fans incl. diamond; 6-wheel Job 17
  D/C + 2.122; u's own 7-wheel D or cfast C-candidate; a wheel with unknown letters counts only if bad for every
  completion over 5..9+; untested words with letters 8/9+ count NOT reducible), then some S in F, |S| >= 2, has
  K(S) = u + S + N(S) (degree 5..8 vertices inside at exact degree, 9+ vertices left on the ring) D (dfast, ring <= 16)
  or C-candidate (cfast --search |X| <= 4).
GUESS: A(4), A(5) hold with D alone at ring <= 15; A(3) fails on a small family (5-15%) needing ring 16-17 or C.
REFUTED BY: a k = 4/5 situation whose every K(S) at ring <= 16 is not D with no C-candidate (and every ring 17-19
K(S) not D by dfast18).

Situation = (L, s): L = link letters (9 = 9+), s[j] = sigma_j or 0 (unknown) -- canonical under the dihedral group.
"""
import sys, os, itertools, collections, hashlib, subprocess, time
HERE = os.path.dirname(os.path.abspath(__file__)); W = os.path.dirname(os.path.dirname(HERE)); DIS = os.path.dirname(W)
sys.path.insert(0, os.path.join(DIS, 'b8b'))
from rings import Layered
_src = open(os.path.join(W, 'defect.py')).read().replace('HERE = os.path.dirname(os.path.abspath(__file__))', 'HERE = %r' % W)
_sv = sys.argv; sys.argv = ['defect.py', '5', '1', '1', '/dev/null', 'strict7']
exec(_src[:_src.index("CENTRE, K, CMIN, OUT")]); sys.argv = _sv
LET = (5, 6, 7, 8, 9)
HERE = os.path.dirname(os.path.abspath(__file__))

def bad_any(d, w):
    """wheel of centre degree d with link word w (0 = unknown letter): reducible for EVERY completion?"""
    unk = [i for i, x in enumerate(w) if x == 0]
    if d == 7 and unk: return False                     # a 9+ completion is never a tested 7-wheel
    for fill in itertools.product(LET[::-1], repeat=len(unk)):
        ww = list(w)
        for i, x in zip(unk, fill): ww[i] = x
        if d == 5 and not isR5(ww): return False
        if d == 6 and not bad6(ww): return False
        if d == 7 and canon(ww) not in D7: return False
        if d not in (5, 6, 7): return False
    return True

# dihedral action on (L, s): rotation j -> j + r ; reflection w_j -> w_{-j}, s_j -> s_{-j-1}
def transforms(L, s):
    for r in range(7):
        yield tuple(L[(j + r) % 7] for j in range(7)) + tuple(s[(j + r) % 7] for j in range(7))
        yield tuple(L[(-j + r) % 7] for j in range(7)) + tuple(s[(-j - 1 + r) % 7] for j in range(7))
def canon_sit(L, s): return min(transforms(L, s))

# ---------- R_opt exclusion of a situation -------------------------------------------------------------------------
def forced_wheels(L, s):
    """all wheels whose centre degree is known (5/6/7) with their link words (0 unknown). Vertices: u, w_j, s_j.
    link of w_j (deg d): u, w_{j+1}, s_j, t.., s_{j-1}, w_{j-1}   (d-5 unknown t's between s_j and s_{j-1}).
    link of s_j (deg e): w_j, w_{j+1}, b, x.., a  where b = s_{j+1} if w_{j+1} is 5 else unknown, a = s_{j-1} if w_j is 5."""
    out = [(7, list(L))]
    for j in range(7):
        d = L[j]
        if d in (5, 6, 7):
            sj = s[j] if s[j] else 0; sm = s[(j - 1) % 7] if s[(j - 1) % 7] else 0
            if d == 5: out.append((5, [7, L[(j + 1) % 7], sj, sm, L[(j - 1) % 7]]))
            else: out.append((d, [7, L[(j + 1) % 7], sj] + [0] * (d - 5) + [sm, L[(j - 1) % 7]]))
        e = s[j]
        if e in (5, 6):
            b = s[(j + 1) % 7] if L[(j + 1) % 7] == 5 else 0
            a = s[(j - 1) % 7] if L[j] == 5 else 0
            out.append((e, [L[j], L[(j + 1) % 7], b] + [0] * (e - 4) + [a]))
    return out
def excluded(L, s):
    for d, w in forced_wheels(L, s):
        if d == 7 and 9 in w: continue
        if bad_any(d, w): return True
    return False

# ---------- enumeration --------------------------------------------------------------------------------------------
def link_words(k):
    seen = set()
    for L in itertools.product(LET, repeat=7):
        if L.count(5) != k: continue
        c = min(t[:7] for t in transforms(L, (0,) * 7))
        if c in seen: continue
        seen.add(c); yield c
def situations(k):
    """yield canonical non-excluded (L, s) with exactly k fives."""
    for L in link_words(k):
        F = [j for j in range(7) if L[j] == 5]
        J = sorted({j for j in F} | {(j - 1) % 7 for j in F})
        # prune: 5-wheel at each five needs s_{j-1}, s_j; check as soon as both assigned
        checks = {}
        for j in F:
            last = max(J.index(j), J.index((j - 1) % 7)); checks.setdefault(last, []).append(j)
        s = [0] * 7; seen = set()
        def rec(t):
            if t == len(J):
                c = canon_sit(L, s)
                if c in seen: return
                seen.add(c)
                if not excluded(L, s): yield c
                return
            for x in LET:
                s[J[t]] = x; ok = True
                for j in checks.get(t, ()):
                    if isR5([7, L[(j + 1) % 7], s[j], s[(j - 1) % 7], L[(j - 1) % 7]]): ok = False; break
                if ok: yield from rec(t + 1)
            s[J[t]] = 0
        yield from rec(0)

# ---------- configurations ------------------------------------------------------------------------------------------
def build(L, s):
    """layered patch: u, ring1 = L (9 for 9+), ring2: s_j known -> sigma_j else 9; ring 3 created (degrees unused)."""
    P = Layered(7); P.add_ring(list(L))
    adj = collections.defaultdict(set)
    for a, b, c in P.tris:
        for x, y in ((a, b), (b, c), (c, a)): adj[x].add(y); adj[y].add(x)
    w = P.rings[1]; R2 = P.rings[2]
    sv = []
    for j in range(7):
        com = [z for z in adj[w[j]] & adj[w[(j + 1) % 7]] if z != 0]; assert len(com) == 1; sv.append(com[0])
    pos = {x: j for j, x in enumerate(sv)}
    P.add_ring([s[pos[x]] if (x in pos and s[pos[x]]) else 9 for x in R2])
    adj = collections.defaultdict(set)
    for a, b, c in P.tris:
        for x, y in ((a, b), (b, c), (c, a)): adj[x].add(y); adj[y].add(x)
    deg = dict(P.deg)
    known = {0} | set(w) | {sv[j] for j in range(7) if s[j]}
    return adj, deg, w, sv, known
def extract_cfg(adj, I):
    Is = set(I); RS = set(y for x in I for y in adj[x]) - Is
    for y in RS:
        if len(adj[y] & RS) != 2: return None
    start = min(RS); order = [start]; prev = None
    while True:
        cur = order[-1]; nb = sorted(adj[cur] & RS); nx = nb[0] if nb[0] != prev else nb[1]
        if nx == start: break
        order.append(nx); prev = cur
    if len(order) != len(RS): return None
    ri = {y: j for j, y in enumerate(order)}; Il = sorted(I); ii = {x: j for j, x in enumerate(Il)}
    f = lambda Ls: ';'.join(','.join(map(str, v)) if v else '-' for v in Ls)
    ia = [sorted(ii[y] for y in adj[x] if y in Is) for x in Il]
    ra = [sorted(ri[y] for y in adj[x] if y in RS) for x in Il]
    return '%d %d %s %s' % (len(order), len(Il), f(ra), f(ia))
def KS(adj, deg, w, sv, known, S):
    """B-fixed configuration for S (tuple of link positions); 9+ vertices stay on the ring.  None if no simple ring."""
    I = {0} | {w[j] for j in S}
    for j in S:
        for y in adj[w[j]]:
            if deg.get(y, 9) <= 8: I.add(y)
    cb = extract_cfg(adj, I)
    if cb is None:                     # pinched: move enclosed ring vertices of known degree <= 8 inside
        RS = set(y for x in I for y in adj[x]) - I
        enc = {y for y in RS if y in known and deg[y] <= 8 and adj[y] <= (I | RS)}
        if enc: cb = extract_cfg(adj, I | enc)
    return cb

# ---------- canonical key of a configuration line (ring rotation/reflection + colour refinement) -------------------
def ckey(cb):
    f = cb.split(); r, m = int(f[0]), int(f[1])
    ra = [[] if x == '-' else list(map(int, x.split(','))) for x in f[2].split(';')]
    ia = [[] if x == '-' else list(map(int, x.split(','))) for x in f[3].split(';')]
    best = None
    for k in range(r):
        for refl in (1, -1):
            phi = lambda i: (refl * (i - k)) % r
            col = [tuple(sorted(phi(i) for i in ra[x])) for x in range(m)]
            for _ in range(m):
                ranks = {c: n for n, c in enumerate(sorted(set(col)))}
                new = [(ranks[col[x]], tuple(sorted(ranks[col[y]] for y in ia[x]))) for x in range(m)]
                if len(set(new)) == len(set(col)): col = new; break
                col = new
            if len(set(col)) < m: return None
            order = sorted(range(m), key=lambda x: col[x]); pos = {x: n for n, x in enumerate(order)}
            s = '%d %d %s %s' % (r, m, ';'.join(','.join(map(str, sorted(phi(i) for i in ra[x]))) or '-' for x in order),
                                 ';'.join(','.join(map(str, sorted(pos[y] for y in ia[x]))) or '-' for x in order))
            if best is None or s < best: best = s
    return 'k' + hashlib.sha1(best.encode()).hexdigest()[:16]
