import glob
K = {l.strip() for l in open('killed_rows.txt') if l.strip()}
for f in sorted(glob.glob('results/res_K5_*.tsv')):
    for l in open(f):
        g = l.rstrip('\n').split('\t')
        if len(g) < 12: continue
        hit = (g[4] == 'D' and 'dfast18:D' in g[10]) or (g[4] == 'C' and 'cfast:C-REDUCIBLE' in g[10])
        if not hit: continue
        rows = ['%d/%s' % (len(r.split('/')[0]), r) for r in g[9].split(':', 1)[1].split(',')]
        new = [r for r in rows if r not in K]
        if new: print(g[0], g[3], g[4], g[6], ','.join(new), f)
