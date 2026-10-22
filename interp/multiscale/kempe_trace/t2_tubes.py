import json, sys, random, time
sys.path.insert(0, '/mnt/project-files/multiscale/kempe_trace'); sys.path.insert(0, '/mnt/project-files/multiscale/opus_attack/bandfill')
from kt import *
from tube import band_graph, INC, nrm, CENTRES, level_any, stack
from pysat.solvers import Cadical153
import sphere as SP

def annulus(rows):
    """rows bottom->top, each a string/tuple; returns adj (list of sets), colouring list"""
    L = len(rows[0]); n, e, t = band_graph(L, len(rows)); adj = [set() for _ in range(n)]
    for u, v in e: adj[u].add(v); adj[v].add(u)
    col = [int(c) for r in rows for c in r]
    return adj, col

def tube_traces(rows, seam_row):
    adj, col = annulus(rows); L = len(rows[0]); n = len(col)
    bd = [seam_row*L + i for i in range(L)]
    tr = traces(adj, range(n), col, bd); s = summary(tr, L)
    return tr, s

def random_level_row(L, rng):
    """random proper cyclic row with base-0 circumradius <= 1 (random DFS)."""
    while True:
        def rec(pref, H, cents):
            if len(pref) == L:
                if pref[-1] == pref[0]: return None
                d = INC[pref[-1] ^ pref[0]]; H2 = (H[0]+d[0], H[1]+d[1])
                return tuple(pref) if any(nrm(H2[0]-p[0], H2[1]-p[1]) <= 4 for p in cents) else None
            cs = list(range(4)); rng.shuffle(cs)
            for c in cs:
                if pref and c == pref[-1]: continue
                if not pref:
                    r = rec([c], H, cents)
                else:
                    d = INC[pref[-1] ^ c]; H2 = (H[0]+d[0], H[1]+d[1])
                    c2 = [p for p in cents if nrm(H2[0]-p[0], H2[1]-p[1]) <= 4]
                    if not c2: continue
                    r = rec(pref+[c], H2, c2)
                if r: return r
            return None
        r = rec([], (0, 0), CENTRES)
        if r: return r

def sat_colour(adj, S, fixed, rng, nrand=8, tris=None):
    """random proper 4-colouring of induced subgraph on S extending `fixed`; random assumptions diversify."""
    vs = sorted(S); ix = {v: k for k, v in enumerate(vs)}
    x = lambda v, c: 4*ix[v] + c + 1
    cls = []
    for v in vs:
        cls.append([x(v, c) for c in range(4)])
        for c in range(4):
            for c2 in range(c+1, 4): cls.append([-x(v, c), -x(v, c2)])
        for u in adj[v]:
            if u in ix and u > v:
                for c in range(4): cls.append([-x(v, c), -x(u, c)])
    for v, c in fixed.items(): cls.append([x(v, c)])
    s = Cadical153(bootstrap_with=cls)
    free = [v for v in vs if v not in fixed]
    for tries in range(5):
        k = max(0, nrand - 2*tries)
        ass = [x(v, rng.randrange(4)) for v in rng.sample(free, k)]
        if s.solve(assumptions=ass): break
    else: s.delete(); return None
    mod = set(l for l in s.get_model() if l > 0); s.delete()
    r = {v: next(c for c in range(4) if x(v, c) in mod) for v in vs}
    assert all(r[v] == c for v, c in fixed.items())
    return r

if __name__ == '__main__':
    out = {'tubes': [], 'sphere_random': []}
    ce = json.load(open('/mnt/project-files/multiscale/opus_attack/bandfill/counterexamples.json'))
    print('== tube counterexample halves (annulus of depth w; traces on the seam row) ==')
    for c in ce:
        L, w = c['L'], c['w']
        rA = c['A_rows_depth_w_to_seam']; rB = c['B_rows_seam_to_depth_w']
        trA, sA = tube_traces(rA, len(rA)-1); trB, sB = tube_traces(rB, 0)
        rec = dict(L=L, w=w, a=c['a'], b=c['b'], A={k: v for k, v in sA.items() if k != 'per_pair'}, B={k: v for k, v in sB.items() if k != 'per_pair'},
                   A_pairs={str(p): s for p, s in sA['per_pair'].items()}, B_pairs={str(p): s for p, s in sB['per_pair'].items()},
                   A_traces={str(p): b for p, b in trA.items()}, B_traces={str(p): b for p, b in trB.items()})
        out['tubes'].append(rec)
        print(f"L={L} w={w}  A: blocks {sA['nblocks']} single {sA['nsingle']} depth {sA['depth']} maxspan {sA['maxspan']} nc {sA['noncrossing']} | "
              f"B: blocks {sB['nblocks']} single {sB['nsingle']} depth {sB['depth']} maxspan {sB['maxspan']} nc {sB['noncrossing']}")
        if L == 18:
            for p, b in trA.items(): print('   A', p, b)
            for p, b in trB.items(): print('   B', p, b)
    # random easy closings on the same L=18 sphere
    d = json.load(open('/mnt/project-files/multiscale/opus_attack/bandfill/sphere_L18_w4.json'))
    L = 18; g = SP.G(); g.adj = [set(a) for a in d['adj']]
    g.tris = [(u, v, w) for u in range(len(g.adj)) for v in g.adj[u] if v > u for w in g.adj[u] & g.adj[v] if w > v]
    n = len(g.adj); A = set(d['A']); B = set(range(n)) - A; m = d['seam_row_A']
    bdA = [m*L + i for i in range(L)]; bdB = [(m+1)*L + i for i in range(L)]
    rng = random.Random(7)
    print('== random level closings on the Opus sphere (seam rows random level, sides random SAT extensions) ==')
    for trial in range(int(sys.argv[1]) if len(sys.argv) > 1 else 6):
        t0 = time.time()
        sa = random_level_row(L, rng); sb = random_level_row(L, rng)
        colA = sat_colour(g.adj, A, {bdA[i]: sa[i] for i in range(L)}, rng)
        colB = sat_colour(g.adj, B, {bdB[i]: sb[i] for i in range(L)}, rng)
        if colA is None or colB is None: print('ext fail'); continue
        res = SP.closing(g, A, B, colA, colB, set(bdA) | set(bdB), Wmax=3)
        trA = traces(g.adj, A, colA, bdA); trB = traces(g.adj, B, colB, bdB); sA = summary(trA, L); sB = summary(trB, L)
        rec = dict(trial=trial, wordA=''.join(map(str, sa)), wordB=''.join(map(str, sb)), W_band=res['W_band'], R_conf=res['R_conf'],
                   A={k: v for k, v in sA.items() if k != 'per_pair'}, B={k: v for k, v in sB.items() if k != 'per_pair'},
                   A_traces={str(p): b for p, b in trA.items()}, B_traces={str(p): b for p, b in trB.items()}, colA=colA, colB=colB, sec=round(time.time()-t0, 1))
        out['sphere_random'].append(rec)
        print(f"trial {trial} W_band={res['W_band']} R={res['R_conf']}  A: blocks {sA['nblocks']} single {sA['nsingle']} depth {sA['depth']} maxspan {sA['maxspan']} | B: blocks {sB['nblocks']} single {sB['nsingle']} depth {sB['depth']} maxspan {sB['maxspan']}  ({rec['sec']}s)", flush=True)
    json.dump(out, open('t2_tubes.json', 'w'), indent=1)
