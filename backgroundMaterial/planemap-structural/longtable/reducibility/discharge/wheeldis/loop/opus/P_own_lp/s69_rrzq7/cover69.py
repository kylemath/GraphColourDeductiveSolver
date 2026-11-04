# s69: how many selftest arrangements have nonzero rr / z / zr coefficients in the Python row, and the rr/z part of the row value.  usage: python3 cover69.py WORKDIR SOL <engine args>
import sys, os, json
wd, solf = sys.argv[1], sys.argv[2]
ENG = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'eng', 'pcheck.py'); sys.argv = [ENG, 'help'] + sys.argv[3:]
ns = {'__file__': ENG, '__name__': 'pcheck_s69c'}; exec(compile(open(ENG).read(), ENG, 'exec'), ns); ns['l3q_load']()
recv = ns['recv_coef_R2']; S = json.load(open(solf)); V = {f: {tuple(k): v for k, v in S[f]} for f in ('rr', 'z', 'zr')}
for d in (7, 8, 9):
    arr = [l.split() for l in open(os.path.join(wd, 'f2b_eval_d%d.txt' % d))]; c = {'rr': 0, 'z': 0, 'zr': 0}; part = 0.0; mx = 0.0
    for lk, sv in arr:
        cf = recv(d, lk, sv, True, None); p = 0.0
        for k, v in cf.items():
            if k[0] in V and V[k[0]].get(tuple(k[1]), 0.0) != 0: c[k[0]] += 1; p += v * V[k[0]][tuple(k[1])]
        mx = max(mx, abs(p)); part += abs(p)
    print('d=%d: %d arrangements; with positive-valued rr coef %d, z %d, zr %d; max |rr+z+zr part of row| %.4g, mean %.4g' % (d, len(arr), c['rr'], c['z'], c['zr'], mx, part / len(arr)))
