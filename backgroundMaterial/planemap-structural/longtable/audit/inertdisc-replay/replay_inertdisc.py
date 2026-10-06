#!/usr/bin/env python3
"""Audit replay of an inert-disc instance (stdlib only; imports no team code).

Conventions (Intern A, docs/working/InternA-inert-disc.md): link x0..x4 in rotation order at the hole h,
DL frame (repeat x_j = x_{j+2} = alpha, middle m = x_{j+1} colour mu, a = x_{j+3}, b = x_{j+4}).
Lock 1: m ~ a in the {mu, c(a)}-subgraph of T - h; lock 2: m ~ b in the {mu, c(b)}-subgraph.
J1 = h + a lock-1 path; D1 = the side of T - J1 containing x_{j+2}. J2 = h + a lock-2 path; D2 = the side
containing x_j. A path is taken as a shortest one; whether it is unique (the chain component is a tree,
or the shortest path is unique) is reported, since the disc depends on the path.
Radius: least number of whole-component Kempe swaps of T - h to a filled state (link <= 3 colours),
exact, by BFS over canonical colourings.

usage: replay_inertdisc.py INSTANCE.json     (fields: graph = plantri ASCII line, hole, example.colouring,
                                              example.component = the swapped component)
"""
import json, sys
from collections import deque


def parse_plantri(line):
    n, rest = line.split()
    return [[ord(c) - 97 for c in part] for part in rest.split(',')]


def main():
    inst = json.load(open(sys.argv[1]))
    rot = parse_plantri(inst['graph']); n = len(rot); h = inst['hole']
    adj = [set(r) for r in rot]
    ex = inst['example']; col0 = {int(k): v for k, v in ex['colouring'].items()}
    comp_claim = sorted(ex['component'])
    out = {}
    V = [u for u in range(n) if u != h]
    out['covers'] = sorted(col0) == V
    out['proper'] = all(col0[u] != col0[w] for u in V for w in adj[u] if w != h)
    L = rot[h]; out['hole_degree'] = len(L)

    def comp(col, s, p, q, block=()):
        seen = {s}; st = [s]
        while st:
            x = st.pop()
            for y in adj[x]:
                if y != h and y not in block and y not in seen and col[y] in (p, q):
                    seen.add(y); st.append(y)
        return seen

    def frame(col):
        lc = [col[x] for x in L]
        if len(set(lc)) != 4: return None
        return next(j for j in range(5) if lc[j] == lc[(j + 2) % 5])

    def dl(col):
        j = frame(col)
        if j is None: return False
        m, a, b = L[(j + 1) % 5], L[(j + 3) % 5], L[(j + 4) % 5]
        return a in comp(col, m, col[m], col[a]) and b in comp(col, m, col[m], col[b])

    def canon(col):
        ren = {}; return tuple(ren.setdefault(col[u], len(ren)) for u in V)

    def swaps(col):
        for p in range(4):
            for q in range(p + 1, 4):
                done = set()
                for s in V:
                    if col[s] in (p, q) and s not in done:
                        K = comp(col, s, p, q); done |= K
                        new = dict(col)
                        for x in K: new[x] = q if col[x] == p else p
                        yield frozenset(K), (p, q), new

    def radius(col):
        start = canon(col); dist = {start: 0}; q = deque([(col, 0)])
        while q:
            c, d = q.popleft()
            if len({c[x] for x in L}) <= 3: return d
            for _, _, t in swaps(c):
                k = canon(t)
                if k not in dist: dist[k] = d + 1; q.append((t, d + 1))
        return None   # class exhausted, no fill

    j = frame(col0); out['frame_j'] = j; out['frame_j_claimed'] = ex.get('frame_j')
    out['link'] = L; out['link_colours'] = [col0[x] for x in L]
    out['doubly_locked'] = dl(col0); out['radius'] = radius(col0); out['radius_claimed'] = ex.get('state_dist')
    if j is None or not out['doubly_locked']:
        out['pass'] = False; print(json.dumps(out, indent=1, default=str)); return
    m, a, b = L[(j + 1) % 5], L[(j + 3) % 5], L[(j + 4) % 5]
    xj, xj2 = L[j], L[(j + 2) % 5]

    # lock paths (shortest) and uniqueness, then the discs
    def shortest_paths(col, s, t, p, q):
        dist = {s: 0}; preds = {s: []}; dq = deque([s])
        while dq:
            x = dq.popleft()
            for y in adj[x]:
                if y == h or col[y] not in (p, q): continue
                if y not in dist: dist[y] = dist[x] + 1; preds[y] = [x]; dq.append(y)
                elif dist[y] == dist[x] + 1: preds[y].append(x)
        cnt = {s: 1}
        for x in sorted(dist, key=dist.get):
            if x != s: cnt[x] = sum(cnt[z] for z in preds[x])
        path = [t]
        while path[-1] != s: path.append(preds[path[-1]][0])
        return path[::-1], cnt.get(t, 0)

    def side(block, start):
        seen = {start}; st = [start]
        while st:
            x = st.pop()
            for y in adj[x]:
                if y != h and y not in block and y not in seen:
                    seen.add(y); st.append(y)
        return seen

    P1, n1 = shortest_paths(col0, m, a, col0[m], col0[a])
    P2, n2 = shortest_paths(col0, m, b, col0[m], col0[b])
    D1 = side(set(P1), xj2); D2 = side(set(P2), xj)
    K1 = comp(col0, m, col0[m], col0[a]); K2 = comp(col0, m, col0[m], col0[b])
    E = lambda S: sum(1 for u in S for w in adj[u] if w in S and w != h) // 2
    out['lock1_path'] = P1; out['lock1_shortest_paths'] = n1; out['lock1_chain_is_tree'] = E(K1) == len(K1) - 1
    out['lock2_path'] = P2; out['lock2_shortest_paths'] = n2; out['lock2_chain_is_tree'] = E(K2) == len(K2) - 1
    Kc = set(comp_claim)
    out['component_in_D1'] = Kc <= D1 and not (Kc & set(P1))

    def all_shortest(col, s0, t0, p, q):
        dist = {s0: 0}; dq = deque([s0])
        while dq:
            x = dq.popleft()
            for y in adj[x]:
                if y != h and col[y] in (p, q) and y not in dist: dist[y] = dist[x] + 1; dq.append(y)
        res = []
        def back(path):
            x = path[-1]
            if x == s0: res.append(path[::-1]); return
            for y in adj[x]:
                if y in dist and dist[y] == dist[x] - 1: back(path + [y])
        back([t0]); return res
    out['D1_membership_per_lock1_path'] = [dict(path=P, inside=(Kc <= side(set(P), xj2) and not (Kc & set(P))))
                                           for P in all_shortest(col0, m, a, col0[m], col0[a])]
    out['D2_membership_per_lock2_path'] = [dict(path=P, inside=(Kc <= side(set(P), xj) and not (Kc & set(P))))
                                           for P in all_shortest(col0, m, b, col0[m], col0[b])]
    out['component_in_D2'] = Kc <= D2 and not (Kc & set(P2))
    out['component_meets_link'] = bool(Kc & set(L))
    out['component_meets_lock_paths'] = bool(Kc & (set(P1) | set(P2)))
    out['component_meets_lock_chains'] = bool(Kc & (K1 | K2))

    # the first move: find every swap of s whose component equals the claimed one
    firsts = []
    for K, pq, t in swaps(col0):
        if sorted(K) == comp_claim:
            firsts.append(dict(pair=pq, after_DL=dl(t), after_frame=frame(t), after_radius=radius(t)))
    out['first_moves'] = firsts
    # Intern A mechanism hypotheses
    role = {'a': col0[xj], 'b': col0[m], 'g': col0[a], 'd': col0[b]}
    w = lambda u, v: [z for z in adj[u] & adj[v] if z != h]
    x1, x2, x3 = L[(j + 1) % 5], L[(j + 2) % 5], L[(j + 3) % 5]
    w1 = w(x1, x2); w2 = w(x2, x3)
    out['internA'] = dict(roles=role, x2_degree=len(adj[x2]), w1=w1, w1_colours=[col0[z] for z in w1],
                          w2=w2, w2_colours=[col0[z] for z in w2],
                          component_is_bd_component_of_w2=any(set(comp(col0, z, role['b'], role['d'])) == Kc for z in w2
                                                              if col0[z] in (role['b'], role['d'])))
    out['pass'] = bool(out['covers'] and out['proper'] and out['hole_degree'] == 5 and out['doubly_locked']
                       and out['radius'] == 3 and out['component_in_D1'] and not out['component_meets_link']
                       and any(f['after_DL'] and f['after_radius'] == 2 for f in firsts))
    print(json.dumps(out, indent=1, default=str))


if __name__ == '__main__':
    main()
