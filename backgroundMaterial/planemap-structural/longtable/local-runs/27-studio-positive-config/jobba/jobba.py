#!/usr/bin/env python3
"""Job BA [exploratory]: sigma-image classification (NightSigmaImage Sec. 2-3) on all Gamma-cycles at (5,5,5,5,6) and (5,5,5,5,7): census orders 25-27 both orientations,
the Job AS constructions, and the Job AQ adversarial graphs (A7_exc h22/h34, r5_80b930d1_exc h2). Engine: uv_lib.Hole (full state space of T - h; rotation systems from
face lists via flipsearch.rotation for the non-census graphs). For every state r of every Gamma-cycle Z (position 0..9 from the NightA34 table, q = the high-degree link vertex):
sigma(r) = swap of the {alpha,mu}-component of x_{j+1}; kind = fixed / filled / lockless / Lock1-only / Lock2-only / DL; the forward run of sigma(r) (u = unfilled states from
sigma(r) on, f = filled states after them); on Z? (then is sigma(r) = pi^10(r)?), else the target cycle's (w, L)."""
import sys, os, json
from collections import Counter
from multiprocessing import Pool
HERE = os.path.dirname(os.path.abspath(__file__))
for d in ('../jobuv', '../jobas'): sys.path.insert(0, os.path.join(HERE, d))
from uv_lib import Hole
POS = {(3, 4): 0, (1, 1): 1, (3, 3): 2, (1, 0): 3, (3, 2): 4, (1, 4): 5, (3, 1): 6, (1, 3): 7, (3, 0): 8, (1, 2): 9}
AQDIR = os.path.join(HERE, '../../../../studiointel/path3-local/run_dd/')
def kind(H, s, r):
    if s == r: return 'fixed'
    lk = H.locks(s)
    if lk is None: return 'filled'
    return {(False, False): 'lockless', (True, False): 'Lock1-only', (False, True): 'Lock2-only', (True, True): 'DL'}[tuple(lk)]
def run_of(H, s):
    u = 0; y = s
    while not H.filled(y) and u < 10000: u += 1; y = H.pi[y]
    f = 0
    while H.filled(y): f += 1; y = H.pi[y]
    return u, f
def job(args):
    src, name, hole, mirror, faces = args
    if faces is None: H = Hole(name, hole, mirror)
    else:
        from flipsearch import rotation
        H = Hole(name, hole, mirror, rot=rotation([tuple(t) for t in faces]))
    deg = [len(H.rot[x]) for x in H.L]; pat = tuple(sorted(deg))
    if pat not in ((5, 5, 5, 5, 6), (5, 5, 5, 5, 7)): return []
    q = next(t for t in range(5) if deg[t] >= 6); out = []
    for ci, z in enumerate(H.cycles):
        if not all(H.DL[x] for x in z): continue
        L = len(z); where = {x: i for i, x in enumerate(z)}; rows = []
        for t, r in enumerate(z):
            j, ty, hi, roles = H.frame(r); pos = POS.get((ty, (q - j) % 5)); s = H.sigma(r); kd = kind(H, s, r)
            row = dict(t=t, pos=pos, kind=kd)
            if kd != 'fixed':
                row['run'] = run_of(H, s)
                if H.cyc[s] == ci: row['same'] = True; row['offset'] = (where[s] - t) % L; row['is_pi10'] = row['offset'] == 10 % L
                else: c = H.cyc[s]; row['same'] = False; row['target_w'] = H.W[c]; row['target_L'] = len(H.cycles[c])
            rows.append(row)
        out.append(dict(source=src, name=name, hole=hole, orientation='mirror' if mirror else 'plantri', pattern=pat, L=L, w=H.W[ci], rows=rows))
    return out
if __name__ == '__main__':
    from jobag import canon
    jobs = set()
    for lab in ['z25', 'z25m', 'z26', 'z26m', 'z27', 'z27m']:
        for l in open(os.path.join(HERE, '../out/%s.jsonl' % lab)):
            if '"jobs": {"pos": [{' not in l: continue
            r = json.loads(l)
            if canon(r['linkdeg']) in ((5, 5, 5, 5, 6), (5, 5, 5, 5, 7)) and any(z['gamma'] for z in r['jobs']['pos']): jobs.add(('census', r['name'], r['hole'], lab.endswith('m'), None))
    jobs = sorted(jobs)
    for g, h in [('A7f1', 22), ('A7f2', 22), ('A7f3', 34), ('A7f4', 22), ('walk-best-A7f1-1', 22), ('walk-best-A7f1-3', 22)]:
        F = json.load(open(os.path.join(HERE, '../jobas/best-%s.json' % g)))['faces']
        for m in (False, True): jobs.append(('construction', g, h, m, F))
    for g, h in [('A7_exc', 22), ('A7_exc', 34), ('r5_80b930d1_exc', 2)]:
        F = json.load(open(AQDIR + 'best-%s.json' % g))['faces']
        for m in (False, True): jobs.append(('adversarial', g, h, m, F))
    with Pool(12) as P: res = [x for xs in P.map(job, jobs) for x in xs]
    with open(os.path.join(HERE, 'jobba-cycles.jsonl'), 'w') as f:
        for r in res: f.write(json.dumps(r, default=list) + '\n')
    for deg in (6, 7):
        for srcs in (('census',), ('construction', 'adversarial')):
            R = [r for r in res if r['pattern'][-1] == deg and r['source'] in srcs]
            if not R: continue
            c = Counter(); dist = Counter(); u34 = Counter()
            for r in R:
                for x in r['rows']:
                    p = x['pos']; dist[(p, x['kind'])] += 1; nf = x['kind'] != 'fixed'
                    if p is None: c['state with no period position'] += 1; continue
                    if p % 2 == 0 and nf:
                        c['(a) non-fixed R3 image is DL: %s' % (x['kind'] == 'DL')] += 1
                        c['(b) non-fixed R3 image target: %s' % ('same cycle' if x['same'] else 'w<0' if x['target_w'] < 0 else 'w=0' if x['target_w'] == 0 else 'w>0')] += 1
                    if p % 2 == 1 and nf and x['same']: c['(c) R1 image on Z equals pi^10(r): %s' % x['is_pi10']] += 1
                    if p % 2 == 1 and nf: c['    R1 image: %s' % ('on Z' if x['same'] else 'other Gamma-cycle' if x['target_w'] * 5 == x['target_L'] else 'other cycle w=%s' % ('<0' if x['target_w'] < 0 else '0' if x['target_w'] == 0 else '>0 non-Gamma'))] += 1
                    if p == 0 and x['kind'] not in ('lockless', 'fixed'):
                        u, f = x['run']; u34['(d) k4 failure image %s: (u,f) = (%d,%d)' % (x['kind'], u, f)] += 1
                        u34['(d) U34 (u in {3,4} and u=4 => f=1): %s' % (u in (3, 4) and (u != 4 or f == 1))] += 1
                    if p == 2 and x['kind'] not in ('lockless', 'fixed'):
                        u, f = x['run']; u34['    k3 failure image %s: forward (u,f) = (%d,%d)' % (x['kind'], u, f)] += 1
            print('== degree %d, %s: %d cycles (L: %s), %d states' % (deg, '+'.join(srcs), len(R), dict(Counter(r['L'] for r in R)), sum(r['L'] for r in R)))
            for k, v in sorted(c.items()): print('   ', v, k)
            for k, v in sorted(u34.items()): print('   ', v, k)
            kinds = ['fixed', 'lockless', 'Lock1-only', 'Lock2-only', 'DL', 'filled']
            print('    (e) %-4s %s' % ('pos', ' '.join('%10s' % k for k in kinds)))
            for p in range(10): print('        %-4d %s' % (p, ' '.join('%10d' % dist[(p, k)] for k in kinds)))
