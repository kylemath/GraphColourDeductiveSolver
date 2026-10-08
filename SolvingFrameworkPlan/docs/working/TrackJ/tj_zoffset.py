#!/usr/bin/env python3
"""Track J: in near-rigid closed classes of example graphs (jsonl 'graph', hole 0), the pi-cycle structure and where the
extra-chain swap Z sends each N = 9 state (offset along its pi-cycle, or 'other cycle').  usage: tj_zoffset.py FILE.jsonl"""
import sys, json
from collections import Counter
from tj_lib import Engine
E = Engine(dump=True, hole=0); offs = Counter(); n = 0
for l in open(sys.argv[1]):
    d = json.loads(l)
    if d.get('ev') != 'example': continue
    js, S = E.run(d['graph'])[0]
    for c in js['cls']:
        if not (c[0] == c[3] and c[6] == 0 and c[5] > 0): continue
        mem = [s['i'] for s in S if s['cls'] == c[-1]]; cycof = {}; cycs = []
        for i in mem:
            if i in cycof: continue
            cyc = [i]
            while S[cyc[-1]]['pi'] != i: cyc.append(S[cyc[-1]]['pi'])
            for t, x in enumerate(cyc): cycof[x] = (len(cycs), t)
            cycs.append(cyc)
        o = []
        for x in mem:
            if S[x]['N'] != 9: continue
            for (y, pr, lm) in S[x]['mv']:
                if lm == 0 and y != x and pr in (0, 1, 2, 3, 4, 5) and S[y]['N'] == 9 and y in cycof:
                    a, b = cycof[x], cycof[y]
                    o.append(('same', (b[1] - a[1]) % len(cycs[a[0]])) if a[0] == b[0] else ('other',))
        offs[(tuple(sorted(len(c) for c in cycs)), tuple(sorted(Counter(o).items())))] += 1; n += 1
print(n, offs.most_common(10))
