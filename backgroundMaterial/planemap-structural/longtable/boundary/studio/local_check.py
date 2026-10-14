"""Independent local check of a boundary-solvability counterexample (no global state enumeration, no shared code with
bnd.cpp or HoleGame): from the given state, (1) the closure under swaps of non-web chains meeting R contains no filled
state, (2) an unrestricted BFS reaches a filled state within the claimed depth.
usage: local_check.py FILE NAME HOLE R(comma) STATE DEPTH"""
import sys, collections
f, name, h, R, state, depth = sys.argv[1], sys.argv[2], int(sys.argv[3]), set(map(int, sys.argv[4].split(','))), sys.argv[5], int(sys.argv[6])
rot = next([[int(x) for x in r.split(',')] for r in l.split()[2].split(';')] for l in open(f) if l.split()[0] == name)
n = len(rot); V = [v for v in range(n) if v != h]
def canon(c):
    mp = {}; return tuple(mp.setdefault(c[v], len(mp)) if v != h else -1 for v in range(n))
def filled(c): return len({c[x] for x in rot[h]}) <= 3
def chains(c):
    out = []
    for a in range(4):
        for b in range(a + 1, 4):
            seen = set(); comps = []
            for s in V:
                if s in seen or c[s] not in (a, b): continue
                comp = {s}; st = [s]; seen.add(s)
                while st:
                    u = st.pop()
                    for w in rot[u]:
                        if w != h and w not in comp and c[w] in (a, b): comp.add(w); seen.add(w); st.append(w)
                comps.append(comp)
            if len(comps) >= 2: out += [((a, b), K) for K in comps]
    return out
def flip(c, ab, K):
    a, b = ab; d = list(c)
    for u in K: d[u] = b if c[u] == a else a
    return canon(d)
c0 = canon([int(x) if x != '.' else -1 for x in state])
# proper colouring check
assert all(c0[u] != c0[w] for u in V for w in rot[u] if w != h), 'not proper'
assert not filled(c0)
seen = {c0}; q = [c0]; anyfill = False
while q:
    c = q.pop(); anyfill |= filled(c)
    for ab, K in chains(c):
        if K & R:
            d = flip(c, ab, K)
            if d not in seen: seen.add(d); q.append(d)
print('restricted closure size', len(seen), 'contains a filled state:', anyfill)
lev = {c0: 0}; q = collections.deque([c0]); hit = None
while q:
    c = q.popleft()
    if filled(c): hit = lev[c]; break
    if lev[c] >= depth: continue
    for ab, K in chains(c):
        d = flip(c, ab, K)
        if d not in lev: lev[d] = lev[c] + 1; q.append(d)
print('unrestricted distance to a fill:', hit)
