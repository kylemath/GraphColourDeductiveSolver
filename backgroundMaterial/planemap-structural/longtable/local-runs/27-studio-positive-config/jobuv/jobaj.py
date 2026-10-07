#!/usr/bin/env python3
"""Job AJ (time reversal): for each hole with Gamma-cycles (orders 25-27, all patterns), compare the plantri-orientation Gamma-cycles with the mirror-orientation
Gamma-cycles at the same hole. States are compared as vertex colourings up to renaming (canonical by original vertex label), so the two orientations' different
canonical forms do not matter. Test: same state set, and mirror pi-order = plantri pi-order reversed (up to a cyclic shift)."""
import json
from collections import Counter
from multiprocessing import Pool
from uv_lib import Hole
def key(H, k):
    mp = {}; return tuple(mp.setdefault(H.col(k, v), len(mp)) for v in sorted(H.sp.order))
def gam(H):
    return [[key(H, x) for x in z] for z in H.cycles if all(H.DL[x] for x in z)]
def job(args):
    name, hole = args
    A = gam(Hole(name, hole, False)); B = gam(Hole(name, hole, True)); res = []
    for ca in A:
        sa = set(ca); match = None
        for cb in B:
            if set(cb) != sa: continue
            n = len(ca); rb = cb[::-1]; i = rb.index(ca[0])
            rev = all(rb[(i + t) % n] == ca[t] for t in range(n)); i2 = cb.index(ca[0]); fwd = all(cb[(i2 + t) % n] == ca[t] for t in range(n))
            match = 'reversed' if rev else ('same order' if fwd else 'same set, other order')
        res.append(match or ('no Gamma-cycle with this state set in the mirror'))
    return name, hole, len(A), len(B), res
if __name__ == '__main__':
    holes = set()
    for lab in ['z25', 'z26', 'z27']:
        for l in open('../out/%s.jsonl' % lab):
            if '"jobs": {"pos": [{' not in l: continue
            r = json.loads(l)
            if any(z['gamma'] for z in r['jobs']['pos']): holes.add((r['name'], r['hole']))
    with Pool(12) as P: out = P.map(job, sorted(holes))
    c = Counter(m for _, _, _, _, res in out for m in res); cnt = Counter((a == b) for _, _, a, b, _ in out)
    print('holes with plantri Gamma-cycles:', len(out), '; equal number of Gamma-cycles in both orientations:', dict(cnt))
    print('per plantri Gamma-cycle:', dict(c))
    print('exceptions:', [(n, h, a, b, res) for n, h, a, b, res in out if any(m != 'reversed' for m in res) or a != b][:8])
    json.dump(out, open('jobaj.json', 'w'))
