# (c) base-point spread of tau_H over all rotations, on random proper boundary colourings of failure discs and edge stars
import sys, pickle, glob, json, random
sys.path.insert(0, '/mnt/project-files/multiscale/canonical/')
from pi import *
rng = random.Random(0); spreads = []; spreads_onelap = []
for fn in sorted(glob.glob('fail_*.pkl')):
    d = pickle.load(open(fn, 'rb')); recs = d['recs']; col = d['col']; B = d['B']
    adj = make(d['job'][0]); degp = collections.Counter()
    present = set(col)
    for x in present: degp[x] = sum(1 for y in adj[x] if y in present)
    s, odd = signs(B, degp)
    for trial in range(3):
        L = len(B); vals = []
        for i0 in range(L):
            Bv = B[i0:] + B[:i0]; sv = np.concatenate([s[i0:], (-1 if odd else 1)*s[:i0]])
            H = walk(Bv, sv, np.array([col[b] for b in Bv]))
            if odd: vals.append(float(np.max(np.abs(H - (H[0]+H[-1])/2))))
            else: t = H[-1]-H[0]; vals.append(mec(H[:-1] - np.arange(L)/L*t))
        spreads.append(dict(f=fn, L=L, odd=odd, spread=max(vals)-min(vals), tau=vals[0]))
        break
print(json.dumps(spreads))
