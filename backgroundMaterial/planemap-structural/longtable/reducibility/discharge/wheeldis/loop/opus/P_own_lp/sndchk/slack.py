import json, sys
SOLS = sys.argv[4:]
exec(open('sr.py').read().split("Q = [")[0])
for sf in SOLS:
    S = json.load(open(sf)); t = S['t']
    V = {('y', tuple(int(c) for c in k.replace('|', ''))): v for k, v in S['y'].items()}
    for nm in ('g', 'r'): V.update({(nm, tuple(k)): v for k, v in S[nm]})
    print(sf.split('/')[-1], 't=%.6f' % t)
    for wd, H, F in [('55667',[0,1,0,0,0],[1,1]),('55667',[0,1,0,1,0],[0,0]),('55667',[0,1,0,1,0],[1,0]),('55758',[0,0,0,0,0],[])]:
        cf = [cf for w, cf, b in SR if w == wd and b == H + ['|'] + F][0]
        lhs = sum(c * V.get(k, 0.0) for k, c in cf.items())
        print('  %s %s %s  lhs %.6f  need %.6f  slack %+.6f' % (wd, H, F, lhs, 1 - t, lhs - (1 - t)))
