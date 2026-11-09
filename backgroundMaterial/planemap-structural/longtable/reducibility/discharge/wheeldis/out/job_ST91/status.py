"""ST-91 progress per pack batch: screened / skipped / total; prints verdict counts."""
import glob, collections
res = {}
for f in glob.glob('results/res_K5_*.tsv'):
    for l in open(f):
        g = l.split('\t')
        if len(g) > 4 and g[4] != 'ERROR': res[g[0]] = g[4]
skip = {l.split()[0] for l in open('skip_b89.txt') if l.strip()}
full = []
for b in range(4):
    ids = [l.split('\t')[0] for l in open('famK5_r1516_b89_%02d.tsv' % b) if l.strip() and not l.startswith('#')]
    s = sum(i in res for i in ids); k = sum(i not in res and i in skip for i in ids)
    print('b%02d total %d screened %d skipped %d left %d' % (b, len(ids), s, k, len(ids) - s - k))
    if s + k == len(ids): full.append(b)
print('verdicts', dict(collections.Counter(res.values())), 'complete', full)
