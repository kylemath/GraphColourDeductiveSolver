"""Case I/II of both neighbours for the 14 triply locked order-23 discs of Math's res_23.txt (data) [exploratory]"""
import sys
from ncounter_lib import *
for line in open(sys.argv[1]):
    if '| DISC' not in line: continue
    d = 'DISC' + line.split('| DISC')[1]
    adj, col, x, ring = parse_disc(d)
    t1, t2 = classify_both(adj, col, x, ring)
    sizes = [sum(1 for v in col if col[v]==k) for k in range(4)]
    print(sizes, "c'", t1[0], "c''", t2[0], t1[1].get('c3_broken_Db'), t2[1].get('c3_broken_Db'))
