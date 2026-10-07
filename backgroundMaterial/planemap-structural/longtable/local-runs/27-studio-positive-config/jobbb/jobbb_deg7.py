#!/usr/bin/env python3
"""Job BB (3) [exploratory]: at (5,5,5,5,7) Gamma-cycles (census orders 25-27, both orientations; Job AQ adversarial A7_exc h22/h34, r5_80b930d1_exc h2), for every
step-8 break (J false at position 9, NightA34 table), which inserted vertex the pocket passes p through. Inserted vertices: p's two outer neighbours other than y, z:
M adjacent to y, M' adjacent to z. The pocket at position 9 is the closed {c(p), c(x+)}-curve p x+ w+ ... X p: X is used <=> c(X) = c(x+) and X is joined to w+ in
G_{c(p),c(x+)} - h - p - x+. Consecutive-break periods: both periods b, b+1 break; do the two pockets use different inserted vertices?"""
import sys, os, json
from collections import Counter
from multiprocessing import Pool
HERE = os.path.dirname(os.path.abspath(__file__))
for d in ('../jobax', '../jobav', '../jobuv', '../jobas'): sys.path.insert(0, os.path.join(HERE, d))
from uv_lib import Hole
from jobax import FrameQ
from jobav import partition, comp
AQDIR = os.path.join(HERE, '../../../../studiointel/path3-local/run_dd/')
def job(args):
    src, name, hole, mirror, faces = args
    if faces is None: H = Hole(name, hole, mirror)
    else:
        from flipsearch import rotation
        H = Hole(name, hole, mirror, rot=rotation([tuple(t) for t in faces]))
    adj = {v: set(r) - {hole} for v, r in enumerate(H.rot) if v != hole}; deg = [len(H.rot[x]) for x in H.L]
    if sorted(deg) != [5, 5, 5, 5, 7]: return []
    q = deg.index(7); F = FrameQ(adj, H.L, H.w, q); n = F.names
    ins = [u for u in adj[n['p']] if u not in (n['xp'], n['xm'], n['y'], n['z'])]
    M = [u for u in ins if n['y'] in adj[u]]; Mp = [u for u in ins if n['z'] in adj[u]]
    if len(M) != 1 or len(Mp) != 1 or M == Mp: return [dict(error='inserted vertices not M/M-prime', name=name, hole=hole)]
    M, Mp = M[0], Mp[0]; out = []
    for z in H.cycles:
        if not all(H.DL[x] for x in z): continue
        cyc = [{v: H.col(x, v) for v in H.sp.order} for x in z]; P = [F.pos(c) for c in cyc]
        if None in P: out.append(dict(error='no labelling')); continue
        s = P.index(0); cyc = cyc[s:] + cyc[:s]; P = P[s:] + P[:s]
        if any(P[t] != t % 10 for t in range(len(z))): out.append(dict(error='positions')); continue
        col = dict(cyc[0]); per = []
        for t in range(len(z)):
            if t % 10 == 9:
                cy, cz = col[n['y']], col[n['z']]; J = n['z'] in comp(adj, col, n['y'], cy, cz)
                a, b = col[n['p']], col[n['xp']]; sub = {v: (c if v not in (n['p'], n['xp']) else -1) for v, c in col.items()}; W = comp(adj, sub, n['wp'], a, b)
                use = [nm for nm, X in (('M', M), ("M'", Mp)) if col[X] == b and X in W]
                per.append(dict(brk=not J, uses=use, colours=dict(p=a, xp=b, M=col[M], Mp=col[Mp])))
            pair, K = F.step(col); u, w = pair; col = {v: (w if v in K and c == u else u if v in K and c == w else c) for v, c in col.items()}
        out.append(dict(source=src, name=name, hole=hole, orientation='mirror' if mirror else 'plantri', L=len(z), periods=per))
    return out
if __name__ == '__main__':
    sys.path.insert(0, os.path.join(HERE, '../jobuv')); from jobag import canon
    jobs = set()
    for lab in ['z25', 'z25m', 'z26', 'z26m', 'z27', 'z27m']:
        for l in open(os.path.join(HERE, '../out/%s.jsonl' % lab)):
            if '"jobs": {"pos": [{' not in l: continue
            r = json.loads(l)
            if canon(r['linkdeg']) == (5, 5, 5, 5, 7) and any(z['gamma'] for z in r['jobs']['pos']): jobs.add(('census', r['name'], r['hole'], lab.endswith('m'), None))
    jobs = sorted(jobs)
    for g, h in [('A7_exc', 22), ('A7_exc', 34), ('r5_80b930d1_exc', 2)]:
        F = json.load(open(AQDIR + 'best-%s.json' % g))['faces']
        for m in (False, True): jobs.append(('adversarial', g, h, m, F))
    with Pool(4) as P: res = [x for xs in P.map(job, jobs) for x in xs]
    json.dump(res, open(os.path.join(HERE, 'jobbb-deg7-pockets.json'), 'w'))
    c = Counter(); cons = Counter(); ex = []
    for r in res:
        if 'error' in r: c['error ' + r['error']] += 1; continue
        ps = r['periods']; m = len(ps)
        for b, p in enumerate(ps):
            if p['brk']: c[(r['source'], 'break; pocket passes p through', '+'.join(p['uses']) or 'NONE')] += 1
            else: c[(r['source'], 'no break; a pocket curve through', '+'.join(p['uses']) or 'none')] += 1
            if m > 1 and p['brk'] and ps[(b + 1) % m]['brk'] and (m > 2 or b == 0):
                u1, u2 = p['uses'], ps[(b + 1) % m]['uses']
                cons[(r['source'], 'consecutive breaks: %s then %s' % ('+'.join(u1) or 'NONE', '+'.join(u2) or 'NONE'), 'different inserted vertices: %s' % (set(u1) != set(u2) and len(u1) == 1 and len(u2) == 1))] += 1
                if len(ex) < 20: ex.append((r['name'], r['hole'], r['orientation'], r['L'], b, u1, u2))
    for k, v in sorted(c.items(), key=str): print(v, k)
    print('consecutive-break period pairs:'); [print('   ', v, k) for k, v in sorted(cons.items(), key=str)]
    print('examples:', ex)
