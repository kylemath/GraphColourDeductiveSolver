#!/usr/bin/env python3
"""S0: rung-d frozen classes through sf_eng (hole 0) + graph-level defects."""
import json, sys
from sf_lib import Engine, cls_dicts, parse_line, defects
src = sys.argv[1]
eng = Engine(hole=0)
rows = []
for l in open(src):
    d = json.loads(l); name, adj = parse_line(d['graph'])
    js = eng.run(d['graph'])[0]
    fr = [c for c in cls_dicts(js) if c['size'] == c['onCyc']]
    df = defects(adj)
    # h-local: is link of h = induced 5-cycle, edges at h
    r = dict(name=name, n=len(adj), states=js['states'], filled=js['filled'], cyclens=js['cyclens'],
             frozen=[(c['size'], c['n8'], c['n9'], c['lawFail']) for c in fr], **df)
    rows.append(r); print(json.dumps(r))
eng.close()
nf = sum(1 for r in rows if r['frozen'])
print('SUMMARY graphs', len(rows), 'with frozen class', nf,
      'bad_edges min/max', min(r['bad_edges'] for r in rows), max(r['bad_edges'] for r in rows),
      'dA min', min(r['dA'] for r in rows), 'nonreg links min', min(r['nonreg_links'] for r in rows),
      'noncycle links min', min(r['noncycle_links'] for r in rows), 'n', min(r['n'] for r in rows), max(r['n'] for r in rows),
      'edges', min(r['edges'] for r in rows), max(r['edges'] for r in rows))
