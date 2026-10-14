"""Within-map analysis of game-out.jsonl: does near curvature C(2) track exact difficulty across the holes of one map?"""
# maxrun 999 = the hole has an all-DL pi-cycle (infinite run); capped at 30 in the pooled correlation
import json, numpy as np, collections
G = [json.loads(l) for l in open('game-out.jsonl')]
M = collections.defaultdict(list)
for g in G: M[g['map']].append(g)
print('maps %d, holes %d' % (len(M), len(G)))
print('map | n | holes | designated hole word C2 maxdF maxrun | corr over holes: C2 vs maxdF, meandF, maxrun')
rows = []
for m, H in sorted(M.items()):
    d = next((h for h in H if h['designated']), None)
    c2 = np.array([h['C'][2] for h in H], float)
    def cr(k):
        y = np.array([h[k] for h in H], float)
        return np.corrcoef(c2, y)[0, 1] if c2.std() > 0 and y.std() > 0 else np.nan
    print('%-13s %2d %2d | %s | %+.2f %+.2f %+.2f' % (m, H[0]['n'], len(H), ('%d %s C2=%d dF=%d run=%d' % (d['hole'], d['word'], d['C'][2], d['maxdF'], d['maxrun'])) if d else '-', cr('maxdF'), cr('meandF'), cr('maxrun')))
    for h in H: rows.append([h['C'][2], h['maxdF'], h['meandF'], min(h['maxrun'], 30), h['C'][1], hash(m) % 100000, h['n']])
X = np.array(rows, float)
# within-map (map FE) correlations
mid = np.unique(X[:, 5], return_inverse=True)[1]
def dm(v): return v - (np.bincount(mid, v) / np.bincount(mid))[mid]
for j, nm in [(1, 'maxdF'), (2, 'meandF'), (3, 'maxrun')]:
    r = np.corrcoef(dm(X[:, 0]), dm(X[:, j]))[0, 1]; n = len(X); se = 1 / np.sqrt(n - len(np.unique(mid)) - 1)
    z = np.arctanh(r); print('within-map corr(C2, %s) = %+.3f  95%% CI [%+.3f, %+.3f] (n=%d holes, %d maps; Fisher, holes treated as independent)' % (nm, r, np.tanh(z - 1.96 * se), np.tanh(z + 1.96 * se), n, mid.max() + 1))
dd = [h for h in G if h['designated']]; ot = [h for h in G if not h['designated']]
print('designated (level) holes: mean C2 %.2f, maxdF %.2f; other degree-5 holes: mean C2 %.2f, maxdF %.2f' % (np.mean([h['C'][2] for h in dd]), np.mean([h['maxdF'] for h in dd]), np.mean([h['C'][2] for h in ot]), np.mean([h['maxdF'] for h in ot])))
T = collections.defaultdict(list)
for h in G: T[h['C'][2]].append(h['maxdF'])
print('maxdF by C2:', {k: (len(v), round(np.mean(v), 2)) for k, v in sorted(T.items())})
