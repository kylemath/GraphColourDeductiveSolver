#!/usr/bin/env python3
"""Job AE (NightLemmaS §5.1 lock-membership form), Gamma-cycles at (5,5,5,5,6) and (5,5,5,5,7), orders 25-27, both orientations. Independent Python.
p = the high-degree link vertex, y, z = its flanking outer neighbours, M = its other outer neighbours (1 at degree 6, 2 at degree 7). Frame per state: m1 = x_{j+1};
Lock1 component = {mu,A}-component of m1, Lock2 component = {mu,B}-component of m1. J = (y ~ z in {c(y),c(z)}). Periods start at R3 with p at k = 4."""
import json
from collections import Counter, defaultdict
from multiprocessing import Pool
from uv_lib import Hole
def canon(ld, cap=8):
    d = [min(x, cap) for x in ld]; return min(tuple(s[r:] + s[:r]) for s in (d, d[::-1]) for r in range(5))
def comp_of(H, k, v, a, b):
    s = H.sp.states[k]; i = H.sp.idx[v]
    for K in H.sp.components(s, a, b):
        if K >> i & 1: return set(H.sp.mask_vertices(K))
    return set()
def analyse(args):
    lab, name, hole = args
    H = Hole(name, hole, lab.endswith('m')); out = []
    t6 = next(t for t in range(5) if len(H.rot[H.L[t]]) >= 6); p = H.L[t6]; y = H.w[(t6 + 4) % 5]; z = H.w[t6]
    M = [w for w in H.rot[p] if w != hole and w not in (H.L[(t6 + 1) % 5], H.L[(t6 + 4) % 5], y, z)]
    for c, zc in enumerate(H.cycles):
        if not all(H.DL[x] for x in zc): continue
        rows = []
        for x in zc:
            j, ty, hi, (al, mu, A, B) = H.frame(x); m1 = H.L[(j + 1) % 5]; x4 = H.L[(j + 4) % 5]
            L1 = comp_of(H, x, m1, mu, A); L2 = comp_of(H, x, m1, mu, B)
            cy, cz = H.col(x, y), H.col(x, z); J = z in comp_of(H, x, y, cy, cz)
            Kyz = len(comp_of(H, x, y, cy, cz))
            xj2 = H.L[(j + 2) % 5]; Kstep = comp_of(H, x, xj2, al, A)   # the R+3 swap component of this state
            s = H.sigma(x); lk = H.locks(s); ex = '-' if ty != 3 else ('lockless' if (not H.filled(s) and not lk[0] and not lk[1]) else 'fail')
            rows.append(dict(L1set=L1, L2set=L2, ty=ty, k=(t6 - j) % 5, J=J, Kyz=Kyz, L1=len(L1), L2=len(L2), L2has={v: (vv in L2) for v, vv in (('y', y), ('x4', x4), ('z', z), ('p', p))} | {'M': any(v in L2 for v in M)},
                             L1has={v: (vv in L1) for v, vv in (('y', y), ('z', z), ('p', p))} | {'M': any(v in L1 for v in M)}, Kstep=Kstep, ex=ex,
                             pair=''.join(nm for nm, vv in (('p', p), ('y', y), ('z', z)) if H.col(x, vv) in (al, A)) + ('M' if any(H.col(x, v) in (al, A) for v in M) else ''),
                             compin=''.join(nm for nm, vv in (('p', p), ('y', y), ('z', z)) if vv in Kstep) + ('M' if any(v in Kstep for v in M) else '')))
        s0 = next(i for i, r in enumerate(rows) if r['ty'] == 3 and r['k'] == 4); rows = rows[s0:] + rows[:s0]
        n = len(rows); brk = []
        for bb in range(0, n, 10):
            per = [rows[(bb + t) % n] for t in range(10)]
            if per[8]['J'] and not per[9]['J']:
                K8 = per[8]['Kstep']; nxt = [rows[(bb + 9 + t) % n] for t in range(11)]
                brk.append(dict(start=bb, L2meetsK=[len(r['L2set'] & K8) > 0 for r in nxt], L1meetsK=[len(r['L1set'] & K8) > 0 for r in nxt],
                                zinL2=[r['L2has']['z'] for r in nxt], J=[r['J'] for r in nxt], types=['R%dk%d' % (r['ty'], r['k']) for r in nxt]))
        out.append(dict(run=lab, name=name, hole=hole, deg=len(H.rot[p]), L=n, breaks=brk,
                        rows=[{k: v for k, v in r.items() if k not in ('Kstep', 'L1set', 'L2set')} | {'Ksize': len(r['Kstep'])} for r in rows]))
    return out
if __name__ == '__main__':
    holes = set()
    for lab in ['z25', 'z25m', 'z26', 'z26m', 'z27', 'z27m']:
        for l in open('../out/%s.jsonl' % lab):
            if '"jobs": {"pos": [{' not in l: continue
            r = json.loads(l)
            if canon(r['linkdeg']) in ((5, 5, 5, 5, 6), (5, 5, 5, 5, 7)) and any(z['gamma'] for z in r['jobs']['pos']): holes.add((lab, r['name'], r['hole']))
    print('holes', len(holes), flush=True)
    with Pool(12) as P: res = [x for xs in P.map(analyse, sorted(holes)) for x in xs]
    json.dump(res, open('jobae.json', 'w'))
    for deg in (6, 7):
        R = [x for x in res if x['deg'] == deg]; print('\n=== degree-%d high vertex: Gamma-cycle records %d' % (deg, len(R)))
        minL1 = min(r['L1'] for x in R for r in x['rows']); minL2 = min(r['L2'] for x in R for r in x['rows'])
        print('(iii) min Lock1-component size %d, min Lock2-component size %d over all Gamma states' % (minL1, minL2))
        pl = Counter(); i_ok = Counter(); brought = Counter(); fails = Counter(); mech = Counter(); Kcmp = defaultdict(list)
        for x in R:
            rows = x['rows']; n = len(rows)
            for b in range(0, n, 10):
                per = rows[b:b + 10]
                Kcmp['all periods: |K step8|'].append(per[8]['Ksize']); Kcmp['all periods: |K_yz(y)| at R3k0'].append(per[8]['Kyz'])
                if not per[8]['J'] or per[9]['J']: pass
                # break at step 8: J at R3k0 (pos 8) true and at R1k2 (pos 9) false
                if per[8]['J'] and not per[9]['J']:
                    Kcmp['break periods: |K step8|'].append(per[8]['Ksize']); Kcmp['break periods: |K_yz(y)| at R3k0'].append(per[8]['Kyz'])
                    mech[(per[8]['pair'], per[8]['compin'] or '-')] += 1
                    nxt = [rows[(b + 9 + t) % n] for t in range(11)]   # R1k2 (break) ... R1k2 one period later
                    i_ok[nxt[10]['L2has']['z']] += 1
                    for t in range(1, 11):
                        if nxt[t]['L2has']['z'] and not nxt[t - 1]['L2has']['z']: brought[(t, rows[(b + 9 + t - 1) % n]['pair'], rows[(b + 9 + t - 1) % n]['compin'] or '-')] += 1; break
            for r in rows:
                if r['ty'] == 3 and r['k'] in (3, 4) and r['ex'] == 'fail': fails[r['k']] += 1
        print('(i) at the R1k2 one period after a step-8 break, z in the Lock2-component of x_{j+1}:', dict(i_ok))
        print('    step (states after the break) and swap (pair, component contents) that brought z into the Lock2-component:', sorted(brought.items()))
        print('(ii) k = 3/4 failures:', dict(fails), '; step-8 break mechanism (pair, component contents):', dict(mech))
        for k, v in Kcmp.items(): print('    %-36s n %5d mean %.2f min %d max %d' % (k, len(v), sum(v) / max(1, len(v)), min(v) if v else -1, max(v) if v else -1))

    print('\n=== lock components vs the step-8 breaking component K (vertex sets), states R1k2(break) .. R1k2 one period later:')
    for deg in (6, 7):
        B = [b | {'id': (x['run'], x['name'], x['hole'])} for x in res if x['deg'] == deg for b in x['breaks']]
        m2 = [sum(b['L2meetsK'][t] for b in B) for t in range(11)]; m1 = [sum(b['L1meetsK'][t] for b in B) for t in range(11)]
        print('  degree %d: %d breaks; per state (0..10) #Lock2 comp meets K: %s; #Lock1 comp meets K: %s' % (deg, len(B), m2, m1))
        bad = [b for b in B if not b['zinL2'][10]]
        for b in bad[:6]: print('    z NOT in Lock2 at R1k2+10:', b['id'], 'J', ''.join('1' if v else '0' for v in b['J']), 'zinL2', ''.join('1' if v else '0' for v in b['zinL2']), b['types'])
