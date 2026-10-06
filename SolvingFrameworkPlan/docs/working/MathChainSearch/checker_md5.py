#!/usr/bin/env python3
"""Checker for the min-degree-5 search (copy of checker.py; chain logic unchanged; adds graph-property report: min degree, 4-/5-connectivity). Does not import the searcher.
Independent checker for F-chains (Conjecture L search). [computed, exploratory]
Written from the pre-registration message and MathCleanVertexAttack/MathConfinementAttack definitions only.
Input: JSON certificate {n, v, link, rot:{vertex:[cyclic neighbour order]}, colour:[...], claimed_length}.
Verdict: ACCEPT (all structure valid and recomputed chain length == claimed) or REJECT with reason.
Usage: checker.py cert.json [--print]
"""
import json, sys
from collections import deque

CHAIN_CAP = 40

def check_triangulation(n, rot):
    """rot: dict int -> list of neighbours in cyclic order. Verify it is a planar triangulation (simple, sphere, all faces triangles)."""
    if sorted(rot) != list(range(n)): return 'vertex set is not 0..n-1'
    for u, ns in rot.items():
        if len(ns) != len(set(ns)): return 'repeated neighbour at %d' % u
        if u in ns: return 'loop at %d' % u
        for w in ns:
            if u not in rot.get(w, []): return 'asymmetric edge %d-%d' % (u, w)
    E = sum(len(ns) for ns in rot.values()) // 2
    if E != 3 * n - 6: return 'edge count %d != 3n-6 = %d' % (E, 3 * n - 6)
    # faces = orbits of darts under (a,b) -> (b, successor of a in cyclic order at b)
    nxt = {}
    for u, ns in rot.items():
        for i, w in enumerate(ns): nxt[(u, w)] = ns[(i + 1) % len(ns)]
    seen = set(); F = 0
    for d in list(nxt):
        if d in seen: continue
        F += 1; a, b = d; length = 0
        while (a, b) not in seen:
            seen.add((a, b)); a, b = b, nxt[(b, a)]; length += 1
        if length != 3: return 'face of length %d' % length
    if n - E + F != 2: return 'Euler characteristic %d != 2' % (n - E + F)
    return None

def is_cyclic_order_of(link, ns):
    k = len(ns)
    if len(link) != k or set(link) != set(ns): return False
    for dirn in (1, -1):
        for off in range(k):
            if all(ns[(off + dirn * i) % k] == link[i] for i in range(k)): return True
    return False

def two_colour_path(adj, col, src, dst, c1, c2):
    """Return a path src..dst using only vertices coloured c1/c2 (excluding v), or None."""
    prev = {src: None}; q = deque([src])
    while q:
        u = q.popleft()
        if u == dst:
            p = []
            while u is not None: p.append(u); u = prev[u]
            return p[::-1]
        for w in adj[u]:
            if w not in prev and col[w] in (c1, c2):
                prev[w] = u; q.append(w)
    return None

def swap_component(adj, col, s, c1, c2):
    comp = {s}; q = deque([s])
    while q:
        u = q.popleft()
        for w in adj[u]:
            if w not in comp and col[w] in (c1, c2): comp.add(w); q.append(w)
    new = dict(col)
    for u in comp: new[u] = c2 if col[u] == c1 else c1
    return new, comp

def link_state(col, link):
    cs = [col[x] for x in link]
    if len(set(cs)) != 4: return None
    reps = [j for j in range(5) if cs[j] == cs[(j + 2) % 5]]
    return reps[0] if len(reps) == 1 else None

def graph_props(n, rot):
    """min degree, number of separating triangles, 4-connected (no separating 3-cycle; triangulation with n>=5), 5-connected (no vertex cut of size <=4, brute force)."""
    from itertools import combinations
    adj = {u: set(ns) for u, ns in rot.items()}
    mind = min(len(a) for a in adj.values())
    faces = set()
    for u in adj:
        ns = rot[u]
        for i in range(len(ns)): faces.add(frozenset((u, ns[i], ns[(i + 1) % len(ns)])))
    sep3 = 0
    for u in adj:
        for w in adj[u]:
            if w > u:
                for x in adj[u] & adj[w]:
                    if x > w and frozenset((u, w, x)) not in faces: sep3 += 1
    def connected_without(rem):
        rest = [u for u in adj if u not in rem]
        seen = {rest[0]}; q = [rest[0]]
        while q:
            a = q.pop()
            for b in adj[a]:
                if b not in rem and b not in seen: seen.add(b); q.append(b)
        return len(seen) == len(rest)
    conn5 = all(connected_without(set(c)) for k in range(1, 5) for c in combinations(list(adj), k)) if n > 6 else None
    return dict(min_degree=mind, separating_triangles=sep3, four_connected=(sep3 == 0), five_connected=conn5)

def verify(cert):
    n, v, link = cert['n'], cert['v'], cert['link']
    rot = {int(u): list(ns) for u, ns in cert['rot'].items()}
    out = []
    msg = check_triangulation(n, rot)
    if msg: return False, 'bad triangulation: ' + msg, 0, out
    gp = graph_props(n, rot)
    out.append(dict(graph_properties=gp))
    if gp['min_degree'] < 5: return False, 'minimum degree %d < 5' % gp['min_degree'], 0, out
    if len(rot[v]) != 5: return False, 'v does not have degree 5', 0, out
    if not is_cyclic_order_of(link, rot[v]): return False, 'link is not the cyclic neighbour order of v', 0, out
    if len(cert['colour']) != n: return False, 'colour length', 0, out
    col = {u: cert['colour'][u] for u in range(n) if u != v}
    if any(c not in (0, 1, 2, 3) for c in col.values()): return False, 'colour out of range', 0, out
    adj = {u: [w for w in rot[u] if w != v] for u in col}
    for u in col:
        for w in adj[u]:
            if col[u] == col[w]: return False, 'improper colouring on edge %d-%d' % (u, w), 0, out
    if link_state(col, link) is None: return False, 'not a state: link does not use four colours with one repeat', 0, out
    L = 0; cur = col
    for step in range(CHAIN_CAP + 1):
        j = link_state(cur, link)
        if j is None:
            out.append(dict(step=step, note='state invalid (link not four-coloured); chain stops')); break
        x = [link[(j + i) % 5] for i in range(5)]   # x[0],x[2] repeat; x[1]=beta; x[3]=gamma; x[4]=delta
        beta, gamma, delta, alpha = cur[x[1]], cur[x[3]], cur[x[4]], cur[x[0]]
        p1 = two_colour_path(adj, cur, x[1], x[3], beta, gamma)
        p2 = two_colour_path(adj, cur, x[1], x[4], beta, delta)
        rec = dict(step=step, repeat_index=j, link_colours=[cur[y] for y in link], lock_beta_gamma=p1, lock_beta_delta=p2)
        out.append(rec)
        if p1 is None or p2 is None:
            rec['doubly_locked'] = False; break
        rec['doubly_locked'] = True; L += 1
        if L >= CHAIN_CAP: rec['note'] = 'cap reached'; break
        cur, K = swap_component(adj, cur, x[2], alpha, gamma)   # F: {c_j, c_{j+3}} component of x_{j+2}
        rec['F_swapped_component_size'] = len(K)
        rec['F_component_contains_xj'] = x[0] in K
    claimed = cert.get('claimed_length')
    if claimed is not None and claimed != L:
        return False, 'claimed length %s but recomputed %d' % (claimed, L), L, out
    return True, 'recomputed chain length %d equals claim' % L, L, out

def main():
    cert = json.load(open(sys.argv[1]))
    ok, msg, L, out = verify(cert)
    if '--print' in sys.argv:
        print('triangulation n=%d, v=%d, link=%s' % (cert['n'], cert['v'], cert['link']))
        print('rotation system:', json.dumps(cert['rot']))
        print('colouring:', cert['colour'])
        for r in out: print(json.dumps(r))
    print('graph properties:', json.dumps([r for r in out if 'graph_properties' in r][0]['graph_properties']))
    print(('ACCEPT' if ok else 'REJECT'), '| chain length', L, '|', msg)
    sys.exit(0 if ok else 1)

if __name__ == '__main__':
    main()
