# classify every non-web chain at unfilled states: full-jam (holds every rim cell of both colours: rim sees a renaming),
# part (both colours, not all), one (one colour), quiet; tally whether the swap lowers dF.
import sys, os, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gear_polarity import map_graphs, gentri_graphs, HoleGame
T = collections.Counter()
def run(rot, h):
    H = HoleGame(len(rot), rot, h, rot[h], ncol=4, limit=60000); L = rot[h]
    for k, c in enumerate(H.states):
        if H.filled[k]: continue
        for K in H.chains(c):
            if K['web']: continue
            p, q = K['pair']; Rp = {x for x in L if c[x] == p}; Rq = {x for x in L if c[x] == q}
            Kp, Kq = K['set'] & Rp, K['set'] & Rq
            if Kp and Kq: kind = 'full' if (Kp == Rp and Kq == Rq) else 'part'
            else: kind = 'one' if (Kp or Kq) else 'quiet'
            t = H.index[H.canon(H.flip(c, K))]
            T[(('DL' if H.dl[k] else 'nonDL'), kind, 'best' if H.dF[t] == H.dF[k] - 1 else ('same' if H.dF[t] == H.dF[k] else 'worse'))] += 1
for name, rot, h in map_graphs(): run(rot, h)
for o in (16, 17, 18, 19):
    for name, rot in gentri_graphs(o):
        for h in range(len(rot)):
            if len(rot[h]) == 5: run(rot, h)
for dl in ('DL', 'nonDL'):
    for kind in ('full', 'part', 'one', 'quiet'):
        b, s, w = (T[(dl, kind, x)] for x in ('best', 'same', 'worse'))
        n = b + s + w
        if n: print('%-5s %-5s n=%6d  lowers dF %.3f  same %.3f  raises %.3f' % (dl, kind, n, b / n, s / n, w / n))
