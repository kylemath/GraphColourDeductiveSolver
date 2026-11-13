"""Stage 0 data: concrete hub balls drawn inside every SP part, with what the proof forwards on each spoke.
usage (from scratchpad/fable): python3 ../stage0/gen.py OUT.pkl REPS [NULLSEED]"""
import sys, os, random, pickle, numpy as np
sys.path.insert(0, 'fable'); sys.path.insert(0, '.')
from common import *
from ball import *
import behav
out, reps = sys.argv[1], int(sys.argv[2]); nseed = int(sys.argv[3]) if len(sys.argv) > 3 else None
P = load()
if nseed is not None:
    N = behav.null_parts(P, nseed); P = [q if p['pre'] == 'SP_' else p for p, q in zip(P, N)]
R = Rules(P)
A = np.load('real58.npz'); pre = np.array([p['pre'] for p in load()]); dr = pre == 'drule'
E0 = {}
for d in (5, 6, 7, 8):
    M = A[f'M{d}'].astype(float); e = 60 * (6 - d) + M[:, dr].sum(1)
    for w, x in zip(A[f'W{d}'], e): E0[tuple(int(v) for v in w)] = x
rng = random.Random(7); rows = []
for p in P:
    if p['pre'] != 'SP_': continue
    seen = set()
    for rep in range(reps):
        d, link, asg = ball_from_part(p, 0, rng)
        key = (link, tuple(sorted(asg.items())))
        if key in seen: continue
        seen.add(key)
        W = Ball(d, link, asg); o = R.out(W); i = R.inn(W)
        c = 60 * (6 - d) - sum(x.get('dr', 0) for x in o) + sum(x.get('dr', 0) for x in i)
        et = []
        for s in range(d):
            tw = target_word(W, s); et.append(E0.get(canon(tw)) if tw else None)
        rows.append(dict(tag=p['tag'], d=d, link=link, asg=asg, c=c, spo=[x.get('SP', 0) for x in o], et=et))
pickle.dump(rows, open(out, 'wb')); print(out, len(rows))
