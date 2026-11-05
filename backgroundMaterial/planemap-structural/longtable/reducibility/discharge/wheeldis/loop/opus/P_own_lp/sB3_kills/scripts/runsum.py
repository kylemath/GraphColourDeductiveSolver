# B3: windows run by family and ring (all B3 result files), verdict counts.  usage: python3 runsum.py res1.tsv [res2.tsv ...]
import sys, collections
c = collections.Counter(); seen = set(); fams = collections.defaultdict(set)
for fn in sys.argv[1:]:
    for l in open(fn):
        g = l.rstrip('\n').split('\t')
        if len(g) < 12 or g[0] in seen: continue
        seen.add(g[0]); f = g[9].split(':')[0]
        f = {'A7': 'A', 'A8': 'A', 'A9': 'A'}.get(f, f)
        v = g[4]
        if v == 'D' and 'noD' in g[10]: v = 'D1'          # kcc D only (not two-engine)
        if v == 'C' and 'C-REDUCIBLE' not in g[10].upper(): v = 'C?'
        c[(f, int(g[1]), v)] += 1; fams[f].add(g[9])
rings = sorted(set(k[1] for k in c)); F = sorted(set(k[0] for k in c))
print('family  ' + ' '.join('%6s' % ('r%d' % r) for r in rings) + '   total   D   C  (families)')
for f in F:
    tot = sum(v for k, v in c.items() if k[0] == f)
    print('%-7s ' % f + ' '.join('%6s' % (sum(v for k, v in c.items() if k[0] == f and k[1] == r) or '.') for r in rings) +
          '  %6d %3d %3d  (%d)' % (tot, sum(v for k, v in c.items() if k[0] == f and k[2] == 'D'), sum(v for k, v in c.items() if k[0] == f and k[2] == 'C'), len(fams[f])))
print('all', len(seen), dict(collections.Counter(k[2] for k in c.elements())))
