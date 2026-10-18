#!/usr/bin/env python3
"""A_rsst_defects [exploratory]: for every RSST hit in a defect patch, write the configuration AS IT SITS IN THE PATCH
(interior = the image vertex set at exact degrees, ring = all their other neighbours) in dfast/cfast WheelMain format,
for an engine check independent of the RSST file's reducibility claim. Rings with a chord or not a simple cycle are
reported and skipped. Usage: extract_hits.py OUT.cfg NAME SIG [NAME SIG ...]"""
import sys, os, collections
sys.argv, OUT = [sys.argv[0]] + sys.argv[2:], sys.argv[1]
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import rsst_in_defect as R
def extract_cfg(adj, I):
    Is = set(I); RS = set(y for x in I for y in adj[x]) - Is
    for y in RS:
        if len(adj[y] & RS) != 2: return None
    start = min(RS); order = [start]; prev = None
    while True:
        cur = order[-1]; nb = sorted(adj[cur] & RS); nx = nb[0] if nb[0] != prev else nb[1]
        if nx == start: break
        order.append(nx); prev = cur
    if len(order) != len(RS): return None
    ri = {y: j for j, y in enumerate(order)}; Il = sorted(I); ii = {x: j for j, x in enumerate(Il)}
    f = lambda Ls: ';'.join(','.join(map(str, v)) if v else '-' for v in Ls)
    ia = [sorted(ii[y] for y in adj[x] if y in Is) for x in Il]
    ra = [sorted(ri[y] for y in adj[x] if y in RS) for x in Il]
    return '%d %d %s %s' % (len(order), len(Il), f(ra), f(ia))
lines = []; skipped = []
a = sys.argv[1:]
for name, sig in zip(a[::2], a[1::2]):
    adj, degT, faces, outer = R.build_patch(sig, 6)
    for i, (c, P) in enumerate(zip(R.CONFS, R.PREP)):
        if not P['degset'] <= set(degT.values()): continue
        emb = R.embeddings(adj, degT, faces, P)
        for j, S in enumerate(sorted(emb, key=sorted)):
            cfg = extract_cfg(adj, S)
            nm = '%s_rsst%d_%s_e%d' % (name, i, 'C' if c['k_contract'] > 0 else 'D', j)
            if cfg is None or int(cfg.split()[0]) != c['r']: skipped.append((nm, None if cfg is None else cfg.split()[0]))
            else: lines.append('%s %s' % (nm, cfg))
open(OUT, 'w').write('\n'.join(lines) + '\n')
print('wrote', len(lines), 'skipped (ring not simple / ring size differs from RSST):', skipped)
