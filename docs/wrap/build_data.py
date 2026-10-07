# Builds data.json for the "Wrapping the sphere" page from the order-22 F-cycle graph
# (backgroundMaterial/planemap-structural/studiointel/fcycle/fcycle_order22.json; hole 15).
import json, math, random, itertools, collections, subprocess
SRC = 'backgroundMaterial/planemap-structural/studiointel/fcycle/fcycle_order22.json'
try:
    d = json.load(open(SRC))
except FileNotFoundError:
    d = json.loads(subprocess.check_output(['git', 'show', 'origin/studio-intel:' + SRC]))
F = [tuple(f) for f in d['faces']]; n = 1 + max(max(f) for f in F); HOLE = d['hole']
adj = [set() for _ in range(n)]
for a, b, c in F:
    for x, y in ((a, b), (b, c), (c, a)): adj[x].add(y); adj[y].add(x)
assert n - sum(len(a) for a in adj) // 2 + len(F) == 2
# ---------- sphere embedding: Tutte (outer face fixed) -> inverse stereographic -> spherical relaxation
outer = F[0]
pos2 = {v: (math.cos(2*math.pi*i/3), math.sin(2*math.pi*i/3)) for i, v in enumerate(outer)}
P = [list(pos2.get(v, (0.0, 0.0))) for v in range(n)]
for _ in range(4000):
    for v in range(n):
        if v in pos2: continue
        P[v] = [sum(P[w][k] for w in adj[v]) / len(adj[v]) for k in range(2)]
def inv_stereo(x, y, s):
    x, y = x*s, y*s; r2 = x*x + y*y
    return [2*x/(1+r2), 2*y/(1+r2), (r2-1)/(1+r2)]
def norm(v): l = math.sqrt(sum(t*t for t in v)); return [t/l for t in v]
def sub(a, b): return [a[i]-b[i] for i in range(3)]
def cross(a, b): return [a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0]]
def dot(a, b): return sum(a[i]*b[i] for i in range(3))
def signs(X):
    out = []
    for a, b, c in F:
        nrm = cross(sub(X[b], X[a]), sub(X[c], X[a])); cen = [X[a][k]+X[b][k]+X[c][k] for k in range(3)]
        out.append(dot(nrm, cen))
    return out
best = None
for s in [0.4, 0.6, 0.8, 1.0, 1.3, 1.7, 2.2, 3.0]:
    X = [inv_stereo(*P[v], s) for v in range(n)]
    sg = signs(X)
    if all(t > 0 for t in sg) or all(t < 0 for t in sg):
        spread = min(math.dist(X[a], X[b]) for a in range(n) for b in adj[a])
        if best is None or spread > best[0]: best = (spread, X)
X = best[1]
# gentle relaxation that keeps every face's orientation
flip = signs(X)[0] < 0
for it in range(3000):
    Y = []
    for v in range(n):
        m = [sum(X[w][k] for w in adj[v]) / len(adj[v]) for k in range(3)]
        Y.append(norm([0.9*X[v][k] + 0.1*m[k] for k in range(3)]))
    sg = signs(Y)
    if all((t < 0) if flip else (t > 0) for t in sg): X = Y
    else: break
if flip: F = [(a, c, b) for a, b, c in F]
assert all(t > 0 for t in signs(X)), 'faces must face outward'
# ---------- all labelled 4-colourings of T, Kempe classes, folding degree
order = sorted(range(n), key=lambda v: -len(adj[v])); cols = []; col = [-1]*n
def bt(i):
    if i == n: cols.append(tuple(col)); return
    v = order[i]
    for c in range(4):
        if all(col[w] != c for w in adj[v]): col[v] = c; bt(i+1); col[v] = -1
bt(0)
s3 = 1/math.sqrt(3)
CORN = [[s3, s3, s3], [s3, -s3, -s3], [-s3, s3, -s3], [-s3, -s3, s3]]
def tsign(t):
    A, B, C = (CORN[k] for k in t)
    nrm = cross(sub(B, A), sub(C, A)); cen = [A[k]+B[k]+C[k] for k in range(3)]
    return 1 if dot(nrm, cen) > 0 else -1
def deg_by_face(c):
    out = []
    for m in range(4):
        out.append(sum(tsign((c[a], c[b], c[cc])) for a, b, cc in F if m not in (c[a], c[b], c[cc])))
    return out
idx = {c: i for i, c in enumerate(cols)}; par = list(range(len(cols)))
def find(x):
    while par[x] != x: par[x] = par[par[x]]; x = par[x]
    return x
for c in cols:
    for a, b in itertools.combinations(range(4), 2):
        seen = set()
        for v in range(n):
            if c[v] in (a, b) and v not in seen:
                comp = [v]; seen.add(v); st = [v]
                while st:
                    u = st.pop()
                    for w in adj[u]:
                        if c[w] in (a, b) and w not in seen: seen.add(w); comp.append(w); st.append(w)
                nc = list(c)
                for u in comp: nc[u] = b if c[u] == a else a
                x, y = find(idx[c]), find(idx[tuple(nc)])
                if x != y: par[x] = y
classes = collections.defaultdict(list)
for c in cols: classes[find(idx[c])].append(c)
cls_sorted = sorted(classes.values(), key=len, reverse=True)
cls_of = {}
for k, members in enumerate(cls_sorted):
    for c in members: cls_of[c] = k
summary = []
for k, members in enumerate(cls_sorted):
    ds = collections.Counter(deg_by_face(c)[0] for c in members)
    assert all(len(set(deg_by_face(c))) == 1 for c in members), 'degree must not depend on the target face'
    assert len({x % 2 for x in ds}) == 1
    summary.append({'size': len(members), 'degrees': sorted(ds.items())})
picks = []
want = [(0, 0), (0, 2), (0, 4), (0, 6), (1, 1), (1, 3)]
for k, dg in want:
    for c in cls_sorted[k]:
        if deg_by_face(c)[0] == dg and len({c[w] for w in adj[HOLE]}) == 3:
            picks.append({'col': list(c), 'degree': dg, 'cls': k}); break
# a blocked (doubly locked) state of T - v from the F-cycle data
st = d['cycle_canonical_states'][0]['state']
blocked = [st.get(str(v), -1) for v in range(n)]
link = [w for w in d['link']]
json.dump({'n': n, 'faces': F, 'pos': [[round(t, 5) for t in p] for p in X], 'hole': HOLE, 'link': link,
           'deg': [len(a) for a in adj], 'picks': picks, 'blocked': blocked, 'classes': summary,
           'ncol': len(cols)}, open('docs/wrap/data.json', 'w'))
print('colourings', len(cols), 'classes', [(s['size'], s['degrees']) for s in summary])
print('picks', [(p['degree'], p['cls']) for p in picks], 'blocked link colours', [blocked[w] for w in link])
