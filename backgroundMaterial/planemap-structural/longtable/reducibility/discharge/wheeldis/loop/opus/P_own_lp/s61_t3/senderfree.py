# driver: sender rows of the fy2 stack at sol_c: slack, and whether the oracle t>=7 frees them (a z key with a visible face and h2 = 0)
import sys, json, collections
eng, sol = sys.argv[1:3]
sys.argv = [eng + '/pcheck.py', 'none'] + sys.argv[3:]
g = {'__file__': eng + '/pcheck.py', '__name__': 'drv'}
exec(open(eng + '/pcheck.py').read(), g)
S = json.load(open(sol)); t = S['t']; y = {}
RIX, ROOTS, root = g['RIX'], g['ROOTS'], g['root']
import numpy as np
yv = np.zeros(len(ROOTS))
for k, v in S['y'].items():
    u, rest = k.split('|'); yv[RIX[root(list((int(u),) + tuple(int(c) for c in rest)), 0)]] = v
GV = {tuple(k): v for k, v in S['g']}; RV = {tuple(k): v for k, v in S['r']}
def val(k):
    return yv[RIX[k[1]]] if k[0] == 'y' else 0.0 if k[0] == 'z' else RV.get(k[1], 0.0) if k[0] == 'r' else GV.get(k[1], 0.0)
def vis2(K): return (K[1] == 5 and K[2] == 5) or (K[4] == 5 and K[3] == 5)
C = collections.Counter(); words = collections.defaultdict(lambda: [0, 0])
for wd, cf, bits in g['R2_sender_rows']():
    sl = sum(c * val(k) for k, c in cf.items()) - (1 - t)
    free = any(k[0] == 'z' and vis2(k[1]) and k[1][7] == 0 for k in cf)
    tight = sl < float(g["OPT"].get("tth", "1e-7"))
    C[('tight' if tight else 'slack', 'freed' if free else 'kept')] += 1
    if tight: words[wd][int(free)] += 1
print('sender rows by (slack<tth, freed by oracle):', dict(C))
kept_words = sorted(w for w, (a, b) in words.items() if a)
print('words with a tight non-freed context: %d of %d words with tight contexts; e.g. %s' % (len(kept_words), len(words), kept_words[:15]))
