import gzip, json, collections, os
base = os.path.expanduser('~/GraphColour/SolvingFrameworkPlan/docs/working/Census33/out/')
G = {}
for l in open(base + 'frame-33.txt'):
    p = l.split(); G[p[0]] = [[int(x) for x in r.split(',')] for r in p[2].split(';')]
rows = []
for l in gzip.open(base + 'eval-33.jsonl.gz', 'rt'):
    r = json.loads(l); rot = G[r['name']]; n = len(rot)
    for hs, h in r['holes'].items():
        v = int(hs); d = [-1] * n; d[v] = 0; q = collections.deque([v])
        while q:
            u = q.popleft()
            for w in rot[u]:
                if d[w] < 0: d[w] = d[u] + 1; q.append(w)
        c = collections.Counter(min(d[u], 4) for u in range(n) if len(rot[u]) == 5 and u != v)
        rows.append((c[1], c[2], c[3], c[4], h['R'], h['NR'], h['mf'], h['S'], h.get('ndlc', 0)))
print('holes', len(rows))
def table(key, idx, name):
    T = collections.defaultdict(list)
    for r in rows: T[key(r)].append(r)
    print('\n' + name + ' | holes | mean R | mean NR | P(R>=4) | P(NR>=6) | min-class F/N mean | P(mf=1/4) | all-DL cycles')
    for k in sorted(T):
        L = T[k]
        if len(L) < 200: continue
        m = lambda i: sum(x[i] for x in L) / len(L)
        print('%6s | %6d | %.2f | %.2f | %.4f | %.4f | %.3f | %.4f | %d' % (k, len(L), m(4), m(5), sum(x[4] >= 4 for x in L) / len(L), sum(x[5] >= 6 for x in L) / len(L), m(6), sum(abs(x[6] - 0.25) < 1e-9 for x in L) / len(L), sum(x[8] for x in L)))
table(lambda r: r[0], 0, 'deg-5 neighbours (dist 1)')
table(lambda r: r[1], 1, 'deg-5 at dist 2')
table(lambda r: r[0] + r[1], 1, 'deg-5 within dist 2')
table(lambda r: r[2] + r[3], 1, 'deg-5 at dist >=3')
