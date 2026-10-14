"""Job 9 summary: D-reducibility of 66666 2-balls (rings <= 15) by ring, by (#5, #7+) in the second ring, and the
5/6-only family; smallest non-reducible patterns."""
import glob, json, collections
R = {}
for f in glob.glob('run9/part*.out'):
    for l in open(f):
        p = l.split()
        if 'D=' in l: R[p[0][1:]] = dict(r=int(p[1][2:]), D=p[6] == 'D=true', cls=int(p[3].split('=')[1]), reached=int(p[5].split('=')[1]))
idx = json.load(open('2ball_index.json'))
print('tested', len(R), 'D-reducible', sum(x['D'] for x in R.values()), 'pruned (2.122)', sum(1 for v in idx.values() if v['pruned']), 'untested ring > 15', sum(1 for v in idx.values() if not v['pruned'] and v['r'] > 15))
byr = collections.defaultdict(lambda: [0, 0])
for w, x in R.items(): byr[x['r']][0] += 1; byr[x['r']][1] += x['D']
print('by ring', {r: '%d/%d' % (d, n) for r, (n, d) in sorted(byr.items())})
tab = collections.defaultdict(lambda: [0, 0])
for w, x in R.items():
    k5 = w.count('5'); k7 = sum(1 for c in w if c in '78'); tab[(k5, k7)][0] += 1; tab[(k5, k7)][1] += x['D']
print('by (#5, #7+): D-red/tested')
for k in sorted(tab): print('  ', k, '%d/%d' % (tab[k][1], tab[k][0]))
nd = sorted((x['r'], w) for w, x in R.items() if not x['D'])
print('smallest non-D-reducible:', nd[:10])
print('5/6-only with >= one 5:', sum(1 for w, x in R.items() if set(w) <= {'5', '6'} and '5' in w), 'D-red', sum(1 for w, x in R.items() if set(w) <= {'5', '6'} and '5' in w and x['D']))
print('all-6:', R.get('6666666666'))
# excess = sum(d-6 over second ring); D-rate vs (#5 - excess of 7/8)
ex = collections.defaultdict(lambda: [0, 0])
for w, x in R.items():
    s = sum(int(c) - 6 for c in w if c in '78'); k5 = w.count('5'); ex[(k5 - s)][0] += 1; ex[(k5 - s)][1] += x['D']
print('by margin #5 - sum(d-6 over 7/8):', {k: '%d/%d' % (v[1], v[0]) for k, v in sorted(ex.items())})
