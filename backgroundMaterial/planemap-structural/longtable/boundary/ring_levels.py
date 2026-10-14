import json, sys, collections, os
sys.path.insert(0, os.path.expanduser('~/4square'))
from kempe_engine import HoleGame
s = open(os.path.expanduser('~/4square/levels.js')).read()
G = json.loads(s[s.index('{'):s.rindex('}') + 1])
lay = open(os.path.expanduser('~/4square/layout.js')).read(); LAY = json.loads(lay[lay.index('{'):lay.rindex('}') + 1])
out = {}
cache = {}
for L in G['levels']:
    key = L['g']; Gr = G['graphs'][key]
    if Gr.get('onboard') or key.startswith('ob'): continue
    if key not in cache:
        n = Gr['n']; adj = [[] for _ in range(n)]
        for a, b in Gr['edges']: adj[a].append(b); adj[b].append(a)
        H = HoleGame(n, adj, Gr['hole'], Gr['link'])
        d = [-1] * n; d[Gr['hole']] = 0; q = collections.deque([Gr['hole']])
        while q:
            u = q.popleft()
            for w in adj[u]:
                if d[w] < 0: d[w] = d[u] + 1; q.append(w)
        dmax = max(d)
        rings = {'outer1': {u for u in range(n) if d[u] == dmax},
                 'outer2': {u for u in range(n) if d[u] >= dmax - 1},
                 'dist>=3': {u for u in range(n) if d[u] >= 3},
                 'border3': set(LAY.get(key, {}).get('border', []))}
        res = {}
        for rn, R in rings.items():
            if not R: res[rn] = None; continue
            # ring-move graph: chains touching R (reversible), BFS from filled
            nb = [[] for _ in range(H.S)]
            for k, c in enumerate(H.states):
                for K in H.chains(c):
                    if K['web'] or not (K['set'] & R): continue
                    nb[k].append(H.index[H.canon(H.flip(c, K))])
            dist = [0 if f else -1 for f in H.filled]; q = collections.deque(k for k in range(H.S) if H.filled[k])
            while q:
                k = q.popleft()
                for t in nb[k]:
                    if dist[t] < 0: dist[t] = dist[k] + 1; q.append(t)
            unf = [k for k in range(H.S) if not H.filled[k]]
            res[rn] = {'size': len(R), 'dist': dist, 'solvable_frac': sum(1 for k in unf if dist[k] >= 0) / max(1, len(unf))}
        cache[key] = (H, dmax, res)
    H, dmax, res = cache[key]
    st = list(L['start']); st[Gr['hole']] = -1 if st[Gr['hole']] is None else st[Gr['hole']]
    k = H.index.get(H.canon(st))
    row = {'lvl': L['num'], 'id': L['id'], 'map': key, 'n': Gr['n'], 'dmax': dmax, 'par': L.get('par'), 'dF': H.dF[k] if k is not None else None}
    for rn, r in res.items():
        row[rn] = None if r is None else (r['dist'][k] if k is not None else None, r['size'], round(r['solvable_frac'], 3))
    print(json.dumps(row), flush=True)
