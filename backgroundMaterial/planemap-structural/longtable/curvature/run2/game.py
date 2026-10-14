"""Deep game maps (~/4square/maps): every degree-5 hole of every map with n >= 17, exact swap distances via
~/4square/kempe_engine.HoleGame. Output JSONL: map, hole, word, C1..C3, ecc, S, maxdF, mean dF (unfilled), DL share,
longest DL run along pi, # all-DL pi-cycles. Usage: game.py OUT.jsonl"""
import sys, os, json, glob, collections
sys.path.insert(0, os.path.expanduser('~/4square'))
from kempe_engine import HoleGame
done = set()
if os.path.exists(sys.argv[1]): done = {json.loads(l)['map'] for l in open(sys.argv[1])}
out = open(sys.argv[1], 'a')
for fn in sorted(glob.glob(os.path.expanduser('~/4square/maps/*.json'))):
    m = json.load(open(fn))
    if 'rot' not in m: continue
    rot = m['rot']; n = len(rot); deg = [len(r) for r in rot]
    if n < 17 or min(deg) < 3 or os.path.basename(fn)[:-5] in done: continue
    for h in range(n):
        if deg[h] != 5: continue
        d = [-1] * n; d[h] = 0; q = collections.deque([h])
        while q:
            u = q.popleft()
            for w in rot[u]:
                if d[w] < 0: d[w] = d[u] + 1; q.append(w)
        C = [sum(6 - deg[v] for v in range(n) if d[v] <= r) for r in range(6)]
        try: H = HoleGame(n, rot, h, rot[h])
        except Exception as e: print(fn, h, e); continue
        un = [k for k in range(H.S) if not H.filled[k]]
        run = {}
        def F(k):
            path = []; kk = k
            while H.dl[kk] and kk not in run and kk not in path: path.append(kk); kk = H.pi[kk]
            b = run.get(kk, 0) if H.dl[kk] and kk in run else (999 if kk in path else 0)
            for x in reversed(path): b = b + 1 if b < 999 else b; run[x] = b
            return run[k]
        mx = max([F(k) for k in un if H.dl[k]] or [0])
        out.write(json.dumps({'map': os.path.basename(fn)[:-5], 'n': n, 'hole': h, 'designated': h == m.get('hole'),
            'word': ''.join(str(deg[x]) for x in rot[h]), 'C': C, 'ecc': max(d), 'S': H.S, 'maxdF': max(H.dF),
            'meandF': sum(H.dF[k] for k in un) / max(1, len(un)), 'dl': sum(H.dl[k] for k in un) / max(1, len(un)),
            'maxrun': mx, 'cyc': len(H.pi_cycles()), 'unreach': sum(x < 0 for x in H.dF)}) + '\n'); out.flush()
