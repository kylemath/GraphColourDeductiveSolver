#!/usr/bin/env python3
"""Track P Part B data checks along law-respecting R-cycles (any graph).  For each cycle s_0..s_{L-1}:
 (I)  N(s) - B(s) = 3 nv - |E(G-h)| at every state, B = total cycle rank of the six pair graphs  [identity]
 (M)  monodromy rho (colour permutation with s_L = rho o s_0 as actual colourings), and: edges whose Q-label (perfect
      matching of K4 containing its colour pair) changes at step t <=> exactly one end in K_t; every edge's label after L
      steps is rho(label) -> if rho != id every edge has exactly one end in some K_t.
 (S)  per step: |K_t|, (#alpha, #A) in K_t, signed degree sum sum_{K_alpha}(deg-1) - sum_{K_A}(deg-1), colour class sizes
usage: tp_struct.py FILE [--max K]"""
import sys, json, collections
from tn_lib import Engine
from tn_forest import parse_dump, cycles_in_R_law, components, PAIRS
MT = [[-1, 0, 1, 2], [0, -1, 2, 1], [1, 2, -1, 0], [2, 1, 0, -1]]

def betti(n, E, col):
    B = 0; N = 0
    for (p, q) in PAIRS:
        V = [v for v in range(1, n) if col[v] in (p, q)]
        Es = [tuple(e) for e in E if all(col[x] in (p, q) for x in e)]
        cs = components(V, Es); N += len(cs); B += len(Es) - len(V) + len(cs)
    return N, B

def main():
    args = sys.argv[1:]; mx = 10 ** 9
    if '--max' in args: k = args.index('--max'); mx = int(args[k + 1]); del args[k:k + 2]
    eng = Engine(dump=True, maxstates=200000); cnt = 0; agg = collections.Counter()
    for f in args:
        for l in open(f):
            if cnt >= mx: break
            if l.startswith('{'):
                d = json.loads(l); l = d.get('graph')
                if not l: continue
            p = l.split(); rot = [list(map(int, r.split(','))) for r in p[2].split(';')]; n = len(rot)
            E = {frozenset((u, v)) for u in range(1, n) for v in rot[u] if v != 0}
            js, tn, dump = eng.run(l)
            if tn is None: continue
            S = parse_dump(dump)
            for C in cycles_in_R_law(S, True)[:1]:
                cnt += 1; L = len(C)
                cols = [[-1 if ch == '-' else int(ch) for ch in S[x]['col']] for x in C]
                const = 3 * (n - 1) - len(E); ok_I = True; Bs = []
                for c in cols:
                    N, B = betti(n, E, c); Bs.append(B)
                    if N - B != const: ok_I = False
                # actual colourings: re-derive by applying swaps; find K_t as the set of vertices whose colour changes up to the renaming
                # reconstruct actual colouring sequence: a_0 = cols[0]; a_{t+1} = swap of K_{alpha A}(x_{j+2}) in a_t
                a = list(cols[0]); seq = [a]; Ks = []
                adj = [[] for _ in range(n)]
                for e in E:
                    u, v = tuple(e); adj[u].append(v); adj[v].append(u)
                for t in range(L):
                    lc = [a[i] for i in range(1, 6)]
                    j = [i for i in range(5) if lc[i] == lc[(i + 2) % 5]][0]
                    al, A = lc[j], lc[(j + 3) % 5]; x2 = 1 + (j + 2) % 5
                    K = {x2}; st = [x2]
                    while st:
                        x = st.pop()
                        for y in adj[x]:
                            if y not in K and a[y] in (al, A): K.add(y); st.append(y)
                    b = list(a)
                    for v in K: b[v] = A if a[v] == al else al
                    Ks.append((K, al, A, sum(1 for v in K if a[v] == al)))
                    a = b; seq.append(a)
                # check seq matches cols up to renaming, and monodromy
                def norm(c):
                    mp = {}; return tuple(mp.setdefault(x, len(mp)) if x >= 0 else -1 for x in c)
                match = all(norm(seq[t]) == norm(cols[t % L]) for t in range(L + 1))
                rho = {}
                for v in range(1, n): rho[seq[0][v]] = seq[L][v]
                al0 = Ks[0][1]
                lab = lambda c, e: MT[c[min(e)]][c[max(e)]]
                cut = set()
                for t, (K, al, A, ka) in enumerate(Ks):
                    for e in E:
                        u, v = tuple(e)
                        ch = lab(seq[t], e) != lab(seq[t + 1], e)
                        one = (u in K) != (v in K)
                        if ch != one: agg['labelchange_mismatch'] += 1
                        if one: cut.add(e)
                # (C) cut balance and role windings.  role label of an edge at t: 0 = P1 (matching of {alpha,mu_t}), 1 = P2, 2 = P3
                def roles(c):
                    lc = [c[i] for i in range(1, 6)]; j = [i for i in range(5) if lc[i] == lc[(i + 2) % 5]][0]
                    al, mu, A, B = lc[j], lc[(j + 1) % 5], lc[(j + 3) % 5], lc[(j + 4) % 5]
                    return {MT[al][mu]: 0, MT[al][A]: 1, MT[al][B]: 2}
                wind = {e: 0 for e in E}; cbal_ok = True
                for t, (K, al, A, ka) in enumerate(Ks):
                    r0, r1 = roles(seq[t]), roles(seq[t + 1])
                    cp1 = cp3 = cp2 = 0; Ecnt0 = [0, 0, 0]; Ecnt1 = [0, 0, 0]
                    for e in E:
                        a0 = r0[lab(seq[t], e)]; a1 = r1[lab(seq[t + 1], e)]; Ecnt0[a0] += 1; Ecnt1[a1] += 1
                        u, v = tuple(e)
                        if (u in K) != (v in K):
                            if a0 == 0: cp1 += 1
                            elif a0 == 2: cp3 += 1
                            else: cp2 += 1
                            inc = {0: 0, 2: -1}.get(a0, 99)
                        else: inc = 1
                        if (a0 + inc) % 3 != a1: agg['winding_rule_fail'] += 1
                        wind[e] += inc
                    if cp2: agg['cut_P2_edges'] += 1
                    if cp1 - cp3 != Ecnt1[0] - Ecnt0[2]: cbal_ok = False
                agg['cutbalance_ok'] += cbal_ok
                agg['winding_div3_fail'] += sum(1 for e in E if wind[e] % 3)
                swapped = set().union(*[K for K, _, _, _ in Ks])
                nonal_unswapped = [v for v in range(1, n) if seq[0][v] != al0 and v not in swapped]
                rho_id = all(rho[x] == x for x in rho)
                deg = [len(adj[v]) for v in range(n)]
                sd = [sum(deg[v] - 1 for v in K if seq[t][v] == al) - sum(deg[v] - 1 for v in K if seq[t][v] != al) for t, (K, al, A, ka) in enumerate(Ks)]
                Nprof = ''.join(str(S[x]['N']) for x in C)
                rec = dict(src=p[0], n=n, E=len(E), excess=len(E) - (3 * (n - 1) - 8), L=L, Nprof=Nprof, identity=ok_I, B=''.join(map(str, Bs)), seqmatch=match,
                           rho_id=rho_id, edges_cut=len(cut), edges=len(E), nonalpha_unswapped=len(nonal_unswapped), alpha_never=sum(1 for v in range(1, n) if seq[0][v] == al0 and v not in swapped),
                           Ksizes=[len(K) for K, _, _, _ in Ks], Kalpha=[ka for _, _, _, ka in Ks], signed_deg=sd, windings=sorted(collections.Counter(w // 3 for w in wind.values()).items()),
                           alpha_size=[sum(1 for v in range(1, n) if seq[t][v] == al0) for t in range(L)])
                print(json.dumps(rec), flush=True)
                agg['cycles'] += 1; agg['identity_ok'] += ok_I; agg['seqmatch'] += match; agg['rho_id'] += rho_id; agg['all_edges_cut'] += (len(cut) == len(E))
                agg['nonalpha_all_swapped'] += (len(nonal_unswapped) == 0)
    print('AGG', json.dumps(agg))

if __name__ == '__main__':
    main()
