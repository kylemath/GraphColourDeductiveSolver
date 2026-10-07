#!/usr/bin/env python3
"""[exploratory] Per-hole link-pattern scan, orders 12-24: classes, positive classes, DL states, all-DL pi-cycles, filled fraction, class sum-winding."""
import sys, json, time
sys.path.insert(0, '../common'); sys.path.insert(0, '../22-winding-escape')
from kempe_py import Space, gentri_rotation, adj_from_rot
from escape import pi_of, is_DL, GENTRI

def run(args):
    n, gi, line = args
    rot = gentri_rotation(line); adj = adj_from_rot(rot); out = []
    for h in range(len(rot)):
        if len(rot[h]) != 5: continue
        try: sp = Space(adj, h, link=rot[h])
        except AssertionError: continue
        S = len(sp.states); pi = [0]*S; lam = [0]*S
        for k in range(S): pi[k], lam[k], _ = pi_of(sp, k)
        dl = [is_DL(sp, k) for k in range(S)]
        cyc = [-1]*S; cycles = []
        for k in range(S):
            if cyc[k] >= 0: continue
            z = []; x = k
            while cyc[x] < 0: cyc[x] = len(cycles); z.append(x); x = pi[x]
            sl = sum(lam[x] for x in z); assert sl % 5 == 0
            cycles.append((z, sl//5))
        # classes: union-find over all moves
        par = list(range(S))
        def f(x):
            while par[x] != x: par[x] = par[par[x]]; x = par[x]
            return x
        for k in range(S):
            for t, *_ in sp.moves(k):
                a, b = f(k), f(t)
                if a != b: par[a] = b
        cl = {}
        for k in range(S): cl.setdefault(f(k), []).append(k)
        classes = []
        for mem in cl.values():
            F = sum(1 for x in mem if sp.filled(x)); size = len(mem)
            cs = {cyc[x] for x in mem}
            sw = sum(cycles[c][1] for c in cs)
            assert sw*5 == size - 4*F, (sw, size, F)
            classes.append(dict(size=size, F=F, sw=sw, npos=sum(1 for c in cs if cycles[c][1] > 0),
                                dl=sum(dl[x] for x in mem),
                                alldl=sum(1 for c in cs if all(dl[x] for x in cycles[c][0]))))
        out.append(dict(n=n, g=gi, h=h, deg=[len(rot[v]) for v in rot[h]] if False else [len(rot[v]) for v in rot[h]],
                        S=S, F=sum(c['F'] for c in classes), classes=classes))
    return out

if __name__ == '__main__':
    import multiprocessing as mp
    n = int(sys.argv[1])
    lines = [l for l in open(GENTRI % n) if l.startswith('G')]
    import os
    fn = 'out-%d.jsonl' % n; done = set()
    if len(sys.argv) > 2 and sys.argv[2] == 'resume' and os.path.exists(fn):   # keep only complete graphs; resume
        keep = [l for l in open(fn) if l.endswith('\n')]
        done = {json.loads(l)['g'] for l in keep}
        # a graph interrupted mid-write may be partial: drop the highest-hole records of graphs not provably complete
        open(fn, 'w').writelines(keep)
    jobs = [(n, gi, l) for gi, l in enumerate(lines, 1) if gi not in done]
    t0 = time.time()
    with mp.Pool(4) as pool, open(fn, 'a' if done else 'w') as o:
        for recs in pool.imap_unordered(run, jobs, chunksize=1):
            for r in recs: o.write(json.dumps(r)+'\n')
            o.flush()
    print(n, len(jobs), '%.0fs' % (time.time()-t0), flush=True)
