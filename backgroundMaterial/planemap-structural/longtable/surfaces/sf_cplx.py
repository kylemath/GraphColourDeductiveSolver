#!/usr/bin/env python3
"""Complex-level surface test for a graph G with hole h = 0 (link 1..5 in order):
is there a set K of triangles of G with every edge of G in exactly two triangles of K (arm A, pseudo-surface whose
1-skeleton is G), the star of h being the 5 triangles h x_i x_{i+1}?  Arm B: additionally every vertex link of K is a
single cycle (solutions are enumerated, up to a cap, and checked)."""
from pysat.solvers import Minisat22
from pysat.card import CardEnc, EncType
from collections import defaultdict


def triangles(adj):
    S = [set(a) for a in adj]; T = []
    for a in range(len(adj)):
        for b in S[a]:
            if b <= a: continue
            for c in S[a] & S[b]:
                if c > b: T.append((a, b, c))
    return T


def lower_defect(adj):
    S = [set(a) for a in adj]
    return sum(max(0, 2 - len(S[u] & S[v])) for u in range(len(adj)) for v in adj[u] if v > u)


def links_single(K):
    L = defaultdict(list)
    for a, b, c in K:
        L[a].append((b, c)); L[b].append((a, c)); L[c].append((a, b))
    for v, ed in L.items():
        adj = defaultdict(list)
        for p, q in ed: adj[p].append(q); adj[q].append(p)
        s = next(iter(adj)); seen = {s}; st = [s]
        while st:
            y = st.pop()
            for z in adj[y]:
                if z not in seen: seen.add(z); st.append(z)
        if len(seen) != len(adj): return False
    return True


def solve(adj, armB=False, cap=300, hole_link=(1, 2, 3, 4, 5)):
    """returns (statusA, statusB, K) ; statusB None if not asked"""
    T = triangles(adj)
    if lower_defect(adj) > 0: return False, (False if armB else None), None
    var = {t: i + 1 for i, t in enumerate(T)}; top = len(T)
    byedge = defaultdict(list)
    for t in T:
        a, b, c = t
        for e in ((a, b), (a, c), (b, c)): byedge[e].append(var[t])
    cl = []
    for e, lits in byedge.items():
        enc = CardEnc.equals(lits=lits, bound=2, top_id=top, encoding=EncType.seqcounter)
        top = max(top, enc.nv); cl += enc.clauses
    hl = list(hole_link) if hole_link else []
    for i in range(len(hl) and 5):
        t = tuple(sorted((0, hl[i], hl[(i + 1) % 5])))
        if t not in var: return False, (False if armB else None), None
        cl.append([var[t]])
    with Minisat22(bootstrap_with=cl) as s:
        if not s.solve(): return False, (False if armB else None), None
        m = s.get_model(); K = [t for t in T if m[var[t] - 1] > 0]
        if not armB: return True, None, K
        for _ in range(cap):
            if links_single(K): return True, True, K
            s.add_clause([-var[t] for t in K])
            if not s.solve(): return True, False, None
            m = s.get_model(); K = [t for t in T if m[var[t] - 1] > 0]
        return True, 'cap', None


def maxsat_defect(adj, hole_link=(1, 2, 3, 4, 5), armB=False):
    """min number of edges of G that lie in fewer than 2 faces, over face sets K with every edge in at most 2 faces
    and the hole star forced (RC2 MaxSAT).  0 <=> arm-A complex exists.  Returns (cost, K)."""
    from pysat.formula import WCNF
    from pysat.examples.rc2 import RC2
    T = triangles(adj); var = {t: i + 1 for i, t in enumerate(T)}; top = len(T)
    byedge = defaultdict(list)
    for t in T:
        a, b, c = t
        for e in ((a, b), (a, c), (b, c)): byedge[e].append(var[t])
    w = WCNF()
    for u in range(len(adj)):
        for v in adj[u]:
            if v > u and (u, v) not in byedge: byedge[(u, v)] = []
    for e, lits in byedge.items():
        if len(lits) > 2:
            enc = CardEnc.atmost(lits=lits, bound=2, top_id=top, encoding=EncType.seqcounter); top = max(top, enc.nv)
            for c in enc.clauses: w.append(c)
        top += 1; y = top
        if len(lits) < 2: w.append([-y])
        else:
            enc = CardEnc.atleast(lits=lits, bound=2, top_id=top, encoding=EncType.seqcounter); top = max(top, enc.nv)
            for c in enc.clauses: w.append(c + [-y])
        w.append([y], weight=1)
    hl = list(hole_link)
    for i in range(5):
        t = tuple(sorted((0, hl[i], hl[(i + 1) % 5])))
        if t in var: w.append([var[t]])
    with RC2(w) as r:
        m = r.compute(); cost = r.cost
    K = [t for t in T if m[var[t] - 1] > 0]
    return cost, K
