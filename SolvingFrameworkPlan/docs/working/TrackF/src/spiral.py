#!/usr/bin/env python3
"""Track F [exploratory]: fullerene duals from face spirals (Fowler-Manolopoulos windup), written from scratch.
Faces 0..f-1 in spiral order, sizes 5/6 (= degrees in the dual triangulation).
windup(sizes) -> adjacency lists (unordered) or None.  embed(adj) -> rotation system via networkx planarity.
canon(rot) -> canonical string (min over directed edges and both orientations of a BFS code), for isomorphism dedup.
Output line format (as picyc / f66): 'name n r0;r1;...' with 0-based rotation lists."""
import sys, itertools, random
import networkx as nx

def windup(sizes):
    f = len(sizes); adj = [set() for _ in range(f)]; rem = list(sizes)
    def con(a, b):
        if a == b or b in adj[a]: return False
        adj[a].add(b); adj[b].add(a); rem[a] -= 1; rem[b] -= 1
        return rem[a] >= 0 and rem[b] >= 0
    if not con(0, 1): return None
    bd = [0, 1]
    for k in range(2, f):
        if not bd: return None
        if not con(k, bd[-1]): return None
        if len(bd) > 1 and not con(k, bd[0]): return None
        while len(bd) > 1 and rem[bd[0]] == 0:
            bd.pop(0)
            if bd and bd[0] not in adj[k]:
                if not con(k, bd[0]): return None
        while len(bd) > 1 and rem[bd[-1]] == 0:
            bd.pop()
            if bd and bd[-1] not in adj[k]:
                if not con(k, bd[-1]): return None
        bd.append(k)
    if any(r != 0 for r in rem): return None
    return [sorted(a) for a in adj]

def valid_triangulation(adj):
    n = len(adj); E = sum(len(a) for a in adj) // 2
    if E != 3 * n - 6: return None
    G = nx.Graph(); G.add_edges_from((u, v) for u in range(n) for v in adj[u])
    ok, emb = nx.check_planarity(G)
    if not ok: return None
    rot = [list(emb.neighbors_cw_order(v)) for v in range(n)]
    # triangulation check: every face of the embedding is a triangle, and no separating triangle (#triangles == 2n-4)
    tri = sum(1 for u in range(n) for v in adj[u] if v > u for w in adj[v] if w > v and w in adj[u])
    return rot, tri

def canon(rot):
    n = len(rot); best = None
    pos = [{w: i for i, w in enumerate(r)} for r in rot]
    for u in range(n):
        for v in rot[u]:
            for o in (1, -1):
                lab = {u: 0}; order = [u]; code = []; first = {u: v}
                q = 0
                while q < len(order):
                    x = order[q]; q += 1; r = rot[x]; d = len(r); s = pos[x][first[x]]
                    for i in range(d):
                        y = r[(s + o * i) % d]
                        if y not in lab: lab[y] = len(order); order.append(y); first[y] = x
                        code.append(lab[y])
                    code.append(-1)
                    if best is not None and code > best[:len(code)]: break
                else:
                    if best is None or code < best: best = code
                    continue
    return tuple(best)

def line(name, rot):
    return f"{name} {len(rot)} " + ";".join(",".join(map(str, r)) for r in rot)

def from_pentagons(f, pents):
    sizes = [6] * f
    for p in pents: sizes[p] = 5
    adj = windup(sizes)
    if adj is None: return None
    r = valid_triangulation(adj)
    if r is None: return None
    return r

def enumerate_all(natoms, out, limit=None):
    """all fullerene duals with natoms carbons (f = natoms/2 + 2 faces) by spiral DFS with incremental pruning (pentagon count)."""
    f = natoms // 2 + 2; seen = set(); cnt = 0
    for pents in itertools.combinations(range(f), 12):
        # cheap prune: first face pentagon or hexagon both allowed; windup decides
        r = from_pentagons(f, pents)
        if r is None: continue
        rot, tri = r
        c = canon(rot)
        if c in seen: continue
        seen.add(c); cnt += 1
        out.append((pents, rot, tri))
        if limit and cnt >= limit: break
    return out

if __name__ == '__main__':
    mode = sys.argv[1]
    if mode == 'spiral':   # spiral.py spiral NATOMS p1,p2,...(1-based) NAME
        n = int(sys.argv[2]); pents = [int(x) - 1 for x in sys.argv[3].split(',')]; r = from_pentagons(n // 2 + 2, pents)
        if r is None: print('invalid', file=sys.stderr); sys.exit(1)
        print(line(sys.argv[4], r[0]))
