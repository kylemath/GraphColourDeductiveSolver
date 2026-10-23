# For each failure (R = 0: only v recoloured): uncapped cuts anywhere -> min #cuts and each cut's boundary distance to
# the nearest held position / to v; and the smallest slide d such that letting every held position move up to d edges
# (plus the vortex window, budget unchanged in count = npos + dn) makes the step feasible.
import sys, pickle, glob
sys.path.insert(0, '/mnt/project-files/multiscale/multicut/unbounded/')
import vr, mc
from pi import make
for fn in sorted(glob.glob('/mnt/project-files/multiscale/multicut/unbounded/fail_*.pkl')):
    D = pickle.load(open(fn, 'rb')); fl = D['fail']; adj = make(D['spec'].split(':')[0]); var = D['spec'].split(':')[3]
    B2 = fl['B']; s = [int(x) for x in fl['s']]; v = fl['v']; col = dict(fl['col']); L = len(B2); pos = {b: i for i, b in enumerate(B2)}
    held = [pos[a] for (a, b) in fl['posn'] if a in pos and b in pos and pos[b] == (pos[a]+1) % L]
    pv = pos[v]; win = [(pv-1) % L, pv, (pv+1) % L]
    def cd(i, S): return min([min((i-j) % L, (j-i) % L) for j in S], default=None)
    best = None; slide = None
    for c in range(4):
        if any(col.get(y) == c for y in adj[v] if y in col): continue
        c2 = dict(col); c2[v] = c; lab = [c2[B2[i]] ^ c2[B2[(i+1) % L]] for i in range(L)]
        if 0 in lab: continue
        H = mc.int_walk(lab, s); vr.FrontierVR.NB = vr.BIG
        cp = mc.cut_positions(H, fl['odd'], vr.BIG, var, 1.0, None)
        if cp is not None and (best is None or len(cp) < best[0]):
            best = (len(cp), sorted(cd(i, held) for i in cp), sorted(cd(i, [pv]) for i in cp))
        for d in range(0, 41):
            al = [0]*L
            for h in held:
                for e in range(-d, d+1): al[(h+e) % L] = 1
            for e in win: al[e] = 1
            if mc.ncuts(H, fl['odd'], len(held) + fl['dn'], var, 1.0, al) is not None:
                if slide is None or d < slide: slide = d
                break
    print(fn.split('/')[-1], 'L', L, 'odd', fl['odd'], 'nodd', fl['nodd'], 'dn', fl['dn'], 'held', len(held), 'anywhere(min#, dist to held, dist to v)', best, 'slide d', slide, flush=True)
