"""Ring classification for vertex sets I in a triangulated patch / sphere (exploratory; loop/appears).
Region = union of the faces having a vertex in I (the closed star of I = the image of the free completion's disc).
Ring walks = boundary walks of the region (region on the left), traced by rotating at each ring vertex through the
region sector.  Labels: simple / chord / pinch / fold (enclosed ring vertex or ring edge with region faces on both
sides, i.e. the free disc folded along an edge) / hole (>= 2 boundary walks).
Separating short cycles are detected locally: non-facial triangle; chordless 4-cycle; chordless 5-cycle that is not
the link of a degree-5 vertex (in a triangulation each side of a chordless cycle has an interior vertex, and a side
with exactly one vertex makes the cycle that vertex's link)."""
import sys, os, collections, itertools
HERE = os.path.dirname(os.path.abspath(__file__))
WD = os.path.dirname(os.path.dirname(HERE)); DIS = os.path.dirname(WD)
sys.path.insert(0, os.path.join(DIS, 'b8b'))
from rings import Layered

def patch(sig, sea=5):
    """verbatim copy of defect_check2.patch"""
    rings = sig.split('|'); L = Layered(int(rings[0]))
    for k in range(1, len(rings)): L.add_ring([int(c) for c in rings[k]])
    for _ in range(sea): L.add_ring([6] * len(L.ring()))
    adj = collections.defaultdict(set); nxt = collections.defaultdict(dict)
    for a, b, c in L.tris:
        for x, y in ((a, b), (b, c), (c, a)): adj[x].add(y); adj[y].add(x)
        nxt[a][b] = c; nxt[b][c] = a; nxt[c][a] = b
    return L, adj, nxt

def sphere(rot):
    """rot: list of rotation lists (plantri orientation). Returns adj, nxt with nxt[a][b] = c for faces (a,b,c)."""
    adj = {v: set(r) for v, r in enumerate(rot)}; nxt = collections.defaultdict(dict)
    for v, r in enumerate(rot):
        d = len(r)
        for i in range(d):
            a, b = r[i], r[(i + 1) % d]
            nxt[v][a] = b; nxt[a][b] = v; nxt[b][v] = a
    return adj, nxt

def rotf(nxt, x):
    s0 = min(nxt[x]); r = [s0]; y = nxt[x][s0]
    while y != s0: r.append(y); y = nxt[x][y]
    return r

def extract_cfg(adj, I):
    """defect_check2.extract_cfg's simplicity test (every ring vertex has exactly 2 ring neighbours, one cycle)"""
    Is = set(I); RS = set(y for x in I for y in adj[x]) - Is
    if not RS: return False
    for y in RS:
        if len(adj[y] & RS) != 2: return False
    start = min(RS); order = [start]; prev = None
    while True:
        cur = order[-1]; nb = sorted(adj[cur] & RS); nx = nb[0] if nb[0] != prev else nb[1]
        if nx == start: break
        order.append(nx); prev = cur
    return len(order) == len(RS)

def code_fill(adj, I):
    """defect_check2's repair: move ring vertices whose neighbourhood lies in I + ring inside; True if then simple"""
    I = set(I); RS = set(y for x in I for y in adj[x]) - I
    I2 = I | {y for y in RS if adj[y] <= (I | RS)}
    return I2 != I and extract_cfg(adj, I2)

def classify(adj, nxt, I):
    I = set(I); RS = set(y for x in I for y in adj[x]) - I
    inreg = lambda a, b: a in I or b in I or nxt[a][b] in I        # the face containing dart (a,b)
    bd = [(x, y) for x in RS for y in adj[x] if y in RS and inreg(x, y) and not inreg(y, x)]
    def succ(x, y):
        c = nxt[x][y]; sweep = [c]
        while inreg(c, y):
            c = nxt[c][y]; sweep.append(c)
        return (y, c), sweep[:-1]
    seen = set(); walks = []
    for d0 in bd:
        if d0 in seen: continue
        w = []; d = d0
        while d not in seen:
            seen.add(d); nd, sw = succ(*d); w.append((d[1], sw)); d = nd   # (vertex, I-side sector swept there)
        walks.append(w)
    onw = set(v for w in walks for v, _ in w)
    enclosed = RS - onw
    chords = [(x, y) for x in RS for y in adj[x] if x < y and y in RS and not inreg(x, y) and not inreg(y, x)]
    double = [(x, y) for x in RS for y in adj[x] if x < y and y in RS and inreg(x, y) and inreg(y, x)]
    rep = [v for w in walks for v, c in collections.Counter(v for v, _ in w).items() if c > 1]
    if len(walks) > 1: lab = 'hole'
    elif enclosed or double: lab = 'fold'
    elif rep: lab = 'pinch'
    elif chords: lab = 'chord'
    else: lab = 'simple'
    return dict(lab=lab, RS=RS, walks=walks, enclosed=enclosed, chords=chords, double=double, rep=rep)

def dist_in(adj, S, A, B):
    """shortest path length inside S from set A to set B (A, B subsets of S)"""
    A = set(A) & S; B = set(B) & S
    if not A or not B: return None
    dist = {a: 0 for a in A}; q = collections.deque(A)
    while q:
        x = q.popleft()
        if x in B: return dist[x]
        for y in adj[x]:
            if y in S and y not in dist: dist[y] = dist[x] + 1; q.append(y)
    return None

def witness(adj, I, cl):
    """shortest closing cycle through I for each defect: pinch (two sectors at r), chord (r1 r2); min over defects"""
    I = set(I); best = None
    for w in cl['walks']:
        occ = collections.defaultdict(list)
        for v, sw in w: occ[v].append(sw)
        for v, sws in occ.items():
            if len(sws) < 2: continue
            for s1, s2 in itertools.combinations(sws, 2):
                dd = dist_in(adj, I, s1, s2)
                if dd is not None: L = dd + 2; best = L if best is None else min(best, L)
    for x, y in cl['chords']:
        dd = dist_in(adj, I, adj[x] & I, adj[y] & I)
        if dd is not None: L = dd + 3; best = L if best is None else min(best, L)
    return best

def short_sep_cycles(adj, nxt, verts, deg):
    """separating triangles, chordless 4-cycles, nontrivial chordless 5-cycles, all of whose vertices lie in verts"""
    V = set(verts); out = []
    face = lambda a, b, c: nxt.get(a, {}).get(b) == c or nxt.get(a, {}).get(c) == b
    for a in V:
        for b in adj[a] & V:
            if b <= a: continue
            for c in adj[b] & V:
                if c <= a or c == b: continue
                if a in adj[c]:
                    if b < c and not face(a, b, c): out.append((a, b, c))
                    continue
                for d in adj[c] & V:
                    if d <= a or d in (b,) or d in adj[b]: continue
                    if a in adj[d]:
                        if b < d: out.append((a, b, c, d))          # chordless 4-cycle (a~c? no: c not in adj[a]; b~d? no)
                        continue
                    for e in adj[d] & adj[a] & V:
                        if e <= a or e in (b, c) or e in adj[b] or e in adj[c]: continue
                        if b > e: continue                          # each 5-cycle once (min vertex a, direction b<e)
                        C = {a, b, c, d, e}
                        common = set.intersection(*(adj[x] for x in C))
                        if any(deg.get(z) == 5 for z in common): continue   # link of a degree-5 vertex: trivial
                        out.append((a, b, c, d, e))
    return out
