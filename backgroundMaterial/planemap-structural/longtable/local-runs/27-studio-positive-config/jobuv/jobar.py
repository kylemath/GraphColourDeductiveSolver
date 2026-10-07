#!/usr/bin/env python3
"""Job AR: names of the HOLE gates R_b & H11 for every break in jobap.json. Names relative to p = x_q: x+ = x_{q+1}, x_i = x_{q+i}, z = w_q, y = w_{q-1}, w_i = w_{q+i};
p's middle outer neighbours: at degree 6 'm'; at degree 7 'M_z' (adjacent to z) and 'M_y' (adjacent to y)."""
import json
from collections import Counter
from uv_lib import load
def names(name, hole, mirror):
    rot = load(name, mirror); L = rot[hole]; t6 = next(t for t in range(5) if len(rot[L[t]]) >= 6)
    w = []
    for t in range(5):
        a, b = L[t], L[(t + 1) % 5]; ra = rot[a]; i = ra.index(b); c1, c2 = ra[(i + 1) % len(ra)], ra[(i - 1) % len(ra)]; w.append(c2 if c1 == hole else c1)
    p = L[t6]; y, z = w[(t6 + 4) % 5], w[t6]
    M = [u for u in rot[p] if u != hole and u not in (L[(t6 + 1) % 5], L[(t6 + 4) % 5], y, z)]
    nm = {L[(t6 + i) % 5]: ('x+' if i == 1 else 'p' if i == 0 else 'x%d' % i) for i in range(5)}
    nm.update({w[(t6 + i) % 5]: ('z' if i == 0 else 'y' if i == 4 else 'w%d' % i) for i in range(5)})
    if len(M) == 1: nm[M[0]] = 'm'
    else:
        for u in M: nm[u] = 'M_z' if z in rot[u] else ('M_y' if y in rot[u] else 'M?')
    return nm
d = json.load(open('jobap.json')); cache = {}
def nmset(r, vs):
    key = (r['name'], r['hole'], r['run'].endswith('m'))
    if key not in cache: cache[key] = names(*key)
    return tuple(sorted(cache[key].get(v, '?%d' % v) for v in vs))
out = []
for deg in (6, 7):
    B = [b for b in d['gamma'] if b['deg'] == deg]
    single = Counter(nmset(b, b['near']) for b in B if not b['double'])
    first = Counter(nmset(b, b['double_info']['first']['near']) for b in B if b['double'])
    second = Counter(nmset(b, b['double_info']['second']['near']) for b in B if b['double'])
    pairs = Counter((nmset(b, b['double_info']['first']['near']), nmset(b, b['double_info']['second']['near'])) for b in B if b['double'])
    out.append('degree-%d Gamma: single breaks %s; consecutive-break records %d: first-break hole gates %s; second %s; (first, second) %s' % (deg, dict(single), sum(b['double'] for b in B), dict(first), dict(second), dict(pairs)))
O = d['open']
out.append('open double breaks (73, degree 6): first-break hole gates %s; second %s' % (dict(Counter(nmset(o, o['first']['near']) for o in O)), dict(Counter(nmset(o, o['second']['near']) for o in O))))
out.append('   second break hole-gate set with the run reaching R3k3^{b+2}: %s' % dict(Counter(nmset(o, o['second']['near']) for o in O if o['reaches_R3k3_b2'])))
print('\n'.join(out))
