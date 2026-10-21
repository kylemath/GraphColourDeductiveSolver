"""EXPLORE round 60: pair windows grown by apexes.  Row LK/SV, link 7 w_k, privates (a, b) as pw60.py (9 = on the ring);
interior = u + every exact link vertex + s_(k-1), s_k + the exact privates + any subset of the other exact apexes.
Writes the windows at ring <= RMAX, by ring, named x60_<LK>_<SV>_w<K>_<a><b>_<apex letters, '.' = out>.
usage: python3 pw60x.py LK/SV K RMAX AB [AB ...]"""
import sys, os, itertools
H = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, H); sys.path.insert(0, os.path.join(H, '..', 'k59'))
A = sys.argv[1:]; sys.argv = sys.argv[:1] + ['x', 'x', 'x']
import pair60 as P, tw60
row, k, RMAX = A[0], int(A[1]), int(A[2]); lk, sv = row.split('/'); LK = [int(c) for c in lk]; SV = [int(c) for c in sv]
out = []
for ab in A[3:]:
    a, b = int(ab[0]), int(ab[1])
    D, u, W, S = P.frame(LK, SV); p1, p2 = P.privates(D, W, S, k)
    for x, l in ((p1, a), (p2, b)):
        if l <= 8: assert D.close(x, l)
    base = [u] + [w for w in W if w in D.deg] + [s for s in (S[k - 1], S[k]) if s in D.deg] + [x for x in (p1, p2) if x in D.deg]
    other = [i for i in range(len(S)) if S[i] in D.deg and S[i] not in base]
    for n in range(1, len(other) + 1):
        for sub in itertools.combinations(other, n):
            tag = ''.join(str(SV[i]) if (i in sub or S[i] in base) else '.' for i in range(len(S)))
            try:
                line, il, rl = tw60.window(D, base + [S[i] for i in sub], 'x60_%s_%s_w%d_%d%d_%s' % (lk, sv, k, a, b, tag))
            except AssertionError:
                continue
            if int(line.split()[1]) <= RMAX: out.append(line)
for l in sorted(set(out), key=lambda l: (int(l.split()[1]), l.split()[0])): print(l)
