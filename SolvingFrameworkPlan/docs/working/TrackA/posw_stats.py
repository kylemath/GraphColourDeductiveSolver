#!/usr/bin/env python3
"""Track A task 3: statistics of positive pi-cycles from posw/scan-*.jsonl (dedup graphs by name)."""
import json, sys
from collections import Counter
def canon(ld):
    d = [min(x, 8) for x in ld]; return min(tuple(s[r:] + s[:r]) for s in (d, d[::-1]) for r in range(5))
for fn in sys.argv[1:]:
    R = [json.loads(l) for l in open(fn)]
    print('==', fn, 'graphs', len(R), 'frame', sum(r['frame'] for r in R), 'n', dict(sorted(Counter(r['n'] for r in R).items())))
    for o in ('p', 'm'):
        H = [(r['name'], r['n'], h) for r in R for h in r['orient'][o]]
        pos = [(nm, n, h) for nm, n, h in H if h['npos'] > 0]
        print(' orient', o, 'holes', len(H), '; holes with a w>0 cycle', len(pos), '; positive cycles', sum(h['npos'] for *_, h in pos),
              '; max w', max([h['maxw'] for *_, h in H]), '; max class sum w', max(h['max_cls_sumw'] for *_, h in H),
              '; min class slack %.5f' % min(h['min_slack'] for *_, h in H))
        print('   positive holes by n', dict(sorted(Counter(n for _, n, _ in pos).items())), '; by link word', dict(Counter(canon(h['linkdeg']) for *_, h in pos).most_common()))
        for nm, n, h in sorted(pos, key=lambda x: -x[2]['posw'])[:8]:
            print('   ', nm, 'n', n, 'hole', h['hole'], 'link', h['linkdeg'], 'pos (w,L,count)', h['pos'], 'classes', [(N, F, s) for N, F, s in h['cls']][:4], 'states', h['states'])
        # slack distribution by n
        by = {}
        for nm, n, h in H: by[n] = min(by.get(n, 9), h['min_slack'])
        print('   min class slack by n', {k: round(v, 5) for k, v in sorted(by.items())})
