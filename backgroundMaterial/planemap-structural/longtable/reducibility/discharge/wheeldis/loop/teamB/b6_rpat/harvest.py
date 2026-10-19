"""B6: run the configuration oracle on every arrangement recorded in a PFH checkpoint; write the kill patterns and the
list of killed arrangements (used to drop their rows when the run resumes with the oracle)."""
import sys, os, pickle
from multiprocessing import Pool
import rpat

def job(a):
    d, ws, ss = a
    return a, rpat.kill(d, [int(c) for c in ws], [int(c) for c in ss])

if __name__ == '__main__':
    ck, opat, killed = sys.argv[1:4]
    C = pickle.load(open(ck, 'rb'))
    arrs = sorted({(k[0], v[0], v[1]) for k, v in C['LASTARR'].items()})
    print('arrangements', len(arrs), flush=True)
    seen = set(); nk = 0
    with Pool(2) as P, open(opat, 'w') as fo, open(killed, 'w') as fk:
        for a, k in P.imap_unordered(job, arrs, chunksize=50):
            if k:
                nk += 1
                fk.write('%d %s %s\n' % a)
                line = rpat.fmt(a[0], k[1])
                if line not in seen:
                    seen.add(line)
                    fo.write('%s # %s %s/%s\n' % (line, k[0], a[1], a[2]))
    print('killed', nk, 'patterns', len(seen))
