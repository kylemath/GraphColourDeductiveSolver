#!/usr/bin/env python3
"""Job AF (NightP1 §6 Studio requests + item 4). Independent Python (kempe_py + escape.pi_of).
Exits: lockless images (on another cycle) of sigma (and, where stated, sigma') applied at DD endpoints of positive cycles, all R-types; credit 3f - 1.
rem(T) = Lambda(T) + sum of credits into T (T nonpositive). Charge-back: rem(T) > 0 is charged to T's sources in proportion to credit; def'(Z) = Lambda(Z) - CrN(Z) + charge.
P1: each def' > 0 assigned to ONE neighbour T with rem(T) < 0, capacity -rem(T) (exact search). Neighbours: UNDIRECTED links from DD endpoints of any cycle.
P1^str: the same with demand Lambda(Z) for every positive Z. Star(g): the most negative cycle M of each sigma-group g with a positive cycle is sigma-adjacent to all
positive cycles of g and -Lambda(M) (Star) / -rem(M) (Star_rem) >= sum of Lambda over the positive cycles of g."""
import json, sys
from fractions import Fraction
from collections import defaultdict, Counter
from multiprocessing import Pool
from uv_lib import Hole
def canon(ld, cap=8):
    d = [min(x, cap) for x in ld]; return min(tuple(s[r:] + s[:r]) for s in (d, d[::-1]) for r in range(5))
def imgkind(H, s):
    if H.filled(s): return 'filled'
    lk = H.locks(s); return 'lockless' if not lk[0] and not lk[1] else ('DL' if lk[0] and lk[1] else ('Lock1' if lk[0] else 'Lock2'))
def assign(defs, cap):
    order = sorted(defs, key=lambda z: (-z[1], len(z[2]))); used = defaultdict(Fraction)
    def bt(i):
        if i == len(order): return True
        z, d, nb = order[i]
        for t in sorted(nb, key=lambda t: -(cap.get(t, 0) - used[t])):
            if cap.get(t, 0) - used[t] >= d:
                used[t] += d
                if bt(i + 1): return True
                used[t] -= d
        return False
    return bt(0)
def build(H, with_sigmap):
    lmask = 0
    for i in H.sp.linki: lmask |= 1 << i
    sig = defaultdict(set); sigp = defaultdict(set); exits = {}
    for k in range(H.S):
        if not H.isDDend(k): continue
        c = H.cyc[k]; s = H.sigma(k)
        if H.cyc[s] != c:
            sig[c].add(H.cyc[s]); sig[H.cyc[s]].add(c)
            if H.W[c] > 0 and imgkind(H, s) == 'lockless': exits.setdefault(s, (c, 3 * H.f_after(s) - 1, 'sigma'))
        if with_sigmap:
            for t, p, q, K in H.sp.moves(k):
                if t == k or K & lmask or H.DL[t] or H.cyc[t] == c: continue
                sigp[c].add(H.cyc[t]); sigp[H.cyc[t]].add(c)
                if H.W[c] > 0 and imgkind(H, t) == 'lockless': exits.setdefault(t, (c, 3 * H.f_after(t) - 1, 'sigmap'))
    return sig, sigp, exits
def p1_tests(H, sig, nbr, exits, use_sigmap_exits):
    pos = [c for c in range(len(H.cycles)) if H.W[c] > 0]
    src = defaultdict(lambda: defaultdict(int)); crN = defaultdict(int)
    for s, (c, cr, via) in exits.items():
        if not use_sigmap_exits and via == 'sigmap': continue
        T = H.cyc[s]
        if H.W[T] <= 0: src[T][c] += cr; crN[c] += cr
    rem = {T: 5 * H.W[T] + sum(src[T].values()) for T in range(len(H.cycles)) if H.W[T] <= 0}
    charge = defaultdict(Fraction)
    for T, r in rem.items():
        if r > 0 and src[T]:
            tot = sum(src[T].values())
            for c, cr in src[T].items(): charge[c] += Fraction(r * cr, tot)
    cap = {T: Fraction(-r) for T, r in rem.items() if r < 0}
    defs = [(z, 5 * H.W[z] - crN[z] + charge[z], [t for t in nbr[z] if t in cap]) for z in pos]
    p1 = assign([d for d in defs if d[1] > 0], cap)
    strd = [(z, Fraction(5 * H.W[z]), [t for t in nbr[z] if t in cap]) for z in pos]
    p1str = assign(strd, cap)
    strng = [(z, d, nb) for z, d, nb in strd if not all(H.DL[x] for x in H.cycles[z])]
    p1str_ng = assign(strng, cap)
    return p1, (p1str, p1str_ng), rem, defs
def stars(H, sig, rem):
    seen = {}; res = []
    for c0 in range(len(H.cycles)):
        if c0 in seen: continue
        comp = [c0]; seen[c0] = 1; st = [c0]
        while st:
            u = st.pop()
            for v in sig[u]:
                if v not in seen: seen[v] = 1; comp.append(v); st.append(v)
        P = [c for c in comp if H.W[c] > 0]
        if not P: continue
        M = min(comp, key=lambda c: H.W[c]); sup = 5 * sum(H.W[c] for c in P)
        adj = all(M in sig[z] for z in P); big = -5 * H.W[M] >= sup; bigr = -rem.get(M, 5 * H.W[M]) >= sup
        res.append(dict(adj=adj, big=big, bigrem=bigr, star=adj and big, starrem=adj and bigr, ncyc=len(comp), npos=len(P), sup=sup, M=5 * H.W[M], remM=rem.get(M)))
    return res
def job_holes(args):
    lab, name, hole, mode = args
    H = Hole(name, hole, lab.endswith('m'))
    if mode == 'fail22':
        sig, sigp, ex = build(H, True)
        a, _, _, d1 = p1_tests(H, sig, sig, ex, False)
        nb = defaultdict(set)
        for c in set(sig) | set(sigp): nb[c] = sig[c] | sigp[c]
        b, _, _, d2 = p1_tests(H, sig, nb, ex, True)
        return dict(lab=lab, name=name, hole=hole, undirected_sigma_P1=a, sigma_sigmap_P1=b,
                    unassigned_sigma=[(z, str(d), nb) for z, d, nb in d1 if d > 0 and not a], pattern=','.join(map(str, canon([len(H.rot[x]) for x in H.L]))))
    sig, sigp, ex = build(H, False)
    a, (s, sng), rem, defs = p1_tests(H, sig, sig, ex, False)
    return dict(lab=lab, name=name, hole=hole, P1_undirected=a, P1str_undirected=s, P1str_nonGamma=sng, stars=stars(H, sig, rem),
                pos=[(z, 5 * H.W[z], len(H.cycles[z]), str(d)) for z, d, nb in defs])
if __name__ == '__main__':
    # (1) Job Z's 22 failing holes (charge-back P1 failures, all patterns) from jobz-p1fails.txt
    f22 = []
    for l in open('../jobz-p1fails.txt'):
        p = l.split()
        if p and p[0].startswith('z2'): f22.append((p[0], p[1], int(p[2]), 'fail22'))
    # (2) every hole with a positive cycle at (5,5,5,5,6)/(5,5,5,6,6), orders 25-27, both orientations
    h2 = set()
    for lab in ['z25', 'z25m', 'z26', 'z26m', 'z27', 'z27m']:
        for l in open('../out/%s.jsonl' % lab):
            if '"jobs": {"pos": [{' not in l: continue
            r = json.loads(l)
            if canon(r['linkdeg']) in ((5, 5, 5, 5, 6), (5, 5, 5, 6, 6)): h2.add((lab, r['name'], r['hole'], 'pat'))
    print('fail22 holes', len(f22), 'pattern holes', len(h2), flush=True)
    with Pool(12) as P:
        r1 = P.map(job_holes, f22); r2 = P.map(job_holes, sorted(h2))
    json.dump(dict(fail22=r1, patterns=r2), open('jobaf.json', 'w'))
    print('\n(1) Job Z failing holes:', len(r1))
    print('    undirected sigma-P1 holds: %d / %d; sigma u sigma\' P1 holds: %d / %d' % (sum(x['undirected_sigma_P1'] for x in r1), len(r1), sum(x['sigma_sigmap_P1'] for x in r1), len(r1)))
    for x in r1:
        if not x['undirected_sigma_P1'] or not x['sigma_sigmap_P1']: print('     ', x['lab'], x['name'], x['hole'], x['pattern'], 'undirected sigma:', x['undirected_sigma_P1'], 'sigma u sigma\':', x['sigma_sigmap_P1'], x['unassigned_sigma'][:3])
    print('\n(2) (5,5,5,5,6)/(5,5,5,6,6), orders 25-27, both orientations: holes', len(r2))
    print('    P1 (undirected sigma) holds %d / %d; P1^str (undirected, all positive cycles) holds %d / %d; P1^str on NON-Gamma positive cycles holds %d / %d' % (sum(x['P1_undirected'] for x in r2), len(r2), sum(x['P1str_undirected'] for x in r2), len(r2), sum(x['P1str_nonGamma'] for x in r2), len(r2)))
    for x in r2:
        if not x['P1str_nonGamma']: print('      P1^str (non-Gamma) fails:', x['lab'], x['name'], x['hole'], x['pos'][:4])
    for x in r2:
        if not x['P1str_undirected']: print('      P1^str fails:', x['lab'], x['name'], x['hole'], x['pos'][:4])
    S = [s for x in r2 for s in x['stars']]; C = Counter()
    for s in S:
        for k in ('adj', 'big', 'bigrem', 'star', 'starrem'): C[k] += s[k]
    print('    Star over %d sigma-groups with a positive cycle: (i) M adjacent to all positive %d; (ii) -Lambda(M) >= supply %d; with -rem(M) %d; Star %d; Star_rem %d' % (len(S), C['adj'], C['big'], C['bigrem'], C['star'], C['starrem']))
