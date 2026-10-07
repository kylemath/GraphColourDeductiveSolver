#!/usr/bin/env python3
"""Job AY [exploratory]: NightSigmaImage Sec. 3 check on all Gamma-cycle periods at (5,5,5,5,6) and (5,5,5,5,7) (census orders 25-27 both orientations; Job AS constructions
via the Job AV replays). Absolute replay as in Job AX (jobax.FrameQ). sigma at every position uses that state's own j: swap of the {c(x_j), c(x_{j+1})}-component of x_{j+1};
fixed <=> that component contains every vertex of T - h with colour c(x_j) or c(x_{j+1}). Per period: the 10-bit fixed pattern (positions 0..9), k4/k3 failure flags (sigma at
positions 0/2 not lockless), and at each fixed position the cycle ranks (E - V + C) of the six 2-colour subgraphs of T - h, colours named in the period's position-4 frame:
1 = c(p), 2 = c(m) (the fourth colour), 3 = c(y), 4 = c(z)."""
import sys, os, json
from collections import Counter
from itertools import combinations
from multiprocessing import Pool
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../jobax')); sys.path.insert(0, os.path.join(HERE, '../jobav')); sys.path.insert(0, os.path.join(HERE, '../jobuv'))
from jobax import FrameQ
from jobav import partition, comp
def rank(adj, col, a, b):
    V = [v for v in adj if col[v] in (a, b)]; E = sum(1 for v in V for u in adj[v] if u > v and col[u] in (a, b)); seen = set(); C = 0
    for v in V:
        if v not in seen: C += 1; seen |= comp(adj, col, v, a, b)
    return E - len(V) + C
def periods(F, cyc):
    L = len(cyc); P = [F.pos(c) for c in cyc]
    if None in P or 0 not in P: return 'no labelling'
    s = P.index(0); cyc = cyc[s:] + cyc[:s]; P = P[s:] + P[:s]
    if any(P[t] != t % 10 for t in range(L)): return 'positions not cyclic'
    n = F.names; adj = F.adj; col = dict(cyc[0]); out = []
    for b in range(L // 10):
        bits = []; fixinfo = {}; fl = {}
        names = None; states = []
        for i in range(10):
            if partition(col) != partition(cyc[10 * b + i]): return 'replay diverged'
            states.append(dict(col)); pair, K = F.step(col); a, c2 = pair
            col = {v: (c2 if v in K and x == a else a if v in K and x == c2 else x) for v, x in col.items()}
        c4 = states[4]; cp, cy, cz = c4[n['p']], c4[n['y']], c4[n['z']]; cm = ({0, 1, 2, 3} - {cp, cy, cz}).pop()
        nm = {cp: '1', cm: '2', cy: '3', cz: '4'}
        for i, st in enumerate(states):
            j, ty, (al, mu, A, B) = F.lframe(st); K = comp(adj, st, F.L[(j + 1) % 5], al, mu)
            fx = all(v in K for v in adj if st[v] in (al, mu)); bits.append(int(fx))
            if fx:
                rk = {''.join(sorted(nm[a] + nm[c])): rank(adj, st, a, c) for a, c in combinations(range(4), 2)}
                fixinfo[i] = dict(sigma_pair=''.join(sorted(nm[al] + nm[mu])), complement_pair=''.join(sorted(nm[A] + nm[B])), ranks=rk,
                                  acyclic=sorted(k for k, v in rk.items() if v == 0))
            if i in (0, 2): fl['k4fail' if i == 0 else 'k3fail'] = not F.lockless(F.sigma(st))
        out.append(dict(pattern=''.join(map(str, bits)), fixed=fixinfo, **fl))
    if partition(col) != partition(cyc[0]): return 'no closure'
    return out
def census_job(args):
    from uv_lib import Hole
    lab, name, hole = args
    H = Hole(name, hole, lab.endswith('m')); adj = {v: set(r) - {hole} for v, r in enumerate(H.rot) if v != hole}
    deg = [len(H.rot[x]) for x in H.L]; q = next(t for t in range(5) if deg[t] >= 6); F = FrameQ(adj, H.L, H.w, q); out = []
    for z in H.cycles:
        if not all(H.DL[x] for x in z): continue
        out.append(dict(source='census', run=lab, name=name, hole=hole, pattern=tuple(sorted(deg)), L=len(z), periods=periods(F, [{v: H.col(x, v) for v in H.sp.order} for x in z])))
    return out
if __name__ == '__main__':
    from jobag import canon
    holes = set()
    for lab in ['z25', 'z25m', 'z26', 'z26m', 'z27', 'z27m']:
        for l in open(os.path.join(HERE, '../out/%s.jsonl' % lab)):
            if '"jobs": {"pos": [{' not in l: continue
            r = json.loads(l)
            if canon(r['linkdeg']) in ((5, 5, 5, 5, 6), (5, 5, 5, 5, 7)) and any(z['gamma'] for z in r['jobs']['pos']): holes.add((lab, r['name'], r['hole']))
    with Pool(12) as P: res = [x for xs in P.map(census_job, sorted(holes)) for x in xs]
    sys.path.insert(0, os.path.join(HERE, '../jobaq')); import jobaq; jobaq.GDIR = os.path.join(HERE, '../jobas/')
    for l in open(os.path.join(HERE, '../jobav/jobav-cycles.jsonl')):
        r = json.loads(l)
        if r['source'] != 'construction': continue
        E, adj0, link, w = jobaq.load(r['name'], r['hole'], r['orientation'] == 'mirror'); adj = {v: set(a) - {r['hole']} for v, a in adj0.items() if v != r['hole']}
        q = next(t for t in range(5) if len(adj0[link[t]]) >= 6)
        res.append(dict(source='construction', name=r['name'], hole=r['hole'], orientation=r['orientation'], pattern=(5, 5, 5, 5, 6), L=r['L'],
                        periods=periods(FrameQ(adj, link, w, q), [dict(zip(r['vertices'], c)) for c in r['colourings']])))
    with open(os.path.join(HERE, 'jobay-periods.jsonl'), 'w') as f:
        for r in res: f.write(json.dumps(r, default=list) + '\n')
    for tag, sel in (('degree 6 census', lambda r: r['source'] == 'census' and r['pattern'] == (5, 5, 5, 5, 6)), ('degree 6 constructions', lambda r: r['source'] == 'construction'),
                     ('degree 7 census', lambda r: r['pattern'] == (5, 5, 5, 5, 7))):
        R = [r for r in res if sel(r)]; err = Counter(r['periods'] for r in R if isinstance(r['periods'], str)); R = [r for r in R if not isinstance(r['periods'], str)]
        Pd = [p for r in R for p in r['periods']]; c = Counter()
        for p in Pd:
            f = p['k4fail'] or p['k3fail']; c['(k3 or k4 failure) <=> fixed at position 1: %s' % (f == (p['pattern'][1] == '1'))] += 1
            c['k4fail %d k3fail %d fixed@1 %s' % (p['k4fail'], p['k3fail'], p['pattern'][1])] += 1
            c['W2 (4,6,8 not all fixed): %s' % (p['pattern'][4] + p['pattern'][6] + p['pattern'][8] != '111')] += 1
            c['W2* (4,8 not both fixed): %s' % (p['pattern'][4] + p['pattern'][8] != '11')] += 1
            for i, fi in p['fixed'].items():
                c['fixed at %s: sigma pair %s / complement %s rank %d' % (i, fi['sigma_pair'], fi['complement_pair'], fi['ranks'][fi['complement_pair']])] += 1
                c['fixed at %s: acyclic pairs %s' % (i, ','.join(fi['acyclic']))] += 1
        cons = Counter(); joint = Counter()
        for r in R:
            ps = r['periods']; m = len(ps)
            for b in range(m):
                if m > 1: cons['consecutive periods both fixed at position 1: %s' % (ps[b]['pattern'][1] == '1' and ps[(b + 1) % m]['pattern'][1] == '1')] += 1
                joint[(ps[b]['pattern'], ps[(b + 1) % m]['pattern'], 'L=%d' % r['L'] if r['L'] <= 20 else 'L>20')] += 1
        print('== %s: %d cycles, %d periods, errors %s' % (tag, len(R), len(Pd), dict(err)))
        for k, v in sorted(c.items()): print('   ', v, k)
        for k, v in sorted(cons.items()): print('   ', v, k)
        print('   10-bit patterns (positions 0..9):', dict(Counter(p['pattern'] for p in Pd).most_common()))
        print('   joint patterns of consecutive periods (b, b+1):')
        for k, v in sorted(joint.items(), key=lambda x: -x[1]): print('      ', v, k)
