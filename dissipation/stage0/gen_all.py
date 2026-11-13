"""Wider data: random hub balls of degree 5..8 (plus balls drawn inside every part, any kind),
with the full outflow of the hub per spoke split by rule kind (dr = RSST, SP, ST).
usage (from scratchpad/fable): python3 ../stage0/gen_all.py OUT.pkl NRANDOM_PER_DEGREE REPS_PER_PART SEED"""
import sys, random, pickle
sys.path.insert(0, 'fable'); sys.path.insert(0, '.')
from common import *
from ball import *
out, nr, reps, seed = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
P = load(); R = Rules(P); rng = random.Random(seed); rows = []
def add(d, link, asg, src):
    W = Ball(d, link, asg); o = R.out(W)
    rows.append(dict(src=src, d=d, link=link, asg=asg, dr=[x.get('dr', 0) for x in o], sp=[x.get('SP', 0) for x in o], st=[x.get('ST', 0) for x in o]))
for d in (5, 6, 7, 8):
    for _ in range(nr): add(*random_ball(d, rng), 'random')
for p in P:
    for _ in range(reps): add(*ball_from_part(p, 0, rng), p['tag'])
pickle.dump(rows, open(out, 'wb')); print(out, len(rows))
