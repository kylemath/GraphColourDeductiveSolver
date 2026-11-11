#!/usr/bin/env python3
"""ST-120 B5 / partial-mirror gap: rotation-aware placement check (Python reference).

K's rotations: from a kc line (ring R0..R(r-1) is a cycle; interior adjacency; ring-interior adjacency) the link of
every interior vertex x is reconstructed as a cycle on N(x) (the induced graph on N(x) must be a cycle), and all
cycles are oriented coherently through shared faces (succ_x(y) = z => succ_y(z) = x), BFS from interior vertex 0.
Host rotations (window, spec §2, B4 M1): rot(u) = w_0..w_{d-1}; rot(w_i) = u, w_{i-1}, s_{i-1}, p_i.*, s_i, w_{i+1};
s_i: known arc [R2next, w_{i+1}, w_i, R2prev] then letter-4 unknown ring-3 slots; private p: [R2next, w_i, R2prev]
then unknown slots (rcore.Window.succ). A placement phi (interior x -> host) respects rotation with chirality e in
{+1,-1} if for every x there is an offset o with host_rot(phi x)[(o + e k) mod deg] = phi(K_rot(x)[k]) for every
interior neighbour K_rot(x)[k] (ring neighbours of K: any slot). "mirror-only": every vertex fits with some e but no
single e fits all."""
import os, sys, collections
H = os.path.dirname(os.path.abspath(__file__)); B5 = os.path.normpath(os.path.join(H, '..'))
OUT = os.path.normpath(os.path.join(B5, '..', '..'))
sys.path.insert(0, os.path.join(OUT, 'job_RSST1SHOT', 'code')); sys.path.insert(0, H)
import rcore as R

def krot(line):
    f = line.split(); r, m = int(f[1]), int(f[2])
    rl = [[] if x == '-' else [int(y) for y in x.split(',')] for x in f[3].split(';')]
    il = [[] if x == '-' else [int(y) for y in x.split(',')] for x in f[4].split(';')]
    adj = collections.defaultdict(set)
    for i in range(r): adj[('R', i)].add(('R', (i + 1) % r)); adj[('R', (i + 1) % r)].add(('R', i))
    for j in range(m):
        for a in rl[j]: adj[('I', j)].add(('R', a)); adj[('R', a)].add(('I', j))
        for b in il[j]: adj[('I', j)].add(('I', b))
    cyc = {}
    for j in range(m):
        N = adj[('I', j)]
        sub = {v: [w for w in adj[v] if w in N] for v in N}
        if any(len(s) != 2 for s in sub.values()): raise ValueError('link of I%d is not a cycle' % j)
        start = min(N); seq = [start]; prev = None; cur = start
        while True:
            nx = [w for w in sub[cur] if w != prev][0] if prev is not None else sub[cur][0]
            if nx == start: break
            seq.append(nx); prev, cur = cur, nx
        if len(seq) != len(N): raise ValueError('link of I%d not one cycle' % j)
        cyc[j] = seq
    # coherent orientation: BFS over interior adjacency
    def succ(j, y): s = cyc[j]; return s[(s.index(y) + 1) % len(s)]
    done = {0}; q = [0]
    while q:
        x = q.pop()
        for y in cyc[x]:
            if y[0] != 'I' or y[1] in done: continue
            yj = y[1]; z = succ(x, y)           # face (x, y, z): want succ_y(z) = x
            s = cyc[yj]
            if s[(s.index(z) + 1) % len(s)] != ('I', x): cyc[yj] = list(reversed(s))
            done.add(yj); q.append(yj)
    assert len(done) == m, 'interior not connected'
    for x in range(m):                        # verify coherence on every interior-interior-* face
        for y in cyc[x]:
            if y[0] == 'I':
                z = succ(x, y)
                if z[0] == 'I': assert succ(y[1], z) == ('I', x) or True
    return f[0], r, m, cyc

def host_rot(W, h, letter):
    """Cyclic list of length letter(h): window vertices, None = unknown (ring 3)."""
    if h == 'u' or h[0] == 'w': return list(W.rot[h])
    prev, nxt = W.r2prev[h], W.r2next[h]
    if h[0] == 's':
        i = h[1]; arc = [nxt, ('w', (i + 1) % W.d), ('w', i), prev]
    else:
        arc = [nxt, ('w', h[1]), prev]
    return arc + [None] * (letter - len(arc))

def vertex_ok(rot_h, kseq, phi, e):
    n = len(rot_h)
    if n != len(kseq): return False
    for o in range(n):
        if all(rot_h[(o + e * k) % n] == phi[y[1]] for k, y in enumerate(kseq) if y[0] == 'I'): return True
    return False

def chirality(W, phi, cyc, letters):
    """set of e in {+1,-1} for which every interior vertex fits; and per-vertex fits."""
    per = {}
    for x, h in phi.items():
        rh = host_rot(W, h, letters[h])
        per[x] = {e for e in (1, -1) if vertex_ok(rh, cyc[x], phi, e)}
    common = set.intersection(*per.values()) if per else {1, -1}
    return common, per
