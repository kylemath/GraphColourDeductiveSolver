import sys, json, numpy as np, collections as C
sys.path.insert(0, 'code')
from parts import parse
from mir import mirror
sc, P = parse('data/synth_rules_588.txt'); T = 2
def roles(slots, h):
    out = {}
    for j, s in enumerate(slots):
        o = (j - T) % h
        if o > h // 2: o -= h
        out[('s', o)] = (s[0], s[1]); out[('h', o)] = (s[2], s[3])
        for k, f in enumerate(s[4]): out[('f', o, k)] = f
    return out
def dist(a, b):
    ks = set(a) | set(b)
    return sum(1 for k in ks if a.get(k) != b.get(k))
# mirror pairs
key = {}
for i, p in enumerate(P): key.setdefault((p['pre'], p['hub'], p['w'], p['slots']), []).append(i)
used = set(); pairs = []
for i, p in enumerate(P):
    if i in used: continue
    ms = mirror(p, T, 1, 'with_spoke')
    js = [j for j in key.get((p['pre'], p['hub'], p['w'], ms), []) if j not in used and j != i]
    g = [i] + js[:1]; used |= set(g); pairs.append(g)
n = len(pairs)
R = [[roles(P[g[0]]['slots'], P[g[0]]['hub'])] + [roles(mirror(P[g[0]], T, 1, 'with_spoke'), P[g[0]]['hub'])] for g in pairs]
D = np.zeros((n, n))
for a in range(n):
    for b in range(a + 1, n):
        x = min(dist(R[a][0], rb) for rb in R[b]) + (0 if P[pairs[a][0]]['w'] == P[pairs[b][0]]['w'] else 0)
        D[a, b] = D[b, a] = x
# average-linkage agglomerative clustering, record leaf order
clusters = {i: [i] for i in range(n)}; heights = {}
Dc = {(i, j): D[i, j] for i in range(n) for j in range(i + 1, n)}
nxt = n; merges = []
active = set(range(n))
CD = D.copy().tolist()
import math
dd = {i: {j: D[i, j] for j in range(n) if j != i} for i in range(n)}
while len(active) > 1:
    best = None
    for i in active:
        for j, v in dd[i].items():
            if j in active and i < j and (best is None or v < best[0]): best = (v, i, j)
    v, i, j = best
    new = nxt; nxt += 1
    clusters[new] = clusters[i] + clusters[j]  # leaf order: left then right
    merges.append((v, i, j, new))
    dd[new] = {}
    for k in active:
        if k in (i, j): continue
        val = (dd[i][k] * len(clusters[i]) + dd[j][k] * len(clusters[j])) / (len(clusters[i]) + len(clusters[j]))
        dd[new][k] = val; dd[k][new] = val
    active -= {i, j}; active.add(new)
order = clusters[list(active)[0]]
# shape groups: cut at average distance <= 3 nodes
par = list(range(n))
def f(x):
    while par[x] != x: par[x] = par[par[x]]; x = par[x]
    return x
for v, i, j, new in merges:
    pass
grp = {}
def leaves_cut(th):
    lab = {}
    memb = {i: [i] for i in range(n)}
    for v, i, j, new in merges:
        memb[new] = memb[i] + memb[j]
    # assign: walk merges; a cluster formed at height <= th is a group
    gid = {}
    for v, i, j, new in merges:
        if v <= th:
            for x in memb[new]: gid[x] = new
    return gid
gid = leaves_cut(3.0)
gmap = {}; groups = []
for x in order:
    g = gid.get(x, ('solo', x))
    if g not in gmap: gmap[g] = len(gmap) + 1
    groups.append(gmap[g])
seq = []
for pos, x in enumerate(order):
    prev = order[pos - 1] if pos else None
    nn = sorted(range(n), key=lambda y: D[x, y])[1:6]
    seq.append(dict(pair=[int(v) for v in pairs[x]], group=groups[pos], dprev=None if prev is None else int(D[x, prev]),
                    near=[[int(pairs[y][0]), int(D[x, y])] for y in nn]))
json.dump(seq, open('db/continuum.json', 'w'))
gs = C.Counter(s['group'] for s in seq)
print('pairs', n, 'shape groups (<=3 nodes avg)', len(gs), 'sizes', sorted(gs.values(), reverse=True)[:15])
print('dprev dist', C.Counter(min(s['dprev'], 10) for s in seq if s['dprev'] is not None))
