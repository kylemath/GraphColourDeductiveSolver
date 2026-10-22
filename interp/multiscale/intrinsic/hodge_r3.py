# tau_Hodge / tau_int / one-lap of the round-3 hard closing sides (one-lap-level colourings with R = 3).
import sys, glob, pickle, json
sys.path.insert(0, '/mnt/project-files/multiscale/intrinsic'); sys.path.insert(0, '/mnt/project-files/multiscale/closing')
import ic
from cl import *
out = []
for f in sorted(glob.glob('/mnt/project-files/multiscale/closing/round3/hard_*.pkl')):
    d = pickle.load(open(f, 'rb')); T_ = Tri(d['adj']); A = d['A']; n = len(d['adj'])
    try: cA = Cluster(T_, A); cB = Cluster(T_, set(range(n)) - set(A))
    except Exception as e: continue
    r = dict(f=f.split('/')[-1], R=d['out'].get('R'), W=d['out'].get('W_band'))
    for nm, cl, c in (('A', cA, d['colA']), ('B', cB, d['colB'])):
        W = dict(walk=cl.walk, s=cl.s, odd=cl.parity_odd)
        if not all(v in c for v in cl.walk): continue
        r[nm] = dict(onelap=round(ic.tau_walk(W, c), 3), tau_int=round(ic.tau_int(W, c), 3), hodge=round(ic.tau_hodge(W, c), 3), drift=round(ic.drift(W, c), 2))
    out.append(r); print(json.dumps(r), flush=True)
json.dump(out, open('/mnt/project-files/multiscale/intrinsic/hodge_r3.json', 'w'))
