#!/usr/bin/env python3
"""Job AT (NightGammaLength §2): for every Gamma-cycle, per period of 10 pi-steps, how often each edge of T - v is CUT (exactly one endpoint in the step's swapped
component). Ring = edges with both ends among the hole vertices (link, w's, p's middle neighbour(s)); far = the rest. D_b = far edges cut an odd number of times in period b.
Checks: ring edges cut 4 times / ring faces met 6 times per period (single high-degree vertex holes); every edge cut an even number of times over the whole cycle;
H_D (D_b nonempty for every b); D_b the same for all b; XOR of D over any odd number of consecutive periods nonempty."""
import json, sys
from collections import Counter, defaultdict
from multiprocessing import Pool
from uv_lib import Hole
from jobag import canon
from jobam import stepK
def analyse(H):
    rot = H.rot; h = H.h; L5 = H.L
    hi = [t for t in range(5) if len(rot[L5[t]]) >= 6]
    w = H.w; M = []
    if len(hi) == 1:
        t6 = hi[0]; p = L5[t6]; M = [u for u in rot[p] if u != h and u not in (L5[(t6 + 1) % 5], L5[(t6 + 4) % 5], w[(t6 + 4) % 5], w[t6])]
    hv = set(L5) | set(w) | set(M)
    edges = sorted({(min(a, b), max(a, b)) for a in range(len(rot)) if a != h for b in rot[a] if b != h})
    ring = [e for e in edges if e[0] in hv and e[1] in hv]; far = [e for e in edges if not (e[0] in hv and e[1] in hv)]
    faces = set()
    for a in range(len(rot)):
        if a == h: continue
        r = rot[a]
        for i in range(len(r)):
            b, c = r[i], r[(i + 1) % len(r)]
            if h not in (b, c): faces.add(frozenset((a, b, c)))
    ringfaces = [f for f in faces if f <= hv]
    out = []
    for cidx, zc in enumerate(H.cycles):
        if not all(H.DL[x] for x in zc): continue
        n = len(zc)
        if len(hi) == 1:
            fr = [H.frame(x) for x in zc]; s0 = next((i for i in range(n) if fr[i][1] == 3 and (hi[0] - fr[i][0]) % 5 == 4), 0); zc = zc[s0:] + zc[:s0]
        Ks = [stepK(H, x) for x in zc]
        total = Counter(); D = []; ringcut = Counter(); facemeet = Counter()
        for b in range(0, n, 10):
            cnt = Counter()
            for K in Ks[b:b + 10]:
                for e in edges:
                    if (e[0] in K) != (e[1] in K): cnt[e] += 1
                for f in ringfaces:
                    if f & K: facemeet[(b, f)] += 1
            total.update(cnt)
            D.append(frozenset(e for e in far if cnt[e] % 2))
            for e in ring: ringcut[cnt[e]] += 1
        P = len(D)
        odd_xor_empty = []
        for start in range(P):
            acc = frozenset()
            for ln in range(1, P + 1):
                acc = acc ^ D[(start + ln - 1) % P]
                if ln % 2 == 1 and not acc: odd_xor_empty.append((start, ln))
        out.append(dict(L=n, periods=P, all_even_total=all(total[e] % 2 == 0 for e in edges), ring_cut_hist=dict(ringcut), ringface_meet_hist=dict(Counter(facemeet.values())),
                        D_sizes=[len(d) for d in D], HD=all(D), D_same=len(set(D)) == 1, odd_window_xor_empty=odd_xor_empty[:4], n_odd_window_xor_empty=len(odd_xor_empty)))
    return out
def job(args):
    lab, name, hole = args
    H = Hole(name, hole, lab.endswith('m')); return [dict(r, run=lab, name=name, hole=hole, pattern=','.join(map(str, canon([len(H.rot[x]) for x in H.L])))) for r in analyse(H)]
def job_faces(args):
    fn, hole, mirror = args
    import sys; sys.path.insert(0, '../jobas'); from flipsearch import rotation
    F = [tuple(t) for t in json.load(open(fn))['faces']]; rot = rotation(F)   # NOTE: labels relabelled 0..n-1 in sorted order = original labels here (0..n-1)
    H = Hole(fn, hole, mirror, rot=rot)
    return [dict(r, run='mirror' if mirror else 'plantri', name=fn, hole=hole, pattern=','.join(map(str, canon([len(H.rot[x]) for x in H.L])))) for r in analyse(H)]
if __name__ == '__main__':
    holes = set()
    for lab in ['z25', 'z25m', 'z26', 'z26m', 'z27', 'z27m']:
        for l in open('../out/%s.jsonl' % lab):
            if '"jobs": {"pos": [{' not in l: continue
            r = json.loads(l)
            if any(zz['gamma'] for zz in r['jobs']['pos']): holes.add((lab, r['name'], r['hole']))
    extra = [('../jobas/best-%s.json' % g, h, m) for g, h in (('A7f1', 22), ('A7f2', 22), ('A7f3', 34), ('A7f4', 22)) for m in (False, True)]
    with Pool(12) as P:
        res = [x for xs in P.map(job, sorted(holes)) for x in xs]; res2 = [x for xs in P.map(job_faces, extra) for x in xs]
    json.dump(dict(census=res, constructions=res2), open('jobat.json', 'w'))
    for tag, R in (('census orders 25-27', res), ('degree-6 constructions (A7 + flips)', res2)):
        print('=== %s: Gamma-cycle records %d' % (tag, len(R)))
        print('  every edge cut an even number of times over the whole cycle: %d / %d' % (sum(r['all_even_total'] for r in R), len(R)))
        rc = Counter(); rf = Counter()
        for r in R:
            if r['pattern'] in ('5,5,5,5,6', '5,5,5,5,7'): rc.update(r['ring_cut_hist']); rf.update(r['ringface_meet_hist'])
        print('  single-high-vertex patterns: ring-edge cut counts per period %s; ring faces met per period %s' % (dict(rc), dict(rf)))
        print('  H_D (D_b nonempty every period): %d / %d; D_b identical in all periods: %d / %d; some odd window with XOR(D) empty: %d records' % (
            sum(r['HD'] for r in R), len(R), sum(r['D_same'] for r in R), len(R), sum(1 for r in R if r['n_odd_window_xor_empty'])))
        print('  |D_b| distribution:', sorted(Counter(d for r in R for d in r['D_sizes']).items())[:12], '; L:', dict(Counter(r['L'] for r in R)))
