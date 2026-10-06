#!/usr/bin/env python3
"""studiointel check.py -- INDEPENDENT CHECKER. Imports NO producer code (not radius.py, graphs.py, builders.py). stdlib only.
Input: a graph file {"faces": [[a,b,c],...]} (CCW), a hole, and a certificate. Verifies by its own definitions, written from the
spec text in radius.py's docstring / MathConjectureR sec.1, with a different algorithm (explicit alternating-path search for the
locks; union-find for swaps; colourings kept as dicts).

  python3 check.py lb   GRAPH.json HOLE STATE.json K     -> verifies r(s) >= K : s is a proper colouring of T-hole (dict vertex->colour), and every state within
                                                            K-2 swaps of s is unfilled and doubly locked (so no filled/non-DL state is that close).
  python3 check.py tl   GRAPH.json HOLE CLASS.json       -> verifies a TARGETLESS class: a list of colourings, each proper, each DL, closed under every whole-component swap.
  python3 check.py enum GRAPH.json HOLE                  -> independent exhaustive count: #states, #filled, #unfilled-nonDL, #DL (by own enumeration), for regression.
"""
import sys, json, itertools

def load(path, hole):
    faces = [tuple(f) for f in json.load(open(path))['faces']]
    nxt = {}                               # at the hole: successor in rotation
    for f in faces:
        for i in range(3):
            if f[i] == hole: nxt[f[(i + 1) % 3]] = f[(i + 2) % 3]
    x = min(nxt); link = [x]
    for _ in range(4): x = nxt[x]; link.append(x)
    assert nxt[x] == link[0] and len(set(link)) == 5, 'hole is not a degree-5 vertex'
    adj = {}
    for f in faces:
        for i in range(3):
            a, b = f[i], f[(i + 1) % 3]
            if hole not in (a, b): adj.setdefault(a, set()).add(b); adj.setdefault(b, set()).add(a)
    return adj, link

def proper(adj, col):
    return set(col) == set(adj) and all(col[u] != col[w] for u in adj for w in adj[u]) and all(0 <= c < 4 for c in col.values())

def alt_path(adj, col, s, t, p, q):
    """is there a path s..t using only vertices coloured p or q (both ends included)? iterative DFS."""
    stack = [s]; seen = {s}
    while stack:
        u = stack.pop()
        if u == t: return True
        for w in adj[u]:
            if w not in seen and col[w] in (p, q): seen.add(w); stack.append(w)
    return False

def kind(adj, link, col):
    cs = [col[x] for x in link]
    if len(set(cs)) < 4: return 'filled'
    reps = [j for j in range(5) if cs[j] == cs[(j + 2) % 5]]
    assert len(reps) == 1
    j = reps[0]; m, a, b = link[(j + 1) % 5], link[(j + 3) % 5], link[(j + 4) % 5]
    l1 = alt_path(adj, col, m, a, col[m], col[a]); l2 = alt_path(adj, col, m, b, col[m], col[b])
    return 'DL' if (l1 and l2) else 'nonDL'

def neighbours(adj, col):
    """all whole-component swaps, via union-find"""
    out = []
    for p, q in itertools.combinations(range(4), 2):
        par = {u: u for u in adj if col[u] in (p, q)}
        def find(x):
            while par[x] != x: par[x] = par[par[x]]; x = par[x]
            return x
        for u in par:
            for w in adj[u]:
                if w in par: par[find(u)] = find(w)
        groups = {}
        for u in par: groups.setdefault(find(u), []).append(u)
        for g in groups.values():
            new = dict(col)
            for u in g: new[u] = q if col[u] == p else p
            out.append(new)
    return out

def norm(col):
    mp = {}
    for u in sorted(col):
        if col[u] not in mp: mp[col[u]] = len(mp)
    return tuple(sorted((u, mp[c]) for u, c in col.items()))

def lb(path, hole, spath, K):
    adj, link = load(path, hole); s = {int(u): c for u, c in json.load(open(spath)).items()}
    assert proper(adj, s), 'not a proper 4-colouring of T-hole'
    seen = {norm(s)}; layer = [s]
    for depth in range(K - 1):                    # states at distance 0..K-2
        nxt = []
        for col in layer:
            k = kind(adj, link, col)
            if k != 'DL': return 'FAIL: a %s state at distance %d (< K-1 = %d)' % (k, depth, K - 1)
            if depth < K - 2:
                for nc in neighbours(adj, col):
                    key = norm(nc)
                    if key not in seen: seen.add(key); nxt.append(nc)
        layer = nxt
    return 'OK: r(s) >= %d (all %d states within %d swaps are doubly locked)' % (K, len(seen), K - 2)

def tl(path, hole, cpath):
    adj, link = load(path, hole); cl = [{int(u): c for u, c in d.items()} for d in json.load(open(cpath))]
    keys = {norm(c) for c in cl}
    for c in cl:
        if not proper(adj, c): return 'FAIL: improper colouring'
        if kind(adj, link, c) != 'DL': return 'FAIL: a member is not doubly locked'
        for nc in neighbours(adj, c):
            if norm(nc) not in keys: return 'FAIL: not closed under swaps'
    return 'OK: targetless class of %d doubly locked states, closed under all swaps' % len(cl)

def enum(path, hole):
    adj, link = load(path, hole)
    verts = sorted(adj, key=lambda u: -len(adj[u]))        # different order from the producer: highest degree first, then connectivity
    order = []; seen = set()
    for r in verts:
        if r in seen: continue
        stack = [r]; seen.add(r)
        while stack:
            u = stack.pop(); order.append(u)
            for w in sorted(adj[u], reverse=True):
                if w not in seen: seen.add(w); stack.append(w)
    tally = {'states': 0, 'filled': 0, 'nonDL': 0, 'DL': 0}; col = {}
    def rec(i):
        if i == len(order):
            tally['states'] += 1; tally[kind(adj, link, col)] += 1; return
        u = order[i]; used = {col[w] for w in adj[u] if w in col}
        top = len(set(col.values()))
        for c in range(min(top + 1, 4)):
            if c not in used: col[u] = c; rec(i + 1); del col[u]
    col[order[0]] = 0; rec(1)
    return tally

if __name__ == '__main__':
    cmd = sys.argv[1]
    if cmd == 'lb': print(lb(sys.argv[2], int(sys.argv[3]), sys.argv[4], int(sys.argv[5])))
    elif cmd == 'tl': print(tl(sys.argv[2], int(sys.argv[3]), sys.argv[4]))
    elif cmd == 'enum': print(enum(sys.argv[2], int(sys.argv[3])))
