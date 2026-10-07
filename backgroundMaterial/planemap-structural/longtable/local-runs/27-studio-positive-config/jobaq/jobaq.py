#!/usr/bin/env python3
"""Job AQ: stress test of the F6 lemma chain on the night's adversarial graphs (studiointel/path3-local/run_dd/best-*.json), holes carrying Gamma-cycles in run 26's sample
(seed 1, 40 random colourings, classes by BFS), both orientations. Class engine = ../../26-transport-adversarial/lib26.Eng (canonical states over the BFS order).
Per class with a Gamma-cycle: (1) link degree pattern; (2) Lemma S with sigma-exits from all DD endpoints (C_neg, C_pos, D = Lambda); (3) period tuples / universal period
(single high-degree link vertex only); (4) A34' (consecutive k = 4 failures) and W2 (a period with R3 k = 2, 1, 0 all fixed); (5) sigma-C, charge-back P1 (undirected sigma
neighbours), sigma'-C (H1); (6) the quarter floor F >= |class| / 4 (equivalently sum w <= 0)."""
import sys, json, itertools, random
from fractions import Fraction
from collections import Counter, defaultdict
sys.path.insert(0, '../../26-transport-adversarial'); sys.path.insert(0, '../../25-transport'); sys.path.insert(0, '../../common'); sys.path.insert(0, '../../22-winding-escape')
from lib26 import Eng
D = '../../../../studiointel/path3-local/run_dd/'
ALLSTATES = False
def ALLSEEDS(E, adj, hole, link):
    from kempe_py import Space
    sp = Space({v: set(a) for v, a in adj.items()}, hole, link=link)
    assert sp.order == E.order
    return sp.states
GDIR = D
def load(gname, hole, mirror):
    faces = json.load(open(GDIR + 'best-%s.json' % gname))['faces']; adj = {}
    for t in faces:
        for a, b in itertools.combinations(t, 2): adj.setdefault(a, set()).add(b); adj.setdefault(b, set()).add(a)
    nxt = {}
    for t in faces:
        if hole in t: i = t.index(hole); nxt[t[(i + 1) % 3]] = t[(i + 2) % 3]
    s = min(nxt); link = [s]
    while nxt[link[-1]] != s: link.append(nxt[link[-1]])
    if mirror: link = [link[0]] + link[1:][::-1]
    E = Eng(adj, hole, link)
    # outer vertices w_t (third vertex of the face x_t x_{t+1} other than the hole)
    w = []
    for t in range(5):
        a, b = link[t], link[(t + 1) % 5]; c = [v for v in adj[a] & adj[b] if v != hole]; assert len(c) == 1; w.append(c[0])
    return E, adj, link, w
def run(gname, hole, mirror, seed=1, T=40):
    E, adj, link, w = load(gname, hole, mirror); idx = {u: i for i, u in enumerate(E.order)}; li = E.li; wi = [idx[v] for v in w]
    deg = [len(adj[x]) for x in link]; hi = [t for t in range(5) if deg[t] >= 6]
    rng = random.Random(seed); done = set(); out = []
    lc = lambda s: [s[i] for i in li]
    def frame(s):
        c = lc(s); cnt = Counter(c); j = next(j for j in range(5) if c[j] == c[(j + 2) % 5] and cnt[c[j]] == 2)
        al, mu, A, B = c[j], c[(j + 1) % 5], c[(j + 3) % 5], c[(j + 4) % 5]
        w0, w3 = s[wi[j]], s[wi[(j + 3) % 5]]
        ty = 1 if w0 == A else (2 if (w0 == B and w3 == al) else (3 if (w0 == B and w3 == mu) else 0)); return j, ty, (al, mu, A, B)
    def sigma(s):
        j, ty, (al, mu, A, B) = frame(s); K = E.comp(s, li[(j + 1) % 5], al, mu); return E.swap(s, K, al, mu)
    def lockless(s):
        if E.is_filled(s): return False
        c = lc(s); cnt = Counter(c); j = next(j for j in range(5) if c[j] == c[(j + 2) % 5] and cnt[c[j]] == 2)
        mu, A, B = c[(j + 1) % 5], c[(j + 3) % 5], c[(j + 4) % 5]
        return not (E.comp(s, li[(j + 1) % 5], mu, A) >> li[(j + 3) % 5] & 1) and not (E.comp(s, li[(j + 1) % 5], mu, B) >> li[(j + 4) % 5] & 1)
    seeds = ALLSEEDS(E, adj, hole, link) if ALLSTATES else [E.randcol(rng) for _ in range(T)]
    for s0 in seeds:
        if s0 in done: continue
        mem = E.bfs(s0); done |= set(mem)
        pi = {}; lam = {}
        for x in mem: pi[x], lam[x] = E.pi_of(x)
        cyc = {}; cycles = []
        for x in mem:
            if x in cyc: continue
            z = []; y = x
            while y not in cyc: cyc[y] = len(cycles); z.append(y); y = pi[y]
            cycles.append(z)
        W = [sum(lam[y] for y in z) // 5 for z in cycles]
        DL = {x: E.dl_info(x) is not None for x in mem}
        G = [c for c, z in enumerate(cycles) if all(DL[x] for x in z)]
        if not G: continue
        pinv = {pi[x]: x for x in mem}; isDD = lambda x: DL[x] and (DL[pi[x]] or DL[pinv[x]])
        F = sum(1 for x in mem if E.is_filled(x))
        def fafter(s):
            y = pi[s]; f = 0
            while E.is_filled(y): f += 1; y = pi[y]
            return f
        # sigma links / exits from DD endpoints (all cycles), sigma' links
        sig = defaultdict(set); sigp = defaultdict(set); exits = {}
        for x in mem:
            if not isDD(x): continue
            s = sigma(x); a, b = cyc[x], cyc[s]
            if a != b:
                sig[a].add(b); sig[b].add(a)
                if W[a] > 0 and lockless(s): exits.setdefault(s, (a, 3 * fafter(s) - 1))
            for t, p, q, K in E.moves(x):
                if t == x or K & E.linkmask or DL[t] or cyc[t] == a: continue
                sigp[a].add(cyc[t]); sigp[cyc[t]].add(a)
        def groups(links):
            up = list(range(len(cycles)))
            def f(u):
                while up[u] != u: up[u] = up[up[u]]; u = up[u]
                return u
            for a, ts in links.items():
                for t in ts: up[f(a)] = f(t)
            g = defaultdict(int)
            for c in range(len(cycles)): g[f(c)] += 5 * W[c]
            return max(g.values()), sum(1 for v in g.values() if v > 0)
        sigC_max, sigC_fail = groups(sig); sp = {c: sig[c] | sigp[c] for c in set(sig) | set(sigp)}; H1_max, H1_fail = groups(sp)
        # charge-back P1 (undirected sigma neighbours)
        src = defaultdict(lambda: defaultdict(int)); crN = defaultdict(int); crP = defaultdict(int)
        for s, (a, cr) in exits.items():
            T_ = cyc[s]
            if W[T_] <= 0: src[T_][a] += cr; crN[a] += cr
            else: crP[a] += cr
        rem = {t: 5 * W[t] + sum(src[t].values()) for t in range(len(cycles)) if W[t] <= 0}
        charge = defaultdict(Fraction)
        for t, r in rem.items():
            if r > 0 and src[t]:
                tot = sum(src[t].values())
                for a, cr in src[t].items(): charge[a] += Fraction(r * cr, tot)
        cap = {t: Fraction(-r) for t, r in rem.items() if r < 0}
        defs = sorted([(z, 5 * W[z] - crN[z] + charge[z], [t for t in sig[z] if t in cap]) for z in range(len(cycles)) if W[z] > 0 and 5 * W[z] - crN[z] + charge[z] > 0], key=lambda d: -d[1])
        used = defaultdict(Fraction)
        def bt(i):
            if i == len(defs): return True
            z, d, nb = defs[i]
            for t in sorted(nb, key=lambda t: -(cap[t] - used[t])):
                if cap[t] - used[t] >= d:
                    used[t] += d
                    if bt(i + 1): return True
                    used[t] -= d
            return False
        p1 = bt(0)
        for gc in G:
            z = cycles[gc]; L = len(z); rec = dict(graph=gname, hole=hole, orientation='mirror' if mirror else 'plantri', link_degrees=deg, class_states=len(mem), class_F=F,
                                                  floor_ok=4 * F >= len(mem), class_sumw=sum(W), L=L, w=W[gc], D=5 * W[gc], C_neg=crN[gc], C_pos=crP[gc],
                                                  lemmaS=crN[gc] >= 5 * W[gc], sigmaC_fail_groups=sigC_fail, sigmaC_max_group=sigC_max, H1_fail_groups=H1_fail, H1_max_group=H1_max, P1_chargeback=p1)
            if len(hi) == 1:
                t6 = hi[0]; seq = []
                for x in z:
                    j, ty, _ = frame(x); k = (t6 - j) % 5; s = sigma(x)
                    ex = '-' if ty != 3 else ('fixed' if s == x else ('L%d' % fafter(s) if lockless(s) else ('DL' if DL.get(s, E.dl_info(s) is not None) else 'single')))
                    seq.append((ty, k, ex))
                s0 = next((i for i, e in enumerate(seq) if e[0] == 3 and e[1] == 4), 0); seq = seq[s0:] + seq[:s0]
                pat = [(3, 4), (1, 1), (3, 3), (1, 0), (3, 2), (1, 4), (3, 1), (1, 3), (3, 0), (1, 2)]
                rec['universal_period'] = all((e[0], e[1]) == pat[i % 10] for i, e in enumerate(seq))
                per = [tuple(seq[b + q][2] for q in (0, 2, 4, 6, 8)) for b in range(0, L, 10)] if rec['universal_period'] else []
                rec['period_tuples'] = Counter(per).most_common(8)
                k4fail = [not p[0].startswith('L') for p in per]
                rec['A34_consecutive_k4_failures'] = sum(1 for b in range(len(per)) if k4fail[b] and k4fail[(b + 1) % len(per)])
                rec['W2_periods_all_k_le2_fixed'] = sum(1 for p in per if p[2] == 'fixed' and p[3] == 'fixed' and p[4] == 'fixed')
                rec['W2star_periods_k2_and_k0_fixed'] = sum(1 for p in per if p[2] == 'fixed' and p[4] == 'fixed')
            out.append(rec)
    return out
if __name__ == '__main__':
    jobs = [('A6_chain', 13), ('A6_chain', 31), ('A7_exc', 22), ('A7_exc', 34), ('hog1152_chain', 11), ('r5_80b930d1_exc', 2), ('r5_80b930d1_exc', 23)]
    allr = []
    for g, h in jobs:
        for mirror in (False, True):
            rs = run(g, h, mirror); allr += rs
            for r in rs: print(json.dumps({k: v for k, v in r.items() if k != 'period_tuples'}), flush=True)
    json.dump(allr, open('jobaq.json', 'w'), indent=0)
