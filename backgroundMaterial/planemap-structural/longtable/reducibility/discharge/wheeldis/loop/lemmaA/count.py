"""count canonical non-excluded situations for k fives; write sit_k<k>.txt (L s per line)."""
import sys, os, time, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from la import *
k = int(sys.argv[1]); t0 = time.time(); n = 0; byL = collections.Counter()
with open(os.path.join(HERE, 'sit_k%d.txt' % k), 'w') as f:
    for c in situations(k):
        n += 1; byL[c[:7]] += 1
        f.write(''.join(map(str, c[:7])) + ' ' + ''.join(map(str, c[7:])) + '\n')
print('k=%d situations %d, link words with >=1 situation %d, %.1fs' % (k, n, len(byL), time.time() - t0))
