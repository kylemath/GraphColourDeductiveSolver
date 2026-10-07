#!/usr/bin/env python3
"""Job AO (2)-(3): for every Gamma-cycle with L = 40 or 60 (orders 25-27, both orientations): orientation-preserving automorphisms phi of T fixing the hole (rotation-system maps
sending dart (h, x_0) to (h, x_r)); is there a phi and a shift d (10, 20, 30) with s(t + d) = phi(s(t)) for all t (as partitions)? Also the L = 20 cycles for comparison."""
import json
from collections import Counter
from multiprocessing import Pool
from uv_lib import Hole
from jobag import canon
def automorphisms(H):
    rot = H.rot; n = len(rot); h = H.h; out = []
    for r in range(5):
        phi = {h: h}; st = [(h, 0, rot[h][r] if False else None)]
        # map dart (h, x0) -> (h, x_r): BFS over darts
        phi = {h: h}; dmap = {(h, H.L[0]): (h, H.L[r])}; q = [(h, H.L[0])]; ok = True
        while q and ok:
            u, v = q.pop(); a, b = dmap[(u, v)]
            if phi.setdefault(v, b) != b: ok = False; break
            ru, ra = rot[u], rot[a]
            if len(ru) != len(ra): ok = False; break
            i, k = ru.index(v), ra.index(b)
            for t in range(len(ru)):
                v2, b2 = ru[(i + t) % len(ru)], ra[(k + t) % len(ra)]
                if (u, v2) in dmap:
                    if dmap[(u, v2)] != (a, b2): ok = False; break
                else: dmap[(u, v2)] = (a, b2); q.append((u, v2))
                if (v2, u) not in dmap: dmap[(v2, u)] = (b2, a); q.append((v2, u))
                elif dmap[(v2, u)] != (b2, a): ok = False; break
        if ok and len(phi) == n and len(set(phi.values())) == n: out.append((r, phi))
    return out
def part(H, k):
    cls = {}
    for v in H.sp.order: cls.setdefault(H.col(k, v), set()).add(v)
    return frozenset(frozenset(s) for s in cls.values())
def job(args):
    lab, name, hole = args
    H = Hole(name, hole, lab.endswith('m')); auts = automorphisms(H); res = []
    for c, z in enumerate(H.cycles):
        if not all(H.DL[x] for x in z): continue
        L = len(z); P = [part(H, x) for x in z]; found = []
        for d in (10, 20, 30, 40):
            if d >= L: continue
            for r, phi in auts:
                for s in range(L):
                    img = frozenset(frozenset(phi[v] for v in cl) for cl in P[0])
                    if img == P[s % L]:
                        if all(frozenset(frozenset(phi[v] for v in cl) for cl in P[t]) == P[(t + s) % L] for t in range(L)): found.append((r, s))
                        break
        res.append(dict(run=lab, name=name, hole=hole, pattern=','.join(map(str, canon([len(H.rot[x]) for x in H.L]))), L=L, n_aut=len(auts), equivariant_shifts=sorted(set(found))))
    return res
if __name__ == '__main__':
    holes = set()
    for lab in ['z25', 'z25m', 'z26', 'z26m', 'z27', 'z27m']:
        for l in open('../out/%s.jsonl' % lab):
            if '"jobs": {"pos": [{' not in l: continue
            r = json.loads(l)
            if any(z['gamma'] and z['L'] in (40, 60) for z in r['jobs']['pos']): holes.add((lab, r['name'], r['hole']))
    with Pool(12) as P: res = [x for xs in P.map(job, sorted(holes)) for x in xs]
    json.dump(res, open('jobao.json', 'w'))
    C = Counter()
    for r in res: C[(r['L'], 'aut group (fixing h, orientation-preserving) order %d' % r['n_aut'], 'shift by an automorphism: ' + (str(sorted({s for _, s in r['equivariant_shifts']})) if r['equivariant_shifts'] else 'NONE'))] += 1
    for k, v in sorted(C.items()): print(v, k)
