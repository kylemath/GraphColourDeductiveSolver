import sys, random, time; sys.path.insert(0, '/tmp/swarm-W16/code')
import w16lib as W, torus as TT
ns = W.init(); random.seed(5)
arrs = []
for it in range(400):
    d = random.choice([7, 8, 9]); arrs.append((d, [random.choice([5, 6, 7, 8]) for _ in range(d)], [random.choice([5, 6, 7, 8, 9]) for _ in range(d)]))
t0 = time.time(); r1 = [W.patmatch_fast(d, w, s) for d, w, s in arrs]; t1 = time.time()
r2 = [ns['patmatch'](d, w, s) for d, w, s in arrs[:100]]; t2 = time.time()
print('fast %.2f ms/row; slow %.2f ms/row; agree %s' % ((t1 - t0) / 4, (t2 - t1) * 10, r1[:100] == r2))
