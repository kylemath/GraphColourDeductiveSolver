"""Seed vcache.txt with the round-1 dfast verdicts (scratchpad loop/cache.txt, configs from loop/bf_n*_k*.txt),
re-keyed by the canonical configuration key la.ckey.  Usage: python3 seed.py LOOPDIR"""
import sys, os, glob
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from la import *
LD = sys.argv[1]; C = dict(l.split()[:2] for l in open(os.path.join(LD, 'cache.txt')))
VC = os.path.join(HERE, 'vcache.txt'); have = set()
if os.path.exists(VC): have = {l.split()[0] for l in open(VC)}
n = 0
with open(VC, 'a') as f:
    for fn in glob.glob(os.path.join(LD, 'bf_n*_k*.txt')):
        for l in open(fn):
            nm, cb = l.split(' ', 1); cb = cb.strip()
            if nm not in C: continue
            kb = ckey(cb)
            if kb is None or kb in have: continue
            have.add(kb); f.write('%s %s r=%s seed\n' % (kb, C[nm], cb.split()[0])); n += 1
print('seeded', n, 'of', len(C))
