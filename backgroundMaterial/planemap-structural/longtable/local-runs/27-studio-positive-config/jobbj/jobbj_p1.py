#!/usr/bin/env python3
"""Job BJ (1): charge-back P1 variants at every hit-graph hole with a Gamma-cycle (any link pattern), both orientations, all states (lib26.Eng + Space).
Exits: lockless sigma-images of DD endpoints of positive cycles (Job AQ convention), credit 3f - 1; rem(T) = Lambda(T) + credits on T; charge-back of rem > 0 to sources;
def'(Z) = Lambda(Z) - CrN(Z) + charge(Z). Single-target assignment (backtracking) with candidate targets = (P1) sigma-neighbours of Z with rem < 0; (P1g) ANY nonpositive cycle with
rem < 0 in Z's sigma-group; (P1u) any such cycle in Z's (sigma u sigma')-group."""
import sys, os, json
from fractions import Fraction
from collections import defaultdict, Counter
from multiprocessing import Pool
HERE = os.path.dirname(os.path.abspath(__file__))
for d in ('../jobaq', '../../26-transport-adversarial', '../../25-transport', '../../common', '../../22-winding-escape'): sys.path.insert(0, os.path.join(HERE, d))
import jobaq
from kempe_py import Space
def job(args):
    g, hole, mirror = args
    jobaq.GDIR = os.path.join(HERE, '../jobbi/hitgraphs/')
    E, adj, link, w = jobaq.load(g, hole, mirror); li = E.li
    sp = Space({v: set(a) for v, a in adj.items()}, hole, link=link); done = set(); out = []
    def lockless(s):
        if E.is_filled(s): return False
        return E.dl_info(s) is None and not any(True for _ in []) and _ll(s)
    def _ll(s):
        from collections import Counter as C
        c = [s[i] for i in li]; cnt = C(c); j = next(j for j in range(5) if c[j] == c[(j + 2) % 5] and cnt[c[j]] == 2); mu, A, B = c[(j + 1) % 5], c[(j + 3) % 5], c[(j + 4) % 5]
        return not (E.comp(s, li[(j + 1) % 5], mu, A) >> li[(j + 3) % 5] & 1) and not (E.comp(s, li[(j + 1) % 5], mu, B) >> li[(j + 4) % 5] & 1)
    def sigma(s):
        c = [s[i] for i in li]; cnt = Counter(c); j = next(j for j in range(5) if c[j] == c[(j + 2) % 5] and cnt[c[j]] == 2); al, mu = c[j], c[(j + 1) % 5]
        return E.swap(s, E.comp(s, li[(j + 1) % 5], al, mu), al, mu)
    for s0 in sp.states:
        if s0 in done: continue
        mem = E.bfs(s0); done |= set(mem); pi = {x: E.pi_of(x) for x in mem}
        cyc = {}; cycles = []
        for x in mem:
            if x in cyc: continue
            z = []; y = x
            while y not in cyc: cyc[y] = len(cycles); z.append(y); y = pi[y][0]
            cycles.append(z)
        W = [sum(pi[y][1] for y in z) // 5 for z in cycles]
        DL = {x: E.dl_info(x) is not None for x in mem}
        if not any(all(DL[x] for x in z) for z in cycles): continue
        pinv = {pi[x][0]: x for x in mem}; isDD = lambda x: DL[x] and (DL[pi[x][0]] or DL[pinv[x]])
        def fafter(s):
            y = pi[s][0]; f = 0
            while E.is_filled(y): f += 1; y = pi[y][0]
            return f
        sig = defaultdict(set); exits = {}; n = len(cycles); up1 = list(range(n)); up2 = list(range(n))
        def fd(up, u):
            while up[u] != u: up[u] = up[up[u]]; u = up[u]
            return u
        for x in mem:
            if not isDD(x): continue
            s = sigma(x); a, b = cyc[x], cyc[s]
            if a != b:
                sig[a].add(b); sig[b].add(a); up1[fd(up1, a)] = fd(up1, b); up2[fd(up2, a)] = fd(up2, b)
                if W[a] > 0 and not E.is_filled(s) and _ll(s): exits.setdefault(s, (a, 3 * fafter(s) - 1))
            for t, p, q, K in E.moves(x):
                if t == x or K & E.linkmask or DL[t] or cyc[t] == a: continue
                up2[fd(up2, a)] = fd(up2, cyc[t])
        src = defaultdict(lambda: defaultdict(int)); crN = defaultdict(int)
        for s, (a, cr) in exits.items():
            if W[cyc[s]] <= 0: src[cyc[s]][a] += cr; crN[a] += cr
        rem = {t: 5 * W[t] + sum(src[t].values()) for t in range(n) if W[t] <= 0}
        charge = defaultdict(Fraction)
        for t, r in rem.items():
            if r > 0 and src[t]:
                tot = sum(src[t].values())
                for a, cr in src[t].items(): charge[a] += Fraction(r * cr, tot)
        cap = {t: Fraction(-r) for t, r in rem.items() if r < 0}
        res = {}
        for name, cand in (('P1', lambda z: [t for t in sig[z] if t in cap]), ('P1g', lambda z: [t for t in cap if fd(up1, t) == fd(up1, z)]), ('P1u', lambda z: [t for t in cap if fd(up2, t) == fd(up2, z)])):
            defs = sorted([(z, 5 * W[z] - crN[z] + charge[z], cand(z)) for z in range(n) if W[z] > 0 and 5 * W[z] - crN[z] + charge[z] > 0], key=lambda d: -d[1]); used = defaultdict(Fraction)
            def bt(i):
                if i == len(defs): return True
                z, d, nb = defs[i]
                for t in sorted(nb, key=lambda t: -(cap[t] - used[t])):
                    if cap[t] - used[t] >= d:
                        used[t] += d
                        if bt(i + 1): return True
                        used[t] -= d
                return False
            res[name] = bt(0); res['n_deficit_' + name] = len(defs)
        out.append(dict(graph=g, hole=hole, orientation='mirror' if mirror else 'plantri', linkdeg=sorted(len(adj[x]) for x in link), class_states=len(mem), **res))
    return out
if __name__ == '__main__':
    G = json.load(open(os.path.join(HERE, 'gamma-holes.json')))
    jobs = [(g, h, ori == 'mirror') for g, h, ori, pat in G]
    with Pool(12) as P: res = [x for xs in P.map(job, jobs) for x in xs]
    json.dump(res, open(os.path.join(HERE, 'jobbj-p1.json'), 'w'))
    c = Counter()
    for r in res:
        for k in ('P1', 'P1g', 'P1u'): c['%s holds: %s' % (k, r[k])] += 1
        c['classes with a deficit cycle (P1 sense): %s' % (r['n_deficit_P1'] > 0)] += 1
    print('Gamma classes:', len(res), dict(c))
