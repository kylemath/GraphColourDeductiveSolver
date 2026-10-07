#!/usr/bin/env python3
"""Job AM (NightA34 §6). Independent Python. Names relative to p = x_q: z = w_q, w2 = w_{q+2}, y = w_{q-1}; hole vertices H11 = link + w's + p's middle outer neighbour(s).
G_J = the {c(y), c(z)}-graph of the state. Step component of a state = the component swapped by its pi-move (R+3 / phiB^-1 / phiA / tau, as escape.pi_of).
Periods start at R3k4 (pos 0). A step-8 break at period b = J true at pos 8, false at pos 9. With r4 = the R3k4 of period b+1:
Z_b = G_J-component of z at r4 - 1 (R1k2^b); Pi_b = step component of r4 - 1; K0, K1 = step components of r4, r4 + 1; R_b = vertices of K0 u K1 adjacent to Z_b;
Sigma = (K0 u K1 of period b+2, i.e. of r4 + 10, r4 + 11) meets (R_b u Z_b) minus H11."""
import json, sys
from collections import Counter, defaultdict
from multiprocessing import Pool
from uv_lib import Hole
from jobag import canon
def comp(H, k, v, a, b):
    s = H.sp.states[k]; i = H.sp.idx[v]
    return next((set(H.sp.mask_vertices(K)) for K in H.sp.components(s, a, b) if K >> i & 1), set())
def stepK(H, k):
    s = H.sp.states[k]; li = H.L; c = H.linkc(k); cnt = Counter(c)
    if len(cnt) == 4:
        j = next(j for j in range(5) if c[j] == c[(j + 2) % 5] and cnt[c[j]] == 2); al, mu, A, B = c[j], c[(j + 1) % 5], c[(j + 3) % 5], c[(j + 4) % 5]
        if B in [H.col(k, v) for v in comp(H, k, li[(j + 1) % 5], mu, B) if v == li[(j + 4) % 5]] or li[(j + 4) % 5] in comp(H, k, li[(j + 1) % 5], mu, B):
            return comp(H, k, li[(j + 2) % 5], al, A)
        return comp(H, k, li[(j + 4) % 5], mu, B)
    i = next(i for i in range(5) if cnt[c[i]] == 1); W, X, Y = c[i], c[(i + 1) % 5], c[(i + 2) % 5]; Z = ({0, 1, 2, 3} - {W, X, Y}).pop()
    K = comp(H, k, li[(i + 2) % 5], Y, Z)
    if li[(i + 4) % 5] not in K: return K
    return comp(H, k, li[(i + 3) % 5], W, X)
def setup(H):
    t6 = next(t for t in range(5) if len(H.rot[H.L[t]]) >= 6); p = H.L[t6]; y = H.w[(t6 + 4) % 5]; z = H.w[t6]; w2 = H.w[(t6 + 2) % 5]
    M = [w for w in H.rot[p] if w != H.h and w not in (H.L[(t6 + 1) % 5], H.L[(t6 + 4) % 5], y, z)]
    return t6, p, y, z, w2, M, set(H.L) | set(H.w) | set(M)
def partition(H, k, y, w2, z):
    a, b = H.col(k, y), H.col(k, z); G = comp(H, k, y, a, b); Gz = comp(H, k, z, a, b)
    yw = w2 in G; zw = w2 in Gz; yz = z in G
    if yz and yw: return 'y w2 z'
    if yw: return 'y w2 | z'
    if zw: return 'y | w2 z'
    return 'y | w2 | z'
def sigma_at(H, zc, r4, y, z, H11):
    n = len(zc); g = lambda t: zc[t % n]
    x9 = g(r4 - 1); Zb = comp(H, x9, z, H.col(x9, y), H.col(x9, z)); Pi = stepK(H, x9)
    K0, K1 = stepK(H, g(r4)), stepK(H, g(r4 + 1)); Rb = {v for v in K0 | K1 if any(w in Zb for w in H.rot[v])}
    K0n, K1n = stepK(H, g(r4 + 10)), stepK(H, g(r4 + 11)); target = (Rb | Zb) - H11
    return dict(Z=len(Zb), Zfar=len(Zb - H11), Pi=len(Pi), K0=len(K0), K1=len(K1), R=len(Rb), Rfar=len(Rb - H11), sigma=bool((K0n | K1n) & target),
                sets=dict(Z=sorted(Zb), Pi=sorted(Pi), K0=sorted(K0), K1=sorted(K1), R=sorted(Rb)))
def gamma_job(args):
    lab, name, hole = args
    H = Hole(name, hole, lab.endswith('m')); t6, p, y, z, w2, M, H11 = setup(H); out = dict(run=lab, name=name, hole=hole, deg=len(H.rot[p]), win=Counter(), breaks=[])
    for c, zc in enumerate(H.cycles):
        if not all(H.DL[x] for x in zc): continue
        n = len(zc); fr = [H.frame(x) for x in zc]
        s0 = next(i for i in range(n) if fr[i][1] == 3 and (t6 - fr[i][0]) % 5 == 4); zc = zc[s0:] + zc[:s0]
        for b in range(0, n, 10):
            for pos in (9, 0, 2, 3, 4):
                out['win'][(pos, partition(H, zc[(b + pos) % n], y, w2, z))] += 1
            x8, x9 = zc[(b + 8) % n], zc[(b + 9) % n]
            J8 = z in comp(H, x8, y, H.col(x8, y), H.col(x8, z)); J9 = z in comp(H, x9, y, H.col(x9, y), H.col(x9, z))
            if J8 and not J9:
                r4 = (b + 10) % n
                nxt = zc[(r4 + 8) % n], zc[(r4 + 9) % n]
                dbl = (z in comp(H, nxt[0], y, H.col(nxt[0], y), H.col(nxt[0], z))) and not (z in comp(H, nxt[1], y, H.col(nxt[1], y), H.col(nxt[1], z)))
                out['breaks'].append(dict(cycle=c, period=b // 10, double=dbl, **sigma_at(H, zc, r4, y, z, H11)))
    return out
def open_job(case):
    lab, name, hole, e = case
    H = Hole(name, hole, lab.endswith('m')); t6, p, y, z, w2, M, H11 = setup(H); zc = H.cycles[e['cycle']]; Lz = len(zc)
    for i in range(Lz):
        if not H.DL[zc[i]] or H.DL[zc[i - 1]]: continue
        rr = []; t = i
        while H.DL[zc[t % Lz]]: rr.append(t); t += 1
        if len(rr) != e['run_len']: continue
        r4 = rr[e['first_fail_pos']]   # R3k4 of period b+1 (first failing visit) as an absolute cycle index
        win = Counter()
        for q in range(-1, 5):
            st = zc[(r4 + q) % Lz]
            if H.DL[st]: win[((q) % 10, partition(H, st, y, w2, z))] += 1
        rec = sigma_at(H, zc, r4, y, z, H11)
        return dict(run=lab, name=name, hole=hole, run_len=e['run_len'], win=win, **rec)
    return None
if __name__ == '__main__':
    holes = set()
    for lab in ['z25', 'z25m', 'z26', 'z26m', 'z27', 'z27m']:
        for l in open('../out/%s.jsonl' % lab):
            if '"jobs": {"pos": [{' not in l: continue
            r = json.loads(l)
            if canon(r['linkdeg']) in ((5, 5, 5, 5, 6), (5, 5, 5, 5, 7)) and any(zz['gamma'] for zz in r['jobs']['pos']): holes.add((lab, r['name'], r['hole']))
    cases = []
    for lab in ['x25', 'x25m', 'x26', 'x26m', 'x27', 'x27m']:
        for l in open('../out/%s.jsonl' % lab):
            if '"events": [{' not in l: continue
            r = json.loads(l)
            for e in r['jobx']['events']: cases.append((lab, r['name'], r['hole'], e))
    with Pool(12) as P:
        G = P.map(gamma_job, sorted(holes)); O = [x for x in P.map(open_job, cases) if x]
    json.dump(dict(gamma=[dict(g, win={'%s|%s' % k: v for k, v in g['win'].items()}) for g in G], open=[dict(o, win={'%s|%s' % k: v for k, v in o['win'].items()}) for o in O]), open('jobam.json', 'w'))
    for deg in (6, 7):
        W = Counter(); B = [b for g in G if g['deg'] == deg for b in g['breaks']]
        for g in G:
            if g['deg'] == deg: W.update(g['win'])
        print('\n=== Gamma-cycles, degree %d' % deg)
        print('(2) window partitions of {y, w2, z} in G_J at DL states (pos, partition):'); [print('     ', k, v) for k, v in sorted(W.items())]
        sb = [b for b in B if not b['double']]; db = [b for b in B if b['double']]
        print('(3)/(4) step-8 breaks %d: single %d, Sigma true %d; double (break at b and b+1) %d, Sigma true %d' % (len(B), len(sb), sum(b['sigma'] for b in sb), len(db), sum(b['sigma'] for b in db)))
        for k in ('Z', 'Zfar', 'Pi', 'K0', 'K1', 'R', 'Rfar'):
            v = [b[k] for b in B]; print('     |%s| mean %.2f min %d max %d' % (k, sum(v) / max(1, len(v)), min(v) if v else -1, max(v) if v else -1))
    print('\n=== the %d open double breaks (Job X / AA)' % len(O))
    W = Counter()
    for o in O: W.update(o['win'])
    print('(2) window partitions at DL states (pos, partition):'); [print('     ', k, v) for k, v in sorted(W.items())]
    print('(3) Sigma true: %d / %d' % (sum(o['sigma'] for o in O), len(O)))
    for k in ('Z', 'Zfar', 'Pi', 'K0', 'K1', 'R', 'Rfar'):
        v = [o[k] for o in O]; print('     |%s| mean %.2f min %d max %d' % (k, sum(v) / max(1, len(v)), min(v), max(v)))
