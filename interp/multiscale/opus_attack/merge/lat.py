# Lattice infrastructure for the merge attack (independent of the authors' code, except where marked).
# Triangular lattice, vertex (i,j), Cartesian x = i + j/2, y = j*sqrt(3)/2; neighbours +-(1,0), +-(0,1), +-(-1,1).
# Up triangle (i,j),(i+1,j),(i,j+1); down triangle (i+1,j),(i+1,j+1),(i,j+1); both listed ccw.
import sys, os, types, itertools, collections, subprocess, math, random, tempfile
HERE = os.path.dirname(os.path.abspath(__file__))
SCR = '/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad'
MSAT = os.path.join(SCR, 'msat')
if not os.path.exists(MSAT):
    subprocess.run(['gcc', '-O2', '-o', MSAT, os.path.join(HERE, 'msat.c')], check=True)

DIRS = [(1, 0), (0, 1), (-1, 1), (-1, 0), (0, -1), (1, -1)]
# height sign of a lattice direction: +1 iff the up triangle lies on the left of u->w (tilt.py convention)
SGN = {(1, 0): 1, (0, 1): -1, (-1, 1): 1, (-1, 0): -1, (0, -1): 1, (1, -1): -1}
INC = {1: (2, 0), 2: (0, 2), 3: (-2, -2)}   # half-lattice units, as levelling/lev.py
def n2(p): return (p[0]*p[0] + p[1]*p[1] - p[0]*p[1]) / 4.0
PERMS = list(itertools.permutations(range(4)))

# ---------------------------------------------------------------- SAT
def solve(nvars, cls, budget=None):
    """returns set of true vars, None (UNSAT) or 'UNK'.  Every model is verified here."""
    fd, path = tempfile.mkstemp(dir=SCR, suffix='.cnf')
    with os.fdopen(fd, 'w') as f:
        f.write('p cnf %d %d\n' % (nvars, len(cls)))
        f.write(''.join(' '.join(map(str, c)) + ' 0\n' for c in cls))
    args = [MSAT] + ([str(budget)] if budget else [])
    with open(path) as f:
        out = subprocess.run(args, stdin=f, capture_output=True, text=True).stdout
    os.unlink(path)
    if out.startswith('s UNSAT'): return None
    if out.startswith('s UNKNOWN'): return 'UNK'
    lits = [int(x) for x in out.split('\nv', 1)[1].split()[:-1]]
    tv = set(l for l in lits if l > 0)
    for c in cls:
        assert any((l > 0) == (abs(l) in tv) for l in c), 'model check failed'
    return tv

# ------------------------------------------------------------- lattice patch as a "g" object usable by wk.Disc
class Lat:
    def __init__(self, pts):
        pts = sorted(set(pts)); self.pts = pts; self.id = {p: k for k, p in enumerate(pts)}; n = self.n = len(pts)
        self.adj = [set() for _ in range(n)]
        for p in pts:
            for d in DIRS:
                q = (p[0]+d[0], p[1]+d[1])
                if q in self.id: self.adj[self.id[p]].add(self.id[q])
        self.faces = []; self.face = collections.defaultdict(lambda: -1)
        for (i, j) in pts:
            for tri in (((i, j), (i+1, j), (i, j+1)), ((i+1, j), (i+1, j+1), (i, j+1))):
                if all(t in self.id for t in tri):
                    f = tuple(self.id[t] for t in tri); fid = len(self.faces); self.faces.append(f)
                    for a in range(3): self.face[(f[a], f[(a+1) % 3])] = fid
        self.vf = [[] for _ in range(n)]
        for k, f in enumerate(self.faces):
            for x in f: self.vf[x].append(k)
        self.deg = [len(a) for a in self.adj]
    def sgn(self, u, w):
        p, q = self.pts[u], self.pts[w]; return SGN[(q[0]-p[0], q[1]-p[1])]

def bfs(adj, srcs, allowed):
    d = {s: 0 for s in srcs}; q = collections.deque(srcs)
    while q:
        x = q.popleft()
        for y in adj[x]:
            if y in allowed and y not in d: d[y] = d[x]+1; q.append(y)
    return d

# ------------------------------------------------------------- my own disc / boundary / pocket code
def disc_info(g, S):
    """faces, boundary walk (interior on the left), internal chords; asserts S spans a disc."""
    S = set(S)
    tris = set(k for v in S for k in g.vf[v] if all(x in S for x in g.faces[k]))
    V = set(x for k in tris for x in g.faces[k]); assert V == S, 'isolated vertices'
    E = set(); bd = {}
    for k in tris:
        f = g.faces[k]
        for a in range(3):
            u, w = f[a], f[(a+1) % 3]; E.add((min(u, w), max(u, w)))
            if g.face[(w, u)] not in tris:
                assert u not in bd, 'pinch'; bd[u] = w
    assert len(V) - len(E) + len(tris) == 1, 'not a disc (Euler)'
    s0 = min(bd); walk = [s0]
    while bd[walk[-1]] != s0: walk.append(bd[walk[-1]])
    assert len(walk) == len(bd), 'boundary not one cycle'
    be = set((min(u, w), max(u, w)) for u, w in bd.items()); bs = set(walk)
    chords = [e for e in E if e[0] in bs and e[1] in bs and e not in be]
    return dict(tris=tris, E=E, walk=walk, bset=bs, chords=chords)

def true_heights(g, S, col, root=None):
    """single-valued height on a flat (all interior degree 6, lattice) region; BFS integration; checks closure."""
    S = list(S); Ss = set(S); root = S[0] if root is None else root
    h = {root: (0, 0)}; q = collections.deque([root])
    while q:
        u = q.popleft()
        for w in g.adj[u]:
            if w not in Ss: continue
            l = col[u] ^ col[w]; assert l, 'improper'
            d = INC[l]; s = g.sgn(u, w); hw = (h[u][0]+s*d[0], h[u][1]+s*d[1])
            if w in h: assert h[w] == hw, 'height not single valued'
            else: h[w] = hw; q.append(w)
    return h

def col_of_height(h):
    return ((h[0]//2) % 2) | (((h[1]//2) % 2) << 1)
