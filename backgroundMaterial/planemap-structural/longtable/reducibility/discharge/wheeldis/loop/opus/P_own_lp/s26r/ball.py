"""s26r: u-centred ball completions avoiding the 0125c46b forbidden set (strict section 14' semantics).
Frame = rings.Layered(D): ring 1 = link LK, ring 2 = apexes s_i + privates p_{i,k}, ring 3 (radius 3 only) = ('r', k).
Letter 9 = degree >= 9: coded 99, never an exact match; vertices whose existence/adjacency depends on a >=9 degree
(privates of a >=9 link vertex at r=2; ring-3 vertices touching a >=9 ring-2 vertex at r=3) are UNKNOWN (99)."""
import sys, os, pickle, itertools, collections
LOOP = '/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad/ex59/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop'
sys.path.insert(0, os.path.join(LOOP, 'k42'))
import grow
from rings import Layered
HERE = os.path.dirname(os.path.abspath(__file__))
NEVER = 99
def registry(): return pickle.load(open(os.path.join(HERE, 'reg_A59.pkl'), 'rb'))

def _adj(L):
    adj = {}
    for a, b, c in L.tris:
        for x, y in ((a, b), (b, c), (c, a)): adj.setdefault(x, set()).add(y); adj.setdefault(y, set()).add(x)
    return adj

def frame(D, LK, R2=None):
    """R2 None: 2-ball frame (P = rings 0..2). R2 = dict name->letter for ring 2: 3-ball frame (P = rings 0..3).
    Returns P, pa, pf, name->ring-index info, inn (in-count of ring-3 vertices), touch (ring-3 -> ring-2 names)."""
    L = Layered(D); L.add_ring([9 if l == 9 else l for l in LK]); Wr = L.rings[1]; Z = L.ring(); adj = _adj(L)
    name = {0: ('u',)}
    for i, w in enumerate(Wr): name[w] = ('w', i)
    Wi = {w: i for i, w in enumerate(Wr)}; cnt = {}
    for z in Z:
        ws = sorted(Wi[x] for x in adj[z] if x in Wi)
        if len(ws) == 2: i, j = ws; name[z] = ('s', j if (i, j) == (0, D - 1) else i)
        else: i = ws[0]; cnt[i] = cnt.get(i, 0) + 1; name[z] = ('p', i, cnt[i])
    order2 = [name[z] for z in Z]
    inn3 = {}; touch = {}
    if R2 is not None:
        L.add_ring([9 if R2[name[z]] >= 9 else R2[name[z]] for z in Z]); Z3 = L.ring(); adj = _adj(L)
        for k, z in enumerate(Z3): name[z] = ('r', k)
        Zs = set(Z)
        for z in Z3: touch[name[z]] = sorted(name[y] for y in adj[z] if y in Zs); inn3[name[z]] = len(touch[name[z]])
        L.add_ring([9] * len(Z3))
    else:
        L.add_ring([9] * len(Z))
    adj = _adj(L)
    inv = {v: x for x, v in name.items()}
    pa = {x: {name[y] for y in adj[inv[x]] if y in name} for x in inv}
    pf = {frozenset(name[y] for y in f) for f in L.tris if all(y in name for y in f)}
    return list(inv), pa, pf, order2, inn3, touch

def reqsets(C, P, pa, pf, fd, free):
    """requirement sets: frozenset of (free vertex, degree) for each embedding (strict: fd's 99s never match)."""
    R = {}
    for c in C:
        for e_ in grow.embeddings(c, P, pa, pf, fd):
            req = frozenset((v, c[3][u]) for u, v in e_ if v not in fd)
            assert all(v in free for v, _ in req)
            if req not in R: R[req] = c[0]
    return R
