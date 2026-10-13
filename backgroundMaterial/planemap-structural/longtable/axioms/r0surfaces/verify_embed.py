"""Explicit, independently checkable witnesses that R0 fails off the sphere (Long Table, r0surfaces).

For a labelled graph line (TrackU format: n m edges f0..f4) this script
 (1) finds an explicit closed R0 sequence M_0..M_{L-1} (closed walk through the Hamiltonian arc M_0 -> M_1)
     and checks it with ax_lib.G5 (perfect matchings, consecutive disjointness, frames k_t = 2 - 2t,
     M_0 u M_1 Hamiltonian); optionally the V2 condition (every M_{2j} u M_{2j+1} Hamiltonian);
 (2) finds by brute force (pure Python, independent of genus.c) a signed rotation system with the rotation
     (f0 f1 f2 f3 f4) at v and the requested surface (RP2: non-orientable, chi = 1; T2: orientable, chi = 0);
 (3) re-checks the embedding from its FACE LIST ALONE (polygon gluing): every edge used exactly twice, the
     corners at every vertex form one cycle (closed surface, G cellular), the cyclic order read off at v is
     f0..f4 up to reversal, chi = V - E + F, orientability by a face-orientation 2-colouring.
usage: verify_embed.py 'line' L [RP2|T2|both|given] [--v2] [--v3] [--tw HEX]  (--tw: check the embedding with
       canonical rotations and this twist vector, as printed by egheur)"""
import sys, itertools
from collections import deque
sys.path.insert(0, '..')
from ax_lib import G5, parse_line

line, L = sys.argv[1], int(sys.argv[2]); which = sys.argv[3] if len(sys.argv) > 3 else 'both'
n, E, fv = parse_line(line); g = G5(n, E, fv); m = len(E); v = g.v
other = lambda e, x: E[e][1] if E[e][0] == x else E[e][0]

# ---------- (1) explicit closed R0 sequence ----------
P = [frozenset(p) for p in g.pms()]
idx = {p: i for i, p in enumerate(P)}
k = [g.kidx(p) for p in P]
arc = [[j for j, q in enumerate(P) if not (P[i] & q) and k[j] == (k[i] - 2) % 5] for i in range(len(P))]
M0 = frozenset(e for e, (a, b) in enumerate(E[:n]) if e % 2 == 0)
M1 = frozenset(e for e, (a, b) in enumerate(E[:n]) if e % 2 == 1)
i0, i1 = idx[M0], idx[M1]
ham = lambda i, j: g.ncomp(P[i] | P[j]) == 1
v2 = '--v2' in sys.argv or '--v3' in sys.argv; v3 = '--v3' in sys.argv
# layered search for a walk M_1 = W_1, ..., W_{L-1}, W_L = M_0 (with V2: W_{2j} -> W_{2j+1} Hamiltonian)
layers = [{i1: None}]
for t in range(2, L + 1):
    nxt = {}
    for i in layers[-1]:
        for j in arc[i]:
            if v2 and (t - 1) % 2 == 0 and not ham(i, j): continue   # pair (W_{t-1}, W_t), t-1 even
            if v3 and (t - 1) % 2 == 1 and g.ncomp(P[i] | P[j]) != 2: continue
            if j not in nxt: nxt[j] = i
    layers.append(nxt)
assert i0 in layers[-1], 'no closed walk of this length'
walk = [i0]
for t in range(L - 1, 0, -1): walk.append(layers[t][walk[-1]])
walk = walk[::-1]          # W_1..W_L with W_L = M_0
seq = [P[i0]] + [P[i] for i in walk[:-1]]   # M_0, M_1, ..., M_{L-1}
pm = all(sorted(x for e in Mt for x in E[e]) == list(range(n)) for Mt in seq)
dis = all(not (seq[t] & seq[(t + 1) % L]) for t in range(L))
fr = [g.kidx(Mt) for Mt in seq]
frok = all(fr[t] == (2 - 2 * t) % 5 for t in range(L))
hams = [g.ncomp(seq[t] | seq[(t + 1) % L]) for t in range(L)]
print(f'R0 sequence L={L}: PM {pm} disjoint {dis} frames {fr} ok {frok} components(M_t u M_t+1) {hams}')
assert pm and dis and frok and hams[0] == 1
if v2: assert all(hams[t] == 1 for t in range(0, L, 2)); print('V2 (Hamiltonian at every even step): True')
if v3: assert all(hams[t] == 2 for t in range(1, L, 2)); print('V3 (word 1212): True')
for t, Mt in enumerate(seq): print(f'  M_{t}:', sorted(tuple(E[e]) for e in Mt))

# ---------- (2) brute-force embedding ----------
inc = [[e for e in range(m) if u in E[e]] for u in range(n)]
rot0 = {u: inc[u] for u in range(n)}
rot0[v] = list(fv)


def faces_of(rot, tw):
    """face-tracing on states (u, e, sigma); returns one walk per face (list of (u, e))."""
    pos = {u: {e: i for i, e in enumerate(rot[u])} for u in range(n)}
    seen = set(); walks = []
    for u in range(n):
        for e in rot[u]:
            for sg in (1, -1):
                if (u, e, sg) in seen: continue
                W = []; x, f, s = u, e, sg
                while (x, f, s) not in seen:
                    seen.add((x, f, s)); W.append((x, f))
                    y = other(f, x); s2 = s * (-1 if tw[f] else 1)
                    r = rot[y]; f = r[(pos[y][f] + s2) % len(r)]; x = y; s = s2
                walks.append(W)
    return walks   # each face appears twice (both directions)


def search(want):
    best = None
    cubic = [u for u in range(n) if u != v]
    for flips in itertools.product((0, 1), repeat=len(cubic)):
        rot = dict(rot0)
        for u, fl in zip(cubic, flips):
            if fl: rot[u] = rot0[u][::-1]
        tws = [tuple([0] * m)] if want == 'T2' else itertools.product((0, 1), repeat=m)
        for tw in tws:
            if want == 'RP2' and flips != tuple([0] * len(cubic)): return None
            W = faces_of(rot, tw); F = len(W) // 2
            chi = n - m + F
            if (want == 'RP2' and chi == 1) or (want == 'T2' and chi == 0):
                # keep one walk per face: drop the reversed copy
                faces = []; used = set()
                for w in W:
                    key = frozenset((x, f) for x, f in w)
                    rev = frozenset((other(f, x), f) for x, f in w)
                    if rev in used: continue
                    used.add(key); faces.append(w)
                if '--simple' in sys.argv and not check_faces(faces)['primal_simple_triangulation']: continue
                return faces
    return None


# ---------- (3) independent check from the face list ----------
def check_faces(faces):
    cnt = [0] * m; occ = [[] for _ in range(m)]
    for fi, w in enumerate(faces):
        for x, f in w:
            cnt[f] += 1; occ[f].append((fi, 1 if E[f][0] == x else -1))
    assert all(c == 2 for c in cnt), 'edge-side count'
    link_ok = True; vorder = None
    for u in range(n):
        adj = {e: [] for e in inc[u]}
        for w in faces:
            for i, (x, f) in enumerate(w):
                y = other(f, x); f2 = w[(i + 1) % len(w)][1]
                if y == u: adj[f].append(f2); adj[f2].append(f)
        if any(len(a) != 2 for a in adj.values()): link_ok = False; continue
        start = inc[u][0]; cyc = [start]; prev = None; cur = start
        while True:
            nxt = adj[cur][0] if adj[cur][0] != prev else adj[cur][1]
            if nxt == start: break
            cyc.append(nxt); prev, cur = cur, nxt
        if len(cyc) != len(inc[u]): link_ok = False
        if u == v: vorder = cyc
    lab = [fv.index(e) for e in vorder]
    i = lab.index(0); lab = lab[i:] + lab[:i]
    rot_ok = lab in ([0, 1, 2, 3, 4], [0, 4, 3, 2, 1])
    F = len(faces); chi = n - m + F
    # orientability: eps_f * d1 = - eps_g * d2 for the two occurrences of each edge
    eps = [None] * F; orient = True
    for f0 in range(F):
        if eps[f0] is not None: continue
        eps[f0] = 1; dq = deque([f0])
        while dq:
            a = dq.popleft()
            for e in range(m):
                (fa, da), (fb, db) = occ[e]
                for (x, dx), (y, dy) in (((fa, da), (fb, db)), ((fb, db), (fa, da))):
                    if x != a: continue
                    want = -eps[x] * dx * dy
                    if eps[y] is None: eps[y] = want; dq.append(y)
                    elif eps[y] != want: orient = False
    # primal triangulation T = dual of the embedded G with a vertex x filling the pentagon at v:
    # simple iff every G-edge separates two distinct faces, no two G-edges separate the same pair, and the
    # five faces around v are distinct.  deg_T(face) = face length (+1 if the face meets v); deg_T(x) = 5.
    pairs = []
    for e in range(m):
        (fa, _), (fb, _) = occ[e]; pairs.append(tuple(sorted((fa, fb))))
    at_v = [fi for fi, w in enumerate(faces) for x, f in w if x == v]
    simple = all(a != b for a, b in pairs) and len(set(pairs)) == m and len(set(at_v)) == 5
    degT = sorted([len(w) + (1 if fi in at_v else 0) for fi, w in enumerate(faces)] + [5])
    return dict(F=F, chi=chi, closed_surface=link_ok, rotation_at_v=lab, rotation_ok=rot_ok, orientable=orient,
                primal_simple_triangulation=simple, primal_degrees=degT)


def from_twist(hexstr):
    tw = [(int(hexstr, 16) >> e) & 1 for e in range(m)]
    W = faces_of(rot0, tw); faces = []; used = set()
    for w in W:
        key = frozenset((x, f) for x, f in w); rev = frozenset((other(f, x), f) for x, f in w)
        if rev in used: continue
        used.add(key); faces.append(w)
    return faces


for want in (['RP2', 'T2'] if which == 'both' else [which]):
    faces = from_twist(sys.argv[sys.argv.index('--tw') + 1]) if '--tw' in sys.argv else search(want)
    if faces is None: print(want, ': no embedding found'); continue
    res = check_faces(faces)
    surf = {(1, False): 'RP2', (0, True): 'torus', (2, True): 'sphere', (0, False): 'Klein bottle'}.get((res['chi'], res['orientable']), '?')
    print(f'{want}: {res} -> surface {surf}')
    for w in faces: print('   face', [x for x, f in w])
