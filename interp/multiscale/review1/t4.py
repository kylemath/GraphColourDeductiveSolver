# Claim 2: (i) minimal interior winding + tau<=1 on the E1 ball set (192 clusters) and fail (chorded) clusters;
#          (ii) Burgers vector: is t=0 forced/possible; 2-vortex caps; with and without minimal winding.
import sys, time, math, json, glob, pickle, random; sys.path.insert(0,'/mnt/project-files/multiscale/review1')
from rv import *
sys.path.insert(0, '/mnt/project-files/multiscale/levelling')
from e1_survey import graph
out = open('t4_minw.jsonl', 'w')
def rec(d):
    print(json.dumps(d), flush=True); out.write(json.dumps(d)+'\n'); out.flush()
rows = [json.loads(l) for l in open('/mnt/project-files/multiscale/levelling/e1_survey.jsonl')]
rows = [r for r in rows if 'err' not in r]
rows.sort(key=lambda r: r['n'])
tot = collections.Counter(); t_hist = collections.Counter()
for r in rows:
    T = graph(r['name']); cl = Cluster(T, bfs(T.adj, r['c'], r['r']))
    if chords(cl): tot['chorded_skipped'] += 1; continue
    t0 = time.time()
    res = dict(name=r['name'], c=r['c'], r=r['r'], n=len(cl.S), m=cl.m, nodd=len(cl.odd), tau_min_unconstrained=r['tau'])
    # minimal winding + tau^2 <= 1
    _, c1 = level_w(T, cl.S, K2=1.0, wmode='min', seed=1, budget=3*10**6)
    res['minw_tau1'] = (c1 is not None) if c1 != 'UNK' else 'UNK'
    if c1 and c1 != 'UNK':
        tau, t = cl.tau(c1); res['tau'] = round(tau, 3); res['t'] = None if t is None else round(t, 3)
        assert count_w2(T, c1, cl.S)[0] == 0
        # can we also get tau^2<=3/4 with min winding?
        _, c2 = level_w(T, cl.S, K2=0.75, wmode='min', seed=1, budget=3*10**6)
        res['minw_tau_flat'] = (c2 is not None) if c2 != 'UNK' else 'UNK'
        if not cl.parity_odd:
            # Burgers: t=0 with min winding, and t=0 without
            _, c3 = level_w(T, cl.S, K2=1.0, wmode='min', t=(0, 0), seed=1, budget=3*10**6)
            _, c4 = level_w(T, cl.S, K2=1.0, wmode=None, t=(0, 0), seed=1, budget=3*10**6)
            res['t0_minw'] = (c3 is not None) if c3 != 'UNK' else 'UNK'
            res['t0_anyw'] = (c4 is not None) if c4 != 'UNK' else 'UNK'
            t_hist[(len(cl.odd) > 0, res['t0_anyw'], res['t0_minw'])] += 1
    res['sec'] = round(time.time()-t0, 1); rec(res)
    tot['tested'] += 1; tot['minw_level_ok'] += (res['minw_tau1'] is True); tot['minw_flat_ok'] += (res.get('minw_tau_flat') is True)
    tot['unk'] += (res['minw_tau1'] == 'UNK')
rec(dict(summary='E1 balls', **tot, t0_hist={str(k): v for k, v in t_hist.items()}))
# chorded clusters from the recursion failures: whole-boundary level is impossible (tau 1.32-1.73); test min winding
# with the measured min tau threshold (3.0 = sqrt3^2) as the level bound
for fn in sorted(glob.glob('/mnt/project-files/multiscale/levelling/fail_*.pkl'))[:12]:
    d = pickle.load(open(fn, 'rb')); T = graph(d['name'])
    try: cl = Cluster(T, set(d['A']) | set(d['B']))
    except Exception as e: rec(dict(file=fn.split('/')[-1], err=str(e))); continue
    if len(cl.S) > 1000: continue
    t0 = time.time(); _, c1 = level_w(T, cl.S, K2=3.0, wmode='min', seed=1, budget=3*10**6)
    _, c0 = level_w(T, cl.S, K2=3.0, wmode=None, seed=1, budget=3*10**6)
    rec(dict(file=fn.split('/')[-1], n=len(cl.S), m=cl.m, chords=len(chords(cl)), nodd=len(cl.odd), tau3_anyw=(c0 is not None) if c0 != 'UNK' else 'UNK', tau3_minw=(c1 is not None) if c1 != 'UNK' else 'UNK', sec=round(time.time()-t0,1)))
