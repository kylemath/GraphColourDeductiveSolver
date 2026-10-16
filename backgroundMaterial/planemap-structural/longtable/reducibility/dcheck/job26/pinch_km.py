"""Job 26, B2 brute-force test (exploratory): does R2's KempeMatching hold for a PINCHED ring?
Outside map G' = A ∪_u B (two triangulated discs sharing the vertex u); the configuration's face walk is
u, A's boundary, u, B's boundary (u at two ring positions).  P = ring codes of all proper 4-colourings of G'
(colours = 2-bit values, as in DCheck).  KempeMatching (DCheckSound.lean): for every k in P and theta in {1,2,3} with
transitions, SOME non-crossing perfect matching of the transitions has every union of its regions flippable
(XOR theta on the region's ring positions) inside P.  matchTable is complete (R1), so we enumerate all matchings.
Also run on unpinched controls (one disc with the same ring length).  Usage: python3 pinch_km.py"""
import itertools, sys

def disc(m, kind):
    """Triangulated disc with boundary cycle 0..m-1 (in order) plus interior vertices; returns (nverts, edges)."""
    E = {(i, (i + 1) % m) for i in range(m)}
    if kind == 'wheel':                      # one interior vertex m adjacent to all
        E |= {(i, m) for i in range(m)}; return m + 1, E
    if kind == 'two':                        # m = 5: x1 = 5 on c0,c1,c2; x2 = 6 on c2,c3,c4,c0; x1-x2
        E |= {(0, 5), (1, 5), (2, 5), (2, 6), (3, 6), (4, 6), (0, 6), (5, 6)}; return 7, E
    if kind == 'fan':                        # chords from boundary vertex 0 (no interior)
        E |= {(0, i) for i in range(2, m - 1)}; return m, E
    raise ValueError(kind)

def pinched(mA, kA, mB, kB):
    """Glue disc A (boundary a_0 = u, a_1..) and disc B (boundary b_0 = u, ..) at u.  Ring walk: u, a_1..a_{mA-1}, u, b_1.."""
    nA, EA = disc(mA, kA); nB, EB = disc(mB, kB)
    mapB = {0: 0}; nxt = nA
    for v in range(1, nB): mapB[v] = nxt; nxt += 1
    E = set(EA) | {(mapB[a], mapB[b]) for a, b in EB}
    ring = list(range(mA)) + [0] + [mapB[v] for v in range(1, mB)]
    return nxt, E, ring

def simple(m, kind):
    n, E = disc(m, kind); return n, E, list(range(m))

def codes(n, E, ring):
    adj = [[] for _ in range(n)]
    for a, b in E: adj[a].append(b); adj[b].append(a)
    P = set(); col = [0] * n
    def go(v):
        if v == n:
            k = 0
            for i, x in enumerate(ring): k |= col[x] << (2 * i)
            P.add(k); return
        for c in range(4):
            if all(col[w] != c for w in adj[v] if w < v): col[v] = c; go(v + 1)
    go(0); return P

def colof(k, i): return (k >> (2 * i)) & 3
def transitions(r, k, th):
    return [v for v in range(r) if (lambda x: x != 0 and x != th)(colof(k, v) ^ colof(k, (v + 1) % r))]
def matchings(pts):
    if not pts: yield []; return
    a = pts[0]
    for j in range(1, len(pts), 2):          # partner must leave an even number on each side (non-crossing)
        for L in matchings(pts[1:j]):
            for R in matchings(pts[j + 1:]): yield [(a, pts[j])] + L + R
def regions(r, T, M):
    """arcs j = ring positions after transition T[j] up to T[j+1]; region = orbit of arc j -> arc at partner(T[j+1])."""
    n = len(T); idx = {t: i for i, t in enumerate(T)}; part = {}
    for a, b in M: part[a] = b; part[b] = a
    seen = [-1] * n; regs = []
    for j in range(n):
        if seen[j] >= 0: continue
        cur = j; R = []
        while seen[cur] < 0:
            seen[cur] = len(regs); R.append(cur); cur = idx[part[T[(cur + 1) % n]]]
        regs.append(R)
    pos = []
    for R in regs:
        ps = []
        for j in R:
            v = (T[j] + 1) % r
            while True:
                ps.append(v)
                if v == T[(j + 1) % n]: break
                v = (v + 1) % r
        pos.append(ps)
    return pos

def km(r, P):
    bad = 0; tot = 0
    for k in P:
        for th in (1, 2, 3):
            T = transitions(r, k, th)
            if not T: continue
            tot += 1; ok = False
            for M in matchings(T):
                regs = regions(r, T, M)
                masks = [sum(th << (2 * v) for v in ps) for ps in regs]
                if all((k ^ sum(masks[i] for i in range(len(masks)) if s >> i & 1)) in P for s in range(1 << len(masks))):
                    ok = True; break
            if not ok: bad += 1
    return tot, bad

cases = [('simple 6 wheel', simple(6, 'wheel')), ('simple 8 wheel', simple(8, 'wheel')),
         ('pinch 4w+4w (ring 8)', pinched(4, 'wheel', 4, 'wheel')), ('pinch 3f+5w (ring 8)', pinched(3, 'fan', 5, 'wheel')),
         ('pinch 5two+4w (ring 9)', pinched(5, 'two', 4, 'wheel')), ('pinch 5two+5two (ring 10)', pinched(5, 'two', 5, 'two')),
         ('pinch 4f+4f (ring 8, no interior)', pinched(4, 'fan', 4, 'fan'))]
for name, (n, E, ring) in cases:
    P = codes(n, E, ring); tot, bad = km(len(ring), P)
    print('%-34s n=%2d ring=%2d realised codes %6d  (k,theta) with transitions %7d  KempeMatching fails %d' % (name, n, len(ring), len(P), tot, bad), flush=True)
# negative control: ring 6 with two crossing chords outside (not planar with the ring as a face): must fail somewhere
n, E, ring = 6, {(i, (i + 1) % 6) for i in range(6)} | {(0, 3), (1, 4)}, list(range(6))
P = codes(n, E, ring); tot, bad = km(6, P)
print('%-34s n=%2d ring=%2d realised codes %6d  (k,theta) with transitions %7d  KempeMatching fails %d' % ('CONTROL crossing chords (nonplanar)', n, 6, len(P), tot, bad))
n, E, ring = 8, {(i, (i + 1) % 8) for i in range(8)} | {(0, 4), (2, 6)}, list(range(8))
P = codes(n, E, ring); tot, bad = km(8, P)
print('%-34s n=%2d ring=%2d realised codes %6d  (k,theta) with transitions %7d  KempeMatching fails %d' % ('CONTROL crossing chords 8', n, 8, len(P), tot, bad))
