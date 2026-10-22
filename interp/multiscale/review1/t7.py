# Claim 2(i) on chorded clusters (weak invariant): one colouring, every pocket tau<=1, plus minimal interior winding.
import sys, time, math, json, glob, pickle, random; sys.path.insert(0,'/mnt/project-files/multiscale/review1')
from rv import *
sys.path.insert(0, '/mnt/project-files/multiscale/levelling')
from e1_survey import graph
out = open('t7_weak_minw.jsonl', 'w')
def rec(d):
    print(json.dumps(d), flush=True); out.write(json.dumps(d)+'\n'); out.flush()
class W: pass
def pockets(T, cl):
    ch = set(chords(cl)); tris = set(cl.tris); par = {i: i for i in tris}
    def find(x):
        while par[x] != x: par[x] = par[par[x]]; x = par[x]
        return x
    for i in tris:
        f = T.faces[i]
        for j in range(3):
            u, w = f[j], f[(j+1) % 3]; o = T.face[(w, u)]
            if o in tris and (min(u, w), max(u, w)) not in ch: par[find(i)] = find(o)
    comp = collections.defaultdict(set)
    for i in tris: comp[find(i)].add(i)
    res = []
    for P in comp.values():
        bd = {}; cnt = collections.Counter()
        for i in P:
            f = T.faces[i]
            for j in range(3):
                u, w = f[j], f[(j+1) % 3]; cnt[u] += 1
                if T.face[(w, u)] not in P: bd[u] = w
        start = min(bd); walk = [start]
        while bd[walk[-1]] != start: walk.append(bd[walk[-1]])
        k = [cnt[b]-1 for b in walk]; s = [1]
        for i in range(1, len(walk)): s.append(s[-1]*(-1 if k[i] % 2 else 1))
        closing = s[-1]*(-1 if k[0] % 2 else 1)
        w_ = W(); w_.walk = walk; w_.s = s; w_.m = len(walk); w_.parity_odd = (closing != s[0]); res.append(w_)
    return res
def weak_sat(T, cl, K2, wmode, seed=0, budget=3*10**6):
    enc = CNF(cl.verts)
    for u, w in cl.edges: enc.neq(u, w)
    f = T.faces[cl.tris[0]]
    for j in range(3): enc.fix(f[j], j)
    if wmode == 'min': add_winding(enc, T, {v: 'min' for v in cl.S if v not in cl.bset})
    for P in pockets(T, cl): enc.level(P, K2)
    r = enc.solve(phases=rand_phases(enc, random.Random(seed)), budget=budget)
    return r
tot = collections.Counter()
for fn in sorted(glob.glob('/mnt/project-files/multiscale/levelling/fail_*.pkl')):
    d = pickle.load(open(fn, 'rb')); T = graph(d['name'])
    try: cl = Cluster(T, set(d['A']) | set(d['B']))
    except Exception as e: continue
    if len(cl.S) > 1200: continue
    t0 = time.time(); P = pockets(T, cl)
    r0 = weak_sat(T, cl, 1.0, None); r1 = weak_sat(T, cl, 1.0, 'min')
    res = dict(file=fn.split('/')[-1], n=len(cl.S), m=cl.m, chords=len(chords(cl)), pockets=len(P), nodd=len(cl.odd),
               weak_anyw=(r0 is not None) if r0 != 'UNK' else 'UNK', weak_minw=(r1 is not None) if r1 != 'UNK' else 'UNK', sec=round(time.time()-t0, 1))
    if r1 and r1 != 'UNK':
        assert count_w2(T, r1, cl.S)[0] == 0
        res['max_pocket_tau'] = round(max(Cluster.tau(P_, r1)[0] if False else 0 for P_ in P), 3) if False else None
    rec(res); tot['n'] += 1; tot['anyw'] += res['weak_anyw'] is True; tot['minw'] += res['weak_minw'] is True
rec(dict(summary='fail clusters weak', **tot))
