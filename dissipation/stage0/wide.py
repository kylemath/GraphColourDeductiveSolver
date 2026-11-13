"""Wider imitation: one integer model per rule kind predicts the amount the hub sends on each edge,
for every rule in the 604-part proof (RSST push, added push, tunnels), on random and in-part hub balls.
Categorical positions around the edge -> single and pair features (sparse indices), multi-class averaged perceptron.
usage: python3 wide.py all1.pkl all2.pkl ... [--single]"""
import sys, pickle, random, zlib, numpy as np, collections as C, time
sys.path.insert(0, '../code')
from behav import npriv
files = [a for a in sys.argv[1:] if not a.startswith('--')]; SINGLE = '--single' in sys.argv
rows = []
for f in files: rows += [dict(r, file=f) for r in pickle.load(open(f, 'rb'))]
cat = lambda x: 0 if x is None else x - 4          # 0 none, 1..5 for 5..9
def edge_positions(r, i, sgn):
    d, link, asg = r['d'], r['link'], r['asg']
    L = lambda o: link[(i + sgn * o) % d]
    def fans(j):
        f = [asg[200 + 3 * (j % d) + t] for t in range(npriv(link[j % d]))]
        if sgn < 0: f = f[::-1]
        return [cat(f[t]) if t < len(f) else 0 for t in range(3)]
    hl = lambda k: asg[100 + (i + k) % d]     # hat between spoke i+k and i+k+1
    near = (hl(-1), hl(0)); far = (hl(-2), hl(1))
    if sgn < 0: near = near[::-1]; far = far[::-1]
    p = [d - 4, cat(L(0))] + [cat(L(o)) for o in (1, -1, 2, -2, 3, -3)] + [cat(x) for x in near + far]
    p += fans(i) + fans(i - sgn) + fans(i + sgn)
    return p
NP = 21; pa, pb = np.triu_indices(NP, 1)
def index(Pm):
    """Pm [n, NP] categories -> sparse feature indices [n, NP (+ pairs)]"""
    s = np.arange(NP) * 6 + Pm
    if SINGLE: return s
    pr = NP * 6 + np.arange(len(pa)) * 36 + Pm[:, pa] * 6 + Pm[:, pb]
    return np.concatenate([s, pr], 1)
NFEAT = NP * 6 + (0 if SINGLE else len(pa) * 36)
fam = lambda t: t.rstrip('m')
def is_test(r):
    if r['src'] == 'random': return r['file'] == files[-1]
    return zlib.crc32(fam(r['src']).encode()) % 5 == 0
E = dict(tr=[], te=[])
for r in rows:
    te = is_test(r)
    for i in range(r['d']):
        y = (r['dr'][i], r['sp'][i], r['st'][i])
        if te: E['te'].append((edge_positions(r, i, 1), y, r['src'] != 'random', id(r)))
        else:
            E['tr'].append((edge_positions(r, i, 1), y, 0, 0)); E['tr'].append((edge_positions(r, i, -1), y, 0, 0))
def pack(L):
    return index(np.array([e[0] for e in L], np.int64)), np.array([e[1] for e in L]), np.array([e[2] for e in L], bool), np.array([e[3] for e in L])
Xtr, Ytr, _, _ = pack(E['tr']); Xte, Yte, inpart, ball = pack(E['te'])
print('balls', len(rows), 'train edges', len(Xtr), 'test edges', len(Xte), 'features', NFEAT, 'active per edge', Xtr.shape[1], flush=True)
def fit(X, y, epochs=12, bs=256, seed=0):
    classes = np.unique(y); ci = {c: k for k, c in enumerate(classes)}; t = np.array([ci[v] for v in y])
    W = np.zeros((len(classes), NFEAT), np.int32); A = np.zeros_like(W, dtype=np.float64); rng = np.random.default_rng(seed); n = 0
    for ep in range(epochs):
        order = rng.permutation(len(X)); miss = 0
        for s in range(0, len(X), bs):
            b = order[s:s + bs]; xb = X[b]; sc = W[:, xb].sum(2); p = sc.argmax(0); bad = p != t[b]
            if bad.any():
                xi = xb[bad]; np.add.at(W, (t[b][bad][:, None], xi), 1); np.add.at(W, (p[bad][:, None], xi), -1); miss += int(bad.sum())
            A += W; n += 1
        if miss == 0: break
    A /= n; mx = np.abs(A).max() or 1
    return classes, np.round(63 * A / mx).astype(np.int32)      # 6-bit weights
def pred(classes, W, X):
    out = np.empty(len(X), np.int64)
    for s in range(0, len(X), 4096): out[s:s + 4096] = classes[W[:, X[s:s + 4096]].sum(2).argmax(0)]
    return out
res = {}; allok = np.ones(len(Xte), bool); t0 = time.time()
for k, name in enumerate(('RSST push', 'added push', 'tunnel')):
    cl, W = fit(Xtr, Ytr[:, k]); p = pred(cl, W, Xte); ok = p == Yte[:, k]; nz = Yte[:, k] != 0; allok &= ok
    nzw = int((W != 0).sum())
    print('%-11s classes %s  edge exact %.4f  on non-zero edges %.3f (n=%d)  false alarms %.4f  non-zero weights %d  (%.0fs)' % (
        name, list(cl), ok.mean(), ok[nz].mean() if nz.any() else float('nan'), int(nz.sum()), (p[~nz] != 0).mean(), nzw, time.time() - t0), flush=True)
    res[name] = (cl, W)
# per hub: every edge and every kind right
bid = {}
for b, o in zip(ball, allok): bid[b] = bid.get(b, True) and bool(o)
src = {}
for b, ip in zip(ball, inpart): src[b] = ip
v = np.array([bid[b] for b in bid]); ip = np.array([src[b] for b in bid])
print('whole hub exact (all edges, all kinds): random balls %.3f (n=%d)   balls inside held-out parts %.3f (n=%d)' % (v[~ip].mean(), (~ip).sum(), v[ip].mean(), ip.sum()))
pickle.dump(res, open('wide_model%s.pkl' % ('_single' if SINGLE else ''), 'wb'))
