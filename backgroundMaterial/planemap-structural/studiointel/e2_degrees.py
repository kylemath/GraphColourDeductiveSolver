#!/usr/bin/env python3
"""studiointel e2_degrees.py -- [computed, exploratory, post hoc] Intern A cycle 4 check: on every E2 record (frame of intern-A-cycle2),
degrees of w0, w1, w3; how many have all three >= 6; lock status after AB for those. Graphs: the 32 of e2_kills.py plus the four Phase C radius-5 graphs."""
import sys, json, itertools
from collections import Counter, defaultdict
sys.path.insert(0, '.')
import radius, graphs
from ring_patterns import third, one_flips
from coset_potential import orient

def comp(adjT, col, hole, s, cols):
    K = {s}; st = [s]
    while st:
        u = st.pop()
        for w in adjT[u]:
            if w != hole and w not in K and col[w] in cols: K.add(w); st.append(w)
    return K

res = Counter(); ex = []
def run(name, faces, hole):
    deg = graphs.degrees(faces); adjT = graphs.adjacency(faces)
    fbe = defaultdict(list)
    for f in faces:
        for e in itertools.combinations(f, 2): fbe[frozenset(e)].append([z for z in f if z not in e][0])
    order, idx, nb, link = radius.prepare(faces, hole); L = [order[i] for i in link]
    for s in radius.enumerate_states(nb, 10 ** 6):
        if radius.classify(nb, link, s) != 2: continue
        col = {order[i]: s[i] for i in range(len(s))}
        lc = [col[x] for x in L]; j = [j for j in range(5) if lc[j] == lc[(j + 2) % 5]][0]
        for sense in (1, -1):
            X = [L[(j + t) % 5] for t in range(5)] if sense > 0 else [L[(j + 2 - t) % 5] for t in range(5)]
            if not (deg[X[3]] == 6 and deg[X[4]] == 6 and all(deg[X[t]] == 5 for t in (0, 1, 2))): continue
            A, B, G, D = col[X[0]], col[X[1]], col[X[3]], col[X[4]]
            let = {A: 'a', B: 'b', G: 'g', D: 'd'}
            W = [third(fbe, X[t], X[(t + 1) % 5], hole) for t in range(5)]
            if ''.join(let[col[w]] for w in W) != 'dgdag': continue
            m = {t: [u for u in adjT[X[t]] if u not in {hole, X[(t - 1) % 5], X[(t + 1) % 5], W[(t - 1) % 5], W[t]}][0] for t in (3, 4)}
            if not (let[col[m[3]]] == 'b' and let[col[m[4]]] == 'b'): continue
            new = dict(col)
            for t in (0, 1, 2): new[X[t]] = B if col[X[t]] == A else A
            l1 = X[3] in comp(adjT, new, hole, X[1], (A, G)); l2 = X[4] in comp(adjT, new, hole, X[1], (A, D))
            d = (deg[W[0]], deg[W[1]], deg[W[3]])
            allbig = all(x >= 6 for x in d)
            res[('deg(w0,w1,w3)', d, 'all>=6', allbig, 'locks after AB', (l1, l2))] += 1
            if allbig and len(ex) < 3: ex.append({'graph': name, 'hole': hole, 'sense': sense, 'X': X, 'W': W, 'deg_w0_w1_w3': d, 'locks_after_AB': (l1, l2)})

T4 = [tuple(f) for f in json.load(open('seeds/T4.json'))['faces']]
base = [('T4', T4), ('A_3', graphs.A_r(3)), ('A_4', graphs.A_r(4)), ('A_5', graphs.A_r(5))]
gl = list(base)
for nm, fs in base[:3]:
    for e, nf in one_flips(fs): gl.append(('%s-flip%d-%d' % (nm, e[0], e[1]), nf))
for t in ('91a307d1852a1764', '8a23ee3ec7b2bb33', '62661a3f304f4caa', '80b930d1540e4ee3'):
    gl.append(('cert-' + t, [tuple(f) for f in json.load(open('run-C-2026-10-06/cert/%s.graph.json' % t))['faces']]))
for nm, fs in gl:
    dg = graphs.degrees(fs)
    for h in sorted(dg):
        if dg[h] == 5: run(nm, fs, h)
print('E2 records:', sum(res.values()), '; in the four radius-5 graphs:', 'see rows')
for k, v in sorted(res.items(), key=lambda kv: -kv[1]): print(v, k)
print('examples with all three >= 6:', json.dumps(ex))
