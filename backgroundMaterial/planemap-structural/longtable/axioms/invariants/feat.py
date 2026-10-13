"""Runs and per-state features (INVARIANTS-1, Long Table, 13 Oct 2026).

Sources -> list of runs (graph G5 + consecutive DL-good matchings M_0..M_{R-1}, closed flag):
  win   : SAT windows (enum_win.py), extended to the maximal 1212 run by the matching-form dynamics,
          with ('a5') or without ('free') the A5v requirement; dedup by the normal form at the first
          Hamiltonian state of the maximal run.
  planar: sphere NR runs (planar_runs.py), with primal data for areas.
  t1    : closed law/1212 orbits of TrackU's n = 22 T1 walk graphs.
Features: see state_features(); planar extras in planar_features().
"""
import json, itertools
from collections import deque
from ax_lib import G5, parse_line, fig8_diagram, fig8_axioms, ham_diagram, signed_graph, parity_consistent, \
    shortest_odd_cycle, cross


# ---------------- dynamics ----------------
def pm_classes(g, M, d):
    k, lp = d
    s0, s1, verts, edges = lp['X']; xs = set(edges[1:-1:2])
    s0, s1, verts, edges = lp['Y']; c0 = set(edges[0::2]); c1 = set(edges[1::2])
    return xs, c0, c1


def succ(g, M):
    d = g.dl(M)
    if d is None: return None
    xs, c0, c1 = pm_classes(g, M, d); f = g.fv[(d[0] - 2) % 5]
    return frozenset(xs | (c0 if f in c0 else c1))


def pred(g, M):
    d = g.dl(M)
    if d is None: return None
    xs, c0, c1 = pm_classes(g, M, d); f = g.fv[(d[0] + 2) % 5]
    return frozenset(xs | (c0 if f in c0 else c1))


def a5bit(g, M, d=None):
    d = d or g.dl(M)
    if d is None: return None
    k, lp = d; w = g.other(g.fv[k], g.v)
    return 1 if w in lp['X'][2] else 0


def maximal_run(g, M0, M1, need_a5, maxlen=200):
    """M0 u M1 Hamiltonian (w = 1).  Extend both ways keeping: every state DL-good (and A5v if
    need_a5), consecutive successor rule, word alternating.  Returns (Ms, start_reason, end_reason, closed)."""
    ok = lambda M: M is not None and g.dl(M) is not None and (not need_a5 or a5bit(g, M) == 1)
    assert ok(M0) and ok(M1) and succ(g, M0) == M1
    Ms = [M0, M1]; ws = [None, g.ncomp(M0 | M1)]
    # forward
    end = None
    while True:
        N = succ(g, Ms[-1])
        if N == Ms[0] and len(Ms) % 2 == 0:
            if g.ncomp(Ms[-1] | N) == (2 if ws[-1] == 1 else 1):
                return Ms, None, None, True
        if len(Ms) > maxlen: end = 'maxlen'; break
        if g.dl(N) is None: end = 'notDL'; break
        w = g.ncomp(Ms[-1] | N)
        if w != (2 if ws[-1] == 1 else 1): end = f'word{w}'; break
        if need_a5 and a5bit(g, N) != 1: end = 'A5v'; break
        Ms.append(N); ws.append(w)
    start = None
    while True:
        P = pred(g, Ms[0])
        if len(Ms) > maxlen: start = 'maxlen'; break
        if P is None or g.dl(P) is None: start = 'notDL'; break
        w = g.ncomp(P | Ms[0])
        w1 = g.ncomp(Ms[0] | Ms[1])
        if w != (2 if w1 == 1 else 1): start = f'word{w}'; break
        if need_a5 and a5bit(g, P) != 1: start = 'A5v'; break
        Ms.insert(0, P)
    return Ms, start, end, False


def normal_key(g, Ms):
    """canonical key of (graph, run): relabel along the first Hamiltonian pair (M_a, M_{a+1})."""
    a = next(t for t in range(len(Ms) - 1) if g.ncomp(Ms[t] | Ms[t + 1]) == 1)
    M0, M1 = Ms[a], Ms[a + 1]; H = M0 | M1
    k0 = g.kidx(M0); v = g.v
    lab = {v: 0}; x = g.other(g.fv[k0], v); e = g.fv[k0]; i = 1
    while x != v:
        lab[x] = i; i += 1
        e = [f for f in g.inc[x] if f in H and f != e][0]; x = g.other(e, x)
    ch = []
    for f in range(g.m):
        if f in H: continue
        p, q = g.E[f]
        tag = (g.fidx[f] - k0 + 2) % 5 if f in g.fidx else -1
        ch.append((min(lab[p], lab[q]), max(lab[p], lab[q]), tag))
    return (g.n, tuple(sorted(ch)), len(Ms), a)


# ---------------- loaders ----------------
def load_windows(path, need_a5):
    runs = {}
    for l in open(path):
        d = json.loads(l)
        g = G5(*parse_line(d['line']))
        Ms = [frozenset(m) for m in d['M']]
        Rs, st, en, closed = maximal_run(g, Ms[0], Ms[1], need_a5)
        key = normal_key(g, Rs) if not closed else ('closed', d['line'])
        if key in runs: continue
        runs[key] = dict(src=path.split('/')[-1], kind='a5' if need_a5 else 'free', g=g, Ms=Rs, start=st,
                         end=en, closed=closed, n=g.n)
    return list(runs.values())


def load_planar(path):
    out = []
    for l in open(path):
        d = json.loads(l)
        g = G5(d['n'], [tuple(e) for e in d['E']], d['fv'])
        Ms = [frozenset(m) for m in d['M']]
        # keep the matching-form DL-good part (Q_t a connected figure-eight with DL pairing)
        good = [g.dl(M) is not None for M in Ms]
        a = 0
        while a < len(Ms) and not good[a]: a += 1
        b = a
        while b < len(Ms) and good[b]: b += 1
        trimmed = (a, len(Ms) - b)
        Ms = Ms[a:b]
        out.append(dict(src=d['name'] + ':' + str(d['hole']), kind='planar', g=g, Ms=Ms, trimmed=trimmed,
                        start='censusNR', end='censusNR', closed=False, n=g.n, rot=d['rot'], hole=d['hole'],
                        prim=[tuple(p) for p in d['prim']], Nch=d['Nch'][a:b]))
    return out


def load_t1(path, maxg=10 ** 9):
    out = []; seen = set()
    for l in open(path):
        if len(out) >= maxg: break
        n, E, fv = parse_line(l)
        key = (n, tuple(sorted(tuple(sorted(e)) for e in E)), tuple(tuple(sorted(E[f])) for f in fv))
        if key in seen: continue
        seen.add(key)
        g = G5(n, E, fv); P, good, cyc = g.orbits()
        for c in cyc:
            w = g.word(c)
            if all(w[t] in (1, 2) and w[t] != w[t - 1] for t in range(len(c))):
                # rotate so that w[1] = 1
                r = next(t for t in range(len(c)) if w[(t + 1) % len(c)] == 1)
                c = c[r:] + c[:r]
                out.append(dict(src='t1walk22', kind='t1', g=g, Ms=list(c), start=None, end=None, closed=True, n=n))
    return out


# ---------------- features ----------------
def loop_pos(lp, key, start_s, x):
    s0, s1, verts, edges = lp[key]
    vs = verts if s0 == start_s else verts[::-1]
    return vs.index(x) if x in vs else -1


def ham_feats(g, P, M):
    chords, cons = ham_diagram(g, P, M)
    nv, ed = signed_graph(chords, cons); nv0, ed0 = signed_graph(chords, [])
    ncr = sum(1 for (a, b, p) in ed0)
    # interlace components
    adj = [[] for _ in range(nv0)]
    for a, b, p in ed0: adj[a].append(b); adj[b].append(a)
    comp = 0; seen = set()
    for s in range(nv0):
        if s in seen: continue
        comp += 1; st = [s]; seen.add(s)
        while st:
            x = st.pop()
            for y in adj[x]:
                if y not in seen: seen.add(y); st.append(y)
    # positions of v-chord far ends along H (circle positions 0..n-2 cubic, v blow-up at n-1..n+1)
    k = g.kidx(M); e = lambda i: g.fv[(k - 2 + i) % 5]
    pos = {c[0]: (c[1], c[2]) for c in chords}
    N = g.n - 1
    vend = {}
    for i in (0, 1, 3):
        a, b = pos[e(i)]; vend[i] = a if a < N else b
    # crossings of each v-chord
    vcross = {i: sum(1 for c in chords if c[0] != e(i) and cross(c, (e(i),) + pos[e(i)])) for i in (0, 1, 3)}
    # max bipartite defect (min #chords to delete for bipartite IG) by brute force if small
    mbd = None
    if nv0 <= 16:
        best = None
        for r in range(0, nv0 + 1):
            for S in itertools.combinations(range(nv0), r):
                Ss = set(S)
                sub = [(a, b, p) for a, b, p in ed0 if a not in Ss and b not in Ss]
                if parity_consistent(nv0, sub): best = r; break
            if best is not None: break
        mbd = best
    return dict(h_ncross=ncr, h_comp=comp, h_bip=int(parity_consistent(nv0, ed0)),
                h_bip_rot=int(parity_consistent(nv, ed)), h_oddc=shortest_odd_cycle(nv0, ed0) or 0,
                h_e0=vend[0], h_e1=vend[1], h_e3=vend[3], h_e0x=vcross[0], h_e1x=vcross[1], h_e3x=vcross[3],
                h_bipdef=mbd)


def state_features(g, Ms, t, closed):
    R = len(Ms); M = Ms[t]
    d = g.dl(M); k, lp = d
    v = g.v; w_partner = g.other(g.fv[k], v)
    X = lp['X']; Y = lp['Y']
    Xv = set(X[2]); Yv = set(Y[2])
    xy = xx = yy = 0
    for f in M:
        if f == g.fv[k]: continue
        a, b = g.E[f]
        if a in Xv and b in Xv: xx += 1
        elif a in Yv and b in Yv: yy += 1
        else: xy += 1
    chords, nxl, nyl = fig8_diagram(g, M, d)
    vch = [c for c in chords if c[3].startswith('v')][0]
    vcr = sum(1 for c in chords if c is not vch and cross(c, vch))
    f8 = fig8_axioms(g, M, d)
    F = dict(t=t, k=k, a5=a5bit(g, M, d), nX=len(X[2]), nY=len(Y[2]), xx=xx, yy=yy, xy=xy,
             pX=loop_pos(lp, 'X', (k - 1) % 5, w_partner), pY=loop_pos(lp, 'Y', (k + 2) % 5, w_partner),
             vcross=vcr, xycross=f8['xy_cross'], f8planar=int(f8['fig8_planar']))
    prv = Ms[t - 1] if (t > 0 or closed) else None
    nxt = Ms[(t + 1) % R] if (t + 1 < R or closed) else None
    if prv is not None:
        F['w'] = g.ncomp(prv | M)
        F['Y_on_prev'] = len(set(Y[3]) & prv)          # = (|Y|+1)/2 always (S2)
        if F['w'] == 1: F.update(ham_feats(g, prv, M))
    if nxt is not None:
        dn = g.dl(nxt)
        if dn is not None:
            Yn = set(dn[1]['Y'][3]); Xn = set(dn[1]['X'][3])
            F['YYn'] = len(set(Y[3]) & Yn); F['XXn'] = len(set(X[3]) & Xn)
            F['D'] = len(set(Y[3]) ^ Yn)
            F['XYn'] = len(set(X[3]) & Yn); F['YXn'] = len(set(Y[3]) & Xn)
    return F


# ---------------- planar extras ----------------
def primal_regions(run, edge_set_keep):
    """components of (primal - h) using primal edges whose dual edge is in edge_set_keep."""
    rot = run['rot']; h = run['hole']; prim = run['prim']
    pid = {tuple(sorted(p)): e for e, p in enumerate(prim)}
    comp = {}; c = 0
    for s in range(len(rot)):
        if s == h or s in comp: continue
        comp[s] = c; q = [s]
        for x in q:
            for y in rot[x]:
                if y == h or y in comp: continue
                e = pid.get(tuple(sorted((x, y))))
                if e is not None and e in edge_set_keep: comp[y] = c; q.append(y)
        c += 1
    return comp, c


def planar_features(run, t):
    g = run['g']; Ms = run['Ms']; M = Ms[t]; d = g.dl(M); k = d[0]
    link = run['rot'][run['hole']]
    F = {}
    comp, c = primal_regions(run, M)                 # regions of the figure-eight Q_t
    F['f8_regions'] = c
    rX = comp[link[k]]; rY = comp[link[(k + 3) % 5]]; rO = comp[link[(k + 2) % 5]]
    F['f8_ok'] = int(comp[link[(k + 1) % 5]] == rX and comp[link[(k + 4) % 5]] == rO and len({rX, rY, rO}) == 3)
    cnt = lambda r: sum(1 for x in comp if comp[x] == r)
    F['aX'], F['aY'], F['aO'] = cnt(rX), cnt(rY), cnt(rO)
    if t > 0 and g.ncomp(Ms[t - 1] | M) == 1:
        H = Ms[t - 1] | M; C = set(range(g.m)) - H
        comp2, c2 = primal_regions(run, C)
        sA = comp2[link[(k + 1) % 5]]
        F['h_sides'] = c2
        F['hA'] = sum(1 for x in comp2 if comp2[x] == sA); F['hB'] = len(comp2) - F['hA']
        F['hA_link_ok'] = int(comp2[link[(k + 2) % 5]] == sA and comp2[link[(k + 3) % 5]] != sA)
        # chords by side: a chord (dual edge not in H) lies on the side of its primal endpoints
        side = {}
        for e in C:
            u, w = run['prim'][e]; side[e] = 'A' if comp2[u] == sA else 'B'
        F['_side'] = side
    return F
