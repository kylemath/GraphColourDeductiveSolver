"""Show one ring case in a defect patch: show_case.py SIG U S(comma positions) KIND(rc|bf)"""
import sys, collections
from ringlib import *
sig, u, S, kind = sys.argv[1], int(sys.argv[2]), [int(x) for x in sys.argv[3].split(',')], sys.argv[4]
L, adj, nxt = patch(sig); deg = L.deg; outer = set(L.ring())
lk = rotf(nxt, u); Sv = {lk[i] for i in S}; I = {u} | Sv
for s in Sv: I |= adj[s] if kind == 'bf' else {y for y in adj[s] if deg[y] <= 6}
cl = classify(adj, nxt, I)
print('sig', sig, 'u', u, 'deg', deg[u], 'link', [(x, deg[x]) for x in lk], 'S', S, kind)
print('I', sorted((x, deg[x]) for x in I))
for w in cl['walks']: print('walk', len(w), ' '.join('%d:%d' % (v, deg[v]) for v, _ in w))
print('lab', cl['lab'], 'rep', cl['rep'], 'chords', cl['chords'], 'enclosed', sorted(cl['enclosed']), 'double', cl['double'])
print('extract_cfg simple', extract_cfg(adj, I), 'fill ok', code_fill(adj, I), 'witness', witness(adj, I, cl))
rest = set(adj) - I - cl['RS']; comps = []
while rest:
    st = [rest.pop()]; c = [st[0]]
    while st:
        x = st.pop()
        for y in adj[x]:
            if y in rest: rest.discard(y); st.append(y); c.append(y)
    comps.append((len(c), bool(set(c) & outer), sorted((v, deg.get(v)) for v in c)[:12]))
for c in sorted(comps, reverse=True): print('component of G-I-ring: size', c[0], 'reaches patch boundary', c[1], c[2] if c[0] < 12 else '')
for x, y in cl['chords']:
    print('chord', x, y, 'I-nbrs', sorted(adj[x] & I), sorted(adj[y] & I))
for r in cl['rep']: print('pinch', r, 'deg', deg[r], 'I-nbrs', sorted(adj[r] & I))
for r in sorted(cl['enclosed']):
    print('enclosed', r, 'deg', deg[r], 'rotation (vertex:deg:inI)', ' '.join('%d:%d:%s' % (x, deg[x], 'I' if x in I else 'R') for x in rotf(nxt, r)))
