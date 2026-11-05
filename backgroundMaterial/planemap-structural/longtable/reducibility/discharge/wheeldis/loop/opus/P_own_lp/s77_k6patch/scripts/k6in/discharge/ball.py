"""B8 (exploratory): 2-balls of degree-5 vertices in triangulations, for any first-ring word.

Key of the 2-ball at a degree-5 vertex v with neighbours x_0..x_4 (cyclic):
  block_k = (deg x_k, (degrees of the private second-ring neighbours of x_k, in order), deg s_k)
where s_k is the second-ring vertex shared by x_k and x_{k+1}; x_k has deg x_k - 5 private neighbours.
The key is canonical under the dihedral group of the wheel.  For 66666 the second ring order is
p_0 s_0 p_1 s_1 ... = gen_2ball.py's y-order, so build(key) gives the same configuration as gen_2ball.build.

build(key) -> (r, m, D, intadj, ringadj) in WheelMain/dfast format (free completion: each second-ring vertex y_j
with o_j outward edges sees t_{j-1}, o_j - 2 private ring vertices, t_j; o_j = 1 means t_{j-1} = t_j).
"""
import itertools


def parse_line(line):
    f = line.split()
    name, n = f[0], int(f[1])
    rot = [list(map(int, s.split(','))) for s in f[2].split(';')]
    assert len(rot) == n
    return name, rot


def wheel_canon(w):
    w = tuple(w); best = None
    for s in (w, w[::-1]):
        for k in range(len(s)):
            r = s[k:] + s[:k]
            if best is None or r < best: best = r
    return best


def canon_blocks(blocks):
    """blocks: list of 5 (dx, privs tuple, ds).  Reflection: order x_0, x_4, x_3, ...; x_{-k} gets reversed privs
    and its shared vertex on the new right is s_{-k-1}."""
    B = [tuple((b[0], tuple(b[1]), b[2])) for b in blocks]
    F = [(B[(-k) % 5][0], tuple(reversed(B[(-k) % 5][1])), B[(-k - 1) % 5][2]) for k in range(5)]
    best = None
    for S in (B, F):
        for k in range(5):
            r = tuple(S[k:] + S[:k])
            if best is None or r < best: best = r
    return best


def key_str(key):
    """e.g. 6.5|6.6|... : per block  dx:privs:ds"""
    return '|'.join('%d:%s:%d' % (b[0], ''.join(map(str, b[1])), b[2]) for b in key)


def key_from_str(s):
    out = []
    for blk in s.split('|'):
        a, p, c = blk.split(':')
        out.append((int(a), tuple(int(ch) for ch in p), int(c)))
    return tuple(out)


def ball_at(rot, v):
    """Return (wordkey, key, status) for degree-5 vertex v.  status 'ok' or a reason the 2-ball is irregular."""
    X = rot[v]; deg = [len(r) for r in rot]
    word = [deg[x] for x in X]
    Xs = set(X)
    outer = []
    for k in range(5):
        x = X[k]; R = rot[x]; i = R.index(v); d = len(R)
        a, b = R[(i + 1) % d], R[(i - 1) % d]
        nxt, prv = X[(k + 1) % 5], X[(k - 1) % 5]
        if {a, b} != {nxt, prv}: return word, None, 'wheel-irregular'
        mid = [R[(i + j) % d] for j in range(2, d - 1)]   # strictly between a and b
        if a == nxt: mid = mid[::-1]                       # now from s_{k-1} side to s_k side
        outer.append(mid)
    for k in range(5):
        if outer[k][0] != outer[(k - 1) % 5][-1]: return word, None, 'shared-mismatch'
    Y = []
    for k in range(5): Y += outer[k][1:]
    if len(set(Y)) != len(Y) or (set(Y) & (Xs | {v})): return word, None, 'ring2-not-simple'
    Yset = set(Y); L = len(Y)
    pos = {y: j for j, y in enumerate(Y)}
    for j, y in enumerate(Y):
        for z in rot[y]:
            if z in Yset and (pos[z] - j) % L not in (1, L - 1): return word, None, 'ring2-chord'
    # each y adjacent to exactly the expected x's
    exp = {}
    for k in range(5):
        for y in outer[k]: exp.setdefault(y, set()).add(X[k])
    for y in Y:
        if set(z for z in rot[y] if z in Xs) != exp[y]: return word, None, 'x-y-extra'
    blocks = []
    for k in range(5):
        blocks.append((deg[X[k]], tuple(deg[y] for y in outer[k][1:-1]), deg[outer[k][-1]]))
    return word, canon_blocks(blocks), 'ok'


def build(key):
    """Free-completion configuration of the 2-ball with this key.  Interior ids: 0 hole, 1..5 x_k, then y's."""
    dx = [b[0] for b in key]
    ylist = []          # (degree, owner k, kind) in ring order: privates of x_k then s_k
    for k, b in enumerate(key):
        for d in b[1]: ylist.append((d, k, 'p'))
        ylist.append((b[2], k, 's'))
    L = len(ylist); m = 6 + L
    A = [set() for _ in range(m)]
    def E(a, b): A[a].add(b); A[b].add(a)
    D = [5] + dx + [y[0] for y in ylist]
    sidx = {}
    for j, (d, k, t) in enumerate(ylist):
        if t == 's': sidx[k] = 6 + j
    for k in range(5):
        E(0, 1 + k); E(1 + k, 1 + (k + 1) % 5)
    for j, (d, k, t) in enumerate(ylist):
        y = 6 + j; E(1 + k, y)
        if t == 's': E(1 + (k + 1) % 5, y)
        E(y, 6 + (j + 1) % L)
    for k in range(5):
        if len(A[1 + k]) != D[1 + k]: return None   # cannot happen for a consistent key
    o = [D[6 + j] - len(A[6 + j]) for j in range(L)]
    if any(x < 1 for x in o) or all(x == 1 for x in o): return None
    j0 = next(j for j in range(L) if o[j] >= 2)
    ring = []; ringadj = [[] for _ in range(m)]; prev_t = None
    for jj in range(L):
        j = (j0 + jj) % L; y = 6 + j; nb = [prev_t if prev_t is not None else 'T0']
        if o[j] >= 2:
            for _ in range(o[j] - 2): ring.append(len(ring)); nb.append(ring[-1])
            ring.append(len(ring)); prev_t = ring[-1]; nb.append(prev_t)
        ringadj[y] = nb
    for y in range(6, m):
        ringadj[y] = list(dict.fromkeys(prev_t if x == 'T0' else x for x in ringadj[y]))
    return len(ring), m, D, [sorted(s) for s in A], ringadj


def ring_size(key):
    """r = sum over y of (o_y - 1), without building."""
    tot = 0
    for k, b in enumerate(key):
        for d in b[1]: tot += d - 3 - 1        # private: x_k + 2 ring-neighbours
        tot += b[2] - 4 - 1                     # shared: 2 x's + 2 ring-neighbours
    return tot


def fmt_config(name, cfg):
    r, m, D, ia, ra = cfg
    f = lambda Ls: ';'.join(','.join(map(str, x)) if x else '-' for x in Ls)
    return '%s %d %d %s %s' % (name, r, m, f(ra), f(ia))


def key_to_66666_name(key):
    """66666 keys -> gen_2ball name (y-degree word p0 s0 ... in gen_2ball's canonical form)."""
    if any(b[0] != 6 for b in key): return None
    t = []
    for b in key: t += [b[1][0], b[2]]
    # gen_2ball canon: min over rotations by (p,s) pair and its reflection
    best = None
    for k in range(5):
        r = tuple(t[2 * k:] + t[:2 * k]); best = r if best is None or r < best else best
        f = [None] * 10
        for i in range(5): f[2 * i] = t[2 * ((-i) % 5)]; f[2 * i + 1] = t[2 * ((-i - 1) % 5) + 1]
        f = tuple(f); r = f[2 * k:] + f[:2 * k]; best = r if r < best else best
    return 'b' + ''.join(map(str, best))


# ---------- class checks (for constructed graphs) ----------
def faces_of(rot):
    F = set()
    for a in range(len(rot)):
        R = rot[a]
        for i in range(len(R)):
            b, c = R[i], R[(i + 1) % len(R)]
            F.add(frozenset((a, b, c)))
    return F


def _components(n, adj, removed):
    seen = set(removed); comps = []
    for s in range(n):
        if s in seen: continue
        st = [s]; seen.add(s); c = [s]
        while st:
            u = st.pop()
            for w in adj[u]:
                if w not in seen: seen.add(w); st.append(w); c.append(w)
        comps.append(c)
    return comps


def class_check(rot):
    """returns dict: mindeg, septri, sep4, sep5nontriv (counts; 0 = in class)."""
    n = len(rot); adj = [set(r) for r in rot]
    res = dict(n=n, mindeg=min(len(r) for r in rot))
    tri = sum(1 for a in range(n) for b in adj[a] if b > a for c in adj[a] & adj[b] if c > b)
    res['septri'] = tri - (2 * n - 4)
    s4 = 0
    for a in range(n):
        for c in range(a + 1, n):
            if c in adj[a]: continue
            com = sorted(adj[a] & adj[c])
            for b, d in itertools.combinations(com, 2):
                if d in adj[b]: continue   # a 4-cycle with chord bd: separating iff a triangle is separating
                if len(_components(n, adj, {a, b, c, d})) > 1: s4 += 1
    res['sep4'] = s4
    s5 = 0; seen = set()
    for a in range(n):
        for b in adj[a]:
            for c in adj[b]:
                if c in (a,) or c in adj[a]: continue
                for d in adj[c]:
                    if d in (a, b) or d in adj[b]: continue
                    for e in adj[d] & adj[a]:
                        if e in (b, c) or e in adj[c] or e in adj[b]: continue
                        cyc = frozenset((a, b, c, d, e))
                        if len(cyc) != 5 or cyc in seen: continue
                        seen.add(cyc)
                        comps = _components(n, adj, cyc)
                        if len(comps) > 1 and sum(1 for c_ in comps if len(c_) >= 2) >= 2: s5 += 1
    res['sep5'] = s5
    res['in_class'] = res['mindeg'] >= 5 and res['septri'] == 0 and s4 == 0 and s5 == 0
    return res
