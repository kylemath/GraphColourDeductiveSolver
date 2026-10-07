"""NightStatementC: statistics of (c) from the Job BI records (no recomputation)."""
import json, sys
from collections import Counter
B = '../27-studio-positive-config/jobbi/'
for fn in ('jobbi-cycles.json', 'jobbi-cycles-census.json'):
    R = json.load(open(B + fn))
    if 'census' in fn: R = [r for r in R if r['tag'].startswith('census:')]
    print('==', fn, len(R))
    nheavy = Counter(); ndist = Counter(); nnf = Counter(); phi = []; frac_heavy = []; Lc = Counter()
    for r in R:
        LZ = r['Lambda']; Lc[r['L']] += 1
        im = r['sigma_images']  # non-fixed, off-Z sigma images
        heavy = [i for i in im if 5 * i['T'][0] <= -LZ]
        nheavy[len(heavy)] += 1; ndist[len({tuple(i['T']) for i in im})] += 1
        nnf[len(im)] += 1
        frac_heavy.append(len(heavy) / r['L'])
        # heaviest target among images
        if im:
            Tm = min(im, key=lambda i: i['T'][0]); phi.append(Tm['T'][1] / r['class_states'])
    print('L', dict(Lc)); print('#images off Z (non-fixed):', sorted(nnf.items()))
    print('#images on heavy T (Lambda<=-Lambda Z):', sorted(nheavy.items()))
    print('#distinct targets:', sorted(ndist.items()))
    print('L(heaviest target)/|class|: min %.3f median %.3f max %.3f' % (min(phi), sorted(phi)[len(phi)//2], max(phi)))
    print('fraction of Z states whose sigma-image is on a heavy T: min %.3f median %.3f' % (min(frac_heavy), sorted(frac_heavy)[len(frac_heavy)//2]))
