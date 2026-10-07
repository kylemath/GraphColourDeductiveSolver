#!/usr/bin/env python3
"""[exploratory] Orders 12-24 pi-cycle scan: all-cycle histograms + detailed positive-class records. Reuses ../22-winding-escape/escape.py."""
import sys, json, time, os
sys.path.insert(0, '../common'); sys.path.insert(0, '../22-winding-escape')
from collections import Counter, defaultdict
from kempe_py import Space, gentri_rotation, adj_from_rot
from escape import pi_of, is_DL, abpairs, GENTRI

def analyse(n, gi, h, sp, rot, recs, hist):
    S = len(sp.states); pi = [None] * S; lam = [0] * S
    for k in range(S):
        t, l, _ = pi_of(sp, k); pi[k] = t; lam[k] = l
    assert sorted(pi) == list(range(S))
    cyc_of = [-1] * S; cycles = []
    for k in range(S):
        if cyc_of[k] >= 0: continue
        z = []; x = k
        while cyc_of[x] < 0: cyc_of[x] = len(cycles); z.append(x); x = pi[x]
        sl = sum(lam[x] for x in z); assert sl % 5 == 0
        cycles.append((z, sl // 5))
    for z, w in cycles: hist[(w, len(z))] += 1
    pos = [ci for ci, (z, w) in enumerate(cycles) if w > 0]
    if not pos: return
    linkmask = 0
    for i in sp.linki: linkmask |= 1 << i
    ring2 = 0
    for i in sp.linki: ring2 |= sp.nbm[i]
    ring2 &= ~linkmask
    mvc = {}
    def mv(k):
        if k not in mvc: mvc[k] = sp.moves(k)
        return mvc[k]
    done = set()
    for c0 in pos:
        if cycles[c0][0][0] in done: continue
        mem = [cycles[c0][0][0]]; seen = {mem[0]}
        for x in mem:
            for t, *_ in mv(x):
                if t not in seen: seen.add(t); mem.append(t)
        done |= seen
        cls = sorted({cyc_of[x] for x in mem})
        U = sum(1 for x in mem if len(set(sp.states[x][i] for i in sp.linki)) == 4); F = len(mem) - U
        assert 3 * F - U == -5 * sum(cycles[ci][1] for ci in cls)
        posc = [ci for ci in cls if cycles[ci][1] > 0]
        cw = Counter(cycles[ci][1] for ci in cls)
        cr = dict(n=n, gentri=gi, hole=h, states=len(mem), ncyc=len(cls), windings=sorted(cw.items()),
                  npos=len(posc), cycles=[])
        for ci in posc:
            z, w = cycles[ci]
            nb = {}   # neighbour cycle -> list of swap descriptors
            for x in z:
                dl = is_DL(sp, x); ab = abpairs(sp, x) if dl else None
                for t, p, q, K in mv(x):
                    if t == x or K & linkmask: continue
                    cj = cyc_of[t]
                    if cj == ci: continue
                    desc = ('DL' if dl else 'nonDL', ('alphaAB' if frozenset((p, q)) in ab else 'otherpair') if dl else '-',
                            'ring2' if K & ring2 else 'noring2', bin(K).count('1'))
                    nb.setdefault(cj, []).append(desc)
            nbw = sorted(Counter(cycles[cj][1] for cj in nb).items())
            rec = dict(L=len(z), w=w, nbw=nbw, nnb=len(nb), nDLstates=sum(1 for x in z if is_DL(sp, x)))
            if nb:
                mn = min(cycles[cj][1] for cj in nb)
                rec['minnb'] = mn; rec['dominates'] = (-mn >= w)
                ds = Counter()
                for cj in nb:
                    if cycles[cj][1] == mn:
                        for d in set(nb[cj]): ds[d[:3]] += 1
                rec['minnb_swaps'] = [[list(k), v] for k, v in sorted(ds.items())]
                rec['minnb_L'] = sorted({len(cycles[cj][0]) for cj in nb if cycles[cj][1] == mn})
            cr['cycles'].append(rec)
        recs.append(cr)

def run(args):
    n, gi, line = args
    rot = gentri_rotation(line); adj = adj_from_rot(rot); recs = []; hist = Counter()
    for h in range(len(rot)):
        if len(rot[h]) != 5: continue
        try: sp = Space(adj, h, link=rot[h])
        except AssertionError: continue
        analyse(n, gi, h, sp, rot, recs, hist)
    return n, gi, recs, [[w, L, c] for (w, L), c in hist.items()]

if __name__ == '__main__':
    import multiprocessing as mp
    n = int(sys.argv[1]); step = int(sys.argv[2]) if len(sys.argv) > 2 else 1
    extra = set(json.loads(sys.argv[3])) if len(sys.argv) > 3 else set()
    lines = [l for l in open(GENTRI % n) if l.startswith('G')]
    jobs = [(n, gi, l) for gi, l in enumerate(lines, 1) if gi % step == 0 or gi in extra]
    t0 = time.time()
    with mp.Pool(4) as pool, open('out-%d.jsonl' % n, 'w') as out:
        for _, gi, recs, hist in pool.imap_unordered(run, jobs, chunksize=1):
            out.write(json.dumps(dict(kind='graph', gentri=gi, hist=hist)) + '\n')
            for r in recs: out.write(json.dumps(dict(kind='class', **r)) + '\n')
            out.flush()
    print(n, len(jobs), 'graphs', '%.0fs' % (time.time() - t0), flush=True)
