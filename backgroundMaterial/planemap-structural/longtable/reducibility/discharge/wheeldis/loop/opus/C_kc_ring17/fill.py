"""C_kc_ring17 part 3: per (s1,s4) filling of the 7/27 certificate row R (d7 link 5675765; fixed s0=6 s2=7 s3=7 s5=7
s6=5; s1, s4 free in R).  Every connected induced subset X of {u, w0..w6, s0..s6} (s1/s4 only at 6/7/8; 9 = >=9 = ring),
exact degrees, ring <= RMAX, not round 34's u+all-link windows, and not using s1=5 / s4=5 (explore's fillings).
Names x7_<u|-><w mask>_<s mask>.  usage: python3 fill.py OUT RMAX"""
import sys, os, collections
W = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../..'))
src = open(os.path.join(W, 'gen28.py')).read(); src = src[:src.rindex('arrs = []')]
OUT, RMAX = sys.argv[1], int(sys.argv[2])
sys.argv = ['gen28.py', '/dev/null', '24']; G = {'__file__': os.path.join(W, 'gen28.py'), '__name__': 'g28'}; exec(src, G)
d, lk = 7, '5675765'
out = {}
for a in '6789':
    for b in '6789':
        sv = '6' + a + '77' + b + '75'
        sd = {('s', j): int(sv[j]) for j in range(d) if sv[j] != '9'}
        adj, name = G['build'](d, [int(c) for c in lk], sd)
        inv = {v: x for x, v in name.items()}
        V = [('u',)] + [('w', j) for j in range(d)] + [('s', j) for j in range(d) if sv[j] != '9']
        deg = {('u',): 7}; deg.update({('w', j): int(lk[j]) for j in range(d)}); deg.update({k: v for k, v in sd.items()})
        def conn(X):
            X = set(X); st = [next(iter(X))]; seen = {st[0]}
            while st:
                x = st.pop()
                for y in adj[inv[x]]:
                    y = name.get(y)
                    if y in X and y not in seen: seen.add(y); st.append(y)
            return len(seen) == len(X)
        for mask in range(1, 1 << len(V)):
            X = [V[i] for i in range(len(V)) if mask >> i & 1]
            if len(X) < 2: continue
            if ('u',) in X and all(('w', j) in X for j in range(d)): continue
            nm = 'x7_%s%s_%s' % ('u' if ('u',) in X else '-', ''.join(lk[j] if ('w', j) in X else '.' for j in range(d)), ''.join(sv[j] if ('s', j) in X else '.' for j in range(d)))
            if nm in out: continue
            if not conn(X): continue
            c = G['extract'](adj, [inv[x] for x in X], {inv[x]: deg[x] for x in X})
            if c is None or c[0] > RMAX: continue
            out[nm] = (c[0], '%s %d %d %s %s' % ((nm,) + c))
L = sorted(out.values())
open(OUT, 'w').write(''.join(t[1] + '\n' for t in L))
print('lines', len(L), sorted(collections.Counter(t[0] for t in L).items()))
