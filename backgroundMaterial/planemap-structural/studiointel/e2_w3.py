#!/usr/bin/env python3
"""studiointel e2_w3.py -- [computed, exploratory, post hoc] Intern A cycle 3 check: on every E2 record (frame of intern-A-cycle2/3),
after the AB swap: does w3 have a g-neighbour y1 != x3 and a d-neighbour y2 != x4? deg w3? which new lock fails?
For a failing lock we also record whether x1's two-colour component reaches ANY neighbour of w3 (other than x3/x4),
i.e. whether the path is cut off far from w3 or only at the last step."""
import sys, itertools
from collections import Counter, defaultdict
sys.path.insert(0, '.')
import graphs
from ring_patterns import third, one_flips
from coset_potential import orient
import radius

def comp(adjT, col, hole, s, cols):
    K = {s}; st = [s]
    while st:
        u = st.pop()
        for w in adjT[u]:
            if w != hole and w not in K and col[w] in cols: K.add(w); st.append(w)
    return K

res = Counter()
def run(faces, hole):
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
            new = dict(col)
            for t in (0, 1, 2): new[X[t]] = B if col[X[t]] == A else A
            w3 = W[3]
            y1 = [u for u in adjT[w3] if u != hole and new[u] == G and u != X[3]]
            y2 = [u for u in adjT[w3] if u != hole and new[u] == D and u != X[4]]
            Kg = comp(adjT, new, hole, X[1], (A, G)); Kd = comp(adjT, new, hole, X[1], (A, D))
            l1 = X[3] in Kg; l2 = X[4] in Kd
            near = set(adjT[w3]) - {X[3], X[4], hole}
            res[(('deg w3', deg[w3]), ('y1', len(y1) > 0), ('y2', len(y2) > 0), ('lock_ag', l1), ('lock_ad', l2),
                 ('ag-comp of x1 touches N(w3)', bool(Kg & near)), ('ad-comp of x1 touches N(w3)', bool(Kd & near)))] += 1

T4 = [(0,1,2),(0,1,5),(0,2,3),(0,3,4),(0,4,5),(1,2,6),(1,5,10),(1,6,10),(2,3,7),(2,6,11),(2,7,11),(3,4,8),(3,7,8),(4,5,9),(4,8,9),(5,9,10),(6,10,15),(6,11,15),(7,8,12),(7,11,12),(8,9,13),(8,12,13),(9,10,14),(9,13,14),(10,14,15),(11,12,16),(11,15,16),(12,13,16),(13,14,16),(14,15,16)]
base = [('T4', orient(T4)), ('A_3', graphs.A_r(3)), ('A_4', graphs.A_r(4)), ('A_5', graphs.A_r(5))]
gl = list(base)
for nm, fs in base[:3]:
    for e, nf in one_flips(fs): gl.append((nm, nf))
for nm, fs in gl:
    dg = graphs.degrees(fs)
    for h in sorted(dg):
        if dg[h] == 5: run(fs, h)
print('E2 records:', sum(res.values()))
for k, v in sorted(res.items(), key=lambda kv: -kv[1]): print(v, k)
