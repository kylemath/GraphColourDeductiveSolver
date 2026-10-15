"""Max number of LONE-BIG senders (degree-5 neighbours whose link word has the receiver as its only letter >= 7) around
a receiver of degree 7 / 8, with the wheel-level R of wlp.py (option bigw: D-reducible 7-/8-wheels excluded).
A lone-big sender must get its whole unit from the receiver, so a d-vertex with more than d - 6 of them is an
obstruction to every wheel-level rule.  Lists the maximisers.  Usage: python3 lone.py [bigw] [nofan]"""
import sys, os, itertools, collections
HERE = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(HERE, 'wlp.py')).read().replace('__file__', repr(os.path.join(HERE, 'wlp.py')))
exec(src[:src.index('A_ub, b_ub = [], []')])
out = []
for d in (7, 8):
    if d not in WORDS: _prep(d)
    words, IDX = WORDS[d]; best = 0; ex = []
    lone = np.array([1.0 if (r[0] < 9 and max(r[1:]) <= 6) else 0.0 for r in roots])
    W = np.concatenate([lone, [0.0, -np.inf]])[np.where(IDX >= 0, IDX, np.where(IDX == -1, len(roots), len(roots) + 1))]
    P = W[:, 0]
    for k in range(1, d): P = (P[:, :, :, None] + W[:, k][:, None, :, :]).max(axis=2)
    val = np.einsum('nii->ni', P).max(axis=1); best = int(val.max()); ex = []
    for n in np.where(val == best)[0][:6]:
        Wn = W[n]; bb = (-np.inf, None)
        for a0 in range(5):
            V = Wn[0][a0].copy(); bk = []
            for i in range(1, d):
                C = V[:, None] + Wn[i]; bk.append(C.argmax(axis=0)); V = C.max(axis=0)
            if V[a0] > bb[0]:
                s = [None] * d; s[d - 1] = a0
                for i in range(d - 1, 0, -1): s[i - 1] = int(bk[i - 1][s[i]])
                bb = (V[a0], s)
        ex.append((words[n], tuple(L[x] for x in bb[1])))
    hist = collections.Counter(val.astype(int).tolist())
    out.append('d=%d: max lone-big senders %d (d-6 = %d); words by max count %s; examples (link word w_0.., shared s_i between w_i,w_i+1):' % (d, best, d - 6, dict(sorted(hist.items()))))
    out += ['   w=%s s=%s' % (''.join(map(str, w)), ''.join(map(str, s))) for w, s in ex]
    print(out[-len(ex) - 1:], flush=True)
open(os.path.join(HERE, 'out', 'lone_%s.txt' % ('_'.join(sorted(OPT)) or 'base')), 'w').write('\n'.join(out) + '\n')
