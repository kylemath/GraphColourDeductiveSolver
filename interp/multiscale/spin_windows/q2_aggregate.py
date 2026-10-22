import csv, glob, collections
tot = collections.defaultdict(collections.Counter)
for f in sorted(glob.glob('/mnt/project-files/multiscale/spin_windows/q2_results_*.tsv')):
    for row in csv.DictReader(open(f), delimiter='\t'):
        t = tot[row['group']]; t['windows'] += 1
        for k in ['classes_sampled', 'ext', 'bad', 'ac', 'blocked', 'oddcol', 'A', 'A_odd', 'A_only_spin', 'Aodd_only_spin', 'A_beyond_ac', 'Aodd_beyond_ac', 'ac_or_A_odd', 'P_tested', 'P_same', 'F_tested', 'F_extra']:
            t[k] += int(row[k])
        g, n = row['good_pass_check'].split('/'); t['good_pass'] += int(g); t['good_checked'] += int(n)
print('| group | windows | classes | extend | bad | bad refuted by local propagation (AC) | spin test A (ring-proper) | spin test A_odd | A beyond "blocked" | A_odd beyond odd-colouring | spin beyond AC | bad left after AC |')
print('|---|---|---|---|---|---|---|---|---|---|---|---|')
for g, t in tot.items():
    b = t['bad']; pc = lambda x: '%d (%.1f%%)' % (x, 100 * x / b)
    print('| %s | %d | %d | %d | %d | %s | %s | %s | %s | %s | %d | %d |' % (g, t['windows'], t['classes_sampled'], t['ext'], b, pc(t['ac']), pc(t['A']), pc(t['A_odd']),
          pc(t['A_only_spin']), pc(t['Aodd_only_spin']), t['Aodd_beyond_ac'], b - t['ac']))
for g, t in tot.items(): print(g, 'soundness good-pass %d/%d, parity==bounded %d/%d, per-face extra kills %d/%d' % (t['good_pass'], t['good_checked'], t['P_same'], t['P_tested'], t['F_extra'], t['F_tested']))
