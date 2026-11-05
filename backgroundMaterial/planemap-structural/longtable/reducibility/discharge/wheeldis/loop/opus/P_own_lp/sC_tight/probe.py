# slack and family split at sol= of listed rows (file of 'tag share d lk sv'), plus the same with rr/z/zr zeroed (what the new families pay)
import sys, os, collections
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ana.py')).read())
ns['load_patterns']()
S = Sol(OPT['sol'])
for line in open(OPT['rows']):
    p = line.split()
    if not p or p[0].startswith('#'): continue
    tag, sh, d, lk, sv = p[0], float(p[1]), int(p[2]), p[3], p[4]
    tot, sl, g, fams, cf = S.row(d, lk, sv)
    ext = sum(g.get(f, 0.0) for f in ('rr', 'z', 'zr', 'q7'))
    keys = {}
    for k, c in cf.items():
        fam = GRP.get(k[0], k[0])
        if fam in ('rr', 'z', 'zr', 'q7') and c and not (k[0] == 'Q' and not ns['q7keys'](k[1])): keys[fam] = keys.get(fam, 0) + 1
    print('%-6s %.4f d=%d %s/%s adm=%s slack %.6f (without rr/z/zr: %.6f) ext-load %+.6f | %s | keys %s' % (tag, sh, d, lk, sv, ns['admissible'](d, lk, sv) or 'yes', sl, sl + ext, ext,
        ' '.join('%s=%+.4f' % kv for kv in sorted(g.items())), ' '.join('%s:%d' % kv for kv in sorted(keys.items())) or 'none'))
