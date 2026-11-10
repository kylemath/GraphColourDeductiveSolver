#!/usr/bin/env python3
"""RSST-1SHOT §7 brute-force sanity check (Studio, independent; spec RSSTFP_SPEC 33338de6 §7).

Question: in an internally 6-connected triangulation (no separating cycle of length <= 4; every separating
5-cycle has a single vertex on one side; min degree 5), can two second-ring vertices of the 2-ball of u
(the s_i and the privates, INCLUDING the undrawn middles of a >= 9 link vertex) be
  (I) identified (equal), or (C) adjacent though not consecutive on the ring-2 cycle R2?
(Link chords, u/w identifications and extra u/w edges are handled by hand in the README, because every
neighbour of u and of an exact-degree w is drawn.)

For each window (d, link word with real degrees; a '9' is drawn with its REAL number of privates, deg-5) and
each pair x, y on R2, we look for an obstruction: a cycle C made of a window path P from y to x closed by the
new adjacency (C) or by the identification (I), with
   effective length L = |P|+1 (C) or |P| (I);  L <= 2: impossible in a simple graph;
   L in {3,4}: window vertices strictly on both sides;  L = 5: >= 2 window vertices strictly on each side.
Sides are computed from the planar rotation system of window + chord (chord drawn in the outer face).
Witness modes: 'all' counts every window vertex; 'uw' counts only u and the w_i (pairwise distinct by the
link argument, so identifications elsewhere cannot merge them).  A pair with no obstruction is reported.
"""
import sys, itertools

def window(d, degs):
    """degs[i] = real degree of w_i (>=5). Returns rot (dict vertex->list, ccw), R2 list."""
    rot = {'u': [('w', i) for i in range(d)]}
    seg = []
    for i in range(d):
        k = degs[i] - 5
        seg.append([('s', (i - 1) % d)] + [('p', i, j) for j in range(1, k + 1)] + [('s', i)])
    for i in range(d):
        rot[('w', i)] = ['u', ('w', (i - 1) % d)] + seg[i] + [('w', (i + 1) % d)]
    R2 = []
    for i in range(d):
        R2 += seg[i][:-1]          # s_{i-1}, p_i.*, (s_i is first of next seg)
    n = len(R2)
    for t, x in enumerate(R2):
        prev, nxt = R2[t - 1], R2[(t + 1) % n]
        if x[0] == 's':
            i = x[1]
            rot[x] = [('w', (i + 1) % d), ('w', i), prev, 'OUT', nxt]
        else:
            rot[x] = [('w', x[1]), prev, 'OUT', nxt]
    return rot, R2

def adj_of(rot):
    return {v: set(z for z in L if z != 'OUT') for v, L in rot.items()}

def sides(rot, C):
    """C: list of vertices of a cycle (in order). Returns (left set, right set) of vertices not on C."""
    onC = set(C); m = len(C); lab = {}
    for t in range(m):
        a, c, b = C[t - 1], C[t], C[(t + 1) % m]
        L = rot[c]; ia, ib = L.index(a), L.index(b)
        k = len(L); j = (ib + 1) % k
        while j != ia:                       # strictly after b, before a, ccw: one side
            z = L[j]
            if z != 'OUT' and z not in onC: lab.setdefault(z, set()).add(0)
            j = (j + 1) % k
        j = (ia + 1) % k
        while j != ib:
            z = L[j]
            if z != 'OUT' and z not in onC: lab.setdefault(z, set()).add(1)
            j = (j + 1) % k
    adj = adj_of(rot)
    side = {}
    for s0 in list(lab):
        if len(lab[s0]) != 1: return None
    # BFS propagate
    from collections import deque
    for v, S in lab.items():
        side[v] = next(iter(S))
    dq = deque(side)
    while dq:
        v = dq.popleft()
        for z in adj[v]:
            if z in onC: continue
            if z in side:
                if side[z] != side[v]: return None
            else: side[z] = side[v]; dq.append(z)
    return ({v for v in side if side[v] == 0}, {v for v in side if side[v] == 1})


def strict_witnesses(rot0, C, A, B, ident=()):
    """Witnesses guaranteed distinct from the cycle even if OTHER ring-2 identifications existed:
    u and w's (distinct by the link argument), whose side is reached inside the wheel {u, w}; and a ring-2
    vertex z drawn in rot(c) for a w-vertex c of C, when every ring-2 vertex of C is also drawn in rot(c)
    (so simplicity of rot(c) separates z from them); z's side is its rotation sector at c."""
    onC = set(C)
    isw = lambda v: v == 'u' or v[0] == 'w'
    # wheel-only BFS from sector seeds at wheel vertices of C
    lab = {}
    m = len(C)
    for t in range(m):
        a, c, b = C[t - 1], C[t], C[(t + 1) % m]
        L = rot0.get(c) if isw(c) else None
        if L is None: continue
        ia, ib = L.index(a), L.index(b); k = len(L)
        for side, (st, en) in ((0, (ib, ia)), (1, (ia, ib))):
            j = (st + 1) % k
            while j != en:
                z = L[j]
                if z not in onC: lab.setdefault(z, side) if True else None
                j = (j + 1) % k
    wA = set(); wB = set()
    # ring-2 witnesses
    r2C = [v for v in C if not isw(v)]
    for t in range(m):
        a, c, b = C[t - 1], C[t], C[(t + 1) % m]
        if not isw(c) or c == 'u': continue
        L = rot0[c]
        inrot = lambda v: v in L or (v in ident and any(q in L for q in ident))
        if not all(inrot(v) for v in r2C): continue
        ia, ib = L.index(a), L.index(b); k = len(L)
        for side, (st, en) in ((0, (ib, ia)), (1, (ia, ib))):
            j = (st + 1) % k
            while j != en:
                z = L[j]
                if z not in onC and not isw(z): (wA if side == 0 else wB).add(z)
                j = (j + 1) % k
    # wheel vertices: side from full BFS restricted to the wheel
    adj = {v: set(z for z in L if z != 'OUT' and isw(z)) for v, L in rot0.items() if isw(v)}
    from collections import deque
    side = {v: s for v, s in lab.items() if isw(v)}
    dq = deque(side)
    while dq:
        v = dq.popleft()
        for z in adj[v]:
            if z in onC or z in side: continue
            side[z] = side[v]; dq.append(z)
    for v, s_ in side.items(): (wA if s_ == 0 else wB).add(v)
    # orientation of sides must agree with the full computation
    if (wA & B) or (wB & A): wA, wB = wB, wA
    return wA, wB

def paths(adj, a, b, maxlen):
    out = []
    def rec(path):
        if len(path) - 1 > maxlen: return
        if path[-1] == b and len(path) > 1:
            out.append(list(path)); return
        for z in adj[path[-1]]:
            if z in path: continue
            path.append(z); rec(path); path.pop()
    rec([a]); return out

def check_pair(rot0, x, y, kind, mode):
    rot = {v: list(L) for v, L in rot0.items()}
    rot[x][rot[x].index('OUT')] = y; rot[x].insert(rot[x].index(y) + 1, 'OUT')
    rot[y][rot[y].index('OUT')] = x; rot[y].insert(rot[y].index(x) + 1, 'OUT')
    adjW = adj_of(rot0)
    maxP = 4 if kind == 'C' else 5
    best = None
    for P in paths(adjW, y, x, maxP):
        L = len(P) if kind == 'C' else len(P) - 1
        if L <= 2: return ('simple', P)
        C = P                                  # y ... x, closed by chord x->y
        sd = sides(rot, C)
        if sd is None: continue
        A, B = sd
        if mode == 'uw':
            A = {v for v in A if v == 'u' or v[0] == 'w'}; B = {v for v in B if v == 'u' or v[0] == 'w'}
        elif mode == 'strict':
            A, B = strict_witnesses(rot0, C, A, B, (x, y) if kind == 'I' else ())
        need = 1 if L <= 4 else 2
        if len(A) >= need and len(B) >= need:
            return (L, P)
    return None

def run(d, degs, mode):
    rot, R2 = window(d, degs)
    adjW = adj_of(rot)
    bad = []; n = 0
    nR = len(R2)
    for a, b in itertools.combinations(range(nR), 2):
        x, y = R2[a], R2[b]
        kinds = ['I']
        if y not in adjW[x]: kinds.append('C')
        for kind in kinds:
            n += 1
            r = check_pair(rot, x, y, kind, mode)
            if r is None: bad.append((kind, x, y))
    return n, bad

if __name__ == '__main__':
    # Stage I: identifications, witnesses u/w only (distinct by the link argument).
    # Stage C: chords, witnesses = all window vertices (distinct once stage I and the hand cases hold).
    maxd = int(sys.argv[1]) if len(sys.argv) > 1 else 9
    for d in range(5, maxd + 1):
        letters = (5, 6, 7, 8, 9, 10) if d == 5 else ((5, 6, 7, 9) if d == 6 else (5, 6, 9))
        seen = set(); npairs = {'I': 0, 'C': 0}; bad = {'I': 0, 'C': 0}
        for wd in itertools.product(letters, repeat=d):
            cands = []
            for r in range(d):
                z = wd[r:] + wd[:r]; cands += [z, z[::-1]]
            c = min(cands)
            if c in seen: continue
            seen.add(c)
            degs = list(c); rot, R2 = window(d, degs); adjW = adj_of(rot)
            for a, b in itertools.combinations(range(len(R2)), 2):
                x, y = R2[a], R2[b]
                for kind, mode in (('I', 'strict'), ('C', 'all')):
                    if kind == 'C' and y in adjW[x]: continue
                    npairs[kind] += 1
                    if check_pair(rot, x, y, kind, mode) is None:
                        bad[kind] += 1
                        print('NO-OBSTRUCTION d=%d degs=%s kind=%s %s %s' % (d, ''.join('%x' % z for z in c), kind, x, y), flush=True)
        print('d=%d letters(real degrees)=%s windows=%d  identifications tested %d unobstructed %d | chords tested %d unobstructed %d'
              % (d, letters, len(seen), npairs['I'], bad['I'], npairs['C'], bad['C']), flush=True)
