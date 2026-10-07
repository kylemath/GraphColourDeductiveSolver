#!/usr/bin/env python3
"""Job AV summary from jobav-cycles.jsonl."""
import json
from collections import Counter
R = [json.loads(l) for l in open('jobav-cycles.jsonl')]
T = Counter((r['source'], r['L']) for r in R); print('records:', dict(T))
chk = Counter(); rows = []; gen = Counter(); meet = Counter(); kpm = Counter(); kk = Counter()
for r in R:
    L, n, b = r['L'], r['names'], r['breaks']; P = L // 10; fixed = set(n.values())
    for t in range(P):
        chk['pocket reaches w+ <=> J false at pos 9: %s' % (r['pockets'][t]['reaches_wp'] == b['step8break'][t])] += 1
        chk['step8break at period b <=> k4fail at period b+1: %s' % (b['step8break'][t] == b['k4fail'][(t + 1) % P])] += 1
        chk['k4fail at b <=> k3fail at b: %s' % (b['k4fail'][t] == b['k3fail'][t])] += 1
        chk['J at pos 0,1,2,3,9 of period b defined: %s' % all(r['J'][10 * t + i] is not None for i in (0, 1, 2, 3, 9))] += 1
        Ka, Kb = set(r['K8'][t]['vertices']), set(r['K8'][(t + 1) % P]['vertices'])
        chk['K8 contains x2, x3, w+: %s' % ({n['x2'], n['x3'], n['wp']} <= Ka)] += 1
        chk['K8 avoids p, m, y, z: %s' % (not Ka & {n['p'], n['m'], n['y'], n['z']})] += 1
    nb = sum(b['step8break']); cls = '%s L=%d, %d step-8 breaks' % (r['source'], L, nb)
    for t in range(P):
        Ka, Kb = set(r['K8'][t]['vertices']), set(r['K8'][(t + 1) % P]['vertices'])
        if P > 1: gen[(cls, 'consecutive K8 far intersection (minus fixed names) nonempty: %s' % bool((Ka & Kb) - fixed))] += 1
    if L == 20 and nb == 1:
        bb = b['step8break'].index(True); o = 1 - bb
        K, Ko = set(r['K8'][bb]['vertices']), set(r['K8'][o]['vertices']); Pk = set(r['pockets'][bb]['vertices']); Po = set(r['pockets'][o]['vertices'])
        far = (K & Ko) - fixed
        row = dict(id='%s %s h%d' % (r['name'], r['orientation'], r['hole']), K8_break=len(K), K8_other=len(Ko), inter=len(K & Ko), inter_far=len(far),
                   pocket_break=len(Pk), other_K8_meets_break_pocket=len(Ko & Pk), other_K8_meets_break_pocket_far=len((Ko & Pk) - fixed),
                   break_K8_meets_break_pocket=len(K & Pk), Kpm_failing_R3k4=r['Kpm_at_k4'][(bb + 1) % 2], Kpm_other=r['Kpm_at_k4'][bb],
                   k3fail=b['k3fail'], k4fail=b['k4fail'], pair_K8_break=r['K8'][bb]['pair'], pair_K8_other=r['K8'][o]['pair'], pocket_pair=r['pockets'][bb]['pair'])
        rows.append(row)
        meet['non-breaking K8 meets breaking pocket: %s' % bool(Ko & Pk)] += 1
        meet['  ... outside the fixed names: %s' % bool((Ko & Pk) - fixed)] += 1
        meet['breaking K8 meets its own pocket: %s' % bool(K & Pk)] += 1
        meet['K8 pairs equal: %s' % (row['pair_K8_break'] == row['pair_K8_other'])] += 1
print('\nchecks (all periods, all cycles):'); [print('   ', v, k) for k, v in sorted(chk.items())]
print('\nconsecutive step-8 components K8^b, K8^{b+1}:'); [print('   ', v, k) for k, v in sorted(gen.items())]
print('\nL = 20 cycles with one step-8 break (%d):' % len(rows)); [print('   ', v, k) for k, v in sorted(meet.items())]
print('    %-28s %5s %5s %5s %5s %6s %6s %6s %5s %5s  %s' % ('cycle', '|K|b', '|K|o', 'n', 'nfar', '|Pk|', 'Ko^Pk', 'far', 'Kb^Pk', 'Kpm f', 'Kpm o / k4fail k3fail'))
for x in rows:
    print('    %-28s %5d %5d %5d %5d %6d %6d %6d %5d %5d %5d / %s %s' % (x['id'], x['K8_break'], x['K8_other'], x['inter'], x['inter_far'], x['pocket_break'],
          x['other_K8_meets_break_pocket'], x['other_K8_meets_break_pocket_far'], x['break_K8_meets_break_pocket'], x['Kpm_failing_R3k4'], x['Kpm_other'], x['k4fail'], x['k3fail']))
json.dump(rows, open('jobav-breaking.json', 'w'), indent=1)
