"""TrackK review: EVERY proper colouring of T - h (every unfilled state) for small random sphere
triangulations (n = 7..11, min degree 3), running all step checks of kr_check.one_state.
Usage: nice -n 10 python3 -I kr_exhaustive.py SEED NGRAPHS
"""
import os, sys, random, time
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import kr_check as K
from kr_core import random_tri, tetra, oriented_link


def all_colourings(adj, verts):
    order = list(verts); col = {}

    def rec(i):
        if i == len(order):
            yield dict(col); return
        v = order[i]; used = {col[u] for u in adj[v] if u in col}
        for c in range(4):
            if c not in used:
                col[v] = c
                yield from rec(i + 1)
                del col[v]
    yield from rec(0)


def main():
    seed, ng = int(sys.argv[1]), int(sys.argv[2])
    rng = random.Random(seed); t0 = time.time(); seen = 0
    for _ in range(ng):
        t = random_tri(tetra(), rng.randint(7, 11), rng, 200)
        n = len(t.adj)
        for h in [v for v in t.adj if len(t.adj[v]) == 5]:
            L = oriented_link(t, h)
            vs = [v for v in t.adj if v != h]
            for col in all_colourings(t.adj, vs):
                x = K.frame(L, col)
                if x is not None:
                    K.one_state(t, 0, h, L, x, col, n, 'exh'); seen += 1
    print('exhaustive small spheres: seed=%d graphs=%d unfilled states=%d time=%.0fs' % (seed, ng, seen, time.time() - t0))
    for k in sorted(K.counts):
        print('  %-55s checks=%-9d fails=%d' % (k, K.counts[k], K.fails[k]))
    for k, v in K.examples.items():
        print('  FIRST FAILURE', k, v)
    print('TOTAL FAILURES', sum(K.fails.values()), flush=True)


if __name__ == '__main__':
    main()
