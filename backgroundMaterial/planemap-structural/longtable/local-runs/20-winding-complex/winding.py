#!/usr/bin/env python3
"""[exploratory] Extend the NightEulerHole winding lambda to all Kempe swaps and test closedness. See README.md."""
import sys, json, itertools, math
from collections import defaultdict, Counter
sys.path.insert(0, '../common')
from kempe_py import Space, gentri_rotation, adj_from_rot

GENTRI = '../../../studiointel/gentri/tri%d.txt'
FA = {0: 0, 1: 1, 4: -1, 2: -3, 3: 3}     # convention A: the note's lift (R+3:+1, phiA/phiB^-1:-1, tau:-3), odd-extended
FC = {0: 0, 1: 1, 2: 2, 3: -2, 4: -1}     # convention C: centred lift into -2..2

def tokens(s, linki):
    ts = [s[linki[k]] ^ s[linki[(k + 1) % 5]] for k in range(5)]   # Tait colour = XOR of colour labels 0..3
    cnt = Counter(ts); assert sorted(cnt.values()) == [1, 1, 3], cnt
    return sorted(k for k in range(5) if cnt[ts[k]] == 1)

def sigma_state(s, linki):
    tk = tokens(s, linki); return sum(tk) % 5, (tk[1] - tk[0]) % 5 in (1, 4)   # sigma, filled?

def rawswap(s, K, p, q, N):
    d = list(s)
    for i in range(N):
        if K >> i & 1: d[i] = q if s[i] == p else p
    return tuple(d)

def analyse(sp, out, tag):
    N = sp.N; linki = sp.linki; S = len(sp.states)
    sig = []; fil = []
    for s in sp.states:
        a, b = sigma_state(s, linki); sig.append(a); fil.append(b)
    for k in range(S): assert fil[k] == sp.filled(k)
    def comp_of(sraw, p, q, v):
        for K in sp.components(sraw, p, q):
            if K >> v & 1: return K
    pi = [None] * S; pitab = [0] * S
    for k, s in enumerate(sp.states):
        x = [s[i] for i in linki]
        if fil[k]:
            cnt = Counter(x); i = [j for j in range(5) if cnt[x[j]] == 1][0]
            W, X, Y = x[i], x[(i + 1) % 5], x[(i + 2) % 5]
            Z = ({0, 1, 2, 3} - {W, X, Y}).pop()
            assert x[(i + 3) % 5] == X and x[(i + 4) % 5] == Y
            v2 = linki[(i + 2) % 5]; v4 = linki[(i + 4) % 5]
            K = comp_of(s, Y, Z, v2)
            if not (K >> v4 & 1):   # M3 short: phi_A
                t = sp.index[sp.canon(rawswap(s, K, Y, Z, N))]; pitab[k] = -1
            else:                   # M3 long: tau
                K = comp_of(s, W, X, linki[(i + 3) % 5]); t = sp.index[sp.canon(rawswap(s, K, W, X, N))]; pitab[k] = -3
        else:
            j = [j for j in range(5) if x[j] == x[(j + 2) % 5]][0]
            al, mu, A, B = x[j], x[(j + 1) % 5], x[(j + 3) % 5], x[(j + 4) % 5]
            vm = linki[(j + 1) % 5]; vb = linki[(j + 4) % 5]
            if comp_of(s, mu, B, vm) >> vb & 1:   # lock 2: R+3
                K = comp_of(s, al, A, linki[(j + 2) % 5]); t = sp.index[sp.canon(rawswap(s, K, al, A, N))]; pitab[k] = 1
            else:                                  # phi_B^-1
                K = comp_of(s, mu, B, vb); t = sp.index[sp.canon(rawswap(s, K, mu, B, N))]; pitab[k] = -1
        pi[k] = t
    mv = [sp.moves(k) for k in range(S)]
    nb = [sorted({t for t, *_ in mv[k] if t != k}) for k in range(S)]
    sp.G = nb; cl, ncl = sp.classes()
    members = defaultdict(list)
    for k in range(S): members[cl[k]].append(k)
    for c, mem in members.items():
        R = {}
        D = lambda s, t: (sig[t] - sig[s]) % 5
        wA = lambda s, t: FA[D(s, t)]
        wC = lambda s, t: FC[D(s, t)]
        # (a) antisymmetry and symmetry of the swap relation
        asyA = asyC = 0
        for s in mem:
            for t in nb[s]:
                assert s in nb[t]
                asyA += wA(s, t) + wA(t, s) != 0; asyC += wC(s, t) + wC(t, s) != 0
        R['asym_fail_A'] = asyA; R['asym_fail_C'] = asyC
        pi_ok = all(pi[s] is not None for s in mem)
        R['pi_is_perm'] = pi_ok and sorted(pi[s] for s in mem) == sorted(mem)
        # (b) commuting squares
        sqs = []
        sqfail = Counter(); sqtot = Counter()
        for s in mem:
            m = mv[s]; sraw = sp.states[s]
            for i in range(len(m)):
                t1, p1, q1, K1 = m[i]
                if t1 == s: continue
                for j in range(i + 1, len(m)):
                    t2, p2, q2, K2 = m[j]
                    if t2 == s or t2 == t1 or K1 & K2: continue
                    r1 = rawswap(sraw, K1, p1, q1, N); r2 = rawswap(sraw, K2, p2, q2, N)
                    if K2 not in sp.components(r1, p2, q2) or K1 not in sp.components(r2, p1, q1): continue
                    u = sp.index[sp.canon(rawswap(r1, K2, p2, q2, N))]
                    if u == s or u == t1 or u == t2: continue
                    rel = 'same' if {p1, q1} == {p2, q2} else ('share' if {p1, q1} & {p2, q2} else 'disj')
                    A = wA(s, t1) + wA(t1, u) - wA(s, t2) - wA(t2, u)
                    C = wC(s, t1) + wC(t1, u) - wC(s, t2) - wC(t2, u)
                    ds = (D(s, t1), D(t1, u), D(s, t2), D(t2, u))
                    nz = tuple(int(x != 0) for x in ds)
                    key = (rel, nz)
                    fk = ''.join('F' if fil[x] else 'U' for x in (s, t1, u, t2))
                    sqtot[key] += 1
                    if A or C:
                        sqfail[key + ((A, C), ds, fk)] += 1
                    sqs.append((s, t1, u, t2))
        R['squares'] = sum(sqtot.values()); R['square_fail_any'] = sum(sqfail.values())
        R['square_fail_detail'] = {str(k): v for k, v in sqfail.items()}
        R['square_tot_by_key'] = {str(k): v for k, v in sqtot.items()}
        R['square_fail_A'] = sum(v for k, v in sqfail.items() if k[2][0]); R['square_fail_C'] = sum(v for k, v in sqfail.items() if k[2][1])
        # (c) triangles and 4-cycles (simple graph, distinct vertices)
        nbs = {s: set(nb[s]) for s in mem}
        tri = [0, 0, 0]; c4 = [0, 0, 0]   # total, failA, failC
        for s in mem:
            for t1, t2 in itertools.combinations(nb[s], 2):
                if s < t1 and s < t2 and t2 in nbs[t1]:
                    tri[0] += 1
                    a = wA(s, t1) + wA(t1, t2) + wA(t2, s); cc = wC(s, t1) + wC(t1, t2) + wC(t2, s)
                    tri[1] += a != 0; tri[2] += cc != 0
                if s < t1 and s < t2:
                    for u in nbs[t1] & nbs[t2]:
                        if u > s and u != t1 and u != t2:
                            c4[0] += 1
                            a = wA(s, t1) + wA(t1, u) + wA(u, t2) + wA(t2, s)
                            cc = wC(s, t1) + wC(t1, u) + wC(u, t2) + wC(t2, s)
                            c4[1] += a != 0; c4[2] += cc != 0
        R['tri'] = tri; R['c4'] = c4
        # (d) potential: spanning tree, inconsistent non-tree edges, gcd of cycle windings
        for name, w in (('A', wA), ('C', wC)):
            root = mem[0]; Phi = {root: 0}; par = {root: None}; q = [root]
            for x in q:
                for t in nb[x]:
                    if t not in Phi: Phi[t] = Phi[x] + w(x, t); par[t] = x; q.append(t)
            ntree = len(mem) - 1; bad = 0; g = 0; edges = 0; omegas = []
            for s in mem:
                for t in nb[s]:
                    if s < t:
                        edges += 1
                        if par.get(t) == s or par.get(s) == t: continue
                        om = Phi[s] + w(s, t) - Phi[t]
                        if om: bad += 1; g = math.gcd(g, abs(om)); omegas.append(om)
            if name == 'C':
                gh = {}
                for s in mem:
                    for t in nb[s]:
                        gh[(s, t)] = (Phi[s] + w(s, t) - Phi[t]) // 5   # holonomy-gauge increment, nonzero only on non-tree edges
                srcs = sorted({x for (a, b), v in gh.items() if v for x in (a, b)})[:60]
                best = None
                for s0 in srcs:
                    dist = {(s0, 0): 0}; qq = [(s0, 0)]; hit = None
                    for (x, o) in qq:
                        d0 = dist[(x, o)]
                        if best is not None and d0 + 1 >= best: break
                        for t in nb[x]:
                            st = (t, o + gh[(x, t)])
                            if st not in dist:
                                dist[st] = d0 + 1; qq.append(st)
                                if t == s0 and st[1] != 0: hit = d0 + 1; break
                        if hit: break
                    if hit and (best is None or hit < best): best = hit
                R['girth_C'] = best
            R['d_' + name] = dict(states=len(mem), edges=edges, cycle_rank=edges - ntree, inconsistent=bad, gcd=g,
                                  omega_pos=sum(o > 0 for o in omegas), omega_neg=sum(o < 0 for o in omegas))
        # pi-cycles (QFB/NightEulerHole table) and winding
        seen = set(); cyc = []; lam_bad = 0
        for s0 in mem:
            if s0 in seen: continue
            path = [s0]; seen.add(s0); x = pi[s0]
            while x != s0: path.append(x); seen.add(x); x = pi[x]
            L = len(path)
            w5 = sum(wA(path[i], path[(i + 1) % L]) for i in range(L))
            wc5 = sum(wC(path[i], path[(i + 1) % L]) for i in range(L))
            cyc.append(dict(L=L, F=sum(fil[x] for x in path), w5=w5, w=w5 / 5, wC5=wc5, t=sum(1 for i in range(L) if wA(path[i], path[(i + 1) % L]) == -3)))
        for s in mem:
            if wA(s, pi[s]) != pitab[s]: lam_bad += 1
        R['lambda_table_mismatch'] = lam_bad
        R['pi_cycles'] = cyc
        R['classUF'] = (sum(not fil[x] for x in mem), sum(fil[x] for x in mem))
        U, F = R['classUF']
        R['thmW_ok'] = (sum(c['w5'] for c in cyc) == U - 3 * F) and all(c['w5'] % 5 == 0 for c in cyc)
        R['hasPos'] = any(c['w5'] > 0 for c in cyc)
        R['hasNeg'] = any(c['w5'] < 0 for c in cyc)
        R['tag'] = tag
        out.write(json.dumps(R) + '\n'); out.flush()

if __name__ == '__main__':
    orders = [int(a) for a in sys.argv[1:]]
    for n in orders:
        lines = [l for l in open(GENTRI % n) if l.startswith('G')]
        with open('out-%d.jsonl' % n, 'w') as out:
            for gi, line in enumerate(lines, 1):
                rot = gentri_rotation(line); adj = adj_from_rot(rot)
                for h in range(len(rot)):
                    if len(rot[h]) != 5: continue
                    sp = Space(adj, h, link=rot[h])
                    analyse(sp, out, dict(order=n, gentri=gi, hole=h))
