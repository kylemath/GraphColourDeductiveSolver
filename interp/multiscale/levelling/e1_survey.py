# E1: exact minimum boundary tilt over 4-colourings, for balls B_r(v), r=3..8
import sys, json, time, random
from multiprocessing import Pool
from lev import *
GR = {}
def graph(name):
    if name not in GR:
        if name.startswith('ico'): adj = icosphere(int(name[3:]))
        else: adj = load_map(name)
        GR[name] = Tri(adj)
    return GR[name]
def job(a):
    name, c, r, tag = a
    T = graph(name)
    try: cl = Cluster(T, bfs(T.adj, c, r))
    except Exception as e: return dict(name=name, c=c, r=r, err=str(e))
    t = time.time()
    K, col, t0, ex = min_tau(cl, budget=300000)
    res = dict(name=name, c=c, r=r, tag=tag, tau=K, tau_rand=t0, exact=ex, sec=round(time.time()-t, 1), **cl.info())
    if not cl.parity_odd: res['t_at_min'] = cl.tau(col)[1]
    return res
if __name__ == '__main__':
    jobs = []
    rng = random.Random(1)
    for f in [5, 7, 10, 14]:
        T = graph('ico%d' % f); n = len(T.adj)
        odd = [v for v in range(n) if T.deg[v] % 2]
        dd = {}
        for o in odd:
            for v, d in bfs(T.adj, o).items(): dd[v] = min(dd.get(v, 99), d)
        far = max(dd, key=dd.get)
        cents = [(0, 'deg5'), (far, 'far'), ] + [(rng.randrange(n), 'rand') for _ in range(2)]
        # vertex at distance 2 from vertex 0 (odd vertex near boundary for r=3)
        cents.append((next(v for v, d in bfs(T.adj, 0).items() if d == 2), 'd2'))
        for c, tag in cents:
            for r in range(3, 9): jobs.append(('ico%d' % f, c, r, tag))
    for name in ['BASE_rand22', 'M3_ico22_hard', 'M5_ico31', 'BASE_defect_ico17']:
        n = len(graph(name).adj)
        for _ in range(3):
            c = rng.randrange(n)
            for r in range(3, 9): jobs.append((name, c, r, 'rand'))
    jobs.sort(key=lambda j: j[2])
    out = open('e1_survey.jsonl', 'w')
    with Pool(4) as p:
        for res in p.imap_unordered(job, jobs):
            out.write(json.dumps(res) + '\n'); out.flush()
            print(res, flush=True)
