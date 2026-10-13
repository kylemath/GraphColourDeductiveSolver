"""For V3 (word-1212) solution graphs: how many perfect matchings are DL-good, and does ax_lib's orbit finder
(DL + unique successor, i.e. a genuine near-rigid pi-orbit / R-cycle) find a closed orbit?  usage: dlcheck.py file"""
import sys
sys.path.insert(0, '..')
from ax_lib import G5, parse_line
from collections import Counter
c = Counter()
for line in open(sys.argv[1]):
    line = line.split('|')[0].strip()
    if not line or line.startswith('{'): continue
    g = G5(*parse_line(line))
    P, good, cyc = g.orbits()
    c[('nDL', len(good), 'orbits', len(cyc))] += 1
    for o in cyc: print('ORBIT', line, 'L =', len(o), 'word', g.word(o))
print(dict(c))
