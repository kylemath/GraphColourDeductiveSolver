#!/usr/bin/env python3
"""studiointel ring_patterns.py -- [computed, exploratory, post hoc] side computation for Interns A, A-cycle2 and B
(SolvingFrameworkPlan/docs/working/interns-2026-10-06/). Not part of the pre-registered search.
Frame (all three files): link x0..x4 coloured (a,b,a,g,d): repeat at x0,x2, m = x1, lock 1 = {b,g}-path x1->x3, lock 2 = {b,d}-path x1->x4.
w_t = third vertex of the face on edge x_t x_{t+1} other than v. Pattern = letters of (w0..w4).
For a degree-6 x_t, m_t = its neighbour outside {v, x_{t-1}, x_{t+1}, w_{t-1}, w_t}.
K_F = {a,g}-component of x2; K_B = {a,d}-component of x0 (Intern A cycle 2, sec. 0).
ORIENTATION: the files fix x0..x4 by colours but not the sense of rotation; the mirror sends w_t -> w_{1-t} and g<->d, which changes
some pattern strings (dgdag -> dggag... is NOT self-mirror as a string). We therefore report every DL state in BOTH senses
(equivalently: every graph together with its mirror image). Class = degree multiset of the link; positions of the degree-6 pair in the frame."""
import sys, json, itertools
from collections import deque, Counter, defaultdict
sys.path.insert(0, '.')
import radius, graphs
from coset_potential import orient

def third(faces_by_edge, x, y, v):
    return [z for z in faces_by_edge[frozenset((x, y))] if z != v][0]

def analyse(name, faces, hole, out):
    deg = graphs.degrees(faces)
    fbe = defaultdict(list)
    for f in faces:
        for e in itertools.combinations(f, 2):
            fbe[frozenset(e)].append([z for z in f if z not in e][0])
    order, idx, nb, link = radius.prepare(faces, hole)        # link: positions in 'order' indexing
    L = [order[i] for i in link]
    adjT = graphs.adjacency(faces)
    states = radius.enumerate_states(nb, 10 ** 6)
    cls = {s: radius.classify(nb, link, s) for s in states}
    nbr = {s: set(radius.swaps(nb, s)) - {s} for s in states}
    dist = {s: 0 for s in states if cls[s] != 2}; q = deque(dist)
    while q:
        s = q.popleft()
        for t in nbr[s]:
            if t not in dist: dist[t] = dist[s] + 1; q.append(t)
    for s in states:
        if cls[s] != 2: continue
        r = 1 + dist[s] if s in dist else None
        col = {order[i]: s[i] for i in range(len(s))}
        lc = [col[x] for x in L]; j = [j for j in range(5) if lc[j] == lc[(j + 2) % 5]][0]
        for sense in (+1, -1):
            X = [L[(j + t) % 5] for t in range(5)] if sense > 0 else [L[(j + 2 - t) % 5] for t in range(5)]
            name_of = {col[X[0]]: 'a', col[X[1]]: 'b', col[X[3]]: 'g', col[X[4]]: 'd'}
            W = [third(fbe, X[t], X[(t + 1) % 5], hole) for t in range(5)]
            pat = ''.join(name_of[col[w]] for w in W)
            free = tuple(t for t in range(5) if deg[X[t]] >= 6)
            degs = tuple(deg[X[t]] for t in range(5))
            rec = {'graph': name, 'hole': hole, 'sense': sense, 'degs': degs, 'free': free, 'pattern': pat, 'radius': r}
            if free == (3, 4) and all(deg[X[t]] == 6 for t in (3, 4)):
                m = {}
                for t in (3, 4):
                    known = {hole, X[(t - 1) % 5], X[(t + 1) % 5], W[(t - 1) % 5], W[t]}
                    rest = [u for u in adjT[X[t]] if u not in known]
                    m[t] = rest[0] if len(rest) == 1 else None
                def compo(start, p, qq):
                    seen = {start}; st = [start]
                    while st:
                        u = st.pop()
                        for w in adjT[u]:
                            if w != hole and w not in seen and col[w] in (p, qq): seen.add(w); st.append(w)
                    return seen
                a_, g_, d_ = col[X[0]], col[X[3]], col[X[4]]
                KF = compo(X[2], a_, g_); KB = compo(X[0], a_, d_)
                if m[3] is not None and m[4] is not None:
                    rec['m3'] = name_of[col[m[3]]]; rec['m4'] = name_of[col[m[4]]]
                    rec['m3_in_KB'] = m[3] in KB; rec['m4_in_KF'] = m[4] in KF
                    rec['E1'] = pat == 'gdbbb' and rec['m3'] == 'd' and rec['m4'] == 'g' and not rec['m3_in_KB'] and not rec['m4_in_KF']
                    rec['E2'] = pat == 'dgdag' and rec['m3'] == 'b' and rec['m4'] == 'b'
            out.append(rec)

def one_flips(faces):
    es = sorted({tuple(sorted((f[i], f[(i + 1) % 3]))) for f in faces for i in range(3)})
    for a, b in es:
        nf = graphs.flip(faces, a, b)
        if nf is None: continue
        dg = graphs.degrees(nf)
        if min(dg.values()) < 5 or graphs.n_separating_triangles(nf): continue
        yield (a, b), nf

if __name__ == '__main__':
    import re
    T4 = [(0,1,2),(0,1,5),(0,2,3),(0,3,4),(0,4,5),(1,2,6),(1,5,10),(1,6,10),(2,3,7),(2,6,11),(2,7,11),(3,4,8),(3,7,8),(4,5,9),(4,8,9),(5,9,10),(6,10,15),(6,11,15),(7,8,12),(7,11,12),(8,9,13),(8,12,13),(9,10,14),(9,13,14),(10,14,15),(11,12,16),(11,15,16),(12,13,16),(13,14,16),(14,15,16)]
    d28 = json.loads(re.search(r'=\s*(\{.*\})\s*;?\s*$', open('../../../docs/66666/data.js').read(), re.S).group(1))
    base = [('T4', orient(T4)), ('A_3', graphs.A_r(3)), ('A_4', graphs.A_r(4)), ('A_5', graphs.A_r(5)), ('order28', orient(d28['faces']))]
    gl = list(base)
    for nm, fs in base[:3]:
        for e, nf in one_flips(fs): gl.append(('%s-flip%d-%d' % (nm, e[0], e[1]), nf))
    out = []
    for nm, fs in gl:
        dg = graphs.degrees(fs)
        for h in sorted(dg):
            if dg[h] == 5: analyse(nm, fs, h, out)
    json.dump(out, open('ring_patterns.jsonl', 'w'))
    print('graphs', len(gl), 'DL records (state x sense)', len(out))
    adj = lambda r: r['free'] == (3, 4) and sorted(r['degs']) == [5, 5, 5, 6, 6]
    nonadj = lambda r: sorted(r['degs']) == [5, 5, 6, 6, 6][:0] or (sorted(r['degs']) == [5, 5, 5, 6, 6] and len(r['free']) == 2 and (r['free'][1] - r['free'][0]) % 5 in (2, 3))
    def summary(title, pred):
        rs = [r for r in out if pred(r)]
        print('\n##', title, ': records', len(rs), ' max radius', max((r['radius'] or 99) for r in rs) if rs else None)
        c = defaultdict(Counter)
        for r in rs: c[(r['free'], r['pattern'])][r['radius']] += 1
        for k in sorted(c): print('  free', k[0], 'pattern', k[1], 'radii', dict(sorted(c[k].items())))
    summary('(5,5,5,6,6) adjacent pair, all positions', lambda r: sorted(r['degs']) == [5, 5, 5, 6, 6] and len(r['free']) == 2 and (r['free'][1] - r['free'][0]) % 5 in (1, 4))
    summary('(5,5,6,5,6) non-adjacent pair, all positions', nonadj)
    for tag in ('E1', 'E2'):
        rs = [r for r in out if r.get(tag)]
        print('\n##', tag, 'occurrences', len(rs), [(r['graph'], r['hole'], r['sense'], r['radius']) for r in rs][:20])
    pa = [r for r in out if r['free'] == (3, 4) and 'm3' in r and r['pattern'] in ('gdbbb', 'dgdag')]
    print('\n## pair {3,4} with pattern gdbbb or dgdag (m-data):', Counter((r['pattern'], r['m3'], r['m4'], r['m3_in_KB'], r['m4_in_KF'], r['radius']) for r in pa))
    closed = {0: 'gdbab dgbab gddbg dgdbg', 1: 'ggdab gdbab dgdbg ddbbg', 2: 'gdbab gddbb dgbag dgdbg', 3: 'gdbab gdbbg dgdab dgdbg', 4: 'gdbab ddbag ggdbb dgdbg'}
    rs = [r for r in out if nonadj(r)]
    hit = Counter(); allp = Counter()
    for r in rs:
        k = r['free'][0] if (r['free'][1] - r['free'][0]) % 5 == 2 else r['free'][1]
        allp[(k, r['pattern'], r['radius'])] += 1
        if r['pattern'] in closed[k].split(): hit[(k, r['pattern'], r['radius'])] += 1
    print('\n## Intern B closed set (P_k = {k,k+2}): occurrences (k, pattern, radius) ->', dict(sorted(hit.items())))
    print('## Intern B all (5,5,6,5,6) DL patterns (k, pattern, radius) ->', dict(sorted(allp.items())))
