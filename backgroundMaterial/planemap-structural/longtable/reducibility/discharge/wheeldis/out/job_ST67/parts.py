"""ST-67 driver helper (Studio): usage parts.py PHASE NP RUNID : PHASE 15 = batches 00-03, 16 = batches 04-07. Deals the windows not yet screened
(any results/res_K5_*.tsv, ERROR lines excluded) and not in skip_b2140.txt, in pack order, round-robin into NP files parts/famK5_RUNID_i.tsv. Prints how many remain."""
import sys, glob, os
ph, np_, run = sys.argv[1], int(sys.argv[2]), sys.argv[3]
done = set()
for f in glob.glob('results/res_K5_*.tsv'):
    for l in open(f):
        g = l.split('\t')
        if len(g) > 4 and g[4] != 'ERROR': done.add(g[0])
done |= {l.split()[0] for l in open('skip_b2140.txt') if l.strip()}
B = ['00', '01', '02', '03'] if ph == '15' else ['04', '05', '06', '07']
rem = []
for b in B:
    for l in open('famK5_r1516_b2140_%s.tsv' % b):
        if l.strip() and not l.startswith('#') and l.split('\t')[0] not in done: done.add(l.split('\t')[0]); rem.append(l)
os.makedirs('parts', exist_ok=True)
for i in range(np_):
    open('parts/famK5_%s_%d.tsv' % (run, i), 'w').writelines(rem[i::np_])
print(len(rem))
