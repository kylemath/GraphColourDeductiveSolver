"""EXPLORE round 60: my own pair windows (independent of the other thread's pairwin.py): row LK/SV, link 7 w_k, its
privates a (p_k_1, next to s_k) and b (p_k_2, next to s_(k-1)) at 5..8 or 9 (= >= 9, left on the ring); interior =
u + every exact link vertex + s_(k-1), s_k when exact + the exact privates, ring from the faces (tw60.window).
usage: python3 pw60.py LK/SV K AB [AB ...]   -> kc lines on stdout, named p60_<LK>_<SV>_w<K>_<a><b>"""
import sys, os
H = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, H); sys.path.insert(0, os.path.join(H, '..', 'k59'))
A = sys.argv[1:]; sys.argv = sys.argv[:1] + ['x', 'x', 'x']
import pair60 as P, tw60
row, k = A[0], int(A[1]); lk, sv = row.split('/'); LK = [int(c) for c in lk]; SV = [int(c) for c in sv]
for ab in A[2:]:
    a, b = int(ab[0]), int(ab[1])
    D, u, W, S = P.frame(LK, SV); p1, p2 = P.privates(D, W, S, k)
    for x, l in ((p1, a), (p2, b)):
        if l <= 8: assert D.close(x, l)
    I = [u] + [w for w in W if w in D.deg] + [s for s in (S[k - 1], S[k]) if s in D.deg] + [x for x in (p1, p2) if x in D.deg]
    line, il, rl = tw60.window(D, I, 'p60_%s_%s_w%d_%d%d' % (lk, sv, k, a, b))
    print(line)
