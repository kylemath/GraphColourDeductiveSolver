#!/usr/bin/env python3
"""Second implementation of the A6 walk (Studio Job 11, exploratory). Pure Python; shares no code with star-rules.js /
rim.js. It re-derives, from the map and a start key, the rule "Fewest locks, new stars":
  - a star is a colouring of T - hole up to renaming; its key renames colours by first appearance along vertex ids;
  - moves are swaps of non-web Kempe chains (a web is the only chain of its colour pair), merged by the resulting key;
    the merged move is labelled by its gentlest chain (fewest rim vertices, then smallest, then smallest first vertex);
  - locks: at an unfilled rim (5 rim vertices, 4 colours) take the first t with c[t] = c[t+2]; with x = rim rotated
    to t, alpha = c[t], gamma = c[t+3], delta = c[t+4]: lock 1 = x3 in the {c(x1), gamma} chain of x1, lock 2 = x4 in
    the {c(x1), delta} chain of x1; pi = swap of the {alpha, gamma} chain of x2 at a double lock;
  - the step: a filling child if any; else among children with the fewest locks (filled counts as -1) prefer one not
    visited before; ties: smaller chain, then smaller key;
  - the walk stops at a fill, after 60 swaps, or when (star, last move was pi, star seen before) repeats with no new
    star visited since (the same stopping rule as star-rules.js for this rule).
usage: a6_check.py MAPS.json KEY START_KEY  -> prints the walk.  As a module: walk(map, start_key)."""
import sys, json

def chains(m, col):
    n, h, adj = m['n'], m['hole'], m['_adj']; out = []
    for a in range(4):
        for b in range(a + 1, 4):
            seen = [False] * n; mine = []
            for s in range(n):
                if s == h or seen[s] or col[s] not in (a, b): continue
                comp = [s]; seen[s] = True; i = 0
                while i < len(comp):
                    for w in adj[comp[i]]:
                        if w != h and not seen[w] and col[w] in (a, b): seen[w] = True; comp.append(w)
                    i += 1
                mine.append(sorted(comp))
            for c in mine: out.append((a, b, c, len(mine) == 1))
    return out

def key(m, col):
    mp = {}; s = []
    for u in range(m['n']):
        if u == m['hole']: continue
        if col[u] not in mp: mp[col[u]] = len(mp)
        s.append(str(mp[col[u]]))
    return ''.join(s)

def chain_at(m, col, u, b):
    a = col[u]; comp = {u}; st = [u]
    while st:
        v = st.pop()
        for w in m['_adj'][v]:
            if w != m['hole'] and w not in comp and col[w] in (a, b): comp.add(w); st.append(w)
    return comp

def star(m, col):
    L = m['link']; c = [col[x] for x in L]
    if len(set(c)) <= 3: return dict(filled=True, lock=-1, pi=None)
    for t in range(5):
        if c[t] == c[(t + 2) % 5]:
            x = [L[(t + i) % 5] for i in range(5)]; alpha, gamma, delta = c[t], c[(t + 3) % 5], c[(t + 4) % 5]
            l1 = x[3] in chain_at(m, col, x[1], gamma); l2 = x[4] in chain_at(m, col, x[1], delta)
            pi = None
            if l1 and l2:
                K = chain_at(m, col, x[2], gamma); d = list(col)
                for u in K: d[u] = gamma if col[u] == alpha else alpha
                pi = key(m, d)
            return dict(filled=False, lock=int(l1) + int(l2), pi=pi)
    return dict(filled=False, lock=0, pi=None)

def moves(m, col):
    rim = set(m['link']); by = {}
    for a, b, c, web in chains(m, col):
        if web: continue
        d = list(col)
        for u in c: d[u] = b if col[u] == a else a
        k = key(m, d); hits = len([u for u in c if u in rim]); lab = (hits, len(c), c[0])
        if k not in by or lab < by[k][0]: by[k] = (lab, d)
    return [(k, lab[1], d) for k, (lab, d) in by.items()]   # (child key, label chain size, colouring)

def col_of(m, k):
    col = [-1] * m['n']; it = iter(k)
    for u in range(m['n']):
        if u != m['hole']: col[u] = int(next(it))
    return col

def walk(m, start, cap=60):
    if '_adj' not in m: m['_adj'] = [set(r) for r in m['rot']]
    cur = start; col = col_of(m, cur); visited = {cur: 1}; path = [cur]; ctx = {}; run = 0; seen = False; steps = 0
    while True:
        f = star(m, col)
        if f['filled']: return dict(solved=True, steps=steps, path=path, why='')
        if steps >= cap: return dict(solved=False, steps=steps, path=path, why='cap')
        ck = (cur, min(run, 1), seen)
        if ctx.get(ck) == len(visited): return dict(solved=False, steps=steps, path=path, why='loop')
        ctx[ck] = len(visited)
        mv = moves(m, col)
        if not mv: return dict(solved=False, steps=steps, path=path, why='dead')
        info = [(k, size, d, star(m, d)) for k, size, d in mv]
        fills = [x for x in info if x[3]['filled']]
        C = fills if fills else info
        if not fills:
            best = min(x[3]['lock'] for x in C); C = [x for x in C if x[3]['lock'] == best]
        new = [x for x in C if x[0] not in visited]
        if new: C = new
        C.sort(key=lambda x: (x[1], x[0]))
        k, size, d, fs = C[0]
        run = run + 1 if (f['pi'] is not None and k == f['pi']) else 0
        steps += 1; cur = k; col = d; path.append(cur)
        c0 = visited.get(cur, 0); visited[cur] = c0 + 1; seen = c0 > 0

if __name__ == '__main__':
    maps = {m['key']: m for m in json.load(open(sys.argv[1]))}
    print(json.dumps(walk(maps[sys.argv[2]], sys.argv[3])))
