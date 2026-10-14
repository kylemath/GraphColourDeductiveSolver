"""Mechanism test: curvature (charge Q = sum(6-deg)) inside the lock chains at doubly locked (DL) states.
Usage: mech.py SAMPLEFILE OUT.jsonl   (SAMPLEFILE lines: name hole; graphs from Census33 frame-33.txt)
Per DL state k (frame x0..x4 = alpha beta alpha gamma delta; TrackF: x_j..x_{j+4} = alpha mu alpha A B):
  KA = {alpha,gamma}-chain of x2 (= the pi swap chain, TrackF K_{alpha A}(x_{j+2})); KB = {alpha,delta}-chain of x2;
  Kmu = {alpha,beta}-chain of x2; L1 = {beta,gamma}-chain x1..x3; L2 = {beta,delta}-chain x1..x4 (the two locks).
  For each: size, Q, #deg-5, #deg>=7, mean BFS distance from the hole, distance of its nearest positive charge.
Outcomes: dF (swaps to fill), fwd = #consecutive DL states along pi from k, cont = pi(k) is DL.
Also, for every unfilled state, the parity check Lock_i <-> Q(chain) odd."""
import sys, os, json, collections, time
sys.path.insert(0, os.path.expanduser('~/4square'))
from kempe_engine import HoleGame
W = os.path.expanduser('~/GraphColour/SolvingFrameworkPlan/docs/working/')
want = collections.defaultdict(list)
for l in open(sys.argv[1]):
    g, h = l.split()[:2]; want[g].append(int(h))
out = open(sys.argv[2], 'w')
src = W + 'Census33/out/frame-33.txt'
for l in open(src):
    p = l.split()
    if p[0] not in want: continue
    rot = [[int(x) for x in r.split(',')] for r in p[2].split(';')]; n = len(rot); deg = [len(r) for r in rot]
    for h in want[p[0]]:
        t0 = time.time()
        d = [-1] * n; d[h] = 0; q = collections.deque([h])
        while q:
            u = q.popleft()
            for w in rot[u]:
                if d[w] < 0: d[w] = d[u] + 1; q.append(w)
        H = HoleGame(n, rot, h, rot[h])
        def desc(X):
            pos = [d[v] for v in X if deg[v] == 5]
            return [len(X), sum(6 - deg[v] for v in X), len(pos), sum(deg[v] > 6 for v in X),
                    round(sum(d[v] for v in X) / len(X), 3), min(pos) if pos else -1]
        par = collections.Counter(); rows = []
        # forward DL run lengths along pi (memo)
        fwd = {}
        def F(k):
            path = []; kk = k
            while kk is not None and H.dl[kk] and kk not in fwd and kk not in path:
                path.append(kk); kk = H.pi[kk]
            base = fwd.get(kk, 0) if kk is not None and H.dl[kk] and kk in fwd else (10**6 if kk in path else 0)
            for x in reversed(path):
                base = base + 1 if base < 10**6 else base; fwd[x] = base
            return fwd[k]
        for k, c in enumerate(H.states):
            if H.filled[k]: continue
            x, al, be, ga, de = H.frame(c)
            KA = H.chain_at(c, x[2], ga); KB = H.chain_at(c, x[2], de)
            qa = sum(6 - deg[v] for v in KA) % 2; qb = sum(6 - deg[v] for v in KB) % 2
            par[(H.L1[k], H.L2[k], qa, qb)] += 1
            if not H.dl[k]: continue
            Km = H.chain_at(c, x[2], be); L1 = H.chain_at(c, x[1], ga); L2 = H.chain_at(c, x[1], de)
            nk = H.pi[k]
            rows.append([H.dF[k], F(k), int(H.dl[nk]), H.locks(nk), H.N[k], desc(KA), desc(KB), desc(Km), desc(L1), desc(L2)])
        out.write(json.dumps({'g': p[0], 'h': h, 'S': H.S, 'nDL': len(rows), 'maxdF': max(H.dF),
                              'par': [[*map(int, kk), v] for kk, v in par.items()], 'dl': rows, 't': round(time.time() - t0, 1)}) + '\n')
        out.flush()
