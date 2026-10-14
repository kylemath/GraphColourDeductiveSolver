"""Verify the exact discrete Gauss-Bonnet identity for BFS balls B_r around a hole:
     C(r) = 12 - 6 k_r + 2 L_r - X_r
   C(r) = sum_{d(v)<=r} (6 - deg v); k_r = # non-triangular faces of the induced plane graph on B_r ("holes" of the ball);
   L_r = total boundary-walk length of those faces; X_r = # edges from S_r to S_{r+1}.
   Clean case (k_r = 1, boundary a chordless simple cycle, L_r = |S_r|, X_r = |S_r| + |S_{r+1}|):
     |S_{r+1}| - |S_r| = 6 - C(r).
Usage: gb.py STEP  (every STEP-th hole of orders 28-33)."""
import sys, collections, os, random
W = os.path.expanduser('~/GraphColour/SolvingFrameworkPlan/docs/working/')
STEP = int(sys.argv[1])
def graphs():
    for o in range(28, 34):
        src = W + ('Census33/out/frame-33.txt' if o == 33 else 'Census29/out/frame-%d.txt' % o)
        for l in open(src):
            p = l.split(); yield o, p[0], [[int(x) for x in r.split(',')] for r in p[2].split(';')]
fail = 0; tot = 0; clean = collections.Counter(); allr = collections.Counter(); resid = collections.Counter()
kdist = collections.Counter(); cnt = 0
for o, g, rot in graphs():
    n = len(rot); deg = [len(x) for x in rot]
    pos = [{w: i for i, w in enumerate(r)} for r in rot]
    tri = set()
    for u in range(n):
        for i, v in enumerate(rot[u]):
            w = rot[u][(i + 1) % deg[u]]; tri.add(frozenset((u, v, w)))
    for h in range(n):
        if deg[h] != 5: continue
        cnt += 1
        if cnt % STEP: continue
        d = [-1] * n; d[h] = 0; q = collections.deque([h])
        while q:
            u = q.popleft()
            for w in rot[u]:
                if d[w] < 0: d[w] = d[u] + 1; q.append(w)
        ecc = max(d); S = collections.Counter(d)
        for r in range(1, ecc + 1):
            B = [v for v in range(n) if d[v] <= r]; inB = [d[v] <= r for v in range(n)]
            C = sum(6 - deg[v] for v in B)
            X = sum(1 for v in B if d[v] == r for w in rot[v] if d[w] == r + 1)
            # face tracing on induced subgraph
            seen = set(); k = 0; L = 0; f = 0; E = 0
            for u in B:
                for v in rot[u]:
                    if inB[v]: E += 1
            E //= 2
            for u in B:
                for v in rot[u]:
                    if not inB[v] or (u, v) in seen: continue
                    walk = []; a, b = u, v
                    while (a, b) not in seen:
                        seen.add((a, b)); walk.append(a)
                        i = pos[b][a]; j = i
                        while True:
                            j = (j - 1) % deg[b]
                            if inB[rot[b][j]]: break
                        a, b = b, rot[b][j]
                    f += 1
                    if not (len(walk) == 3 and frozenset(walk) in tri): k += 1; L += len(walk)
            tot += 1
            ok = (C == 12 - 6 * k + 2 * L - X) and (len(B) - E + f == 2)
            fail += not ok
            kdist[k] += 1
            if r < ecc:
                gr = (S[r + 1] - S[r]) - (6 - C)
                allr[r] += 1; resid[(r, gr)] += 1
                if k == 1 and L == S[r] and X == S[r] + S[r + 1]: clean[r] += 1
print('balls checked', tot, 'identity failures', fail)
print('k (non-triangular faces) distribution', dict(kdist))
for r in sorted(allr):
    rs = {g: c for (rr, g), c in resid.items() if rr == r}
    print('r=%d balls %d clean %.4f  growth residual (|S_r+1|-|S_r|)-(6-C(r)) distribution %s' % (r, allr[r], clean[r] / allr[r], dict(sorted(rs.items()))))
