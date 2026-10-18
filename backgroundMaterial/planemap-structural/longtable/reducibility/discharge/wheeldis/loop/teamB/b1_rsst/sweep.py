"""Round B1 sweep: all 16 open fillings x 5^6 privates.  Output: one line per case with score bounds."""
import sys, itertools
from multiprocessing import Pool
import rstar

def job(f):
    s1, s4 = f
    out = []
    for priv in itertools.product([5, 6, 7, 8, 9], repeat=6):
        try:
            hi, lo = rstar.score_bounds(s1, s4, priv)
        except AssertionError as e:
            out.append(f'{s1}{s4} {"".join(map(str,priv))} ERR')
            continue
        out.append(f'{s1}{s4} {"".join(map(str,priv))} {lo} {hi}')
    return out

if __name__ == '__main__':
    F = [(a, b) for a in (6, 7, 8, 9) for b in (6, 7, 8, 9)]
    with Pool(3) as P, open('sweep.out', 'w') as fo:
        for res in P.imap_unordered(job, F):
            fo.write('\n'.join(res) + '\n'); fo.flush()
