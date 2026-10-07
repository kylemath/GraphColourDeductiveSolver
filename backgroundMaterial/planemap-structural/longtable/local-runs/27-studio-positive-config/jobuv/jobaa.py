#!/usr/bin/env python3
"""Job AA: for each double k = 4 failure on a maximal DL run at (5,5,5,5,6) (Job X events), trace from the second failing R3k4 to the run end.
At the leaving step (last DL state x -> pi x, which keeps Lock1 and loses Lock2): (type, k) of x and pi x, the swapped pair (as colours of p, m, y, z) and which of
p, m, y, z the swapped component contains, the Lock2 witness of x (the {mu,B}-component of m containing b), and whether the step-8 breaking component K of the second
failure meets it. Independent Python (kempe_py + escape.pi_of)."""
import json, sys
from collections import Counter
from uv_lib import Hole
D = '../out/'
cases = []
for lab in ['x25', 'x25m', 'x26', 'x26m', 'x27', 'x27m']:
    for l in open(D + lab + '.jsonl'):
        if '"events": [{' not in l: continue
        r = json.loads(l)
        for e in r['jobx']['events']: cases.append((lab, r['name'], r['hole'], e))
print('Job X events:', len(cases))
KM = {1: 0, 2: 1, 4: 2, 8: 3, 16: 4}
def kpos(H, x):
    j, ty, hi, roles = H.frame(x); return ty, (hi[0] if len(hi) == 1 else None), j, roles
rows = []; summary = Counter()
cache = {}
for lab, name, h, e in cases:
    mirror = lab.endswith('m'); key = (name, h, mirror)
    if key not in cache: cache = {key: Hole(name, h, mirror)}
    H = cache[key]
    t6 = next(t for t in range(5) if len(H.rot[H.L[t]]) >= 6); p = H.L[t6]; y = H.w[(t6 + 4) % 5]; z = H.w[t6]
    m = next(w for w in H.rot[p] if w != h and w not in (H.L[(t6 + 1) % 5], H.L[(t6 + 4) % 5], y, z))
    V4 = {'p': p, 'm': m, 'y': y, 'z': z}
    zc = H.cycles[e['cycle']]; Lz = len(zc)
    # rebuild the run: find run starts in cycle order and pick the one with the C++ run length and failure positions
    found = None
    for i in range(Lz):
        if not H.DL[zc[i]] or H.DL[zc[i - 1]]: continue
        rr = []; t = i
        while H.DL[zc[t % Lz]]: rr.append(zc[t % Lz]); t += 1
        if len(rr) != e['run_len']: continue
        ff = e['first_fail_pos']
        def fails(x):
            ty, k, j, roles = kpos(H, x)
            if ty != 3 or k != 4: return None
            s = H.sigma(x); lk = H.locks(s); return not (not H.filled(s) and lk and not lk[0] and not lk[1])
        if fails(rr[ff]) and fails(rr[ff + 10]): found = rr; break
    if found is None: summary['not reproduced'] += 1; continue
    rr = found; i2 = e['first_fail_pos'] + 10; x2 = rr[i2]
    # breaking step: R3k0 -> R1k2 two steps before x2 (state rr[i2 - 2] -> rr[i2 - 1]); its swapped component = {alpha,A}-component of x_{j+2}
    def stepK(x):
        ty, k, j, roles = kpos(H, x); s = H.sp.states[x]; al, A = roles[0], roles[2]; xj2 = H.sp.linki[(j + 2) % 5]
        K = next(K for K in H.sp.components(s, al, A) if K >> xj2 & 1); return set(H.sp.mask_vertices(K)), (al, A)
    Kb, pb = stepK(rr[i2 - 2]) if i2 >= 2 else (set(), None)
    xl = rr[-1]; xn = H.pi[xl]
    tyl, kl, jl, rl = kpos(H, xl); tyn = kpos(H, xn)[0] if not H.filled(xn) else 'F'
    Kl, pl = stepK(xl)
    # Lock2 witness of xl: {mu,B}-component of m = x_{j+1} (it contains b = x_{j+4})
    s = H.sp.states[xl]; mu, B = rl[1], rl[3]; mm = H.sp.linki[(jl + 1) % 5]
    W2 = set(H.sp.mask_vertices(next(K for K in H.sp.components(s, mu, B) if K >> mm & 1)))
    pair_of = lambda x, pr: ''.join(nm for nm, v in V4.items() if H.col(x, v) in pr)
    row = dict(case=(lab, name, h), run_len=len(rr), second_fail=i2, dist=len(rr) - i2, last_DL=('R%d' % tyl, 'k%s' % kl), leaving=(tyn,),
               leave_pair=pair_of(xl, pl), leave_comp=''.join(nm for nm, v in V4.items() if v in Kl), lock2_witness_size=len(W2),
               break_pair=pair_of(rr[i2 - 2], pb) if pb else None, break_comp=''.join(nm for nm, v in V4.items() if v in Kb), break_meets_witness=len(Kb & W2) > 0,
               break_meets_leaving_comp=len(Kb & Kl) > 0, n_break_in_witness=len(Kb & W2))
    rows.append(row)
    summary[('break meets Lock2 witness', row['break_meets_witness'])] += 1
    summary[('leave pair/comp', row['leave_pair'], row['leave_comp'] or '-')] += 1
    summary[('last DL', row['last_DL'])] += 1
    summary[('break pair/comp', row['break_pair'], row['break_comp'] or '-')] += 1
json.dump(rows, open('jobaa-cases.json', 'w'), indent=0)
print('reproduced cases:', len(rows))
for k, v in sorted(summary.items(), key=str): print('  ', k, v)
