#!/usr/bin/env python3
"""Track R: key sharing in a joint anchored rule (tr_rule.py partA): per cycle, the fraction of its keys that occur in at
least one other cycle of the set, and the fraction of its ground-edge/state incidences carrying such shared keys.
usage: tr_share.py R DATA.json@a ..."""
import sys, os, collections
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from tr_lag import load
from tr_rule import keys_for
r = int(sys.argv[1]); KS = []; names = []
for f in sys.argv[2:]:
    p, a = f.split('@'); D = load(p); KS.append(keys_for(D, r, 'partA', int(a))); names.append(D['src'])
sets = [set(K.values()) for K in KS]; allk = set().union(*sets)
print('joint keys', len(allk), 'sum of per-cycle keys', sum(len(s) for s in sets))
for i, K in enumerate(KS):
    others = set().union(*[s for j, s in enumerate(sets) if j != i])
    sh = sets[i] & others; inc = sum(1 for v in K.values() if v in sh)
    print('  %-24s keys %4d shared %4d (%.2f)  incidences shared %.2f' % (names[i], len(sets[i]), len(sh), len(sh) / len(sets[i]), inc / len(K)))
