"""Track C: data check of the general (corrected) Lemma W, as formalised in ChainMod4.lean.

For ANY Kempe swap of a component K of T - h (colours {p,q}, t = p^q):
    2 * dcw == 4 * m_h(K) - beta(K)   (mod 8)
where, with the oriented link x_0..x_4 (face (h, x_i, x_{i+1}) in rotation order),
I_k = [x_k in K], C_k = c(x_k), E(x, t) = +1 if (x, t, x^t) is a cyclic shift of (1,2,3) else -1,
    beta = sum_k [I_{k+1} and not I_k] E(C_{k+1}^C_k, t) - [I_k and not I_{k+1}] E(C_k^C_{k+1}, t).
The original W (dcw == 2 m_h mod 4) is the case beta == 0.
Usage: nice -n 10 python3 -I tc_wgen.py
"""
import sys, random, os
from collections import Counter
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from tc_mod4 import *  # noqa  (orient, cwcount, oriented_link, CYC, ri_core)

def E(x, t): return 1 if (x, t, x ^ t) in CYC else -1

def run(surfaces, seed, steps, label):
    rng = random.Random(seed); gen = Counter(); oldW = Counter()
    for s in surfaces:
        ori = orient(s)
        for h in [h for h in s.V if len(s.adj[h]) == 5][:3]:
            Lr = oriented_link(s, ori, h)
            V, ix, nbr = graph_minus(s, h); L = [ix[v] for v in Lr]
            c = random_colouring(nbr, rng)
            if c is None: continue
            for _ in range(steps):
                v = rng.randrange(len(c)); o = rng.choice([q for q in range(4) if q != c[v]])
                p = c[v]; t = p ^ o
                K = component(nbr, c, v, p, o); c2 = kempe_swap(nbr, c, v, o)
                I = [L[k] in K for k in range(5)]; C = [c[L[k]] for k in range(5)]
                m = sum(1 for k in range(5) if I[k] and I[(k + 1) % 5])
                beta = sum((I[(k+1) % 5] and not I[k]) * E(C[(k+1) % 5] ^ C[k], t)
                           - (I[k] and not I[(k+1) % 5]) * E(C[k] ^ C[(k+1) % 5], t) for k in range(5))
                d = cwcount(ori, h, ix, c2) - cwcount(ori, h, ix, c)
                gen[(2 * d - 4 * m + beta) % 8 == 0] += 1
                oldW[(beta == 0, (d - 2 * m) % 4 == 0)] += 1
                c = c2
    print(label, 'general W holds', dict(gen), '| (beta==0, old W holds)', dict(oldW), flush=True)

if __name__ == '__main__':
    rng = random.Random(5)
    run([random_surface(tetra(), rng.randint(12, 30), rng, 200) for _ in range(30)], 21, 300, 'sphere')
    run([random_surface(torus_grid(3, 4), rng.randint(12, 24), rng, 100) for _ in range(20)], 22, 300, 'torus')
