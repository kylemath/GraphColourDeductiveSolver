#!/usr/bin/env python3
"""studiointel fast/regress_fast.py -- the fast engine must reproduce the Python engine (radius.py) EXACTLY: n_states, n_filled,
n_unfilled_nonDL, n_DL, DL_radius_hist, unreached_DL, rho, at every degree-5 hole of every listed graph; and its witness state must pass
check.py lb at K = rho (and fail at rho+1). Graphs: ico, A_3..A_6, T4, order28, Phase B bests (seeds/B2-best, B3-best), L(ico), GC:2,
and the three Phase C certificate graphs."""
import sys, os, json, time, subprocess
sys.path.insert(0, '..'); os.chdir(os.path.dirname(os.path.abspath(__file__)))
import radius, graphs, builders, fast
def load(spec):
    if spec.startswith('json:'): return [tuple(f) for f in json.load(open(spec[5:]))['faces']]
    return builders.build(spec)
specs = ['ico', 'A:3', 'A:4', 'A:5', 'A:6', 'json:../seeds/T4.json', 'json:../seeds/order28.json', 'json:../seeds/B2-best.json', 'json:../seeds/B3-best.json',
         'L(ico)', 'GC:2'] + ['json:../run-C-2026-10-06/cert/%s.graph.json' % t for t in ('91a307d1852a1764', '8a23ee3ec7b2bb33', '62661a3f304f4caa')]
keys = ['n_states', 'n_filled', 'n_unfilled_nonDL', 'n_DL', 'DL_radius_hist', 'unreached_DL', 'rho']
bad = 0; tp = tf = 0; nh = 0
for sp in specs:
    faces = load(sp); dg = graphs.degrees(faces)
    for h in sorted(v for v in dg if dg[v] == 5):
        t = time.time(); a = radius.analyse(faces, h); tp += time.time() - t
        t = time.time(); b = fast.analyse(faces, h); tf += time.time() - t
        nh += 1
        if [a[k] for k in keys] != [b[k] for k in keys]: bad += 1; print('MISMATCH', sp, h, [a[k] for k in keys], [b[k] for k in keys])
        if b.get('rho') and b['rho'] >= 2 and 'witness' in b:
            w = b['witness']; p = '/tmp/_fastw.json' if not os.environ.get('TMPDIR') else os.path.join(os.environ['TMPDIR'], '_fastw.json')
            json.dump({str(u): c for u, c in zip(w['order'], w['state'])}, open(p, 'w')); gp = p + '.g.json'; json.dump({'faces': faces}, open(gp, 'w'))
            o1 = subprocess.run(['python3', '../check.py', 'lb', gp, str(h), p, str(b['rho'])], capture_output=True, text=True).stdout
            o2 = subprocess.run(['python3', '../check.py', 'lb', gp, str(h), p, str(b['rho'] + 1)], capture_output=True, text=True).stdout
            if not (o1.startswith('OK') and o2.startswith('FAIL')): bad += 1; print('WITNESS CHECK FAILED', sp, h, o1, o2)
    print('done', sp, flush=True)
print('holes', nh, 'mismatches', bad, 'python %.1fs fast %.1fs' % (tp, tf))
print('regression passed' if bad == 0 else 'REGRESSION FAILED')
