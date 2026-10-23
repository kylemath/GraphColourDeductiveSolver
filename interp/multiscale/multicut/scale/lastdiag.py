import sys, pickle, itertools
sys.path.insert(0, '/mnt/project-files/multiscale/multicut/unbounded/')
import vr, mc
from pi import make, signs
D = pickle.load(open('/mnt/project-files/multiscale/multicut/unbounded/fail_ico10_2_rand_any.pkl','rb')); fl = D['fail']
adj = make('ico10'); B2 = fl['B']; s = [int(x) for x in fl['s']]; v = fl['v']; col = fl['col']
print('v', v, 'B2', B2, 's', s, 'degs', [len(adj[b]) for b in B2], 'P', fl['P'])
print('prev colours on P', [col.get(x) for x in fl['P']])
for cs in itertools.product(range(4), repeat=3):
    if len(set(cs)) < 3: continue
    lab = [cs[i] ^ cs[(i+1) % 3] for i in range(3)]
    H = mc.int_walk(lab, s); vr.FrontierVR.NB = vr.BIG
    cp = mc.cut_positions(H, False, vr.BIG, 'any', 1.0, None)
    print(cs, 'H', H, 't', abs(mc.cz(H[-1])), 'cuts', cp)
