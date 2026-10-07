#!/usr/bin/env python3
"""[exploratory] NightStatementC: class structure behind statement (c) on the 61 Job AW hit graphs (hole 22, both orientations).
Engine: lib26.Eng via jobaq.load (same as Job BI). Per class containing a Gamma-cycle: all pi-cycles (L, w, F); the most negative cycle M;
for every positive cycle Z: sigma-images of its DD endpoints (all L states when Z is Gamma), where they land (M? heavy T with Lambda(T) <= -Lambda(Z)?);
the credit-free Hall/flow test (positive Lambda shipped along sigma-links to nonpositive cycles with capacity -Lambda(T))."""
import sys, os, json, itertools
from collections import Counter, defaultdict
from multiprocessing import Pool
HERE = os.path.dirname(os.path.abspath(__file__)); P27 = os.path.join(HERE, '../27-studio-positive-config')
for d in ('jobaq', '../26-transport-adversarial', '../25-transport', '../common', '../22-winding-escape'): sys.path.insert(0, os.path.join(P27, d))
import jobaq
from scan import maxflow
def account(args):
    tag, path, mirror = args
    src = json.load(open(path)); hole = src['hole']
    jobaq.GDIR = os.path.join(HERE, 'gl') + '/'; os.makedirs(jobaq.GDIR, exist_ok=True); gname = os.path.basename(path)[:-5]
    lk = jobaq.GDIR + 'best-%s.json' % gname
    if not os.path.lexists(lk):
        try: os.symlink(os.path.abspath(path), lk)
        except FileExistsError: pass
    E, adj, link, w = jobaq.load(gname, hole, mirror)
    deg = sorted(len(adj[x]) for x in link)
    li = E.li; lc = lambda s: [s[i] for i in li]; done = set(); out = []
    def jj(c):
        cnt = Counter(c); return next(j for j in range(5) if c[j] == c[(j + 2) % 5] and cnt[c[j]] == 2)
    def lockinfo(s):
        if E.is_filled(s): return 'F'
        c = lc(s); j = jj(c); mu, A, B = c[(j + 1) % 5], c[(j + 3) % 5], c[(j + 4) % 5]
        l1 = E.comp(s, li[(j + 1) % 5], mu, A) >> li[(j + 3) % 5] & 1; l2 = E.comp(s, li[(j + 1) % 5], mu, B) >> li[(j + 4) % 5] & 1
        return {(0, 0): 'N0', (1, 0): 'L1', (0, 1): 'L2', (1, 1): 'DL'}[(l1, l2)]
    def sigma(s):
        c = lc(s); j = jj(c); al, mu = c[j], c[(j + 1) % 5]
        return E.swap(s, E.comp(s, li[(j + 1) % 5], al, mu), al, mu)
    from kempe_py import Space
    sp = Space({v: set(a) for v, a in adj.items()}, hole, link=link)
    for s0 in sp.states:
        if s0 in done: continue
        mem = E.bfs(s0); done |= set(mem)
        pi = {}; lam = {}
        for x in mem: pi[x], lam[x] = E.pi_of(x)
        kind = {x: lockinfo(x) for x in mem}
        cyc = {}; cycles = []
        for x in mem:
            if x in cyc: continue
            z = []; y = x
            while y not in cyc: cyc[y] = len(cycles); z.append(y); y = pi[y]
            cycles.append(z)
        Lam = [sum(lam[y] for y in z) for z in cycles]
        G = [c for c, z in enumerate(cycles) if all(kind[x] == 'DL' for x in z)]
        if not G: continue
        Fc = [sum(kind[y] == 'F' for y in z) for z in cycles]
        N = len(mem); F = sum(Fc); U = N - F
        M = min(range(len(cycles)), key=lambda c: Lam[c]); Lmax = max(range(len(cycles)), key=lambda c: len(cycles[c]))
        pinv = {pi[x]: x for x in mem}
        isDD = lambda x: kind[x] == 'DL' and (kind[pi[x]] == 'DL' or kind[pinv[x]] == 'DL')
        pos = [c for c in range(len(cycles)) if Lam[c] > 0]
        # sigma links from DD endpoints (Job AQ convention), undirected adjacency
        nb = defaultdict(set); img = defaultdict(list)
        for x in mem:
            if not isDD(x): continue
            s = sigma(x); a, b = cyc[x], cyc[s]
            img[a].append((b, kind[s] if s != x else 'fixed'))
            if a != b: nb[a].add(b); nb[b].add(a)
        # credit-free flow: positives -> nonpositive sigma-neighbours (one hop, undirected), capacity -Lambda
        def flow(edges_of):
            if not pos: return True
            return maxflow({z: Lam[z] for z in pos}, {t: -Lam[t] for t in range(len(cycles)) if Lam[t] < 0},
                           {z: {t for t in edges_of(z) if Lam[t] < 0} for z in pos}) >= sum(Lam[z] for z in pos)
        flow1 = flow(lambda z: nb[z])
        # heavy-only edges (the (c) edges)
        flowc = flow(lambda z: {t for t in nb[z] if Lam[t] <= -Lam[z]})
        pz = []
        for z in pos:
            ims = img[z]; off = [(b, k) for b, k in ims if b != z]
            pz.append(dict(L=len(cycles[z]), Lam=Lam[z], gamma=z in G, F=Fc[z], nDD=len(ims), noff=len(off), onM=sum(b == M for b, k in off),
                           heavy=sum(Lam[b] <= -Lam[z] for b, k in off), distinct=len({b for b, k in off}),
                           c=any(Lam[b] <= -Lam[z] for b, k in off), cM=any(b == M for b, k in off),
                           kinds_onM=dict(Counter(k for b, k in off if b == M)), heavy_cycles=sorted({Lam[b] for b, k in off if Lam[b] <= -Lam[z]})[:4]))
        # share of the class's unfilled states on cycles with Lambda <= -t, for t = 20 (the Gamma threshold) and on M
        hU = {t: sum(len(cycles[c]) - Fc[c] for c in range(len(cycles)) if Lam[c] <= -t) / U for t in (20, 100, 1000)}
        hN = {t: sum(len(cycles[c]) for c in range(len(cycles)) if Lam[c] <= -t) / N for t in (20, 100, 1000)}
        nheavy = {t: sum(1 for c in range(len(cycles)) if Lam[c] <= -t) for t in (20, 100, 1000)}
        negmass = -sum(Lam[c] for c in range(len(cycles)) if Lam[c] < 0)
        cyc_sorted = sorted(((Lam[c], len(cycles[c]), Fc[c]) for c in range(len(cycles))))
        out.append(dict(tag=tag, orientation='mirror' if mirror else 'plantri', linkdeg=deg, N=N, U=U, F=F, sumLam=sum(Lam), ncyc=len(cycles), nGamma=len(G),
                        M=dict(Lam=Lam[M], L=len(cycles[M]), F=Fc[M], U=len(cycles[M]) - Fc[M]), M_is_longest=(M == Lmax), Lmax=len(cycles[Lmax]),
                        phiN=len(cycles[M]) / N, phiU=(len(cycles[M]) - Fc[M]) / U, phiF=Fc[M] / F if F else None,
                        posmass=sum(Lam[z] for z in pos), npos=len(pos), star=(-Lam[M] >= sum(Lam[z] for z in pos)),
                        flow_sigma=flow1, flow_c=flowc, hU=hU, hN=hN, nheavy=nheavy, negmass=negmass, Mshare_neg=-Lam[M] / negmass if negmass else None, pos=pz, top5=cyc_sorted[:5]))
    return out
if __name__ == '__main__':
    V = json.load(open(os.path.join(P27, 'jobaw/jobaw-verified.json')))
    jobs = []; seen = set()
    for v in V:
        p = os.path.join(P27, 'jobaw', v['file'])
        if p in seen: continue
        seen.add(p)
        for m in (False, True): jobs.append((v['file'], p, m))
    fn = 'cls-hits.json'
    if len(sys.argv) > 1 and sys.argv[1] == 'census':
        import glob
        jobs = [('census:' + os.path.basename(p)[:-5], p, m) for p in sorted(glob.glob(os.path.join(HERE, 'census/*.json'))) for m in (False, True)]; fn = 'cls-census.json'
    elif len(sys.argv) > 1: jobs = jobs[:int(sys.argv[1])]; fn = 'cls-test.json'
    with Pool(2) as P: res = [x for xs in P.imap_unordered(account, jobs) for x in xs]
    json.dump(res, open(os.path.join(HERE, fn), 'w'))
    print('class records', len(res))
