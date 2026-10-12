#!/usr/bin/env python3
"""Track F: summarise f66 hole records: lock-parity mismatches, pocket parity/mod4, all-DL cycles by pattern, maxrun by pattern."""
import sys, json, collections
for f in sys.argv[1:]:
    R = [json.loads(l) for l in open(f)]; R = [d for d in R if d.get('kind') == 'hole']
    lp = [0, 0, 0, 0]; ad = collections.Counter(); adL = collections.defaultdict(set); mr = collections.defaultdict(int); bad = 0; ndl = 0
    for d in R:
        for i in range(4): lp[i] += d.get('lp', [0, 0, 0, 0])[i]
        if d['allDL']: ad[d['pattern']] += d['allDL']; adL[d['pattern']].update(d['allDL_L'])
        mr[d['pattern']] = max(mr[d['pattern']], d['maxrun']); ndl += d['nDL']
        bad += d['parfail1'] + d['parfail2'] + d['piFail'] + d['jordanfail'] + sum(v for k, v in d['mod4'].items() if k not in ('p1 curv+E mod4=1', 'p2 curv+E mod4=0'))
    print(f"{f}: graphs {len({d['graph'] for d in R})} holes {len(R)} DL states {ndl} unfilled states checked {lp[0]}")
    print(f"   lock-parity mismatches [Lock2, Lock1, K_amu even] = {lp[1:]};  pocket parity / mod4 / pi / Jordan failures = {bad}")
    print(f"   all-DL pi-cycles by pattern: {dict(ad)}  lengths {dict((k, sorted(v)) for k, v in adL.items())}")
    print(f"   maxrun 66666: {mr.get('66666', '-')};  top: {sorted(mr.items(), key=lambda x: -x[1])[:8]}")
