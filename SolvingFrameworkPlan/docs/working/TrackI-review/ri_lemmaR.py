"""Track I review: exhaustive check of Lemma R (written from scratch).

Model: circles C_0..C_r with points in cyclic order; B1 = {(0,1),(2,3),...}, B3 = {(1,2),...,(n-1,0)}
on each circle; each point labelled I or O; Sigma_I a matching of the I-points realisable by disjoint
arcs in the region R (a disc for one circle, an annulus for two); Sigma_O a matching of the O-points
of each circle (non-crossing = realisable in the disc D_i).
lambda(B, Sigma) = number of cycles of B u Sigma.
Lemma R: lambda(B1,S_O) + lambda(B3,S_O) mod 2 independent of S_O (for fixed labels, Sigma_I).
"""
import sys, itertools
from collections import Counter


def all_matchings(pts):
    if not pts:
        yield []
        return
    a = pts[0]
    for i in range(1, len(pts)):
        rest = pts[1:i] + pts[i + 1:]
        for m in all_matchings(rest):
            yield [(a, pts[i])] + m


def crosses(p, q, order):
    a, b = sorted((order[p[0]], order[p[1]])); c, d = sorted((order[q[0]], order[q[1]]))
    return (a < c < b) != (a < d < b)


def noncrossing(m, order):
    return all(not crosses(m[i], m[k], order) for i in range(len(m)) for k in range(i + 1, len(m)))


def ncycles(M1, M2):
    seen = set(); k = 0
    for p in M1:
        if p in seen:
            continue
        k += 1; q = p
        while True:
            seen.add(q); q = M1[q]; seen.add(q); q = M2[q]
            if q == p:
                break
    return k


def todict(pairs):
    d = {}
    for a, b in pairs:
        d[a] = b; d[b] = a
    return d


def circle_B(ci, n):
    B1 = {}; B3 = {}
    for i in range(n):
        p = (ci, i); q = (ci, (i + 1) % n)
        tgt = B1 if i % 2 == 0 else B3
        tgt[p] = q; tgt[q] = p
    return B1, B3


def annulus_realisable(m, ns, d):
    """m: matching on points (ci,pos), two circles; d = +1/-1 relative orientation of C1."""
    bridges = [pr for pr in m if pr[0][0] != pr[1][0]]
    if not bridges:
        for ci in (0, 1):
            sub = [pr for pr in m if pr[0][0] == ci]
            order = {(ci, i): i for i in range(ns[ci])}
            if not noncrossing(sub, order):
                return False
        return True
    b0 = bridges[0]
    p0, q0 = (b0[0], b0[1]) if b0[0][0] == 0 else (b0[1], b0[0])
    seq = [(0, (p0[1] + t) % ns[0]) for t in range(1, ns[0])]
    seq += [(1, (q0[1] + d * t) % ns[1]) for t in range(1, ns[1])]
    order = {p: i for i, p in enumerate(seq)}
    rest = [pr for pr in m if pr != b0]
    return noncrossing(rest, order)


def planar_realisable(m, ns):
    """Sigma_I drawable by disjoint arcs in the complement of the closed discs D_i on S^2:
    planarity of (circle cycles + one hub per disc joined to all its points + Sigma_I edges).
    Each wheel has a unique embedding, so the circle orders are respected; the complement of
    disjoint discs on S^2 is connected, so the arcs automatically lie in one region R."""
    import networkx as nx
    G = nx.MultiGraph()
    for ci, n in enumerate(ns):
        for i in range(n):
            G.add_edge((ci, i), (ci, (i + 1) % n))
            G.add_edge(('hub', ci), (ci, i))
    for a, b in m:
        # subdivide so multi-edges stay simple
        G.add_edge(a, ('mid', a, b)); G.add_edge(('mid', a, b), b)
    H = nx.Graph(); 
    for u, v, k in G.edges(keys=True):
        if H.has_edge(u, v):
            w = ('sub', u, v, k); H.add_edge(u, w); H.add_edge(w, v)
        else:
            H.add_edge(u, v)
    return nx.check_planarity(H)[0]


def test_config(ns, sigmaI_mode, sigmaO_mode, stats):
    """ns: list of circle sizes (1 or 2 circles). sigmaI_mode: 'planar' | 'any'. sigmaO_mode: 'noncross' | 'any'."""
    allpts = [(ci, i) for ci, n in enumerate(ns) for i in range(n)]
    B1 = {}; B3 = {}
    for ci, n in enumerate(ns):
        b1, b3 = circle_B(ci, n); B1.update(b1); B3.update(b3)
    for lab in itertools.product((0, 1), repeat=len(allpts)):  # 1 = I
        Ipts = [p for p, l in zip(allpts, lab) if l]
        Opts_by = [[p for p, l in zip(allpts, lab) if not l and p[0] == ci] for ci in range(len(ns))]
        if len(Ipts) % 2 or any(len(o) % 2 for o in Opts_by):
            continue
        # Sigma_I candidates
        SI = []
        for m in all_matchings(Ipts):
            if sigmaI_mode == 'any':
                SI.append(m)
            elif len(ns) == 1:
                if noncrossing(m, {(0, i): i for i in range(ns[0])}):
                    SI.append(m)
            else:
                pl = planar_realisable(m, ns)
                if len(ns) == 2:
                    an = annulus_realisable(m, ns, 1) or annulus_realisable(m, ns, -1)
                    if an != pl:
                        stats['realisability_disagree'] += 1
                if pl:
                    SI.append(m)
        # Sigma_O candidates (product over circles)
        per = []
        for ci, O in enumerate(Opts_by):
            order = {(ci, i): i for i in range(ns[ci])}
            ms = [m for m in all_matchings(O) if sigmaO_mode == 'any' or noncrossing(m, order)]
            per.append(ms)
        SO = [sum(c, []) for c in itertools.product(*per)]
        for mI in SI:
            par = set()
            for mO in SO:
                S = todict(mI + mO)
                par.add((ncycles(B1, S) + ncycles(B3, S)) % 2)
            stats['configs'] += 1
            stats['SO_total'] += len(SO)
            if len(par) > 1:
                stats['FAIL'] += 1


if __name__ == '__main__':
    out = []
    def run(ns, mi, mo):
        st = Counter()
        test_config(ns, mi, mo, st)
        line = 'circles=%s SigmaI=%s SigmaO=%s : (labelling,Sigma_I) configs=%d, Sigma_O evaluated=%d, configs where parity varies=%d' % (
            ns, mi, mo, st['configs'], st['SO_total'], st['FAIL'])
        if st['realisability_disagree']:
            line += ' REALISABILITY-DISAGREE=%d' % st['realisability_disagree']
        print(line, flush=True); out.append(line)
    for n in (2, 4, 6, 8, 10, 12):
        run([n], 'planar', 'noncross')
    for n in (4, 6, 8):
        run([n], 'planar', 'any')
        run([n], 'any', 'noncross')
    for n0 in (2, 4, 6):
        for n1 in (2, 4, 6):
            if n0 <= n1 and n0 + n1 <= 12:
                run([n0, n1], 'planar', 'noncross')
    for ns in ([2, 2, 2], [2, 2, 4], [2, 4, 4], [2, 2, 2, 2]):
        run(ns, 'planar', 'noncross')
    for n0, n1 in ((2, 4), (4, 4)):
        run([n0, n1], 'any', 'noncross')
        run([n0, n1], 'planar', 'any')
    open(sys.argv[1] if len(sys.argv) > 1 else 'out/lemmaR.log', 'w').write('\n'.join(out) + '\n')
