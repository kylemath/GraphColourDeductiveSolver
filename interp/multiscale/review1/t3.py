# Claim 1(iii): did our level colourings ever contain even-degree |w|=2 vertices?  (a) stored colourings in pkl files;
# (b) regenerate level colourings (lev.min_tau / cl.level_col) on E1 balls and count.
import sys, time, math, json, glob, pickle; sys.path.insert(0,'/mnt/project-files/multiscale/review1')
from rv import *
sys.path.insert(0, '/mnt/project-files/multiscale/levelling')
from e1_survey import graph
out = open('t3_w2.jsonl', 'w')
def rec(d):
    print(json.dumps(d), flush=True); out.write(json.dumps(d)+'\n'); out.flush()
# (a) stored level/merged colourings
tot = collections.Counter()
for fn in sorted(glob.glob('/mnt/project-files/multiscale/levelling/fail_*.pkl'))[:40] + sorted(glob.glob('/mnt/project-files/multiscale/closing/e*_R3_*.pkl')):
    d = pickle.load(open(fn, 'rb'))
    try:
        if 'adj' in d:
            T = Tri(d['adj']); cols = [('cA', d.get('cA') or d.get('c_A')), ('cB', d.get('cB') or d.get('c_B'))]
        else:
            T = graph(d['name']); cols = [('c', d['c'])]
    except Exception as e:
        rec(dict(file=fn.split('/')[-1], err=str(e), keys=list(d.keys()))); continue
    for nm, col in cols:
        if not col: continue
        c2, c3, n, hist = count_w2(T, col)
        tot['w2'] += c2; tot['n'] += n; tot['files'] += 1
        rec(dict(file=fn.split('/')[-1], col=nm, interior_vertices=n, even_w2=c2, odd_w3=c3, hist={str(k): v for k, v in hist.items()}))
rec(dict(summary='stored', **tot))
# (b) regenerated level colourings of E1 balls (tau<=1), via cl.level_col as used in the recursions
import random
tot = collections.Counter(); per = []
rng = random.Random(0)
for l in open('/mnt/project-files/multiscale/levelling/e1_survey.jsonl'):
    r = json.loads(l)
    if r['r'] not in (4, 6, 8) or 'err' in r: continue
    T = graph(r['name']); cl = Cluster(T, bfs(T.adj, r['c'], r['r']))
    col = level_col(cl, rng, K2=1.0)
    if col is None: continue
    c2, c3, n, hist = count_w2(T, col, cl.S)
    tot['w2'] += c2; tot['n'] += n; tot['clusters'] += 1; tot['clusters_with_w2'] += (c2 > 0)
    rec(dict(name=r['name'], c=r['c'], r=r['r'], n=len(cl.S), interior=n, even_w2=c2, odd_w3=c3, tau=round(cl.tau(col)[0],3)))
rec(dict(summary='regenerated_level_col', **tot))
