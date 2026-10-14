#!/usr/bin/env python3
"""Summarise S1 logs: Pareto front (defect -> min gap) and, for every gap-0 front graph, the complex-level status
(edges in < 2 triangles; SAT face set (arm A); single-cycle links (arm B))."""
import sys, json
from sf_lib import parse_line, defects
from sf_cplx import solve, lower_defect
for f in sys.argv[1:]:
    fr = {}; best = {}; hits = 0; n0 = 0
    for l in open(f):
        d = json.loads(l)
        if d['ev'] == 'HIT': hits += 1
        if d['ev'] != 'front': continue
        fr[d['defect']] = min(fr.get(d['defect'], 999), d['gap'])
        if d['gap'] == 0:
            n0 += 1
            adj = parse_line(d['graph'])[1]; ld = lower_defect(adj)
            a, b, _ = solve(adj, armB=True) if ld == 0 else (False, False, None)
            df = defects(adj)
            k = 'lower0' if ld == 0 else 'lower>0'
            best.setdefault('min_lower', 999); best['min_lower'] = min(best['min_lower'], ld)
            best.setdefault('min_flag_bad_edges', 999); best['min_flag_bad_edges'] = min(best['min_flag_bad_edges'], df['bad_edges'])
            best.setdefault('min_noncycle_links', 999); best['min_noncycle_links'] = min(best['min_noncycle_links'], df['noncycle_links'])
            if a: best['satA'] = best.get('satA', 0) + 1
            if b is True: best['satB'] = best.get('satB', 0) + 1
    print(f, 'HIT events', hits, 'gap0 front graphs', n0, json.dumps(best))
    print('  front (defect: min gap):', sorted(fr.items())[:12])
