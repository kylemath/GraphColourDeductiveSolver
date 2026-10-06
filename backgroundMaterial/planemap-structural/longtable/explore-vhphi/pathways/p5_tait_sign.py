#!/usr/bin/env python3
"""p5_tait_sign.py -- [exploratory] Path 5: Tait sign sum S = sum_{cubic n} s(n) on H = dual(T - v), v of degree 5,
with a correction g(Tait word at P).  stdlib only.  Companion to
SolvingFrameworkPlan/docs/working/creative-intel-2026-10-05/path5-tait-sign-invariant.md.

 (A) word system: g(w') - g(w) = 2[ends differ] (mod 4) for every formal P-path move (60 Tait words);
     solved over GF(2) after g = 2*beta (g mod 2 is forced constant).  (No simple closed form; the solved table is used.)
 (B) per graph: I4 = S + g(w) mod 4 and B = S + g(w) mod 8 (its extra bit = the dead disc-degree bit) on every labelled
     colouring; Kempe classes (whole-component swaps in T - v, link allowed) and whether I4 / B are constant
     per class and differ between classes.
Usage:  python3 p5_tait_sign.py                 -> word system + icosahedron + T4 (smoke, ~1 s)
        python3 p5_tait_sign.py --faces F.json --hole h  [...]   -> any triangulation given as a face list
        python3 p5_tait_sign.py --multiclass ../../studio-explore/kempe-census/multiclass-smallest3.json
        (multi-class kclass examples: pass each as --faces/--hole; the report prints per-class values).
"""
import sys, itertools, json, time
sys.path.insert(0, '.')
from pb_lib import T4F, from_faces, colourings, comps, swap

ICO = [(0,1,2),(0,2,3),(0,3,4),(0,4,5),(0,5,1),(1,2,6),(2,3,7),(3,4,8),(4,5,9),(5,1,10),
       (6,7,2),(7,8,3),(8,9,4),(9,10,5),(10,6,1),(6,7,11),(7,8,11),(8,9,11),(9,10,11),(10,6,11)]

# ---------- (A) word system
WORDS = [w for w in itertools.product((1, 2, 3), repeat=5) if w[0] ^ w[1] ^ w[2] ^ w[3] ^ w[4] == 0]

def moves(w, crossing=False):
    for a, b in ((1, 2), (1, 3), (2, 3)):
        pos = [t for t in range(5) if w[t] in (a, b)]
        pairs = list(itertools.combinations(pos, 2))
        if len(pos) == 4 and not crossing:
            pairs.remove((pos[0], pos[2])); pairs.remove((pos[1], pos[3]))   # planar: no crossing chords
        for i, j in pairs:
            w2 = list(w)
            for t in (i, j): w2[t] = a + b - w[t]
            yield tuple(w2), int(w[i] != w[j])

def solve(crossing):
    beta = {WORDS[0]: 0}; st = [WORDS[0]]; bad = 0
    while st:
        w = st.pop()
        for w2, d in moves(w, crossing):
            if w2 not in beta: beta[w2] = beta[w] ^ d; st.append(w2)
            elif beta[w2] != beta[w] ^ d: bad += 1
    return beta, bad, len(beta)

# ---------- (B) graphs
def orient(F):
    """consistent orientation of a sphere triangulation's faces (BFS over shared edges)"""
    F = [tuple(f) for f in F]; out = {0: F[0]}; st = [0]
    edge = {}
    for i, f in enumerate(F):
        for a, b in itertools.combinations(f, 2): edge.setdefault(frozenset((a, b)), []).append(i)
    while st:
        i = st.pop(); f = out[i]
        for k in range(3):
            a, b = f[k], f[(k + 1) % 3]
            for j in edge[frozenset((a, b))]:
                if j == i or j in out: continue
                c = [x for x in F[j] if x not in (a, b)][0]
                out[j] = (b, a, c); st.append(j)
    assert len(out) == len(F)
    return [out[i] for i in range(len(F))]

def sgn(t):  # t = triple of Tait colours (distinct, in {1,2,3}) read in face orientation
    return 1 if t in ((1, 2, 3), (2, 3, 1), (3, 1, 2)) else -1

def setup(F, h):
    OF = orient(F); adj = from_faces(F)
    inner = [f for f in OF if h not in f]
    nxt = {}
    for f in OF:
        if h in f:
            k = f.index(h); nxt[f[(k + 1) % 3]] = f[(k + 2) % 3]
    L = [min(nxt)]
    while len(L) < 5: L.append(nxt[L[-1]])
    return adj, inner, L

def S_of(c, inner):
    return sum(sgn((c[a] ^ c[b], c[b] ^ c[cc], c[cc] ^ c[a])) for a, b, cc in inner)

def word(c, L): return tuple(c[L[t]] ^ c[L[(t + 1) % 5]] for t in range(5))

def run(name, F, h, g):
    t0 = time.time(); adj, inner, L = setup(F, h)
    allc = {}
    for c in colourings(adj, h):
        for p in itertools.permutations(range(4)):
            d = {u: p[x] for u, x in c.items()}; allc[tuple(sorted(d.items()))] = d
    ks = list(allc); idx = {k: i for i, k in enumerate(ks)}; par = list(range(len(ks)))
    def fnd(x):
        while par[x] != x: par[x] = par[par[x]]; x = par[x]
        return x
    for k in ks:
        c = allc[k]
        for a, b, K in comps(adj, c, h): par[fnd(idx[k])] = fnd(idx[tuple(sorted(swap(c, a, b, K).items()))])
    cl = {}
    for k in ks:
        c = allc[k]; S = S_of(c, inner); w = word(c, L)
        I4 = (S + g[w]) % 4; B = (S + g[w]) % 8
        cl.setdefault(fnd(idx[k]), []).append((I4, B))
    rows = [(len(v), sorted({x for x, _ in v}), sorted({y for _, y in v}, key=str)) for v in cl.values()]
    print(f"{name}: labelled colourings={len(ks)} classes={len(cl)}  per class (size, I4 values, (S+g) mod 8 values) = "
          f"{sorted(rows)}  [{time.time()-t0:.2f}s]")
    return adj, inner, L

if __name__ == '__main__':
    for cr in (False, True):
        beta, bad, n = solve(cr)
        print(f"word system ({'all' if cr else 'non-crossing'} pairings): words reached {n}/60, contradictions {bad}")
    beta, _, _ = solve(False)                  # unique up to a constant (word graph connected); orientation-dependent
    g = {w: 2 * beta[w] for w in WORDS}
    graphs = [('icosahedron', ICO, 0), ('T4', T4F, 0)]
    a = sys.argv
    while '--faces' in a:
        i = a.index('--faces'); F = [tuple(x) for x in json.load(open(a[i + 1]))]
        h = json.loads(a[a.index('--hole', i) + 1]); graphs.append((a[i + 1], F, h)); a = a[:i] + a[i + 2:]
    if '--multiclass' in a:
        mc = json.load(open(a[a.index('--multiclass') + 1]))['instances']
        for inst in mc:
            F = json.loads(inst['faces_ccw']) if isinstance(inst['faces_ccw'], str) else inst['faces_ccw']
            graphs.append((f"order{inst['order']}#{inst['plantri_index']}@{inst['hole']} (kappa {inst['kappa_T_minus_v']})",
                           [tuple(f) for f in F], inst['hole']))
    out = {}
    for name, F, h in graphs: out[name] = run(name, F, h, g)
    # the six-step T4 loop of disc-degree-parity.md: same word, opposite face parity
    adj, inner, L = out['T4']
    c = dict(zip(range(1, 17), (0,1,2,0,1,2,0,3,2,3,3,1,0,1,0,2)))
    c2 = dict(zip(range(1, 17), (0,1,2,0,1,3,3,1,3,2,2,0,2,0,1,3)))
    print(f"T4 six-step loop: words {word(c, L)} -> {word(c2, L)}; S = {S_of(c, inner)} -> {S_of(c2, inner)} "
          f"(difference mod 8 = {(S_of(c2, inner) - S_of(c, inner)) % 8})")
