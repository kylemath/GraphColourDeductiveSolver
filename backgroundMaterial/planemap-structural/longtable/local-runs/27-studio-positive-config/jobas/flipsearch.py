#!/usr/bin/env python3
"""Job AS: search for a (5,5,5,5,6) hole carrying a Gamma-cycle with L > 60. Graphs = oriented face lists; moves = edge flips keeping the core class
(min degree 5, max degree 8, no separating triangle, simple). Evaluator = ../picyc (full enumeration of T - v at every degree-5 hole; Gamma <=> w = L/5 > 0).
usage: flipsearch.py SEEDJSON MODE [steps seed]   MODE = targeted | walk"""
import sys, json, random, subprocess, itertools, os, tempfile
from collections import Counter
PICYC = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'picyc')
def canon(ld, cap=8):
    d = [min(x, cap) for x in ld]; return min(tuple(s[r:] + s[:r]) for s in (d, d[::-1]) for r in range(5))
def rotation(F):
    labels = sorted({x for t in F for x in t}); m = {u: i for i, u in enumerate(labels)}; nxt = {}
    for t in F:
        for i in range(3): nxt.setdefault(m[t[i]], {})[m[t[(i + 1) % 3]]] = m[t[(i + 2) % 3]]
    rot = []
    for v in range(len(labels)):
        s = min(nxt[v]); r = [s]
        while nxt[v][r[-1]] != s: r.append(nxt[v][r[-1]])
        rot.append(r[::-1])
    return rot
def adjacency(F):
    adj = {}
    for t in F:
        for a, b in itertools.combinations(t, 2): adj.setdefault(a, set()).add(b); adj.setdefault(b, set()).add(a)
    return adj
def core_ok(F):
    adj = adjacency(F); deg = {v: len(a) for v, a in adj.items()}
    if min(deg.values()) < 5 or max(deg.values()) > 8: return False
    faces = {frozenset(t) for t in F}
    for a in adj:
        for b in adj[a]:
            if b <= a: continue
            for c in adj[a] & adj[b]:
                if c > b and frozenset((a, b, c)) not in faces: return False
    return True
def flip(F, a, b):
    fa = [t for t in F if a in t and b in t]
    if len(fa) != 2: return None
    def third(t): return [x for x in t if x not in (a, b)][0]
    t1, t2 = fa; c, d = third(t1), third(t2)
    if d in adjacency(F)[c]: return None
    # orient: t1 contains a->b in cyclic order
    def has(t, u, v): i = t.index(u); return t[(i + 1) % 3] == v
    if not has(t1, a, b): t1, t2 = t2, t1; c, d = d, c
    G = [t for t in F if t is not fa[0] and t is not fa[1]]
    G += [(a, d, c), (b, c, d)]
    return G
def evaluate(F, name='g'):
    rot = rotation(F); line = '%s %d %s\n' % (name, len(rot), ';'.join(','.join(map(str, r)) for r in rot))
    with tempfile.NamedTemporaryFile('w', suffix='.txt', delete=False) as fh: fh.write(line); fn = fh.name
    out = subprocess.run([PICYC, fn], capture_output=True, text=True).stdout; os.unlink(fn); res = []
    for l in out.splitlines():
        r = json.loads(l)
        if r['kind'] != 'hole' or 'hist' not in r: continue
        g = [(L, c) for w, L, c in r['hist'] if w > 0 and 5 * w == L]
        res.append(dict(hole=r['hole'], pat=canon(r['linkdeg']), gamma=g, maxw=r['maxw'], states=r['states']))
    return res
def score(res):
    best6 = max([L for r in res if r['pat'] == (5, 5, 5, 5, 6) for L, c in r['gamma']] + [0])
    bestany = max([L for r in res for L, c in r['gamma']] + [0])
    return best6, bestany
if __name__ == '__main__':
    F0 = [tuple(t) for t in json.load(open(sys.argv[1]))['faces']]; mode = sys.argv[2]
    steps = int(sys.argv[3]) if len(sys.argv) > 3 else 200; rng = random.Random(int(sys.argv[4]) if len(sys.argv) > 4 else 1)
    base = evaluate(F0); print('seed', sys.argv[1], 'score (best L at 55556, best L anywhere)', score(base), [(r['hole'], r['pat'], r['gamma']) for r in base if r['gamma']], flush=True)
    found = []
    def edges(F): return sorted({(min(a, b), max(a, b)) for t in F for a, b in itertools.combinations(t, 2)})
    if mode == 'targeted':   # all single flips, then all double flips among those keeping the core class, reporting any 55556 Gamma
        cur = [(F0, ())]
        for depth in (1, 2):
            nxt = []
            for F, hist in cur:
                for a, b in edges(F):
                    G = flip(F, a, b)
                    if G is None or not core_ok(G): continue
                    res = evaluate(G); s = score(res)
                    hit = [(r['hole'], r['pat'], r['gamma']) for r in res if r['pat'] == (5, 5, 5, 5, 6) and r['gamma']]
                    if hit: found.append((hist + ((a, b),), s, hit)); print('HIT depth', depth, hist + ((a, b),), s, hit, flush=True)
                    if depth == 1: nxt.append((G, hist + ((a, b),)))
            cur = nxt if depth == 1 else []
            print('depth', depth, 'done; candidates', len(nxt), flush=True)
    else:   # walk: hill-climb on (best L at 55556, best L anywhere) with random acceptance
        F = F0; s = score(base); bestF = F; bests = s
        for it in range(steps):
            es = edges(F); rng.shuffle(es)
            for a, b in es:
                G = flip(F, a, b)
                if G is not None and core_ok(G): break
            else: break
            res = evaluate(G); s2 = score(res)
            if s2 >= s or rng.random() < 0.15: F, s = G, s2
            if s2 > bests: bests, bestF = s2, G; print('it', it, 'new best', s2, [(r['hole'], r['pat'], r['gamma']) for r in res if r['gamma']][:6], flush=True)
            if s2[0] > 60: found.append(s2); json.dump({'faces': [list(t) for t in G]}, open('found-%s-%d.json' % (os.path.basename(sys.argv[1]).replace('.json', ''), it), 'w'))
        json.dump({'faces': [list(t) for t in bestF], 'score': bests}, open('best-walk-%s-%s.json' % (os.path.basename(sys.argv[1]).replace('.json', ''), sys.argv[4] if len(sys.argv) > 4 else '1'), 'w'))
    print('DONE found', len(found))
