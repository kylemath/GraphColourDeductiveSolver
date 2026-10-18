#!/usr/bin/env python3
"""Round B2: convert RSST unavoidable.conf to the wheeldis line format (name r m ringadj intadj) used by kc and cfast,
plus RSST's contract X in engine edge names (R<k> = ring vertex k+1, I<j> = conf vertex r+1+j; ring end first,
interior edges with the smaller index first).  Header fields: n r ext bad (bad = 0 for D)."""
import os
H = os.path.dirname(os.path.abspath(__file__))
CONF = os.path.normpath(os.path.join(H, *(['..'] * 7), 'studiointel', 'routeb', 'rsst', 'unavoidable.conf'))

def load(path=CONF):
    blocks, cur = [], []
    for line in open(path):
        if line.strip() == '':
            if cur: blocks.append(cur); cur = []
        else: cur.append(line.split())
    if cur: blocks.append(cur)
    out = []
    for idx, b in enumerate(blocks):
        name = b[0][0]; n, r, ext, bad = map(int, b[1][:4]); k = int(b[2][0]); xs = list(map(int, b[2][1:]))
        assert len(xs) == 2 * k, name
        adj = {}
        for row in b[3:3 + n]:
            v, d = int(row[0]), int(row[1]); adj[v] = [int(x) for x in row[2:]]; assert len(adj[v]) == d
        m = n - r
        ra = [[t - 1 for t in adj[r + 1 + a] if t <= r] for a in range(m)]
        ia = [[t - r - 1 for t in adj[r + 1 + a] if t > r] for a in range(m)]
        line = '%s %d %d %s %s' % (name, r, m, ';'.join(','.join(map(str, L)) if L else '-' for L in ra),
                                   ';'.join(','.join(map(str, L)) if L else '-' for L in ia))
        X = []
        for q in range(k):
            a, c = xs[2 * q], xs[2 * q + 1]
            assert c in adj[a], (name, a, c)
            if a > c: a, c = c, a
            if c <= r: raise ValueError('ring-ring contract edge in %s' % name)
            X.append(('R%d-I%d' % (a - 1, c - r - 1)) if a <= r else ('I%d-I%d' % (a - r - 1, c - r - 1)))
        out.append(dict(idx=idx, name=name, n=n, r=r, m=m, ext=ext, bad=bad, k=k, X=','.join(X),
                        label='C' if k > 0 else 'D', line=line))
    return out

if __name__ == '__main__':
    import collections
    cs = load(); print(len(cs), collections.Counter(c['label'] for c in cs))
    print(sorted(collections.Counter((c['r'], c['label']) for c in cs).items()))
    print('C with bad==0:', sum(c['k'] > 0 and c['bad'] == 0 for c in cs), ' D with bad>0:', sum(c['k'] == 0 and c['bad'] > 0 for c in cs))
    for c in cs:
        if c['name'] in ('2.126', '122.126'): print(c['idx'], c['line'], c['X'])
