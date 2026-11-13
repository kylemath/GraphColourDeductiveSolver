import sys, pickle, collections; sys.path.insert(0, '/tmp/swarm-W16/code')
import w16lib as W
from lp_patterns import lab_str
ARGV = list(sys.argv); W.init()
found = {}
for f in ARGV[1:]: found.update(pickle.load(open(f, 'rb')))
for key, P in found.items():
    cnt = P['cnt']
    print('== n', P['n'], dict(P['degs']), P['tag'])
    for lab, m in sorted(cnt.items(), key=str): print('  %3d %-44s %s' % (m, lab_str(lab), W.row_status(lab)))
    for fam in ('base', 'rrz', 'all'):
        res, keys, rmap = W.solve_lp(W.build_lp(list(cnt), fam)); print('  LP', fam, res.status, res.fun)
