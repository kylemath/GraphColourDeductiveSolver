"""kill6_U<U>.json (s16_filter.py, wj=6) -> kill6_U<U>.npy: uint8 array [a,b,e,f,s0,s1,s2,s3] (letter-5) = bitmask of killed
private letters (bit i = letter 5+i).  A key kills p when each of its s-requirements is 0 (free) or equal to the row letter.
Also reports mirror symmetry (a,b,e,f,s0..s3) <-> (f,e,b,a,s3..s0).  usage: python3 s16_killnpy.py DIR"""
import sys, json, itertools, numpy as np
D = sys.argv[1]
for U in (7, 8, 9):
    J = json.load(open('%s/kill6_U%d.json' % (D, U))); K = np.zeros((5,) * 8, dtype=np.uint8); n = 0
    for wk, keys in J['kills'].items():
        u, w = wk.split(); a, b, e, f = (int(c) - 5 for c in w)
        for key in keys:
            req = [int(c) for c in key]; p = req[4]; assert p
            for s in itertools.product(range(5), repeat=4):
                if all(r == 0 or r - 5 == x for r, x in zip(req[:4], s)): K[(a, b, e, f) + s] |= 1 << (p - 5)
    M = K.transpose(3, 2, 1, 0, 7, 6, 5, 4)
    print('U=%d windows with kills %d; entries with a kill %d of %d; killed bits %d; mirror-asymmetric entries %d' % (
        U, len(J['kills']), int((K > 0).sum()), K.size, int(np.unpackbits(K).sum()), int((K != M).sum())))
    np.save('%s/kill6_U%d.npy' % (D, U), K)
