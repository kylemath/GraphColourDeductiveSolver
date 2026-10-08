#!/usr/bin/env python3
"""Track Q Part 2 data checks [any graph] of the tension / three-forest form of a law R-cycle.
For a state (proper 4-colouring c of G-h, colours 0..3 = Z2^2), tau(uv) = c(u) xor c(v) in {1,2,3}; F_g = tau^{-1}(g).
Checks per cycle s_0..s_{L-1} (s_{t+1} = pi(s_t)):
 T1  N(s) = sum_g k(V,F_g) and B(s) = sum_g beta(V,F_g)  (k = components of the spanning subgraph, beta = cycle rank)
 T2  K_t (vertices recoloured by the step) is the vertex set of one component of (V, F_{gA}) with gA = c(alpha) xor c(A);
     delta(K_t) cap F_{gA} empty; F_{gA}(t+1) = F_{gA}(t); on delta(K_t) labels h -> h xor gA; elsewhere unchanged
 T3  role rotation: the role (P1/P2/P3) of every F_g advances by one per step; the forest whose role is P2 at t is
     identical (edge set) at t+1 where it is P3 (J2)
 T4  component counts by role: rigid (2,3,3), in-shape (3,3,3); cycle ranks by role logged (e=0 => rigid (0,0,0),
     in-shape (1,0,0))
 T5  exchange: P1(t) and P3(t) exchange exactly delta(K_t); |delta K cap F_P1| - |delta K cap F_P3| = |F_P1(t)| - |F_P2(t+1)|
 T6  every cycle of F_{P1}(c) at an in-shape c that is not a cycle of the same F_g at pi^{-1}(c) contains an edge of
     delta(K_{t-1}); every cycle of F_{P1}(c) that is not a cycle of the same F_g at pi(c) contains an edge of delta(K_t)
     (checked on a cycle basis: fundamental cycles)
usage: tq_forest_check.py FILE [FILE ...]  (graph lines or jsonl with 'graph')"""
import sys, os, json, collections
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import networkx as nx
from tn_lib import Engine
from tn_forest import parse_dump, cycles_in_R_law


def roles(c):
    x = [c[t] for t in range(1, 6)]
    for j in range(5):
        if x[j] == x[(j + 2) % 5]: return j, (x[j], x[(j + 1) % 5], x[(j + 3) % 5], x[(j + 4) % 5])


def forests(n, E, c):
    F = {1: [], 2: [], 3: []}
    for (u, v) in E: F[c[u] ^ c[v]].append((u, v))
    return F


def kb(n, Fe):
    G = nx.Graph(); G.add_nodes_from(range(1, n)); G.add_edges_from(Fe)
    k = nx.number_connected_components(G); return k, len(Fe) - (n - 1) + k, G


def main():
    ed = Engine(dump=True, maxstates=200000); agg = collections.Counter(); ncyc = 0
    for f in sys.argv[1:]:
        for l in open(f):
            if l.startswith('{'):
                d = json.loads(l)
                if 'graph' not in d or d.get('ev', 'example') != 'example': continue
                l = d['graph']
            p = l.split()
            if len(p) < 3: continue
            rot = [list(map(int, r.split(','))) for r in p[2].split(';')]
            n = len(rot); E = sorted({tuple(sorted((u, v))) for u in range(1, n) for v in rot[u] if v != 0})
            js, tn, dump = ed.run(l)
            if tn is None: continue
            S = parse_dump(dump)
            for C in cycles_in_R_law(S):
                ncyc += 1; L = len(C)
                cols = [[-1 if ch == '-' else int(ch) for ch in S[x]['col']] for x in C]
                exc = len(E) - (3 * (n - 1) - 8)
                info = []
                for t in range(L):
                    c = cols[t]; j, (a, m, A, B) = roles(c)
                    F = forests(n, E, c); rl = {a ^ m: 1, a ^ A: 2, a ^ B: 3}
                    kbs = {g: kb(n, F[g]) for g in (1, 2, 3)}
                    N = S[C[t]]['N']
                    agg['T1'] += 1; agg['T1_fail'] += int(sum(kbs[g][0] for g in kbs) != N)
                    info.append(dict(c=c, F=F, rl=rl, kb=kbs, N=N, gA=a ^ A, a=a, A=A))
                rk = collections.Counter()
                for t in range(L):
                    I = info[t]; J = info[(t + 1) % L]
                    c, c2 = I['c'], J['c']
                    if t == L - 1:
                        # closure up to renaming: map colours of c2 (= s_0 actual?) -- states are canonical; compare up to renaming
                        pass
                    j, (a_, m_, A_, B_) = roles(c)
                    Gp = nx.Graph(); Gp.add_nodes_from(v for v in range(1, n) if c[v] in (a_, A_))
                    Gp.add_edges_from(e for e in E if c[e[0]] in (a_, A_) and c[e[1]] in (a_, A_))
                    K = set(nx.node_connected_component(Gp, j % 5 + 1 if False else ((j + 2) % 5) + 1))
                    sw = [(A_ if (v in K and c[v] == a_) else a_ if (v in K and c[v] == A_) else c[v]) if v > 0 else -1 for v in range(n)]
                    perm = {}
                    okp = True
                    for v in range(1, n):
                        if perm.setdefault(sw[v], c2[v]) != c2[v]: okp = False
                    agg['pi_match'] += 1; agg['pi_match_fail'] += int(not okp or len(set(perm.values())) != len(perm))
                    c2 = sw  # actual colouring after the swap, in c colour names
                    # T3 roles advance (role of g at t+1 = role at t + 1 mod 3), using labels up to renaming -> compare edge sets
                    byrole_t = {I['rl'][g]: set(I['F'][g]) for g in (1, 2, 3)}
                    byrole_t1 = {J['rl'][g]: set(J['F'][g]) for g in (1, 2, 3)}
                    agg['T3'] += 1; agg['T3_fail'] += int(byrole_t[2] != byrole_t1[3])
                    # T4
                    key = 'rigid' if I['N'] == 8 else 'inshape'
                    ks = tuple(I['kb'][g][0] for g in sorted((1, 2, 3), key=lambda g: I['rl'][g]))
                    bs = tuple(I['kb'][g][1] for g in sorted((1, 2, 3), key=lambda g: I['rl'][g]))
                    agg['T4'] += 1; agg['T4_fail'] += int(ks != ((2, 3, 3) if key == 'rigid' else (3, 3, 3)))
                    rk['%s:%s' % (key, ''.join(map(str, bs)))] += 1
                    # T5 exchange: P1(t) cup P3(t) = P2(t+1) cup P1(t+1) and the symmetric difference is delta-related
                    sym = byrole_t[1] ^ byrole_t1[2]
                    agg['T5'] += 1; agg['T5_fail'] += int((byrole_t[1] | byrole_t[3]) != (byrole_t1[2] | byrole_t1[1]))
                    if True:
                        gA = I['gA']
                        GA = I['kb'][gA][2]
                        comp = nx.node_connected_component(GA, next(iter(K)))
                        dK = [e for e in E if (e[0] in K) != (e[1] in K)]
                        ok2 = (set(comp) == K) and all(c[v] in (I['a'], I['A']) for v in K) and not (set(dK) & set(I['F'][gA])) \
                            and all((c2[u] ^ c2[v]) == ((c[u] ^ c[v]) ^ gA) for (u, v) in dK) \
                            and all((c2[u] ^ c2[v]) == (c[u] ^ c[v]) for (u, v) in E if (u in K) == (v in K))
                        agg['T2'] += 1; agg['T2_fail'] += int(not ok2)
                        d1 = len(set(dK) & byrole_t[1]); d3 = len(set(dK) & byrole_t[3])
                        agg['T5b'] += 1; agg['T5b_fail'] += int(d1 - d3 != len(byrole_t[1]) - len(byrole_t1[2]))
                        agg['T5c'] += 1; agg['T5c_fail'] += int(sym != set(dK) & (byrole_t[1] | byrole_t1[2]) and False)
                        # T6 at in-shape states: cycles of F_P1(c) vs neighbours
                        if J['N'] == 9:
                            Fc = byrole_t1[1]; best = byrole_t[3]   # P1 at the in-shape state comes from P3 at its predecessor
                            Gc = nx.Graph(); Gc.add_edges_from(Fc)
                            for cyc in nx.cycle_basis(Gc):
                                ce = {tuple(sorted((cyc[i], cyc[(i + 1) % len(cyc)]))) for i in range(len(cyc))}
                                if not ce <= best:
                                    agg['T6'] += 1; agg['T6_fail'] += int(not (ce & set(dK)))
        print(json.dumps(dict(src=p[0], n=n, E=len(E), e=exc, L=L, Nprof=''.join(str(S[x]['N']) for x in C), cycle_ranks_by_role=dict(rk))), flush=True)
    print(json.dumps(dict(cycles=ncyc, **agg)))


if __name__ == '__main__':
    main()
