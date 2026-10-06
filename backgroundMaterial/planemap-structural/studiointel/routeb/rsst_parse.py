#!/usr/bin/env python3
"""routeb/rsst_parse.py -- parse RSST unavoidable.conf into free completions (ring vertices 1..r in order, configuration vertices r+1..n,
adjacency lists in rotation order). faces() returns oriented faces from the rotations of the configuration (interior) vertices."""
def parse(path):
    blocks, cur = [], []
    for line in open(path):
        if line.strip() == '':
            if cur: blocks.append(cur); cur = []
        else: cur.append(line.split())
    if cur: blocks.append(cur)
    confs = []
    for b in blocks:
        name = b[0][0]; n, r, a, bb = map(int, b[1][:4]); k = int(b[2][0]); X = list(map(int, b[2][1:]))
        adj = {}
        for row in b[3:3 + n]:
            i, d = int(row[0]), int(row[1]); adj[i] = [int(x) for x in row[2:]]
            assert len(adj[i]) == d, (name, i)
        confs.append({'name': name, 'n': n, 'r': r, 'a': a, 'b': bb, 'k_contract': k, 'X': X, 'adj': adj})
    return confs

def faces(c):
    fs = set()
    for u in range(c['r'] + 1, c['n'] + 1):
        L = c['adj'][u]
        for i in range(len(L)):
            f = (u, L[i], L[(i + 1) % len(L)]); j = f.index(min(f)); fs.add(f[j:] + f[:j])
    return sorted(fs)

if __name__ == '__main__':
    import sys
    from collections import Counter
    cs = parse(sys.argv[1])
    print('configurations', len(cs))
    print('ring sizes', dict(sorted(Counter(c['r'] for c in cs).items())))
    print('contraction (k>0)', sum(c['k_contract'] > 0 for c in cs))
    d5 = [c for c in cs if any(len(c['adj'][u]) == 5 for u in range(c['r'] + 1, c['n'] + 1))]
    print('with an interior degree-5 vertex', len(d5), ' ring sizes', dict(sorted(Counter(c['r'] for c in d5).items())))
    print('n (free completion) range', min(c['n'] for c in cs), max(c['n'] for c in cs), ' interior sizes', dict(sorted(Counter(c['n'] - c['r'] for c in cs).items())))
