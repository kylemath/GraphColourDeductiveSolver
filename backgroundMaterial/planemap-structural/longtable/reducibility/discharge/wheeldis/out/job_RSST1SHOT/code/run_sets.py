#!/usr/bin/env python3
"""RSST-1SHOT: run every d = 7 / 8 label of the four domain sets (dom_{A,B,C,T}.json), spec §8.1/§8.2/§9,
plus the coordinator's kill-every-group variant (lazy, *_allkill fields) and the per-none-config needs list.
usage: run_sets.py SETS [shard nshard]   e.g. run_sets.py ABCT 0 2"""
import sys, os, json, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rcore as R, rows78

JOB = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sets = sys.argv[1]; shard, nsh = (int(sys.argv[2]), int(sys.argv[3])) if len(sys.argv) > 3 else (0, 1)
tag = ('_' + R.CONTROL) if R.CONTROL else ''
items = []
for S in sets:
    D = json.load(open(os.path.join(JOB, 'in', 'inputs', 'dom_%s.json' % S)))
    for lab in sorted(D): items.append((S, lab, D[lab]))
out = open(os.path.join(JOB, 'logs', 'sets_%s_%dof%d%s.jsonl' % (sets, shard, nsh, tag)), 'w')
t0 = time.time()
for k, (S, lab, dom) in enumerate(items):
    if k % nsh != shard: continue
    need = []
    t1 = time.time()
    res, row = rows78.run_row(lab, dom, kill_all=True, need_log=need)
    res['set'] = S; res['needs_none'] = need; res['secs'] = round(time.time() - t1, 2)
    out.write(json.dumps(res) + '\n'); out.flush()
out.write(json.dumps({'done': True, 'secs': round(time.time() - t0, 1)}) + '\n'); out.close()
