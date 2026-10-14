"""Per-hole radial curvature features for the frame census (orders 28-33).
Usage: feat.py ORDER OUT.npz
For each degree-5 hole h: BFS distances d(v) from h; per shell r = 1..7:
  S[r] = |S_r|, P[r] = #deg-5 at r, M[r] = sum(deg-6) over deg>=7 at r, K[r] = sum(6-deg) = P - M;
  X[r] = #edges S_r -- S_{r+1}.
Plus the hole's link word (canonical, up to rotation/reflection), ecc, and graph-level counts.
Difficulty from Census33 eval (R, NR, mf, ndlc) or TrackO frame-NN (R, NR) + Census29 eval-NN (minfrac)."""
import sys, json, gzip, collections, numpy as np, os
W = os.path.expanduser('~/GraphColour/SolvingFrameworkPlan/docs/working/')
order, out = int(sys.argv[1]), sys.argv[2]
RMAX = 8
def canon(w):
    c = [w[i:] + w[:i] for i in range(len(w))]; rw = w[::-1]; c += [rw[i:] + rw[:i] for i in range(len(w))]
    return min(c)
G = {}
src = W + ('Census33/out/frame-33.txt' if order == 33 else 'Census29/out/frame-%d.txt' % order)
for l in open(src):
    p = l.split(); G[p[0]] = [[int(x) for x in r.split(',')] for r in p[2].split(';')]
recs = []  # (name, hole, R, NR, mf, ndlc)
if order == 33:
    for l in gzip.open(W + 'Census33/out/eval-33.jsonl.gz', 'rt'):
        r = json.loads(l)
        for hs, h in r['holes'].items():
            recs.append((r['name'], int(hs), h['R'], h['NR'], h['mf'], h.get('ndlc', 0)))
else:
    mf = {}
    for l in open(W + 'Census29/out/eval-%d.jsonl' % order):
        r = json.loads(l)
        for hs, v in r['minfrac'].items(): mf[(r['name'], int(hs))] = v
    fn = W + 'TrackO/out/frame-%d.jsonl' % order
    fh = gzip.open(fn + '.gz', 'rt') if not os.path.exists(fn) else open(fn)
    for l in fh:
        r = json.loads(l)
        if 'run' in r: continue
        recs.append((r['g'], r['h'], r['R'], r['NR'], mf.get((r['g'], r['h']), np.nan), 0))
names = sorted(G); gid = {g: i for i, g in enumerate(names)}
N = len(recs)
A = {k: np.zeros((N, RMAX + 1), np.int16) for k in 'SPMKX'}
cols = collections.defaultdict(list)
words = {}
for i, (g, h, R, NR, mf, nd) in enumerate(recs):
    rot = G[g]; n = len(rot); deg = [len(x) for x in rot]
    d = [-1] * n; d[h] = 0; q = collections.deque([h])
    while q:
        u = q.popleft()
        for w in rot[u]:
            if d[w] < 0: d[w] = d[u] + 1; q.append(w)
    for v in range(n):
        r = min(d[v], RMAX)
        A['S'][i, r] += 1
        if deg[v] == 5: A['P'][i, r] += 1
        if deg[v] > 6: A['M'][i, r] += deg[v] - 6
        A['K'][i, r] += 6 - deg[v]
        for w in rot[v]:
            if d[w] == d[v] + 1 and d[v] < RMAX: A['X'][i, r] += 1
    w = canon(''.join(str(deg[x]) for x in rot[h]))
    cols['word'].append(words.setdefault(w, len(words)))
    cols['ecc'].append(max(d)); cols['gid'].append(gid[g]); cols['hole'].append(h)
    cols['n7'].append(sum(x >= 7 for x in deg)); cols['n5'].append(sum(x == 5 for x in deg)); cols['maxdeg'].append(max(deg))
    cols['R'].append(R); cols['NR'].append(NR); cols['mf'].append(mf); cols['ndlc'].append(nd)
np.savez_compressed(out, **A, **{k: np.array(v) for k, v in cols.items()}, wordlist=np.array(sorted(words, key=words.get)), names=np.array(names), order=order)
print(order, N, 'holes', len(words), 'words')
