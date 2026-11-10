"""ST-110 driver helper (Studio): usage parts.py RING NP RUNID : the bindt107 windows of ring RING (column 2) from all 4 batches, not yet
screened (any results/res_K5_*.tsv, ERROR lines excluded) and not in skip_t107.txt, sorted by m (stable, pack order), dealt round-robin
into NP files parts/famK5_RUNID_i.tsv. Prints how many remain. (The t107 batches mix rings, unlike t98's, so phases select by ring.)"""
import sys, glob, os
ph, np_, run = sys.argv[1], int(sys.argv[2]), sys.argv[3]
done = set()
for f in glob.glob('results/res_K5_*.tsv'):
    for l in open(f):
        g = l.split('\t')
        if len(g) > 4 and g[4] != 'ERROR': done.add(g[0])
done |= {l.split()[0] for l in open('skip_t107.txt') if l.strip()}
rem = []
for b in ['00', '01', '02', '03']:
    for l in open('famK5_r1516_t107_%s.tsv' % b):
        g = l.split('\t')
        if l.strip() and not l.startswith('#') and g[1] == ph and g[0] not in done: done.add(g[0]); rem.append(l)
rem.sort(key=lambda l: int(l.split('\t')[2]))
os.makedirs('parts', exist_ok=True)
for i in range(np_):
    open('parts/famK5_%s_%d.tsv' % (run, i), 'w').writelines(rem[i::np_])
print(len(rem))
