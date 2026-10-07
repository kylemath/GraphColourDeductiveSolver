#!/usr/bin/env python3
"""[exploratory] Test Conjecture X (winding escape via link-pattern-preserving swaps). See README.md."""
import sys, json, itertools, time
from collections import defaultdict, Counter
sys.path.insert(0, '../common')
from kempe_py import Space, gentri_rotation, adj_from_rot
GENTRI = '../../../studiointel/gentri/tri%d.txt'

def pi_of(sp, k):
    """Exact pi of NightEulerHole 3: returns (target index, lambda, kind)."""
    s = sp.states[k]; li = sp.linki; c = [s[li[t]] for t in range(5)]
    def comp(v, p, q):
        for K in sp.components(s, p, q):
            if K >> v & 1: return K
        raise AssertionError
    def sw(K, p, q): return sp.index[sp.swap(s, K, p, q)]
    cnt = Counter(c)
    if len(cnt) == 4:
        j = next(j for j in range(5) if c[j] == c[(j + 2) % 5] and cnt[c[j]] == 2)
        al, mu, A, B = c[j], c[(j + 1) % 5], c[(j + 3) % 5], c[(j + 4) % 5]
        m, b = li[(j + 1) % 5], li[(j + 4) % 5]
        lock2 = bool(comp(m, mu, B) >> b & 1)
        if lock2: return sw(comp(li[(j + 2) % 5], al, A), al, A), 1, 'R3'
        return sw(comp(li[(j + 4) % 5], mu, B), mu, B), -1, 'phiB'
    assert len(cnt) == 3
    i = next(i for i in range(5) if cnt[c[i]] == 1)
    W, X, Y = c[i], c[(i + 1) % 5], c[(i + 2) % 5]
    Z = ({0, 1, 2, 3} - {W, X, Y}).pop()
    x2, x4 = li[(i + 2) % 5], li[(i + 4) % 5]
    K = comp(x2, Y, Z)
    if not (K >> x4 & 1): return sw(K, Y, Z), -1, 'phiA'
    return sw(comp(li[(i + 3) % 5], W, X), W, X), -3, 'tau'

def is_DL(sp, k):
    s = sp.states[k]; li = sp.linki; c = [s[li[t]] for t in range(5)]; cnt = Counter(c)
    if len(cnt) != 3 + 1: return False
    j = next(j for j in range(5) if c[j] == c[(j + 2) % 5] and cnt[c[j]] == 2)
    mu, A, B = c[(j + 1) % 5], c[(j + 3) % 5], c[(j + 4) % 5]
    m, a, b = li[(j + 1) % 5], li[(j + 3) % 5], li[(j + 4) % 5]
    l1 = any(K >> m & 1 and K >> a & 1 for K in sp.components(s, mu, A))
    l2 = any(K >> m & 1 and K >> b & 1 for K in sp.components(s, mu, B))
    return l1 and l2

def abpairs(sp, k):
    s = sp.states[k]; li = sp.linki; c = [s[li[t]] for t in range(5)]; cnt = Counter(c)
    j = next(j for j in range(5) if c[j] == c[(j + 2) % 5] and cnt[c[j]] == 2)
    al = c[j]; return {frozenset((al, c[(j + 3) % 5])), frozenset((al, c[(j + 4) % 5]))}

def analyse(n, gi, h, sp, out, stats):
    S = len(sp.states); pi = [None] * S; lam = [0] * S
    for k in range(S):
        t, l, _ = pi_of(sp, k); pi[k] = t; lam[k] = l
    assert sorted(pi) == list(range(S)), 'pi not a permutation'
    cyc_of = [-1] * S; cycles = []
    for k in range(S):
        if cyc_of[k] >= 0: continue
        z = []; x = k
        while cyc_of[x] < 0: cyc_of[x] = len(cycles); z.append(x); x = pi[x]
        assert x == k
        sl = sum(lam[x] for x in z); assert sl % 5 == 0
        cycles.append((z, sl // 5))
    stats['states'] += S
    pos = [ci for ci, (z, w) in enumerate(cycles) if w > 0]
    stats['cycles'] += len(cycles)
    if not pos: return
    linkmask = 0
    for i in sp.linki: linkmask |= 1 << i
    mvcache = {}
    def mv(k):
        if k not in mvcache: mvcache[k] = sp.moves(k)
        return mvcache[k]
    def lp(k):   # link-preserving swaps: component with no link vertex, non-trivial
        return [(t, p, q, K) for t, p, q, K in mv(k) if t != k and not K & linkmask]
    done = set()
    for c0 in pos:
        if cycles[c0][0][0] in done: continue
        # class by BFS over all swaps
        mem = [cycles[c0][0][0]]; seen = {mem[0]}
        for x in mem:
            for t, *_ in mv(x):
                if t not in seen: seen.add(t); mem.append(t)
        done |= seen
        cls = sorted({cyc_of[x] for x in mem})
        U = sum(1 for x in mem if len(set(sp.states[x][i] for i in sp.linki)) == 4); F = len(mem) - U
        sw = sum(cycles[ci][1] for ci in cls)
        assert 3 * F - U == -5 * sw, ('thmW', 3 * F - U, sw)
        dl = {x: is_DL(sp, x) for x in mem}
        wd = Counter(cycles[ci][1] for ci in cls)
        # flow graphs
        par = {ci: ci for ci in cls}
        def find(a):
            while par[a] != a: par[a] = par[par[a]]; a = par[a]
            return a
        adjn = defaultdict(set)
        for x in mem:
            for t, *_ in lp(x):
                a, b = cyc_of[x], cyc_of[t]
                if a != b: par[find(a)] = find(b); adjn[a].add(b); adjn[b].add(a)
        ncomp = len({find(ci) for ci in cls})
        posc = [ci for ci in cls if cycles[ci][1] > 0]
        negnb = sum(1 for ci in posc if any(cycles[b][1] < 0 for b in adjn[ci]))
        nonposnb = sum(1 for ci in posc if any(cycles[b][1] <= 0 for b in adjn[ci]))
        # per positive cycle tests
        res = []
        for ci in posc:
            z, w = cycles[ci]
            dls = [x for x in z if dl[x]]
            Xw = set(); X2 = set(); X2any = set(); X3 = set(); nX = 0; nLP = 0
            for x in z:
                for t, p, q, K in lp(x):
                    X2any.add(cycles[cyc_of[t]][1])
            for x in dls:
                ab = abpairs(sp, x)
                l1 = lp(x)
                if any(frozenset((p, q)) in ab for t, p, q, K in l1): nX += 1
                if l1: nLP += 1
                for t, p, q, K in l1:
                    wt = cycles[cyc_of[t]][1]
                    X2.add(wt); X3.add(wt)
                    if frozenset((p, q)) in ab: Xw.add(wt)
                    for t2, p2, q2, K2 in lp(t):
                        X3.add(cycles[cyc_of[t2]][1])
            rec = dict(n=n, gentri=gi, hole=h, L=len(z), w=w, F=sum(1 for x in z if len(set(sp.states[x][i] for i in sp.linki)) == 3),
                       nDL=len(dls), nDL_X=nX, nDL_LP=nLP, Xw=sorted(Xw), X2w=sorted(X2), X2any=sorted(X2any), X3w=sorted(X3),
                       X=any(v < 0 for v in Xw), Xp=any(v <= 0 for v in Xw), X2=any(v < 0 for v in X2),
                       X2b=any(v <= 0 for v in X2), X2any_neg=any(v < 0 for v in X2any), X3=any(v < 0 for v in X3), X3b=any(v <= 0 for v in X3),
                       cls=len(mem))
            res.append(rec)
        out.write(json.dumps(dict(kind='class', n=n, gentri=gi, hole=h, states=len(mem), U=U, F=F, ncyc=len(cls),
                                  windings=sorted(wd.items()), flow_components=ncomp, npos=len(posc), pos_with_neg_nb=negnb,
                                  pos_with_nonpos_nb=nonposnb, cycles=res)) + '\n'); out.flush()

def run(args):
    n, gi, line = args
    rot = gentri_rotation(line); adj = adj_from_rot(rot); buf = []
    class W:
        def write(self, s): buf.append(s)
        def flush(self): pass
    stats = Counter()
    for h in range(len(rot)):
        if len(rot[h]) != 5: continue
        try: sp = Space(adj, h, link=rot[h])
        except AssertionError: continue
        analyse(n, gi, h, sp, W(), stats)
    return n, gi, buf, dict(stats)

if __name__ == '__main__':
    import multiprocessing as mp
    orders = [int(a) for a in sys.argv[1:]]
    for n in orders:
        t0 = time.time()
        lines = [l for l in open(GENTRI % n) if l.startswith('G')]
        tot = Counter()
        with mp.Pool(3) as pool, open('out-%d.jsonl' % n, 'w') as out:
            for _, gi, buf, st in pool.imap_unordered(run, [(n, gi, l) for gi, l in enumerate(lines, 1)], chunksize=1):
                for b in buf: out.write(b)
                tot.update(st)
        print(n, dict(tot), '%.0fs' % (time.time() - t0), flush=True)
