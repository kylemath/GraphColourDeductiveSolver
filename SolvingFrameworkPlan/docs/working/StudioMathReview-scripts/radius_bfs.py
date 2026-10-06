"""Shortest pure-Kempe fill from a certificate state (whole two-colour components of G - hole, any pair).
Usage: python3 -I radius_bfs.py <graph id> <hole> <cert dir> <out.json>"""
import json, sys, itertools
from collections import deque
gid, hole = sys.argv[1], int(sys.argv[2])
C = sys.argv[3]  # certificate directory, e.g. backgroundMaterial/planemap-structural/studiointel/run-C-2026-10-06/cert/
faces = json.load(open(C+gid+'.graph.json'))['faces']
st = json.load(open(C+gid+'.hole%d.state.json' % hole))
n = 1+max(max(f) for f in faces)
adj = [set() for _ in range(n)]
for f in faces:
    for i in range(3):
        a, b = f[i], f[(i+1) % 3]; adj[a].add(b); adj[b].add(a)
c0 = tuple(st[str(v)] if v != hole else -1 for v in range(n))
assert all(c0[u] != c0[v] for u in range(n) for v in adj[u] if u != hole and v != hole)
def canon(c):
    m = {}; return tuple(-1 if x < 0 else m.setdefault(x, len(m)) for x in c)
def target(c): return len({c[v] for v in adj[hole]}) < 4
def moves(c):
    for a, b in itertools.combinations(range(4), 2):
        seen = set()
        for s in range(n):
            if s == hole or c[s] not in (a, b) or s in seen: continue
            comp = {s}; q = [s]
            while q:
                u = q.pop()
                for w in adj[u]:
                    if w != hole and w not in comp and c[w] in (a, b): comp.add(w); q.append(w)
            seen |= comp
            d = list(c)
            for v in comp: d[v] = b if c[v] == a else a
            yield (a, b, s, sorted(comp)), tuple(d)
start = canon(c0); par = {start: None}; dq = deque([(c0, 0)]); best = None
while dq:
    c, k = dq.popleft()
    if target(c): best = (c, k); break
    for mv, d in moves(c):
        cd = canon(d)
        if cd not in par: par[cd] = (canon(c), mv, c); dq.append((d, k+1))
print('distance', best[1], 'states explored', len(par))
path = []; c = best[0]
while par[canon(c)] is not None:
    pc, mv, cc = par[canon(c)]; path.append((cc, mv)); c = cc
path.reverse()
json.dump({'n': n, 'hole': hole, 'adj': [sorted(a) for a in adj], 'c0': c0,
           'steps': [{'c': list(cc), 'a': mv[0], 'b': mv[1], 's': mv[2], 'S': mv[3]} for cc, mv in path],
           'final': list(best[0])}, open(sys.argv[4], 'w'))
for cc, mv in path: print(mv)
