#!/usr/bin/env python3
"""Job AP (NightA34 §7.4). Independent Python, extending jobam.py. p = x_q, x+ = x_{q+1}, z = w_q, y = w_{q-1}; H11 = hole vertices; r4 = R3k4 of period b+1.
Gate set R_b = vertices of K0 u K1 (step components at r4, r4+1) adjacent to Z_b (G_J-component of z at r4-1). Q_b = z's G_J-component at R3k3^{b+1} (r4+2)."""
import json
from collections import Counter, defaultdict
from multiprocessing import Pool
from uv_lib import Hole
from jobag import canon
from jobam import comp, stepK, setup
def role(H, x, v):
    if H.filled(x): return 'filled'
    j, ty, hi, (al, mu, A, B) = H.frame(x); c = H.col(x, v)
    return {al: 'alpha', mu: 'mu', A: 'A', B: 'B'}[c]
def Jcomp(H, x, y, z, start):
    return comp(H, x, start, H.col(x, y), H.col(x, z))
def gates(H, zc, r4, y, z, H11):
    n = len(zc); g = lambda t: zc[t % n]
    Zb = Jcomp(H, g(r4 - 1), y, z, z); K0, K1 = stepK(H, g(r4)), stepK(H, g(r4 + 1))
    R = {v for v in K0 | K1 if any(w in Zb for w in H.rot[v])}
    return Zb, K0, K1, R
def analyse_break(H, zc, r4, y, z, xplus, H11):
    n = len(zc); g = lambda t: zc[t % n]
    Zb, K0, K1, R = gates(H, zc, r4, y, z, H11); far = sorted(R - H11)
    Qb = Jcomp(H, g(r4 + 2), y, z, z) if not H.filled(g(r4 + 2)) else set()
    rec = dict(near_ok=(R & H11) == {xplus}, near=sorted(R & H11), R=len(R), far=far,
               gate_info=[dict(role=role(H, g(r4), r), inK0=r in K0, inK1=r in K1, adj_z=z in H.rot[r], inQ=r in Qb) for r in far])
    return rec, Zb, K0, K1, R, Qb
def double_info(H, zc, r4, y, z, xplus, H11):
    n = len(zc); g = lambda t: zc[t % n]
    a, Zb, K0, K1, R, Qb = analyse_break(H, zc, r4, y, z, xplus, H11)
    b, Zb1, K01, K11, R1, Qb1 = analyse_break(H, zc, r4 + 10, y, z, xplus, H11)
    reaches = H.DL[g(r4 + 12)] and all(H.DL[g(r4 + t)] for t in range(0, 13))
    fb, fb1 = set(a['far']), set(b['far'])
    K8 = stepK(H, g(r4 + 8)); Pi1 = stepK(H, g(r4 + 9)); K0b2 = stepK(H, g(r4 + 10))
    hist = {}
    for r in fb:
        hist[r] = [(role(H, g(r4 + t), r), [s for s in range(10) if r in stepK(H, g(r4 + t)) and s == t]) for t in range(11)]
    branch1 = len(fb1) >= 2; branch2 = len(fb) == 1 and fb == fb1 and bool(K0b2 & (Qb - H11))
    return dict(first=a, second=b, reaches_R3k3_b2=reaches, rb_in_R1=bool(fb & R1), rb_in_K8=bool(fb & K8), rb_in_Pi1=bool(fb & Pi1), rb_in_Z1=bool(fb & Zb1),
                G2_branch1=branch1, G2_branch2=branch2, G2_neither=not (branch1 or branch2),
                rb_role_history={str(r): [h[0] for h in hh] for r, hh in hist.items()})
def gamma_job(args):
    lab, name, hole = args
    H = Hole(name, hole, lab.endswith('m')); t6, p, y, z, w2, M, H11 = setup(H); xplus = H.L[(t6 + 1) % 5]; out = []
    for c, zc in enumerate(H.cycles):
        if not all(H.DL[x] for x in zc): continue
        n = len(zc); fr = [H.frame(x) for x in zc]
        s0 = next(i for i in range(n) if fr[i][1] == 3 and (t6 - fr[i][0]) % 5 == 4); zc = zc[s0:] + zc[:s0]
        brk = []
        for b in range(0, n, 10):
            x8, x9 = zc[(b + 8) % n], zc[(b + 9) % n]
            if z in Jcomp(H, x8, y, z, y) and z not in Jcomp(H, x9, y, z, y): brk.append(b)
        for b in brk:
            r4 = (b + 10) % n; dbl = ((b + 10) % n) in brk
            rec, *_ = analyse_break(H, zc, r4, y, z, xplus, H11)
            rec.update(run=lab, name=name, hole=hole, deg=len(H.rot[p]), double=dbl)
            if dbl: rec['double_info'] = double_info(H, zc, r4, y, z, xplus, H11)
            else:   # control: r_b colour role history over the next 10 states, alpha again at R3k4^{b+2}?
                rec['control'] = {str(r): [role(H, zc[(r4 + t) % n], r) for t in range(11)] for r in rec['far']}
            out.append(rec)
    return out
def open_job(case):
    lab, name, hole, e = case
    H = Hole(name, hole, lab.endswith('m')); t6, p, y, z, w2, M, H11 = setup(H); xplus = H.L[(t6 + 1) % 5]; zc = H.cycles[e['cycle']]; Lz = len(zc)
    for i in range(Lz):
        if not H.DL[zc[i]] or H.DL[zc[i - 1]]: continue
        rr = []; t = i
        while H.DL[zc[t % Lz]]: rr.append(t); t += 1
        if len(rr) != e['run_len']: continue
        r4 = rr[e['first_fail_pos']]
        d = double_info(H, zc, r4, y, z, xplus, H11); d.update(run=lab, name=name, hole=hole, deg=len(H.rot[p])); return d
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
        G = [x for xs in P.map(gamma_job, sorted(holes)) for x in xs]; O = [x for x in P.map(open_job, cases) if x]
    json.dump(dict(gamma=G, open=O), open('jobap.json', 'w'))
    for deg in (6, 7):
        B = [b for b in G if b['deg'] == deg]
        print('\n=== Gamma-cycles degree %d: breaks %d (double %d)' % (deg, len(B), sum(b['double'] for b in B)))
        print('(1) R_b & H11 = {x+}: %d / %d; near sets seen: %s' % (sum(b['near_ok'] for b in B), len(B), Counter(len(b['near']) for b in B)))
        gi = Counter((g['role'], 'K0' if g['inK0'] else '', 'K1' if g['inK1'] else '', 'adj z' if g['adj_z'] else 'not adj z', 'in Q' if g['inQ'] else 'NOT in Q') for b in B for g in b['gate_info'])
        print('(2) far gates (role at R3k4^{b+1}, K0, K1, adjacent to z, in Q_b):', gi.most_common(8)); print('    |R_b| distribution:', sorted(Counter(b['R'] for b in B).items()))
        D = [b['double_info'] for b in B if b['double']]
        if D:
            print('(3)/(4) double breaks %d: reach R3k3^{b+2} %d; G2 branch1 %d, branch2 %d, neither %d; r_b in R_{b+1} %d, in K8 %d, in Pi_{b+1} %d, in Z_{b+1} %d' % (len(D), sum(d['reaches_R3k3_b2'] for d in D),
                  sum(d['G2_branch1'] for d in D), sum(d['G2_branch2'] for d in D), sum(d['G2_neither'] for d in D), sum(d['rb_in_R1'] for d in D), sum(d['rb_in_K8'] for d in D), sum(d['rb_in_Pi1'] for d in D), sum(d['rb_in_Z1'] for d in D)))
        ctl = [hh for b in B if not b['double'] for hh in b.get('control', {}).values()]
        if ctl: print('(5) control (single breaks): far-gate role at R3k4^{b+2}:', dict(Counter(h[10] for h in ctl)), '; role at R3k4^{b+1}:', dict(Counter(h[0] for h in ctl)))
    print('\n=== the %d open double breaks' % len(O))
    for deg in (6,):
        D = [d for d in O if d['deg'] == deg]
        print('(1) first break R & H11 = {x+}: %d / %d; second: %d / %d' % (sum(d['first']['near_ok'] for d in D), len(D), sum(d['second']['near_ok'] for d in D), len(D)))
        print('    |R_b|, |R_{b+1}| pairs:', sorted(Counter((d['first']['R'], d['second']['R']) for d in D).items()))
        rch = [d for d in D if d['reaches_R3k3_b2']]
        print('(3) reach R3k3^{b+2}: %d; G2 branch1 %d, branch2 %d, neither %d' % (len(rch), sum(d['G2_branch1'] for d in rch), sum(d['G2_branch2'] for d in rch), sum(d['G2_neither'] for d in rch)))
        print('(4) reach R3k3^{b+2} with |R_b| = |R_{b+1}| = 2: %d %s' % (sum(1 for d in rch if d['first']['R'] == 2 and d['second']['R'] == 2), [(d['run'], d['name'], d['hole']) for d in rch if d['first']['R'] == 2 and d['second']['R'] == 2][:5]))
        print('    all open double breaks: r_b in R_{b+1} %d, in K8 %d, in Pi_{b+1} %d, in Z_{b+1} %d' % (sum(d['rb_in_R1'] for d in D), sum(d['rb_in_K8'] for d in D), sum(d['rb_in_Pi1'] for d in D), sum(d['rb_in_Z1'] for d in D)))
        gi = Counter((g['role'], 'K0' if g['inK0'] else '', 'K1' if g['inK1'] else '', 'adj z' if g['adj_z'] else 'not adj z', 'in Q' if g['inQ'] else 'NOT in Q') for d in D for g in d['first']['gate_info'])
        print('(2) far gates of the first break:', gi.most_common(6))
