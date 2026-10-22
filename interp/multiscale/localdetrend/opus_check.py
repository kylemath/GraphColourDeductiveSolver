# Task 3: Opus two-colour-run (bandfill) rows: all three measures on each seam row (t = 0 rows: they must agree).
import sys, json, math, numpy as np
sys.path.insert(0, '/mnt/project-files/multiscale/localdetrend/'); import ld
B = '/mnt/project-files/multiscale/opus_attack/bandfill/'
def H_of(row):
    H = [0j]; L = len(row)
    for i in range(L): H.append(H[-1] + ld.EV[row[i] ^ row[(i+1) % L]])
    return np.array(H)
rows = []
for c in json.load(open(B+'counterexamples.json')):
    for nm, r in (('A', c['A_rows_depth_w_to_seam'][-1]), ('B', c['B_rows_seam_to_depth_w'][0])):
        rows.append((c['L'], nm, [int(x) for x in r]))
d = json.load(open(B+'sphere_L18_w4.json'))
for nm, r in (('A', d['A_rows_bottom_to_seam'][-1]), ('B', d['B_rows_seam_to_top'][0])): rows.append((18, 'sphere_'+nm, [int(x) for x in r]))
agree = 0; out = []
for L, nm, r in rows:
    m = ld.measures(H_of(r), False); out.append(dict(L=L, side=nm, **m))
    if m['t'] == 0: agree += int(abs(m['hodge']-m['strip']) < 1e-6 and abs(m['hodge']-m['step']) < 1e-6)
    print(out[-1])
print('rows', len(rows), 't=0 rows', sum(1 for o in out if o['t'] == 0), 'all three agree on t=0 rows:', agree)
json.dump(out, open('/mnt/project-files/multiscale/localdetrend/opus_check.json', 'w'), indent=0)
