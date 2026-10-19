"""B6 probe: on the most recent arrangements of a checkpoint (not killed private-free), how many die for every private
assignment (exact-arrangement kills)?  Uses binder_check (full private enumeration, strict 9+)."""
import sys, pickle, time
from multiprocessing import Pool
import binder_check, rpat
def job(a):
    d, ws, ss = a
    if '9' in ws:
        return a, None
    t = time.time()
    r = binder_check.check(d, [int(c) for c in ws], [int(c) for c in ss])
    return a, (r[0], r[1], time.time() - t)
if __name__ == '__main__':
    C = pickle.load(open(sys.argv[1], 'rb'))
    arrs = [(k[0], v[0], v[1]) for k, v in C['LASTARR'].items()][-int(sys.argv[2]):]
    arrs = [a for a in arrs if not rpat.kill(a[0], [int(c) for c in a[1]], [int(c) for c in a[2]])]
    print('candidates', len(arrs), flush=True)
    with Pool(2) as P:
        res = P.map(job, arrs)
    k = [a for a, r in res if r and r[0]]
    print('exact kills', len(k), 'of', len(arrs), 'skipped(9 in link)', sum(1 for a, r in res if r is None))
    print('max secs', max((r[2] for a, r in res if r), default=0))
    for a in k[:10]: print(a)
