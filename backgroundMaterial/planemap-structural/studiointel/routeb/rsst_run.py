#!/usr/bin/env python3
"""routeb/rsst_run.py -- [exploratory] vacancy-reducibility (kred joint game, full adversary) of RSST configurations: for each configuration
and each interior degree-5 vertex v of it, H = free completion - v, ring = the configuration's ring. Output one JSON line per (conf, v).
usage: rsst_run.py CONF_FILE i0 i1 [max_nodes] [mode]"""
import sys, json, time
import kred, rsst_parse
cs = rsst_parse.parse(sys.argv[1]); i0, i1 = int(sys.argv[2]), int(sys.argv[3])
mx = int(sys.argv[4]) if len(sys.argv) > 4 else 3000000; mode = sys.argv[5] if len(sys.argv) > 5 else 'joint'
rings = set(int(x) for x in sys.argv[6].split(',')) if len(sys.argv) > 6 else None
stride = int(sys.argv[7]) if len(sys.argv) > 7 else 1; off = int(sys.argv[8]) if len(sys.argv) > 8 else 0
for j, c in enumerate(cs[i0:i1]):
    if rings and c['r'] not in rings: continue
    if j % stride != off: continue
    F = rsst_parse.faces(c)
    for v in range(c['r'] + 1, c['n'] + 1):
        if len(c['adj'][v]) != 5: continue
        t = time.time(); row = {'idx': cs.index(c), 'name': c['name'], 'r': c['r'], 'n': c['n'], 'contract': c['k_contract'] > 0, 'v': v,
                                'link_degrees': [len(c['adj'][u]) if u > c['r'] else None for u in c['adj'][v]], 'mode': mode}
        try:
            res = kred.Game(kred.Config(F, v), mode, max_nodes=mx).solve(); res.pop('startval')
            row.update({k: res[k] for k in ('colourings', 'unfilled', 'nodes', 'reducible', 'lost', 'depth')})
        except OverflowError as e: row['capped'] = str(e)
        except AssertionError as e: row['error'] = str(e)
        row['secs'] = round(time.time() - t, 1)
        print(json.dumps(row), flush=True)
