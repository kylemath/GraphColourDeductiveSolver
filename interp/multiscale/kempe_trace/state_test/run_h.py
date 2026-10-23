"""Height-matched population: other seam words with the same (|t|, tau_H) (4 d.p.) as the experiment's seam word,
random interiors (tube of the experiment's depth w+3 rows), same w, k0.  usage: run_h.py EXP NWORDS NINT"""
import sys, json, random, itertools, hashlib, time
sys.path.insert(0, '/mnt/project-files/multiscale/kempe_trace/state_test')
from st import *
OUT = '/mnt/project-files/multiscale/kempe_trace/state_test/'
exp, NW, NI = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
P = json.load(open(OUT + f'pop_{exp}.json')); L, w, k0 = P['L'], P['w'], P['k0']; seam0 = [int(x) for x in P['seam']]
h0 = tuple(round(x, 4) for x in height_pair(seam0))
rng = random.Random(5)
def canon_word(r):
    best = None
    for p in itertools.permutations(range(4)):
        q = [p[c] for c in r]
        for s in range(L):
            for rr in (q, q[::-1]):
                k = tuple(rr[s:] + rr[:s])
                if best is None or k < best: best = k
    return best
found = {canon_word(seam0)}; words = []
t0 = time.time()
while len(words) < NW and time.time() - t0 < 90:
    r = [rng.randrange(4)]
    for i in range(L - 1): r.append(rng.choice([c for c in range(4) if c != r[-1]]))
    if r[-1] == r[0]: continue
    if tuple(round(x, 4) for x in height_pair(r)) != h0: continue
    cw = canon_word(r)
    if cw in found: continue
    found.add(cw); words.append(r)
print(exp, 'height', h0, 'matched words', len(words), round(time.time() - t0), 's', flush=True)
H = lambda o: hashlib.md5(repr(o).encode()).hexdigest()[:12]
from t2_tubes import annulus
nrows = w + 3
recs = []
for r in words:
    rows = ['0'*L]*(nrows-1) + [''.join(map(str, r))]
    adj, _ = annulus(rows); n = nrows*L; seam = nrows - 1
    E = dict(L=L, adj=adj, S=set(range(n)), bd=[seam*L + i for i in range(L)], rowv=lambda rr, seam=seam: [(seam - rr)*L + i for i in range(L)],
             region=lambda rr, seam=seam, n=n: {v for v in range(n) if v // L <= seam - rr})
    tris = tri_list(adj, E['S'])
    for j in range(NI):
        col = sampler(adj, E['S'], {E['bd'][i]: r[i] for i in range(L)}, rng)
        if col is None: break
        ob = unsat(adj, E['S'], col, E['bd'], w, k0)
        rws, Hs = state(E, col, w, tris); K = keys(rws, Hs, L, w)
        recs.append(dict(mode='hmatch', obstructing=ob, heights=Hs, rows=[''.join(str(col[v]) for v in E['rowv'](q)) for q in range(w+1)],
                         keys={k: H(v) for k, v in K.items()}))
json.dump(dict(exp=exp, L=L, w=w, k0=k0, recs=recs), open(OUT + f'hpop_{exp}.json', 'w'))
print(exp, 'n', len(recs), 'obstructing', sum(x['obstructing'] for x in recs), flush=True)
