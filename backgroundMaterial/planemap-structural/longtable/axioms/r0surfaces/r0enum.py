"""Exhaustive R0 census in the Hamiltonian normal form, ALL cycle lengths at once (Long Table, r0surfaces).

Normal form (as sat_t1v.py): H = 0,1,...,n-1, v = 0, f2 = (0,1) = h_0 in M_0 (even H edges),
f0 = (0,n-1) = h_{n-1} in M_1 (odd H edges); G = H + C, C = 3 chords at v (labelled f1, f3, f4 in all
3! ways) + a perfect matching of the other cubic vertices by non-H chords.  Every R0 configuration
(G, M_0..M_{L-1}) with M_0 u M_1 Hamiltonian has exactly this form, for every L.

Reformulation used [proved, hand]: let D be the digraph on the perfect matchings of G with an arc M -> M'
iff M n M' = 0 and k(M') = k(M) - 2 (k = label of the v-edge).  Any closed walk of D has length = 0 mod 5,
and a closed R0 sequence through the Hamiltonian pair (M_0, M_1) of any length L is exactly a closed walk
through the arc M_0 -> M_1.  So R0 fails on G  <=>  M_0 is reachable from M_1 in D.

Variants (also all L):
  V2 'ham-even': M_{2j} u M_{2j+1} Hamiltonian for every j  (closed walk of D2 = Aham.A through M_0, first
                 Ham arc M_0 -> M_1);
  V3 'word1212': V2 + M_{2j+1} u M_{2j+2} has exactly 2 components (the NRC word without DL).
Output jsonl: one line per violating labelled graph: line (TrackU format), lengths L <= LMAX for R0 / V2 / V3.
usage: r0enum.py n [LMAX] [--max-graphs K]"""
import sys, json, time, itertools
import numpy as np

n = int(sys.argv[1]); LMAX = int(sys.argv[2]) if len(sys.argv) > 2 and sys.argv[2].isdigit() else 40


def chord_matchings(R):
    if not R: yield []; return
    a = R[0]
    for i in range(1, len(R)):
        b = R[i]
        if abs(a - b) == 1 or {a, b} == {0, n - 1}: continue
        rest = R[1:i] + R[i + 1:]
        for m in chord_matchings(rest): yield [(a, b)] + m


def pms(edges, inc):
    out = []; used = [False] * n
    def rec(mask):
        x = next((u for u in range(n) if not used[u]), None)
        if x is None: out.append(mask); return
        used[x] = True
        for e in inc[x]:
            a, b = edges[e]; y = b if a == x else a
            if not used[y]:
                used[y] = True; rec(mask | (1 << e)); used[y] = False
        used[x] = False
    rec(0); return out


def ncomp_union(p, q, edges):
    adj = [[] for _ in range(n)]
    for e, (a, b) in enumerate(edges):
        if (p >> e) & 1 or (q >> e) & 1: adj[a].append(b); adj[b].append(a)
    seen = [False] * n; c = 0
    for s in range(n):
        if seen[s]: continue
        c += 1; st = [s]; seen[s] = True
        while st:
            x = st.pop()
            for y in adj[x]:
                if not seen[y]: seen[y] = True; st.append(y)
    return c


def lengths_from(A_first_targets, Astep, target, LMAX, step=1, offset=1):
    """set of L <= LMAX with a walk: start set at length `offset`, each Astep adds `step` to L, reach target."""
    Ls = []; x = A_first_targets.copy(); L = offset
    while L <= LMAX:
        if x[target]: Ls.append(L)
        x = (x.astype(np.int32) @ Astep.astype(np.int32)) > 0
        L += step
        if not x.any(): break
    return Ls


def reach(start_vec, A, target):
    seen = start_vec.copy(); fr = start_vec.copy()
    while fr.any():
        nx_ = ((fr.astype(np.int32) @ A.astype(np.int32)) > 0) & ~seen
        seen |= nx_; fr = nx_
    return bool(seen[target])


t0 = time.time()
H = [(i, (i + 1) % n) for i in range(n)]
ngraph = nlab = nviol = nv2 = nv3 = 0
maxg = None
if '--max-graphs' in sys.argv: maxg = int(sys.argv[sys.argv.index('--max-graphs') + 1])
out = open(f'out/r0enum_n{n}.jsonl', 'w')
for S in itertools.combinations(range(2, n - 1), 3):
    R = [u for u in range(1, n) if u not in S]
    for C in chord_matchings(R):
        ngraph += 1
        if maxg and ngraph > maxg: break
        edges = H + [(0, s) for s in S] + C
        m = len(edges)
        inc = [[] for _ in range(n)]
        for e, (a, b) in enumerate(edges): inc[a].append(e); inc[b].append(e)
        P = pms(edges, inc)
        M0 = sum(1 << i for i in range(0, n, 2)); M1 = sum(1 << i for i in range(1, n, 2))
        i0, i1 = P.index(M0), P.index(M1)
        Pm = np.array([[(p >> e) & 1 for e in range(m)] for p in P], dtype=np.int32)
        D = (Pm @ Pm.T) == 0
        vedge_of = []
        vE = inc[0]
        for p in P: vedge_of.append(next(e for e in vE if (p >> e) & 1))
        vedge_of = np.array(vedge_of)
        chord_e = {s: n + j for j, s in enumerate(S)}
        cache = {}
        def nc(p, q):
            k = (p, q) if p < q else (q, p)
            if k not in cache: cache[k] = ncomp_union(P[p], P[q], edges)
            return cache[k]
        for perm in itertools.permutations(S):
            nlab += 1
            fv = [n - 1, chord_e[perm[0]], 0, chord_e[perm[1]], chord_e[perm[2]]]
            labof = {e: s for s, e in enumerate(fv)}
            lab = np.array([labof[e] for e in vedge_of])
            A = D & (lab[None, :] == (lab[:, None] - 2) % 5)
            st = np.zeros(len(P), bool); st[i1] = True
            if not reach(st, A, i0): continue
            nviol += 1
            Ls = lengths_from(st, A, i0, LMAX, offset=1)   # walk M_1 ->...-> M_0 of j steps: L = j + 1
            # Ham / 2-comp arcs restricted to the support of A
            Ah = np.zeros_like(A); A2 = np.zeros_like(A)
            for p, q in zip(*np.nonzero(A)):
                c = nc(p, q)
                if c == 1: Ah[p, q] = True
                if c == 2: A2[p, q] = True
            res = {}
            for name, Aodd in (('V2', A), ('V3', A2)):
                st2 = Aodd[i1].copy()          # B in succ(M_1)
                D2 = ((Ah.astype(np.int32) @ Aodd.astype(np.int32)) > 0)
                ok = reach(st2, D2, i0) if st2.any() else False
                res[name] = ok
                if ok:
                    res[name + '_L'] = [2 + 2 * j for j in lengths_from(st2, D2, i0, LMAX, offset=0) if 2 + 2 * j <= LMAX]
            nv2 += res['V2']; nv3 += res['V3']
            line = ' '.join(map(str, [n, m] + [x for e in edges for x in e] + fv))
            out.write(json.dumps(dict(line=line, R0_L=Ls, **res)) + '\n')
    if maxg and ngraph > maxg: break
out.close()
print(json.dumps(dict(n=n, graphs=ngraph, labelled=nlab, R0_viol=nviol, V2_viol=nv2, V3_viol=nv3,
                      sec=round(time.time() - t0, 1))), flush=True)
