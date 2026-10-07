"""Independent replay of an F-cycle file: radius and distance-reducing first moves per state, under
whole-component Kempe swaps of G - hole (any pair). Usage: python3 -I fcycle_check.py <file.json> <out.json>"""
import json, sys, itertools
from collections import deque
D = json.load(open(sys.argv[1])); hole = D['hole']; link = D['link']
n = 1 + max(max(f) for f in D['faces'])
adj = [set() for _ in range(n)]
for f in D['faces']:
    for i in range(3):
        a, b = f[i], f[(i+1) % 3]; adj[a].add(b); adj[b].add(a)
assert sorted(adj[hole]) == sorted(link)
def canon(c):
    m = {}; return tuple(-1 if x < 0 else m.setdefault(x, len(m)) for x in c)
def target(c): return len({c[v] for v in link}) < 4
def moves(c):
    for a, b in itertools.combinations(range(4), 2):
        seen = set()
        for s in range(n):
            if s == hole or c[s] not in (a, b) or s in seen: continue
            comp = {s}; q = [s]
            while q:
                u = q.pop()
                for x in adj[u]:
                    if x != hole and x not in comp and c[x] in (a, b): comp.add(x); q.append(x)
            seen |= comp
            d = list(c)
            for v in comp: d[v] = b if c[v] == a else a
            yield (a, b, min(comp), sorted(comp)), tuple(d)
memo = {}
def dist(c):
    k = canon(c)
    if k in memo: return memo[k]
    seen = {k}; dq = deque([(c, 0)])
    while dq:
        x, d = dq.popleft()
        if target(x): memo[k] = d; return d
        for _, y in moves(x):
            ky = canon(y)
            if ky not in seen: seen.add(ky); dq.append((y, d+1))
def path(c):
    out = []
    while not target(c):
        k = dist(c)
        for mv, d in moves(c):
            if dist(d) == k - 1: out.append((mv, c)); c = d; break
    return out, c
res = []; bad = 0
for i, st in enumerate(D['cycle_canonical_states']):
    c = tuple(st['state'][str(v)] if v != hole else -1 for v in range(n))
    assert all(c[u] != c[v] for u in range(n) for v in adj[u] if hole not in (u, v))
    r = dist(c)
    red = []
    for mv, d in moves(c):
        if dist(d) == r - 1:
            red.append({'pair': [mv[0], mv[1]], 'size': len(mv[3]), 'link_positions_in_K': sorted(link.index(v) for v in mv[3] if v in link), 'S': mv[3], 's': mv[2], 'next': list(d)})
    mine = sorted((tuple(m['pair']), m['size'], tuple(m['link_positions_in_K'])) for m in red)
    theirs = sorted((tuple(m['pair']), m['size'], tuple(sorted(m['link_positions_in_K']))) for m in st['first_moves_toward_fill'])
    ok = (r == st['radius'] and mine == theirs)
    bad += not ok
    silent = [m for m in red if not m['link_positions_in_K']]
    p, fin = path(c)
    res.append({'c': list(c), 'radius': r, 'silent': silent,
                'path': [{'a': mv[0], 'b': mv[1], 's': mv[2], 'S': mv[3], 'c': list(cc)} for mv, cc in p], 'final': list(fin),
                'silent_paths': [{'path': [{'a': mv[0], 'b': mv[1], 's': mv[2], 'S': mv[3], 'c': list(cc)} for mv, cc in path(tuple(m['next']))[0]], 'final': list(path(tuple(m['next']))[1])} for m in silent]})
    print(i, 'radius', r, 'file', st['radius'], 'moves match' if mine == theirs else f'MISMATCH mine={mine} file={theirs}', 'silent', len(silent))
print('mismatches', bad, 'states', len(res), 'with silent', sum(1 for x in res if x['silent']))
json.dump({'n': n, 'hole': hole, 'adj': [sorted(a) for a in adj], 'states': res}, open(sys.argv[2], 'w'))
