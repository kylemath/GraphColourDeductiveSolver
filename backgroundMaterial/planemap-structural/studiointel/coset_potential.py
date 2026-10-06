#!/usr/bin/env python3
"""studiointel coset_potential.py -- [computed, exploratory, post hoc] side computation for Intern D's coset-curvature potential
(SolvingFrameworkPlan/docs/working/interns-2026-10-06/intern-D.md), requested by the coordinator 6 Oct. Not part of the pre-registered search.
k(u) = 6 - deg_T(u); kappa_c = sum of k over colour class c in T-v (sum = 11). For an unfilled state with repeat colour alpha at x_j,x_{j+2},
roles mu = c(m), A = c(a), B = c(b) (m=x_{j+1}, a=x_{j+3}, b=x_{j+4}). With beta = alpha+mu, gamma = alpha+A, delta = alpha+B (Z2xZ2),
the coset of {0,x} containing alpha is {alpha,mu} for beta, {alpha,A} for gamma, {alpha,B} for delta; we report Phi_x as the curvature of
the coset CONTAINING alpha (label-free convention; the other coset has 11 - Phi_x). Radius as in radius.py (0 filled, 1 unfilled non-DL, 1+d DL)."""
import sys, json, itertools
from collections import deque, Counter, defaultdict
sys.path.insert(0, '.')
import radius, graphs

def orient(faces):
    """consistently orient an unoriented sphere triangulation by BFS over faces"""
    faces = [tuple(f) for f in faces]; byedge = defaultdict(list)
    for i, f in enumerate(faces):
        for e in itertools.combinations(f, 2): byedge[frozenset(e)].append(i)
    out = {0: faces[0]}; q = deque([0])
    while q:
        i = q.popleft(); f = out[i]
        for t in range(3):
            a, b = f[t], f[(t + 1) % 3]
            for j in byedge[frozenset((a, b))]:
                if j in out: continue
                c = [x for x in faces[j] if x not in (a, b)][0]
                out[j] = (b, a, c); q.append(j)
    return [out[i] for i in range(len(faces))]

def from_rot(rot):
    fs = set()
    for u, r in enumerate(rot):
        for i in range(len(r)):
            f = (u, r[i], r[(i + 1) % len(r)]); k = f.index(min(f)); fs.add(f[k:] + f[:k])
    return sorted(fs)

def run(name, faces, hole):
    ok, msg = graphs.check_triangulation(faces); assert ok, msg
    deg = graphs.degrees(faces)
    order, idx, nb, link = radius.prepare(faces, hole)
    k = [6 - deg[u] for u in order]
    states = radius.enumerate_states(nb, 10 ** 6)
    cls = {s: radius.classify(nb, link, s) for s in states}
    # distances to NL (filled or unfilled non-DL) over the whole swap graph, and full adjacency for path checks
    nbr = {s: set(radius.swaps(nb, s)) - {s} for s in states}
    dist = {s: 0 for s in states if cls[s] != 2}
    q = deque(dist)
    while q:
        s = q.popleft()
        for t in nbr[s]:
            if t not in dist: dist[t] = dist[s] + 1; q.append(t)
    rad = {s: (0 if cls[s] == 0 else 1 if cls[s] == 1 else 1 + dist.get(s, 10 ** 6)) for s in states}
    def roles(s):
        lc = [s[x] for x in link]
        if len(set(lc)) <= 3: return None
        j = [j for j in range(5) if lc[j] == lc[(j + 2) % 5]][0]
        al, mu, A, B = lc[j], lc[(j + 1) % 5], lc[(j + 3) % 5], lc[(j + 4) % 5]
        kap = [sum(k[i] for i in range(len(s)) if s[i] == c) for c in range(4)]
        K = (kap[al], kap[mu], kap[A], kap[B])
        return K, {'beta': K[0] + K[1], 'gamma': K[0] + K[2], 'delta': K[0] + K[3]}
    rows = []
    for s in states:
        r = roles(s)
        if r is None: continue
        rows.append({'radius': rad[s], 'DL': cls[s] == 2, 'K': r[0], 'Phi': r[1]})
    # separation table: for each statistic, range by radius among unfilled states
    stats = {'K(alpha,mu,A,B)': lambda r: r['K'], 'Phi_beta': lambda r: r['Phi']['beta'], 'Phi_gamma': lambda r: r['Phi']['gamma'],
             'Phi_delta': lambda r: r['Phi']['delta'], 'kappa_alpha-kappa_mu': lambda r: r['K'][0] - r['K'][1],
             'argmin-role': lambda r: tuple(i for i in range(4) if r['K'][i] == min(r['K']))}
    print('==', name, 'hole', hole, 'n=%d' % len(deg), 'canonical states', len(states), 'filled', sum(1 for s in states if cls[s] == 0),
          'DL', sum(1 for s in states if cls[s] == 2), 'radius hist (unfilled)', dict(sorted(Counter(r['radius'] for r in rows).items())))
    verdict = {}
    for nm, f in stats.items():
        byr = defaultdict(Counter)
        for r in rows: byr[r['radius']][f(r)] += 1
        print('  %-22s' % nm, {rr: dict(sorted(byr[rr].items())) for rr in sorted(byr)})
        rs = sorted(byr)
        top = rs[-1]; low = [x for x in rs if x >= 2 and x < top]
        if top >= 3 and low:
            sep = not (set(byr[top]) & set().union(*[set(byr[x]) for x in low]))
            verdict[nm] = 'separates radius %d from radius %s' % (top, low) if sep else 'overlaps'
    # monotonicity along shortest fills: steps s->t with dist[t] = dist[s]-1, both unfilled, compare Phi by role
    steps = defaultdict(Counter)
    for s in states:
        if cls[s] != 2 or s not in dist: continue
        rs_ = roles(s)
        for t in nbr[s]:
            if dist.get(t, 10 ** 6) == dist[s] - 1:
                rt = roles(t)
                if rt is None: continue
                for x in ('beta', 'gamma', 'delta'):
                    d = rt[1][x] - rs_[1][x]; steps[x]['up' if d > 0 else 'down' if d < 0 else 'flat'] += 1
    print('  shortest-fill steps (DL -> closer, unfilled to unfilled), change of Phi by role:', {x: dict(steps[x]) for x in steps})
    print('  verdict:', verdict)
    return verdict

if __name__ == '__main__':
    # T4 face list copied verbatim from longtable/explore-vhphi/pathways/pd_lib.py line 9 (unoriented)
    T4_FACES = [(0,1,2),(0,1,5),(0,2,3),(0,3,4),(0,4,5),(1,2,6),(1,5,10),(1,6,10),(2,3,7),(2,6,11),(2,7,11),(3,4,8),(3,7,8),(4,5,9),(4,8,9),(5,9,10),(6,10,15),(6,11,15),(7,8,12),(7,11,12),(8,9,13),(8,12,13),(9,10,14),(9,13,14),(10,14,15),(11,12,16),(11,15,16),(12,13,16),(13,14,16),(14,15,16)]
    run('T4', orient(T4_FACES), 4)
    run('A_3', graphs.A_r(3), 0)
    import re
    d = json.loads(re.search(r'=\s*(\{.*\})\s*;?\s*$', open('../../../docs/66666/data.js').read(), re.S).group(1))
    run('order-28 (6^5)', orient(d['faces']), d['hole'])
