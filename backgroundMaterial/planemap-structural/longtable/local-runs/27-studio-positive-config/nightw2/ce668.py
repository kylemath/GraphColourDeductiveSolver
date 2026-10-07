#!/usr/bin/env python3
"""ce668.py (NightW2 §11): the Job AK open-run counterexample p25 #668 h18. Own minimal engine: on a DL state pi = R+3 (swap the
{alpha,A}-component of x_{j+2}); backwards pi^-1 = R+2 (swap the {alpha,B}-component of x_j) on a Lock1 state. Iterates forward from the
R3k0 state (pos 8) and backward from R3k2 (pos 4) while DL, printing type/k, locks, lock-chain sizes, and the cycle ranks of the three pairs.
Single core, < 1 s."""
import json
from collections import deque
d = json.load(open('../jobuv/jobak-counterexample.json'))
rot = d['rotation_system']; h = d['hole']; X = d['link']; n = len(rot)
adj = [set(r) for r in rot]
def wv(t):  # third vertex of face x_t x_{t+1} other than h
    a, b = X[t], X[(t + 1) % 5]; c = [u for u in adj[a] & adj[b] if u != h]; assert len(c) == 1, c; return c[0]
W = [wv(t) for t in range(5)]
q = next(t for t in range(5) if len(rot[X[t]]) == 6); p = X[q]; y = W[(q + 4) % 5]; z = W[q]
m = [u for u in adj[p] if u not in (h, X[(q + 1) % 5], X[(q + 4) % 5], y, z)][0]
CM = {'a': 0, 'b': 1, 'c': 2, 'd': 3}
cols = [{int(k): CM[v] for k, v in c.items()} for c in d['colourings']]
def comp(c, a, b, s):
    if c[s] not in (a, b): return set()
    S = {s}; Q = deque([s])
    while Q:
        u = Q.popleft()
        for v in adj[u]:
            if v != h and v not in S and c[v] in (a, b): S.add(v); Q.append(v)
    return S
def rank(c, a, b):
    V = [u for u in range(n) if u != h and c[u] in (a, b)]; Vs = set(V)
    E = sum(1 for u in V for v in adj[u] if v in Vs and u < v); seen = set(); C = 0
    for u in V:
        if u not in seen: C += 1; seen |= comp(c, a, b, u)
    return E - len(V) + C
def frame(c):
    L = [c[x] for x in X]
    for j in range(5):
        if L[j] == L[(j + 2) % 5] and len(set(L)) == 4: return j, L[j], L[(j + 1) % 5], L[(j + 3) % 5], L[(j + 4) % 5]
    return None
def info(c):
    f = frame(c)
    if f is None: return None
    j, al, mu, A, B = f
    l1 = comp(c, mu, A, X[(j + 1) % 5]); l2 = comp(c, mu, B, X[(j + 1) % 5])
    L1 = X[(j + 3) % 5] in l1; L2 = X[(j + 4) % 5] in l2
    ty = 'R1' if c[W[j]] == A else ('R3' if c[W[j]] == B and c[W[(j + 3) % 5]] == mu else ('R2' if c[W[j]] == B else '?'))
    return dict(j=j, k=(q - j) % 5, ty=ty, L1=L1, L2=L2, n1=len(l1), n2=len(l2), al=al, mu=mu, A=A, B=B,
                Kfull=len(comp(c, al, mu, X[(j + 1) % 5])) == sum(1 for u in range(n) if u != h and c[u] in (al, mu)))
def swap(c, S, a, b):
    c = dict(c)
    for v in S: c[v] = b if c[v] == a else a
    return c
def fwd(c):
    I = info(c); S = comp(c, I['al'], I['A'], X[(I['j'] + 2) % 5]); return swap(c, S, I['al'], I['A']), len(S)
def bwd(c):
    I = info(c); S = comp(c, I['al'], I['B'], X[I['j']]); return swap(c, S, I['al'], I['B']), len(S)
def show(tag, c, extra=''):
    I = info(c)
    if I is None: print(tag, 'FILLED (no repeat)', extra); return
    r = {('%d%d' % (a, b)): rank(c, a, b) for a in range(4) for b in range(a + 1, 4)}
    print('%-6s %s k%d j%d Lock1 %d(|%d|) Lock2 %d(|%d|) sigma-fixed %d  ranks %s %s' % (tag, I['ty'], I['k'], I['j'], I['L1'], I['n1'], I['L2'], I['n2'], I['Kfull'], r, extra))
print('p25#668 h18: q=%d p=%d y=%d z=%d m=%d W=%s link=%s' % (q, p, y, z, m, W, X))
# check Studio colourings are consecutive pi-steps
def same_up_to_perm(a, b):
    mp = {}
    for v in a:
        if mp.setdefault(a[v], b[v]) != b[v]: return False
    return True
cc = cols[0]
for i in range(4):
    cc, s = fwd(cc); assert same_up_to_perm(cc, cols[i + 1]), i
print('Studio colourings pos4..8 reproduced by R+3 steps up to colour names (Studio stores canonical colourings): OK')
c = cols[0]; back = []
for t in range(1, 40):
    I = info(c)
    if I is None or not I['L1']: break
    c, s = bwd(c); back.append(c)
for t, cc in reversed(list(enumerate(back, 1))): show('pos4-%d' % t, cc)
c = cols[0]; show('pos4', c)
for i in range(1, 5): c, s = fwd(c); show('pos%d' % (4 + i), c, '|K step|=%d' % s)
for t in range(1, 40):
    I = info(c)
    if I is None or not (I['L1'] and I['L2']): break
    c, s = fwd(c); show('pos%d' % (8 + t), c, '|K step|=%d' % s)
