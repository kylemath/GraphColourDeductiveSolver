import json, sys, pickle, glob
sys.path.insert(0, '/mnt/project-files/multiscale/kempe_trace')
from kt import *
d = json.load(open('/mnt/project-files/multiscale/opus_attack/bandfill/sphere_L18_w4.json'))
adj = [set(a) for a in d['adj']]; L = d['L']; n = len(adj)
A = set(d['A']); B = set(range(n)) - A
colA = {int(k): v for k, v in d['colA'].items()}; colB = {int(k): v for k, v in d['colB'].items()}
m = d['seam_row_A']
bdA = [m*L + i for i in range(L)]; bdB = [(m+1)*L + i for i in range(L)]
assert boundary_cycle(adj, A) is not None and set(boundary_cycle(adj, A)) == set(bdA)
assert set(boundary_cycle(adj, B)) == set(bdB)
out = {}
for nm, S, col, bd in (('A', A, colA, bdA), ('B', B, colB, bdB)):
    tr = traces(adj, S, col, bd); s = summary(tr, L)
    print(nm, 'word', ''.join(str(col[v]) for v in bd), 'noncrossing', s['noncrossing'])
    print('  total blocks', s['nblocks'], 'singletons', s['nsingle'], 'max depth', s['depth'], 'max span', s['maxspan'])
    for p, b in tr.items(): print('  pair', p, 'blocks', b, s['per_pair'][p])
    out[nm] = dict(word=''.join(str(col[v]) for v in bd), summary={k: v for k, v in s.items() if k != 'per_pair'},
                   traces={str(p): b for p, b in tr.items()})
# round3 hard closings (R >= 3), L ~ 200-500
res3 = []
for f in sorted(glob.glob('/mnt/project-files/multiscale/closing/round3/hard_*.pkl')):
    h = pickle.load(open(f, 'rb')); adj = [set(a) for a in h['adj']]; A = set(h['A']); B = set(range(len(adj))) - A
    for nm, S, col in (('A', A, h['colA']), ('B', B, h['colB'])):
        bd = boundary_cycle(adj, S); partial = any(v not in col for v in S); S = set(v for v in S if v in col)
        if bd is None: print(f, nm, 'boundary not induced'); continue
        tr = traces(adj, S, col, bd); s = summary(tr, len(bd))
        r = dict(file=f.split('/')[-1], side=nm, L=len(bd), R=h['out'].get('R'), W=h['out'].get('W_band'), partial=partial, **{k: v for k, v in s.items() if k != 'per_pair'})
        print(r); res3.append(r)
json.dump(dict(opus=out, round3_hard=res3), open('t1_sphere.json', 'w'), indent=1)
