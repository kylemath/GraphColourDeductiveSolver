#!/usr/bin/env python3
"""Job AW verification: every saved hit graph is re-checked independently of picyc: triangulation sanity (Euler, each edge in exactly two faces, consistent orientation),
core class (flipsearch.core_ok), link pattern (5,5,5,5,6) at the hole, then uv_lib.Hole (full Python state space) + the Job AY absolute replay (jobay.periods): per Gamma-cycle
per period the k4/k3 failure flags and the 10-bit sigma fixed pattern. A34' counterexample = two consecutive periods with k4 failures. W2* = positions 4 and 8 fixed in one
period; W2 = positions 4, 6, 8 fixed."""
import sys, os, json
from collections import Counter
HERE = os.path.dirname(os.path.abspath(__file__))
for d in ('../jobas', '../jobuv', '../jobay', '../jobax', '../jobav'): sys.path.insert(0, os.path.join(HERE, d))
from flipsearch import rotation, core_ok
from uv_lib import Hole
from jobax import FrameQ
from jobay import periods
def sane(F):
    V = {x for t in F for x in t}; E = Counter()
    for t in F:
        for i in range(3): E[(t[i], t[(i + 1) % 3])] += 1
    und = Counter(frozenset(e) for e in E)
    return len(F) == 2 * len(V) - 4 and all(v == 1 for v in E.values()) and all(v == 2 for v in und.values()) and all((b, a) in E for a, b in E)
out = []; seen = set()
for l in open(os.path.join(HERE, 'jobaw-walks.jsonl')):
    r = json.loads(l)
    for k, h in enumerate(r['hits']):
        F = [tuple(t) for t in h['faces']]; key = frozenset(F)
        if key in seen: continue
        seen.add(key); rot = rotation(F); res = dict(seed=r['seed'], objective=r['objective'], walk=r['walk'], it=h['it'], score=h['score'], n=len(rot), sane=sane(F), core=core_ok(F), cycles=[])
        for mir in (False, True):
            H = Hole('aw', r['hole'], mir, rot=rot); adj = {v: set(x) - {r['hole']} for v, x in enumerate(H.rot) if v != r['hole']}
            deg = [len(H.rot[x]) for x in H.L]; res['linkdeg'] = sorted(deg)
            if sorted(deg) != [5, 5, 5, 5, 6]: continue
            Fq = FrameQ(adj, H.L, H.w, deg.index(6))
            for z in H.cycles:
                if not all(H.DL[x] for x in z): continue
                ps = periods(Fq, [{v: H.col(x, v) for v in H.sp.order} for x in z])
                if isinstance(ps, str): res['cycles'].append(dict(mirror=mir, L=len(z), error=ps)); continue
                m = len(ps)
                res['cycles'].append(dict(mirror=mir, L=len(z), w=H.W[H.cyc[z[0]]], k4=[p['k4fail'] for p in ps], k3=[p['k3fail'] for p in ps], fixed=[p['pattern'] for p in ps],
                    A34_violation=any(ps[b]['k4fail'] and ps[(b + 1) % m]['k4fail'] for b in range(m)) if m > 1 else False,
                    W2s_violation=any(p['pattern'][4] == '1' and p['pattern'][8] == '1' for p in ps), W2_violation=any(p['pattern'][4] + p['pattern'][6] + p['pattern'][8] == '111' for p in ps)))
        res['A34'] = any(c.get('A34_violation') for c in res['cycles']); res['W2s'] = any(c.get('W2s_violation') for c in res['cycles']); res['W2'] = any(c.get('W2_violation') for c in res['cycles'])
        if res['A34'] or res['W2s'] or res['W2']:
            fn = 'hits/%s-%s-w%d-it%d.json' % (r['seed'], r['objective'], r['walk'], h['it']); json.dump(dict(faces=[list(t) for t in F], hole=r['hole']), open(os.path.join(HERE, fn), 'w')); res['file'] = fn
        out.append(res)
json.dump(out, open(os.path.join(HERE, 'jobaw-verified.json'), 'w'), indent=0)
c = Counter()
for x in out:
    c[('sane %s core %s' % (x['sane'], x['core']))] += 1
    c['A34 violation (consecutive k4 failures): %s' % x['A34']] += 1; c['W2* violation: %s' % x['W2s']] += 1; c['W2 violation: %s' % x['W2']] += 1
print('distinct hit graphs:', len(out)); [print('   ', v, k) for k, v in sorted(c.items())]
for x in out:
    if x['A34']:
        print('A34 COUNTEREXAMPLE', x['seed'], x['objective'], 'walk', x['walk'], 'it', x['it'], 'n', x['n'], x['file'], [c for c in x['cycles'] if c.get('A34_violation')])
