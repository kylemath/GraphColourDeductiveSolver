#!/usr/bin/env python3
"""Track R: the tag word of a law R-cycle: per state, N and the link tags of the link parts (pair:frame positions of
the link vertices it contains).  Prints the word from a given anchor so cycles can be compared.
usage: tr_tagword.py DATA.json[@anchor] ..."""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from tr_lag import load
from tr_show import rolename
sys.path.insert(0, os.path.join(HERE, '..', 'TrackQ'))
from tq_roles import roles
ORDER = ['am', 'AB', 'aA', 'mB', 'aB', 'mA']
def word(D):
    out = []
    for t, c in enumerate(D['cols']):
        j, _ = roles(c); tags = []
        for (tt, p, q, P) in D['parts']:
            if tt != t: continue
            pos = ''.join(str((v - 1 - j) % 5) for v in sorted(P & {1, 2, 3, 4, 5}, key=lambda v: (v - 1 - j) % 5))
            if pos: tags.append((ORDER.index(rolename(c, p, q)), rolename(c, p, q) + ':' + pos))
        out.append(D['Nprof'][t] + '[' + ' '.join(x for _, x in sorted(tags)) + ']')
    return out
for f in sys.argv[1:]:
    p, a = (f.split('@') + ['0'])[:2]; D = load(p); w = word(D); a = int(a); L = len(w)
    print(D['src'])
    for i in range(L): print('   d=%d %s' % (i, w[(a + i) % L]))
