# uniform-weight certificate of a pattern: sum of (sender rows) - (receiver rows) - (cons2 rows); list unmatched keys
import sys, pickle, collections; sys.path.insert(0, '/tmp/swarm-W16/code')
import w16lib as W
from lp_patterns import lab_str
def uniform(cnt, fam='all'):
    off = W.NEWFAM - W.FAMS[fam]; tot = collections.Counter(); D = 0
    for lab, m in cnt.items():
        cf = W.coef_of(lab)
        if cf is None: return None
        sg = 1 if lab[0] == 'S' else -1
        if lab[0] == 'S': D += m
        if lab[0] == 'R': D -= m * (lab[1] - 6)
        for k, v in cf.items():
            if k[0] in off: continue
            tot[k] += sg * m * v
    return D, {k: v for k, v in tot.items() if v}
if __name__ == '__main__':
    ARGV = list(sys.argv); W.init()
    found = pickle.load(open(ARGV[1], 'rb'))
    for key, P in found.items():
        D, tot = uniform(P['cnt'])
        print('== n', P['n'], dict(P['degs']), 'D', D)
        for k, v in sorted(tot.items(), key=str): print('   ', v, k)
