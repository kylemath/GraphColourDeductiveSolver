"""Tabulate axioms x counterexample family. Usage: tabulate.py LABEL FILE [maxgraphs] [stride]"""
import sys, json
from collections import Counter
from ax_lib import *
label, src = sys.argv[1], sys.argv[2]
mx = int(sys.argv[3]) if len(sys.argv) > 3 else 10**9
stride = int(sys.argv[4]) if len(sys.argv) > 4 else 1
def graphs():
    for li, line in enumerate(open(src)):
        line = line.strip()
        if not line or li % stride: continue
        if line.startswith('{'):
            d = json.loads(line)
            if 'edges' not in d: continue
            yield from_json(d)
        else:
            yield parse_line(line)
seen = set(); C = Counter(); rows = []
out = open(f'out/tab_{label}.jsonl', 'w')
for gi, (n, E, fv) in enumerate(graphs()):
    if len(seen) >= mx: break
    key = (n, tuple(sorted(tuple(sorted(e)) for e in E)), tuple(tuple(sorted(E[f])) for f in fv))
    if key in seen: continue
    seen.add(key)
    g = G5(n, E, fv)
    P, good, cyc = g.orbits()
    lawc = []
    for c in cyc:
        r = orbit_axioms(g, c)
        if r['law_viol'] == 0: lawc.append(r)
    if not lawc: C['graphs_without_law_cycle'] += 1; continue
    pl, plr = planar(g), planar_rot(g)
    br = ball_planar_radius(g)[0]
    for r in lawc:
        t1 = set(r['word']) == {'1', '2'}
        ham = r['ham']; f8 = r['fig8']
        rec = dict(n=n, L=r['L'], word=r['word'], T1=t1, A4_planar=pl, A4_planar_rot=plr,
                   A1_bip_rot_all=all(h['bip_rot'] for h in ham) if ham else None,
                   A1_bip_any=any(h['bip'] for h in ham) if ham else None,
                   A1_min_oddcyc=min((h['oddc_rot'] or 99) for h in ham) if ham else None,
                   A5v_vpartner_on_X_all=all(f['v_into_X'] for f in f8),
                   A5v_frac=sum(f['v_into_X'] for f in f8) / len(f8),
                   A5x_XY_noncross_all=all(f['xy_cross'] == 0 for f in f8),
                   A5x_min_xycross=min(f['xy_cross'] for f in f8),
                   A1Q_fig8_planar_any=any(f['fig8_planar'] for f in f8),
                   ballr=br)
        out.write(json.dumps(rec) + '\n'); rows.append(rec)
print(label, 'graphs', len(seen), 'law orbits', len(rows), dict(C))
def cnt(k, f=lambda x: x):
    return Counter(f(r[k]) for r in rows)
for k in ['T1', 'A4_planar', 'A4_planar_rot', 'A1_bip_rot_all', 'A1_bip_any', 'A1_min_oddcyc', 'A5v_vpartner_on_X_all', 'A5v_frac', 'A5x_XY_noncross_all', 'A5x_min_xycross', 'A1Q_fig8_planar_any', 'ballr', 'L', 'n']:
    print(f'  {k}: {dict(cnt(k))}')
