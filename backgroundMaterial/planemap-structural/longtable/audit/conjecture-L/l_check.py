#!/usr/bin/env python3
"""Independent audit check of Long Table's refutation of Conjecture L.

Audit code. It imports and reads no team code. The witness data (faces, hole, colours) are copied as
data from l-attack.md (W6) and from the data constants of lattack_witness.py (A3).
The A_r graphs are rebuilt here from their description.
Definitions are Math's (MathConfinementAttack Step 1; MathCleanVertexAttack section 1; MathVHLine 4):
  state: proper 4-colouring of T - v, link x0..x4 (rotation at v) using 4 colours; repeat colour
         alpha at x_j, x_{j+2};
  doubly locked: x_{j+1} ~ x_{j+3} in the {c(x_{j+1}), c(x_{j+3})} subgraph of T - v, and
         x_{j+1} ~ x_{j+4} in the {c(x_{j+1}), c(x_{j+4})} subgraph;
  F(s): swap the {alpha, c(x_{j+3})}-component of x_{j+2} in T - v;
  chain length: the largest k with s, F(s), ..., F^{k-1}(s) all doubly locked. It is infinite when
         an iterate repeats a raw colouring while every state so far is locked.
The link orientation matters: the reverse orientation turns F into Math's B = F^{-1}. Both are reported.
"""
import json, sys
from itertools import product


def from_faces(faces):
    adj = {}
    for f in faces:
        for i in range(3):
            a, b = f[i], f[(i + 1) % 3]
            adj.setdefault(a, set()).add(b); adj.setdefault(b, set()).add(a)
    V = sorted(adj); n = len(V); E = sum(len(s) for s in adj.values()) // 2
    darts = {}
    for f in faces:
        for i in range(3):
            d = (f[i], f[(i + 1) % 3])
            assert d not in darts, ('dart used twice: orientation inconsistent', d)
            darts[d] = f
    assert all((b, a) in darts for (a, b) in darts), 'edge not in two oppositely oriented faces'
    assert n - E + len(faces) == 2 and len(faces) == 2 * n - 4, 'not a sphere triangulation'
    assert all(len(set(f)) == 3 for f in faces)
    return adj


def link(faces, v):
    """Rotation at v from oriented faces: in face (v,a,b), b follows a."""
    nxt = {}
    for f in faces:
        for i in range(3):
            if f[i] == v: nxt[f[(i + 1) % 3]] = f[(i + 2) % 3]
    a = min(nxt); out = [a]
    while nxt[out[-1]] != a: out.append(nxt[out[-1]])
    assert len(out) == len(nxt)
    return out


def comp(adj, col, s, p, q, v):
    seen = {s}; st = [s]
    while st:
        a = st.pop()
        for b in adj[a]:
            if b != v and b not in seen and col[b] in (p, q):
                seen.add(b); st.append(b)
    return seen


def repeat_index(col, L):
    lc = [col[x] for x in L]
    if len(set(lc)) != 4: return None
    js = [j for j in range(5) if lc[j] == lc[(j + 2) % 5]]
    assert len(js) == 1
    return js[0]


def locked(adj, col, L, v):
    j = repeat_index(col, L)
    if j is None: return False
    m, a, b = L[(j + 1) % 5], L[(j + 3) % 5], L[(j + 4) % 5]
    return a in comp(adj, col, m, col[m], col[a], v) and b in comp(adj, col, m, col[m], col[b], v)


def F(adj, col, L, v):
    j = repeat_index(col, L)
    al, c = col[L[j]], col[L[(j + 3) % 5]]
    K = comp(adj, col, L[(j + 2) % 5], al, c, v)
    new = dict(col)
    for w in K: new[w] = c if col[w] == al else al
    return new


def chain(adj, col, L, v, cap=10000):
    """Returns (length, 'infinite'|'finite'|'cap', period or None)."""
    seen = {}; s = col; k = 0
    while k < cap:
        key = tuple(sorted(s.items()))
        if key in seen:
            return float('inf'), 'infinite', k - seen[key]
        if not locked(adj, s, L, v):
            return k, 'finite', None
        seen[key] = k
        s = F(adj, s, L, v); k += 1
    return k, 'cap', None


def proper(adj, col, v):
    return all(col[a] != col[b] for a in adj if a != v for b in adj[a] if b != v)


def link_seq(adj, col, L, v, steps):
    s = col; out = []
    for _ in range(steps):
        out.append(([s[x] for x in L], repeat_index(s, L)))
        if repeat_index(s, L) is None: break
        s = F(adj, s, L, v)
    return out


# ---------------- witnesses ----------------
W6_FACES = [[1,16,5],[2,4,6],[2,33,22],[3,16,8],[4,2,22],[4,14,21],[4,22,14],[5,31,1],[5,33,6],[6,4,11],
            [6,10,20],[6,11,34],[6,20,5],[6,33,2],[8,13,17],[8,14,3],[9,14,8],[10,1,31],[10,6,34],[11,10,34],
            [11,17,13],[13,1,10],[13,8,16],[13,10,11],[14,17,21],[16,1,13],[16,3,5],[17,9,8],[17,11,21],
            [17,14,9],[20,31,5],[21,11,4],[22,3,14],[31,20,10],[33,3,22],[33,5,3]]
W6_V = 16
W6_COL = {1:2,2:2,3:2,4:0,5:0,6:3,8:3,9:2,10:0,11:2,13:1,14:1,17:0,20:1,21:3,22:3,31:3,33:1,34:1}
W6_LINK_STATED = [13, 8, 3, 5, 1]

A3_FACES = [(0,1,2),(0,2,3),(0,3,4),(0,4,5),(0,5,1),(1,6,2),(2,7,3),(3,8,4),(4,9,5),(5,10,1),(6,7,2),
            (6,11,7),(7,8,3),(7,12,8),(8,9,4),(8,13,9),(9,10,5),(9,14,10),(10,6,1),(10,15,6),(11,12,7),
            (12,13,8),(13,14,9),(14,15,10),(15,11,6),(16,11,15),(16,12,11),(16,13,12),(16,14,13),(16,15,14)]
A3_V = 0
A3_COL = {1:0,2:1,3:0,4:2,5:3,6:2,7:3,8:1,9:0,10:1,11:0,12:2,13:3,14:2,15:3,16:1}


def build_A(r):
    """Audit's own A_r: hub 0; rings R_k = {5k-4..5k}, k = 1..r; pole 5r+1. Antiprism strips:
    ring k vertex i joins ring k+1 vertices i and i+1. Faces oriented consistently (ccw)."""
    R = lambda k, i: 5 * (k - 1) + 1 + (i % 5)
    pole = 5 * r + 1; faces = []
    for i in range(5): faces.append((0, R(1, i), R(1, i + 1)))
    for k in range(1, r):
        for i in range(5):
            faces.append((R(k, i), R(k + 1, i + 1), R(k, i + 1)))
            faces.append((R(k, i), R(k + 1, i), R(k + 1, i + 1)))
    for i in range(5): faces.append((pole, R(r, i + 1), R(r, i)))
    return faces, 0


def colourings(adj, v, fix):
    """All proper 4-colourings of T - v with fix = {vertex: colour}. BFS order."""
    verts = [w for w in sorted(adj) if w != v]
    order = []; seen = set(fix); q = list(fix)
    while q:
        a = q.pop(0)
        for b in sorted(adj[a]):
            if b != v and b not in seen: seen.add(b); order.append(b); q.append(b)
    assert len(order) + len(fix) == len(verts)
    col = dict(fix)
    def rec(i):
        if i == len(order):
            yield dict(col); return
        w = order[i]; used = {col[u] for u in adj[w] if u in col}
        for c in range(4):
            if c not in used:
                col[w] = c; yield from rec(i + 1); del col[w]
    yield from rec(0)


def canon_iso_code(faces, v):
    """Planar code from each dart at v in both orientations; min = isomorphism class (fixing v)."""
    adj = from_faces(faces)
    nxt = {}
    for f in faces:
        for i in range(3): nxt.setdefault(f[i], {})[f[(i + 1) % 3]] = f[(i + 2) % 3]
    prv = {a: {b: c for c, b in d.items()} for a, d in nxt.items()}
    best = None
    for u0 in adj[v]:
        for rot in (nxt, prv):
            num = {v: 0}; order = [v]; first = {v: u0}; code = []; i = 0
            while i < len(order):
                a = order[i]; i += 1; s = first[a]; w = s; row = []
                while True:
                    if w not in num: num[w] = len(order); order.append(w); first[w] = a
                    row.append(num[w]); w = rot[a][w]
                    if w == s: break
                code.append(tuple(row))
            best = code if best is None or code < best else best
    return best


def main():
    out = {}
    # W6
    adj = from_faces(W6_FACES)
    L = link(W6_FACES, W6_V)
    assert len(adj[W6_V]) == 5 and proper(adj, W6_COL, W6_V) and set(W6_COL) == set(adj) - {W6_V}
    rots = [L[i:] + L[:i] for i in range(5)]
    assert W6_LINK_STATED in rots, (L, 'stated link is not a rotation of the ccw link')
    Lw = W6_LINK_STATED
    out['W6'] = dict(order=len(adj), degrees=sorted(len(adj[a]) for a in adj),
                     link_ccw=L, chain_F=chain(adj, W6_COL, Lw, W6_V)[:2],
                     chain_reverse_orientation=chain(adj, W6_COL, Lw[::-1], W6_V)[:2],
                     link_sequence=link_seq(adj, W6_COL, Lw, W6_V, 7))
    # A3 (team's data) and A_r (audit's own)
    adj3 = from_faces(A3_FACES); L3 = link(A3_FACES, A3_V)
    assert proper(adj3, A3_COL, A3_V)
    out['A3_witness'] = dict(order=len(adj3), degrees=sorted(len(adj3[a]) for a in adj3),
                             chain_F=chain(adj3, A3_COL, L3, A3_V), chain_reverse=chain(adj3, A3_COL, L3[::-1], A3_V))
    out['A3_witness_isomorphic_to_audit_A3'] = canon_iso_code(A3_FACES, A3_V) == canon_iso_code(*build_A(3))
    for r in (2, 3, 4, 5):
        faces, v = build_A(r); adjr = from_faces(faces); Lr = link(faces, v)
        stats = dict(colourings_x0_fixed=0, states_4link=0, locked=0, infinite=0, period_hist={}, finite_max=0,
                     infinite_reverse=0, cap=0)
        for col in colourings(adjr, v, {Lr[0]: 0}):
            stats['colourings_x0_fixed'] += 1
            if repeat_index(col, Lr) is None: continue
            stats['states_4link'] += 1
            if not locked(adjr, col, Lr, v): continue
            stats['locked'] += 1
            k, kind, per = chain(adjr, col, Lr, v)
            if kind == 'infinite':
                stats['infinite'] += 1; stats['period_hist'][per] = stats['period_hist'].get(per, 0) + 1
            elif kind == 'cap': stats['cap'] += 1
            else: stats['finite_max'] = max(stats['finite_max'], k)
            if chain(adjr, col, Lr[::-1], v)[1] == 'infinite': stats['infinite_reverse'] += 1
        out[f'A{r}'] = dict(order=len(adjr), degrees=sorted(len(adjr[a]) for a in adjr), **stats)
        print(r, out[f'A{r}'], flush=True, file=sys.stderr)
    json.dump(out, sys.stdout, indent=1, default=str); print()


if __name__ == '__main__':
    main()
