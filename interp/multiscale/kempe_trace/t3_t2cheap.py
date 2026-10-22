# T2 (cheap): random A' with the SAME seam word as Opus A (SAT re-extension of the whole side), closing W_band vs Opus B
# by SAT, their traces, and whether a collar of width w on Opus A reproduces them exactly.
import json, sys, time, random, itertools
from collections import deque
sys.path.insert(0, '/mnt/project-files/multiscale/kempe_trace'); sys.path.insert(0, '/mnt/project-files/multiscale/opus_attack/bandfill')
from kt import *; from collar import *; from t2_tubes import sat_colour, random_level_row
from pysat.solvers import Cadical153
d = json.load(open('/mnt/project-files/multiscale/opus_attack/bandfill/sphere_L18_w4.json'))
adj = [set(a) for a in d['adj']]; L = 18; n = len(adj); A = set(d['A']); B = set(range(n)) - A; m = d['seam_row_A']
colA = {int(k): v for k, v in d['colA'].items()}; colB = {int(k): v for k, v in d['colB'].items()}
bdA = [m*L + i for i in range(L)]; bdB = [(m+1)*L + i for i in range(L)]; seam = set(bdA) | set(bdB)
dS = {v: 0 for v in seam}; q = deque(seam)
while q:
    x = q.popleft()
    for y in adj[x]:
        if y not in dS: dS[y] = dS[x]+1; q.append(y)
PERMS = list(itertools.permutations(range(4)))
def repair_sat(col, free):
    free = set(free); vs = sorted(free); ix = {v: k for k, v in enumerate(vs)}; x = lambda v, c: 4*ix[v]+c+1; cls = []
    for v in vs:
        cls.append([x(v, c) for c in range(4)])
        for u in adj[v]:
            if u in free:
                if u > v:
                    for c in range(4): cls.append([-x(v, c), -x(u, c)])
            else: cls.append([-x(v, col[u])])
    s = Cadical153(bootstrap_with=cls); ok = s.solve(); s.delete(); return ok
def W_band(cA, cB, Wmax=4):
    best = None
    for p in PERMS:
        col = dict(cA); col.update({v: p[cB[v]] for v in B})
        if all(col[u] != col[v] for u in seam for v in adj[u]): return 0
        for W in range(1, Wmax+1):
            if best is not None and W >= best: break
            if repair_sat(col, [v for v in range(n) if dS[v] <= W]): best = W; break
    return best
rng = random.Random(3); out = []
base_tr = traces(adj, A, colA, bdA)
print('Opus A vs Opus B W_band (SAT check):', W_band(colA, colB, 5))
for trial in range(int(sys.argv[1]) if len(sys.argv) > 1 else 6):
    t0 = time.time()
    cA2 = sat_colour(adj, A, {v: colA[v] for v in bdA}, rng, nrand=12)
    tr = traces(adj, A, cA2, bdA); sm = summary(tr, L); Wb = W_band(cA2, colB)
    rec = dict(trial=trial, W_band=Wb, same_as_opus=(tr == base_tr), summary={k: v for k, v in sm.items() if k != 'per_pair'}, exact_w={})
    line = f"A' {trial}: W_band={Wb} blocks {sm['nblocks']} single {sm['nsingle']} depth {sm['depth']} maxspan {sm['maxspan']} same_traces_as_opus={tr == base_tr};"
    for w in (5, 6, 7):
        r = exact(adj, A, colA, bdA, w, tr); rec['exact_w'][w] = r is not None; line += f" collar w{w} reproduces: {r is not None}"
        if r is not None: rec['W_after'] = W_band(r, colB); line += f" (W_band after={rec['W_after']})"; break
    print(line, f'({time.time()-t0:.0f}s)', flush=True); out.append(rec); json.dump(out, open('t3_t2cheap.json', 'w'), indent=1)

print('== random level words on both sides (easy closings, SAT W_band) ==')
rng = random.Random(7); ez = []
for trial in range(4):
    sa = random_level_row(L, rng); sb = random_level_row(L, rng)
    cA2 = sat_colour(adj, A, {bdA[i]: sa[i] for i in range(L)}, rng); cB2 = sat_colour(adj, B, {bdB[i]: sb[i] for i in range(L)}, rng)
    Wb = W_band(cA2, cB2); sA = summary(traces(adj, A, cA2, bdA), L); sB = summary(traces(adj, B, cB2, bdB), L)
    rec = dict(trial=trial, W_band=Wb, A={k: v for k, v in sA.items() if k != 'per_pair'}, B={k: v for k, v in sB.items() if k != 'per_pair'})
    print(f"easy {trial}: W_band={Wb}  A: blocks {sA['nblocks']} single {sA['nsingle']} depth {sA['depth']} maxspan {sA['maxspan']} | B: blocks {sB['nblocks']} single {sB['nsingle']} depth {sB['depth']} maxspan {sB['maxspan']}", flush=True); ez.append(rec)
json.dump(dict(same_word=out, random_words=ez), open('t3_t2cheap.json', 'w'), indent=1)
