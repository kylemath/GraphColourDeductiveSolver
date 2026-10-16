"""Round 1 (EXPLORE-LOOP.md): copy bin/defect_tables.txt with every 7-wheel holding >= T fives marked bad (assumed
reducible), for a conditional defect search.  Usage: python3 loop/mktables.py  ->  bin/tables_f3.txt, bin/tables_f4.txt"""
import itertools
L = open('bin/defect_tables.txt').read().split('\n')
words = list(itertools.product((5, 6, 7), repeat=7))
for T in (3, 4):
    d7 = L[2].split(); t7 = L[3].split()
    d7n = ['1' if (d7[i] == '1' or w.count(5) >= T) else '0' for i, w in enumerate(words)]
    t7n = ['1' if (t7[i] == '1' or w.count(5) >= T) else '0' for i, w in enumerate(words)]
    open('bin/tables_f%d.txt' % T, 'w').write('\n'.join([L[0], L[1], ' '.join(d7n), ' '.join(t7n)]) + '\n')
