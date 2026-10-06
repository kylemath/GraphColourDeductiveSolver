"""Which fan classes of c contain the intermediate colourings of the D-free walk c' -> c1 -> c2 -> c3 ?
For each rigid disc with c' of Case I/II, rebuild c', c1, c2, c3 (same swaps as classify_prime) and test membership of
each (as T-colouring with x coloured like the fan apex, up to colour renaming) in the Kempe class (cap) of c at fans u1,u3,u4,
and of c' at u0 (D-free class).   [exploratory]
usage: python3 ncounter_walk.py FILE [cap]"""
import sys
from collections import Counter, deque
from ncounter_lib import *
fn = sys.argv[1]; cap = int(sys.argv[2]) if len(sys.argv) > 2 else 3000

def class_set(adj, col, x, y, cap):
    n = len(adj)
    Gg = [set(a) for a in adj]; Gg[x].discard(y); Gg[y].discard(x)
    def canon(c):
        m = {}
        return tuple(m.setdefault(v, len(m)) for v in c)
    st0 = tuple(col[v] if v != x else col[y] for v in range(n))
    seen = {canon(st0)}; q = deque([st0])
    while q:
        st = q.popleft()
        for a, b in PAIRS:
            done = set()
            for s in range(n):
                if st[s] not in (a, b) or s in done: continue
                comp = {s}; stk = [s]
                while stk:
                    u = stk.pop()
                    for w in Gg[u]:
                        if w not in comp and st[w] in (a, b): comp.add(w); stk.append(w)
                done |= comp
                nc = list(st)
                for w in comp: nc[w] = b if st[w] == a else a
                k = canon(nc)
                if k not in seen:
                    if len(seen) >= cap: return None
                    seen.add(k); q.append(tuple(nc))
    return seen

def canon_of(col, x, y, n):
    m = {}
    return tuple(m.setdefault(v, len(m)) for v in [col[v] if v != x else col[y] for v in range(n)])

def walk(adj, col, x, ring):
    u0, u1, u2, u3, u4 = ring
    K2 = comp_of(adj, col, u2, {D, G}, x); c1p = swapK(col, K2, D, G)
    if u3 not in comp_of(adj, c1p, u0, {B, D}, x): return None
    Q4 = comp_of(adj, c1p, u4, {A, G}, x)
    if u1 in Q4 or u2 in Q4: return None
    c1 = swapK(c1p, Q4, A, G)
    if u2 not in comp_of(adj, c1, u0, {D, G}, x): return None
    E = comp_of(adj, c1, u3, {A, B}, x)
    if u1 in E: return None
    c2 = swapK(c1, E, A, B)
    R = comp_of(adj, c2, u4, {B, G}, x)
    c3 = swapK(c2, R, B, G)
    return [c1p, c1, c2, c3]

T = Counter(); N = 0
for line in open(fn):
    if not line.startswith('DISC'): continue
    adj, col, x, ring = parse_disc(line); n = len(adj)
    if not is_rigid(adj, col, x): continue
    w = walk(adj, col, x, ring)
    if w is None: continue
    t1 = classify_prime(adj, col, x, ring)[0]
    if t1 == 'II': tt = 'II'
    else: tt = 'I'
    N += 1
    row = []
    for y in (1, 3, 4):
        S = class_set(adj, col, x, ring[y], cap)
        if S is None: row.append('?'); continue
        row.append(''.join('1' if canon_of(c, x, ring[y], n) in S else '0' for c in w))
    T[(tt, tuple(row))] += 1
print(fn, 'walks', N)
for k, v in sorted(T.items()): print('  ', k, v)
