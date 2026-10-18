"""C_kc_ring17 part 2 (course change 18 Oct): every connected induced subset X of the 15 vertices that the 7/27
certificate row R (d7 link 5675765 s 6577575) fixes exactly (u, w0..w6, s0..s6), all at R's exact degrees, rest of the
map free ring.  Written as dfast/kc lines named x7_<u><w mask><s mask>, ring <= RMAX.  Subsets equal to round 34's
full-link windows (u + all w) are skipped.  Any D line forbids R (X is a subconfiguration of every map containing R).
usage: python3 nonu.py OUT RMAX"""
import sys, os, itertools
W = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../..'))
src = open(os.path.join(W, 'gen28.py')).read(); src = src[:src.rindex('arrs = []')]
OUT, RMAX = sys.argv[1], int(sys.argv[2])
sys.argv = ['gen28.py', '/dev/null', '24']; G = {'__file__': os.path.join(W, 'gen28.py'), '__name__': 'g28'}; exec(src, G)
d, lk, sv = 7, '5675765', '6577575'
adj, name = G['build'](d, [int(c) for c in lk], {('s', j): int(sv[j]) for j in range(d)})
inv = {v: x for x, v in name.items()}
V = [('u',)] + [('w', j) for j in range(d)] + [('s', j) for j in range(d)]
deg = {('u',): 7}; deg.update({('w', j): int(lk[j]) for j in range(d)}); deg.update({('s', j): int(sv[j]) for j in range(d)})
for v in V: assert len(adj[inv[v]]) == deg[v], (v, len(adj[inv[v]]))
def conn(X):
    X = set(X); st = [next(iter(X))]; seen = {st[0]}
    while st:
        x = st.pop()
        for y in adj[inv[x]]:
            y = name.get(y)
            if y in X and y not in seen: seen.add(y); st.append(y)
    return len(seen) == len(X)
out = {}; cnt = {}
for mask in range(1, 1 << 15):
    X = [V[i] for i in range(15) if mask >> i & 1]
    if len(X) < 2 or not conn(X): continue
    hu = ('u',) in X; aw = all(('w', j) in X for j in range(d))
    if hu and aw: continue                      # round 34 full-link windows
    c = G['extract'](adj, [inv[x] for x in X], {inv[x]: deg[x] for x in X})
    if c is None: cnt['noring'] = cnt.get('noring', 0) + 1; continue
    if c[0] > RMAX: continue
    nm = 'x7_%s%s_%s' % ('u' if hu else '-', ''.join(lk[j] if ('w', j) in X else '.' for j in range(d)), ''.join(sv[j] if ('s', j) in X else '.' for j in range(d)))
    line = '%s %d %d %s %s' % ((nm,) + c)
    key = c  # identical extracted structure = same configuration
    if key in out: continue
    out[key] = (c[0], hu, nm, line)
L = sorted(out.values(), key=lambda t: (t[0], -len(t[2]), t[2]))
open(OUT, 'w').write(''.join(t[3] + '\n' for t in L))
import collections
print(cnt, 'lines', len(L), 'by ring', sorted(collections.Counter(t[0] for t in L).items()), 'with u', sum(t[1] for t in L))
