#!/usr/bin/env python3
"""Track F section 9: re-run the section 8 cycle-search graphs (out/lpc/cyc_graphs.txt, cyc555_graphs.txt) at their
frame-like holes only (no 555, no 565 run) with kclass4; write out/lpc2/prev_frame.jsonl (every frame-like cycle hole)
and out/lpc2/prev_seeds.txt (graphs with a frame-like cycle hole, 'holes=' token), used as seeds for lpc2_search."""
import os, sys, json
D = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, D)
from lpc2_search import frame_holes, run_kc, K2
OUT = os.path.join(D, '..', 'out', 'lpc2'); seen = set(); fo = open(os.path.join(OUT, 'prev_frame.jsonl'), 'w'); so = open(os.path.join(OUT, 'prev_seeds.txt'), 'w')
for fn in ('cyc_graphs.txt', 'cyc555_graphs.txt'):
    for line in open(os.path.join(D, '..', 'out', 'lpc', fn)):
        line = ' '.join(line.split()[:3]); nm = line.split()[0]
        if nm in seen: continue
        seen.add(nm); rot = [list(map(int, r.split(','))) for r in line.split()[2].split(';')]; hw = dict(frame_holes(rot))
        if not hw: continue
        recs = run_kc(line, list(hw), os.path.join(OUT, 'prev.tmp'), timeout=600); hs = []
        for d in recs:
            if d['allDLcyc']:
                hs.append(d['hole']); fo.write(json.dumps(dict(src=fn, graph=line, hole=d['hole'], word=hw[d['hole']], states=d['states'], allDLcyc=d['allDLcyc'], cls2=d[K2])) + '\n')
        if hs: so.write(line + ' holes=' + ','.join(map(str, hs)) + '\n')
os.unlink(os.path.join(OUT, 'prev.tmp'))
