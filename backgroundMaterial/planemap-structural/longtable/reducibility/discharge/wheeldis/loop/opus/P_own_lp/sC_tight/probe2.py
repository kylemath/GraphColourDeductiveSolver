# per row: extended-family keys by sign (coef < 0 = the centre pays out = the family can relieve the row; coef > 0 = the family loads the row), with values at sol
import sys, os, collections
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ana.py')).read())
ns['load_patterns']()
S = Sol(OPT['sol'])
for line in open(OPT['rows']):
    p = line.split()
    if not p or p[0].startswith('#'): continue
    tag, d, lk, sv = p[0], int(p[2]), p[3], p[4]
    tot, sl, g, fams, cf = S.row(d, lk, sv)
    parts = []
    for fam in ('rr', 'z', 'zr', 'q7', 'r', 'x', 'l3q'):
        neg = [(k, c, S.val(k)) for k, c in cf.items() if GRP.get(k[0], k[0]) == fam and c < 0 and not (k[0] == 'Q' and not ns['q7keys'](k[1]))]
        pos = [(k, c, S.val(k)) for k, c in cf.items() if GRP.get(k[0], k[0]) == fam and c > 0 and not (k[0] == 'Q' and not ns['q7keys'](k[1]))]
        if neg or pos: parts.append('%s out %d (%.4f) in %d (%.4f)' % (fam, len(neg), sum(-c * v for k, c, v in neg), len(pos), sum(c * v for k, c, v in pos)))
    print('%-6s d=%d %s/%s slack %.6f | %s' % (tag, d, lk, sv, sl, '; '.join(parts)))
