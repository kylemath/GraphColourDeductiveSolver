"""[exploratory] Birkhoff diamond / RSST 2.122 detection on a rotation system (definitions: audit msg 2026-10-06_1516 sec 3-4).
Diamond: centres q,r adjacent, tips p,s, p-q-r and q-r-s faces, p,s non-adjacent, all four degree 5.
2.122: same shape, one centre degree 6, other centre and both tips degree 5."""
def faces_of(rot):
    return {frozenset((v, nb[i], nb[(i + 1) % len(nb)])) for v, nb in enumerate(rot) for i in range(len(nb))}
def configs(rot):
    adj = [set(nb) for nb in rot]; F = faces_of(rot); deg = [len(nb) for nb in rot]
    out = []  # (kind, centres(h,c), tips)
    for q in range(len(rot)):
        for r in rot[q]:
            if r < q: continue
            tips = [x for x in rot[q] if x in adj[r] and frozenset((q, r, x)) in F]
            if len(tips) != 2: continue
            p, s = tips
            if s in adj[p] or deg[p] != 5 or deg[s] != 5: continue
            dq, dr = deg[q], deg[r]
            if dq == 5 and dr == 5: out.append(('diamond', (q, r), (p, s)))
            elif (dq, dr) == (6, 5): out.append(('2.122', (q, r), (p, s)))
            elif (dq, dr) == (5, 6): out.append(('2.122', (r, q), (p, s)))
    return out
def cfree(rot): return not configs(rot)
def dist_to(rot, v, S):
    from collections import deque
    d = {v: 0}; Q = deque([v])
    while Q:
        u = Q.popleft()
        if u in S: return d[u]
        for w in rot[u]:
            if w not in d: d[w] = d[u] + 1; Q.append(w)
