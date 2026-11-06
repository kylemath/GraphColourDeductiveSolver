"""ROT (Studio, 6 Nov; claim ST-8): rotation-preserving test for an embedding found by grow.embeddings (which matches
exact degrees, induced adjacency and interior triangles onto faces only, grow.py:104-124).

An embedding phi of configuration K (interior I, ring R) into a frame is ROTATION-PRESERVING iff there is one global
sign sigma in {+1, -1} and, for every interior vertex u, a shift t_u with
    rot_frame(phi(u))[(t_u + sigma * i) mod g(u)] = phi(n_i)   for every interior neighbour n_i = rot_K(u)[i],
and the ring neighbours of the interior vertices then receive one consistent frame vertex each (a ring vertex seen from
two interior vertices maps to the same frame vertex).  rot_K and rot_frame are consistently oriented rotation systems.

rot_K: RSST configurations from unavoidable.conf (neighbour lists in cyclic order, ring = 1..r); kc lines
"name r m ringadj intadj" from the link cycle of each interior vertex in the near-triangulation (ring cycle 0..r-1,
ring-interior and interior-interior edges), oriented by the ring direction and propagated over interior edges.
rot_frame: grow.build2 rebuilt with the requirement set's own letters (w_k, s_k, w_0's slot; unpinned w_k get 5 / 6
from the structure Z, unpinned ring-2 vertices 9), so every image has its true degree; rotations from the faces,
oriented by propagation from u.  Our own code only."""
import collections

def _cycle(nbrs, adj):
    """order the set nbrs into the cycle given by adjacency among them; None if it is not a single simple cycle."""
    nb = list(nbrs)
    if len(nb) < 3: return None
    L = {x: [y for y in nb if y != x and y in adj[x]] for x in nb}
    if any(len(v) != 2 for v in L.values()): return None
    cyc = [nb[0], L[nb[0]][0]]
    while len(cyc) < len(nb):
        a, b = L[cyc[-1]]; nx = a if a != cyc[-2] else b
        if nx == cyc[0]: return None
        cyc.append(nx)
    return cyc if cyc[0] in L[cyc[-1]] else None

def _orient(rot, edges_order):
    """make rotations consistent: for interior u, v adjacent with w = next_u(v) we need next_v(w) = u."""
    nxt = lambda R, x: R[(R.index(x) + 1) % len(R)]
    done = set(); bad = 0
    for s in edges_order:
        if s in done or s not in rot: continue
        done.add(s); Q = collections.deque([s])
        while Q:
            u = Q.popleft()
            for v in rot[u]:
                if v not in rot: continue
                w = nxt(rot[u], v)
                if v in done:
                    if w in rot[v] and nxt(rot[v], w) != u: bad += 1
                    continue
                if w in rot[v] and nxt(rot[v], w) != u: rot[v] = rot[v][::-1]
                done.add(v); Q.append(v)
    return bad

def kc_rotation(line):
    f = line.split(); r, m = int(f[1]), int(f[2]); rp = f[3].split(';'); ip = f[4].split(';')
    I = [('I', u) for u in range(m)]; adj = collections.defaultdict(set)
    for j in range(r):
        a, b = ('R', j), ('R', (j + 1) % r); adj[a].add(b); adj[b].add(a)
    for u in range(m):
        for j in ([] if rp[u] == '-' else map(int, rp[u].split(','))): adj[('I', u)].add(('R', j)); adj[('R', j)].add(('I', u))
        for w in ([] if ip[u] == '-' else map(int, ip[u].split(','))): adj[('I', u)].add(('I', w)); adj[('I', w)].add(('I', u))
    rot = {}
    for u in I:
        c = _cycle(adj[u], adj)
        if c is None: return None
        rot[u] = c
    # orientation from the ring direction: where u sees ring j and j+1 consecutively, require R_{j+1} right after R_j
    for u in I:
        R_ = rot[u]
        for k in range(len(R_)):
            a, b = R_[k], R_[(k + 1) % len(R_)]
            if a[0] == 'R' and b[0] == 'R':
                if (b[1] - a[1]) % r == r - 1: rot[u] = R_[::-1]
                break
    seeds = [u for u in I if any(x[0] == 'R' for x in rot[u])] + I
    if _orient(rot, seeds): return None
    return {u[1]: [('I', x[1]) if x[0] == 'I' else ('R', x[1]) for x in rot[u]] for u in I}

def rsst_rotations(conf):
    out = []; lines = open(conf).read().split('\n'); i = 0
    while i < len(lines):
        if not lines[i].strip(): i += 1; continue
        f = lines[i + 1].split(); n, r = int(f[0]), int(f[1]); i += 3; nb = {}
        for _ in range(n):
            g = lines[i].split(); nb[int(g[0])] = [int(x) for x in g[2:]]; i += 1
        while i < len(lines) and lines[i].strip(): i += 1
        rot = {u: [('I', w) if w > r else ('R', w) for w in nb[u]] for u in range(r + 1, n + 1)}
        out.append(('rsst%03d' % len(out), rot))
    return out

def frame_rotation(G, D, LK, SV, r2):
    G['D'] = D; G['LK'] = list(LK); G['SV'] = dict(SV)
    adj, name, faces = G['build2'](r2)
    inv = {x: v for v, x in name.items()}
    fa = collections.defaultdict(list)
    for t in faces:
        for v in t: fa[v].append(t)
    rot = {}
    for v in name:   # named vertices are within distance 2 of u: full links
        nb = adj[v]; c = _cycle(nb, {x: {y for y in adj[x] if frozenset((v, x, y)) in faces} for x in nb})
        if c is not None: rot[v] = c
    _orient(rot, [inv[('u',)]] + list(rot))
    return adj, name, inv, rot

def rot_ok(phi, rotK, frm):
    """phi: cfg interior vertex -> frame vertex id; rotK: {u: cyclic list of ('I', w) / ('R', j)}; frm from frame_rotation."""
    adj, name, inv, rotF = frm
    for sg in (1, -1):
        ring = {}; ok = True
        order = sorted(phi, key=lambda u: -sum(x[0] == 'I' for x in rotK[u]))
        for u in order:
            rc = rotK[u]; v = phi[u]
            if v not in rotF or len(rotF[v]) != len(rc): ok = False; break
            rf = rotF[v]; g = len(rc); intr = [(i, x[1]) for i, x in enumerate(rc) if x[0] == 'I']
            shifts = [(rf.index(phi[intr[0][1]]) - sg * intr[0][0]) % g] if intr and phi[intr[0][1]] in rf else ([] if intr else range(g))
            found = False
            for t in shifts:
                if any(rf[(t + sg * i) % g] != phi[w] for i, w in intr): continue
                cand = {x[1]: rf[(t + sg * i) % g] for i, x in enumerate(rc) if x[0] == 'R'}
                if any(ring.get(j, fv) != fv for j, fv in cand.items()): continue
                ring.update(cand); found = True; break
            if not found: ok = False; break
        if ok: return True
    return False
