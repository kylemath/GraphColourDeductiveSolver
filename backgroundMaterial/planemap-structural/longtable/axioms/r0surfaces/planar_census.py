"""Planar census of closed frame-sequences, ALL lengths, every rotation at v (Long Table, r0surfaces).

Enumerates every Hamiltonian plane graph G (v = 0 of degree 5, other vertices cubic, simple) as
H = 0..n-1 + chords; planar drawings = proper 2-colourings (inside/outside) of the chord crossing graph;
each drawing gives the ccw rotation at v: (to 1), inside chords by increasing endpoint, (to n-1), outside
chords by decreasing endpoint.  All rotations realisable by some planar embedding are produced (H is a Jordan
curve in any planar embedding).  Mirror images (global inside/outside swap) are identified.

For each (G, rotation) and each constant frame advance a in {-2 (R0), -1}: digraph D_a on perfect matchings,
M -> M' iff M n M' = 0 and k(M') = k(M) + a.  Closed sequences of length L = closed walks of D_a.
Recorded: closed (nontrivial SCC), lengths L <= LMAX with trace(D_a^L) > 0, the set of #components of
M u M' over arcs inside SCCs (=1 would be a Hamiltonian pair on a closed sequence, i.e. an R0 violation
for a = -2), and min/max #components.
Covers every planar G that has a Hamiltonian cycle (all G with a Hamiltonian pair M_0 u M_1 in particular,
so for a = -2 it is an exact all-L test of R0 at this n).  usage: planar_census.py n [LMAX]"""
import sys, json, time, itertools
import numpy as np
from scipy.sparse.csgraph import connected_components

n = int(sys.argv[1]); LMAX = int(sys.argv[2]) if len(sys.argv) > 2 else 40


def chord_matchings(R):
    if not R: yield []; return
    a = R[0]
    for i in range(1, len(R)):
        b = R[i]
        if abs(a - b) == 1: continue
        for m in chord_matchings(R[1:i] + R[i + 1:]): yield [(a, b)] + m


def pms(edges, inc):
    out = []; used = [False] * n
    def rec(mask):
        x = next((u for u in range(n) if not used[u]), None)
        if x is None: out.append(mask); return
        used[x] = True
        for e in inc[x]:
            a, b = edges[e]; y = b if a == x else a
            if not used[y]: used[y] = True; rec(mask | (1 << e)); used[y] = False
        used[x] = False
    rec(0); return out


def ncomp(p, q, edges):
    par = list(range(n))
    def f(x):
        while par[x] != x: par[x] = par[par[x]]; x = par[x]
        return x
    c = n
    for e, (a, b) in enumerate(edges):
        if (p >> e) & 1 or (q >> e) & 1:
            ra, rb = f(a), f(b)
            if ra != rb: par[ra] = rb; c -= 1
    return c


def cross(c, d):
    a1, b1 = sorted(c); a2, b2 = sorted(d)
    if len({a1, b1, a2, b2}) < 4: return False
    return (a1 < a2 < b1) != (a1 < b2 < b1)


def rotations(chords):
    """set of ccw rotations at 0 (tuples of neighbour ids, canonical up to cyclic shift & reversal)."""
    k = len(chords)
    adj = [[j for j in range(k) if j != i and cross(chords[i], chords[j])] for i in range(k)]
    comp = [-1] * k; col = [0] * k; comps = []
    for s in range(k):
        if comp[s] >= 0: continue
        comp[s] = len(comps); col[s] = 0; st = [s]; mem = [s]
        while st:
            x = st.pop()
            for y in adj[x]:
                if comp[y] < 0: comp[y] = comp[s]; col[y] = 1 - col[x]; st.append(y); mem.append(y)
                elif col[y] == col[x]: return None    # not planar
        comps.append(mem)
    vch = [i for i in range(k) if 0 in chords[i]]
    vcomps = sorted(set(comp[i] for i in vch))
    rots = set()
    for flips in itertools.product((0, 1), repeat=max(0, len(vcomps) - 1)):
        fl = dict(zip(vcomps[1:], flips)); fl[vcomps[0]] = 0
        side = {i: col[i] ^ fl[comp[i]] for i in vch}
        ins = sorted(max(chords[i]) for i in vch if side[i] == 0)
        out = sorted((max(chords[i]) for i in vch if side[i] == 1), reverse=True)
        r = [1] + ins + [n - 1] + out
        # canonical up to rotation and reversal
        cands = []
        for rr in (r, r[::-1]):
            i = rr.index(1); cands.append(tuple(rr[i:] + rr[:i]))
        rots.add(min(cands))
    return rots


t0 = time.time()
H = [(i, (i + 1) % n) for i in range(n)]
stats = dict(n=n, graphs=0, planar_graphs=0, labelled=0)
for a in (-2, -1):
    stats[f'a{a}_closed'] = 0; stats[f'a{a}_hamarc_in_scc'] = 0
outf = open(f'out/planar_census_n{n}.jsonl', 'w')
for S in itertools.combinations(range(2, n - 1), 3):
    R = [u for u in range(1, n) if u not in S]
    for C in chord_matchings(R):
        stats['graphs'] += 1
        chords = [(0, s) for s in S] + C
        rots = rotations(chords)
        if not rots: continue
        stats['planar_graphs'] += 1
        edges = H + chords
        inc = [[] for _ in range(n)]
        for e, (x, y) in enumerate(edges): inc[x].append(e); inc[y].append(e)
        P = pms(edges, inc); NP = len(P)
        Pm = np.array([[(p >> e) & 1 for e in range(len(edges))] for p in P], dtype=np.int32)
        Dm = (Pm @ Pm.T) == 0
        nbr = {}
        for e in inc[0]:
            x, y = edges[e]; nbr[y if x == 0 else x] = e
        vedge = [next(e for e in inc[0] if (p >> e) & 1) for p in P]
        ccache = {}
        for rot in rots:
            stats['labelled'] += 1
            labof = {nbr[w]: s for s, w in enumerate(rot)}
            lab = np.array([labof[e] for e in vedge])
            rec = dict(rot=list(rot), chords=chords, nPM=NP)
            for a in (-2, -1):
                A = Dm & (lab[None, :] == (lab[:, None] + a) % 5)
                ncc, cc = connected_components(A, directed=True, connection='strong')
                ii, jj = np.nonzero(A)
                inscc = [(i, j) for i, j in zip(ii, jj) if cc[i] == cc[j]]
                if not inscc: continue
                stats[f'a{a}_closed'] += 1
                comps = set()
                for i, j in inscc:
                    key = (min(i, j), max(i, j))
                    if key not in ccache: ccache[key] = ncomp(P[i], P[j], edges)
                    comps.add(ccache[key])
                if 1 in comps: stats[f'a{a}_hamarc_in_scc'] += 1
                X = A.astype(np.int64); Lset = []; Pw = np.eye(NP, dtype=np.int64)
                for L in range(1, LMAX + 1):
                    Pw = ((Pw @ X) > 0).astype(np.int64)
                    if np.trace(Pw) > 0: Lset.append(L)
                rec[f'a{a}'] = dict(L=Lset, comps=sorted(comps),
                                   scc_sizes=sorted([int((cc == c).sum()) for c in set(cc[i] for i, j in inscc)]))
            if 'a-2' in rec or 'a-1' in rec: outf.write(json.dumps(rec) + '\n')
outf.close()
stats['sec'] = round(time.time() - t0, 1)
print(json.dumps(stats), flush=True)
