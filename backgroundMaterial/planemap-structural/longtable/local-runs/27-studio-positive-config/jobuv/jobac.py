#!/usr/bin/env python3
"""Job AC. Part 1: every Job Z Lemma S failure Gamma-cycle -> (sigma u sigma')-group accounting. Part 2: (5,5,5,5,7) Gamma-cycles: R-type / k / exit sequences.
Independent Python (kempe_py + escape.pi_of). sigma' = link-free swaps from DD endpoints whose image is not DL (lock-breaking)."""
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
def part1(args):
    lab, name, hole, gid_hint = args
    H = Hole(name, hole, lab.endswith('m')); lmask = 0
    for i in H.sp.linki: lmask |= 1 << i
    links = defaultdict(set); exits = {}   # exits: image state -> (source state, source cycle, credit, via)
    sigp_rows = defaultdict(list)
    for k in range(H.S):
        if not H.isDDend(k): continue
        s = H.sigma(k)
        if H.cyc[s] != H.cyc[k]: links[H.cyc[k]].add(H.cyc[s]); links[H.cyc[s]].add(H.cyc[k])
        if H.W[H.cyc[k]] > 0 and H.cyc[s] != H.cyc[k] and imgkind(H, s) == 'lockless': exits.setdefault(s, (k, H.cyc[k], 3 * H.f_after(s) - 1, 'sigma'))
        for t, p, q, K in H.sp.moves(k):
            if t == k or K & lmask or H.DL[t]: continue
            if H.cyc[t] != H.cyc[k]: links[H.cyc[k]].add(H.cyc[t]); links[H.cyc[t]].add(H.cyc[k])
            if H.W[H.cyc[k]] > 0:
                ik = imgkind(H, t); cr = 3 * H.f_after(t) - 1 if ik == 'lockless' else 0
                sigp_rows[H.cyc[k]].append((k, (p, q), bin(K).count('1'), H.cyc[t], H.W[H.cyc[t]], len(H.cycles[H.cyc[t]]), ik, cr))
                if ik == 'lockless' and H.cyc[t] != H.cyc[k]: exits.setdefault(t, (k, H.cyc[k], cr, 'sigmap'))
    gam = [c for c, z in enumerate(H.cycles) if all(H.DL[x] for x in z)]
    # group of each Gamma-cycle
    seen = {}; out = []
    for g0 in gam:
        comp = {g0}; st = [g0]
        while st:
            u = st.pop()
            for v in links[u]:
                if v not in comp: comp.add(v); st.append(v)
        D = 5 * H.W[g0]
        crs = sum(cr for s, (k, c, cr, via) in exits.items() if c == g0 and via == 'sigma' and H.W[H.cyc[s]] <= 0)
        crp = sum(cr for s, (k, c, cr, via) in exits.items() if c == g0 and via == 'sigmap' and H.W[H.cyc[s]] <= 0)
        # charge-back P1 on the group with exits (sigma and sigma' lockless, distinct images)
        hit = defaultdict(int); src = defaultdict(lambda: defaultdict(int)); crN = defaultdict(int)
        for s, (k, c, cr, via) in exits.items():
            T = H.cyc[s]
            if T in comp and H.W[T] <= 0: hit[T] += 1 - (cr + 1); src[T][c] += cr; crN[c] += cr   # excursion mass 1 - 3f = -(cr)
        rem = {T: 5 * H.W[T] + sum(src[T].values()) for T in comp if H.W[T] <= 0}
        charge = defaultdict(Fraction)
        for T, r in rem.items():
            if r > 0 and src[T]:
                tot = sum(src[T].values())
                for c, cr in src[T].items(): charge[c] += Fraction(r * cr, tot)
        defs = [(c, 5 * H.W[c] - crN[c] + charge[c], [t for t in links[c] if t in rem and rem[t] < 0]) for c in comp if H.W[c] > 0]
        defs = [d for d in defs if d[1] > 0]; cap = {t: Fraction(-r) for t, r in rem.items() if r < 0}
        used = defaultdict(Fraction)
        def bt(i):
            if i == len(defs): return True
            z, d, nb = defs[i]
            for t in sorted(nb, key=lambda t: -(cap[t] - used[t])):
                if cap[t] - used[t] >= d:
                    used[t] += d
                    if bt(i + 1): return True
                    used[t] -= d
            return False
        p1 = bt(0)
        out.append(dict(run=lab, name=name, hole=hole, pattern=','.join(map(str, canon([len(H.rot[x]) for x in H.L]))), gamma=g0, L=len(H.cycles[g0]), D=D, CrN_sigma=crs, CrN_sigmap=crp,
                        deficit_after_sigma=D - crs, covered_by_sigmap=crp >= D - crs, group_ncycles=len(comp), group_sum_lambda=5 * sum(H.W[c] for c in comp),
                        group_positive=[(c, H.W[c]) for c in comp if H.W[c] > 0], P1_chargeback=p1, unassigned=[(c, str(d)) for c, d, nb in defs] if not p1 else [],
                        sigmap_links=sigp_rows[g0][:40]))
    return out
def part2(args):
    lab, name, hole = args
    H = Hole(name, hole, lab.endswith('m')); res = []
    for c, z in enumerate(H.cycles):
        if not all(H.DL[x] for x in z): continue
        seq = []
        for x in z:
            j, ty, hi, roles = H.frame(x); s = H.sigma(x); ik = imgkind(H, s) if ty == 3 else '-'
            if ik == 'DL' and s == x: ik = 'fixed'
            kk = next((i for i in range(5) if len(H.rot[H.L[(j + i) % 5]]) >= 7), None)
            seq.append(('R%d' % ty, kk, ik, H.f_after(s) if ik == 'lockless' else None))
        res.append(dict(run=lab, name=name, hole=hole, L=len(z), seq=seq))
    return res
if __name__ == '__main__':
    fails = []; g57 = set()
    for lab in ['z25', 'z25m', 'z26', 'z26m', 'z27', 'z27m']:
        for l in open('../out/%s.jsonl' % lab):
            if '"jobs": {"pos": [{' not in l: continue
            r = json.loads(l); pat = canon(r['linkdeg'])
            for z in r['jobs']['pos']:
                if z['gamma'] and z['CrN'] < z['Lambda']: fails.append((lab, r['name'], r['hole'], z['id']))
                if z['gamma'] and pat == (5, 5, 5, 5, 7): g57.add((lab, r['name'], r['hole']))
    fails = sorted(set(fails)); print('Lemma S failure Gamma records:', len(fails), '; (5,5,5,5,7) Gamma holes:', len(g57), flush=True)
    with Pool(12) as P:
        r1 = [x for xs in P.map(part1, sorted({(a, b, c, None) for a, b, c, d in fails})) for x in xs]
        r2 = [x for xs in P.map(part2, sorted(g57)) for x in xs]
    fk = {(a, b, c, d) for a, b, c, d in fails}
    r1 = [x for x in r1 if (x['run'], x['name'], x['hole'], x['gamma']) in fk or x['D'] > x['CrN_sigma']]
    json.dump(dict(part1=r1, part2=r2), open('jobac.json', 'w'))
    print('\nPART 1: failing Gamma-cycles (deficit after sigma exits from all DD endpoints):')
    for x in r1:
        print('  %s %s h%d %s Gamma %d L %d: D %d, sigma CrN %d, sigma\' lockless CrN %d -> covered by sigma\': %s; (sigma u sigma\')-group %d cycles, sum lambda %d; charge-back P1 on the group: %s %s'
              % (x['run'], x['name'], x['hole'], x['pattern'], x['gamma'], x['L'], x['D'], x['CrN_sigma'], x['CrN_sigmap'], x['covered_by_sigmap'], x['group_ncycles'], x['group_sum_lambda'], x['P1_chargeback'], x['unassigned']))
    print('\nPART 2: (5,5,5,5,7) Gamma-cycles: %d' % len(r2))
    pats = Counter(); kex = Counter()
    for x in r2:
        seq = x['seq']; L = len(seq)
        # period: start at an R3 state with the degree-7 vertex at k = 4 if any
        try: s0 = next(i for i, e in enumerate(seq) if e[0] == 'R3' and e[1] == 4)
        except StopIteration: s0 = 0
        sq = seq[s0:] + seq[:s0]
        pats[tuple((e[0], e[1]) for e in sq[:10])] += 1
        for e in seq:
            if e[0] == 'R3': kex[(e[1], e[2], e[3])] += 1
    print('  10-step (type, k of the degree-7 vertex) patterns from R3@k4:'); [print('    ', v, k) for k, v in pats.most_common(6)]
    print('  R3 exits by (k, kind, f):', sorted(kex.items(), key=str))
