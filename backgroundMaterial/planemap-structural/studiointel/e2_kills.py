#!/usr/bin/env python3
"""studiointel e2_kills.py -- [computed, exploratory, post hoc]. For every realisation of Intern A cycle 2's E2 (frame as in ring_patterns.py),
list the first swaps that leave the doubly locked set (E2 has radius 2, so such a swap exists): colour pair in frame letters,
which named vertices (x0..x4, w0..w4, m3, m4) the swapped component contains, its size, and its depth (max graph distance from v)."""
import sys, json, itertools
from collections import Counter, defaultdict, deque
sys.path.insert(0, '.')
import radius, graphs
from ring_patterns import third, one_flips
from coset_potential import orient

def run(name, faces, hole, tally, examples):
    deg = graphs.degrees(faces); adjT = graphs.adjacency(faces)
    fbe = defaultdict(list)
    for f in faces:
        for e in itertools.combinations(f, 2): fbe[frozenset(e)].append([z for z in f if z not in e][0])
    dv = {hole: 0}; q = deque([hole])
    while q:
        u = q.popleft()
        for w in adjT[u]:
            if w not in dv: dv[w] = dv[u] + 1; q.append(w)
    order, idx, nb, link = radius.prepare(faces, hole); L = [order[i] for i in link]
    for s in radius.enumerate_states(nb, 10 ** 6):
        if radius.classify(nb, link, s) != 2: continue
        col = {order[i]: s[i] for i in range(len(s))}
        lc = [col[x] for x in L]; j = [j for j in range(5) if lc[j] == lc[(j + 2) % 5]][0]
        for sense in (+1, -1):
            X = [L[(j + t) % 5] for t in range(5)] if sense > 0 else [L[(j + 2 - t) % 5] for t in range(5)]
            if not (deg[X[3]] == 6 and deg[X[4]] == 6 and all(deg[X[t]] == 5 for t in (0, 1, 2))): continue
            let = {col[X[0]]: 'a', col[X[1]]: 'b', col[X[3]]: 'g', col[X[4]]: 'd'}
            W = [third(fbe, X[t], X[(t + 1) % 5], hole) for t in range(5)]
            if ''.join(let[col[w]] for w in W) != 'dgdag': continue
            m = {t: [u for u in adjT[X[t]] if u not in {hole, X[(t - 1) % 5], X[(t + 1) % 5], W[(t - 1) % 5], W[t]}][0] for t in (3, 4)}
            if not (let[col[m[3]]] == 'b' and let[col[m[4]]] == 'b'): continue
            named = {**{X[t]: 'x%d' % t for t in range(5)}, **{W[t]: 'w%d' % t for t in range(5)}, m[3]: 'm3', m[4]: 'm4'}
            kills = []
            for p, qq in itertools.combinations(range(4), 2):
                seen = set()
                for u in col:
                    if u in seen or col[u] not in (p, qq): continue
                    K = {u}; st = [u]
                    while st:
                        y = st.pop()
                        for w in adjT[y]:
                            if w != hole and w not in K and col[w] in (p, qq): K.add(w); st.append(w)
                    seen |= K
                    new = [s[i] if order[i] not in K else (qq if s[i] == p else p) for i in range(len(s))]
                    c2 = radius.classify(nb, link, radius.canon(new))
                    if c2 != 2:
                        desc = (''.join(sorted(let[p] + let[qq])), tuple(sorted(named[z] for z in K if z in named)),
                                'filled' if c2 == 0 else 'unlocked', 'depth%d' % max(dv[z] for z in K))
                        kills.append((desc, len(K)))
            tally['states'] += 1
            for d, sz in kills: tally[d] += 1
            key = tuple(sorted(d for d, _ in kills))
            examples[key] += 1

if __name__ == '__main__':
    T4 = [(0,1,2),(0,1,5),(0,2,3),(0,3,4),(0,4,5),(1,2,6),(1,5,10),(1,6,10),(2,3,7),(2,6,11),(2,7,11),(3,4,8),(3,7,8),(4,5,9),(4,8,9),(5,9,10),(6,10,15),(6,11,15),(7,8,12),(7,11,12),(8,9,13),(8,12,13),(9,10,14),(9,13,14),(10,14,15),(11,12,16),(11,15,16),(12,13,16),(13,14,16),(14,15,16)]
    base = [('T4', orient(T4)), ('A_3', graphs.A_r(3)), ('A_4', graphs.A_r(4)), ('A_5', graphs.A_r(5))]
    gl = list(base)
    for nm, fs in base[:3]:
        for e, nf in one_flips(fs): gl.append(('%s-flip%d-%d' % (nm, e[0], e[1]), nf))
    tally = Counter(); examples = Counter()
    for nm, fs in gl:
        dg = graphs.degrees(fs)
        for h in sorted(dg):
            if dg[h] == 5: run(nm, fs, h, tally, examples)
    print('E2 records (state x sense):', tally.pop('states'))
    print('\nkilling first swaps (pair, named vertices in K, result, depth) : number of records having it')
    for k, v in tally.most_common(): print('  ', v, k)
    print('\nfull kill-sets per record (how many records have exactly this set of killing swaps):')
    for k, v in examples.most_common(10): print('  ', v, k)
