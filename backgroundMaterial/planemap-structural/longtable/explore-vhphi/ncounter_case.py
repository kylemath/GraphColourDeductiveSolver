"""Classify c', c'' Case I/II over Math's disc lists (read as DATA), no lock requirement.
usage: python3 ncounter_case.py FILE [maxn] ; prints summary.  [exploratory]"""
import sys
from collections import Counter
from ncounter_lib import *
fn = sys.argv[1]
cnt = Counter(); both_I = []
for line in open(fn):
    if not line.startswith('DISC'): continue
    adj, col, x, ring = parse_disc(line)
    if not is_rigid(adj, col, x): cnt['notrigid'] += 1; continue
    t1, t2 = classify_both(adj, col, x, ring)
    k = (t1[0], t2[0]); cnt[k] += 1
    if t1[0] == 'FO' or t1[0] == 'FO2': pass
    if t1[0] == 'I' and t2[0] == 'I': both_I.append(line.strip())
print(fn, dict(cnt))
if both_I:
    open(fn.replace('.txt', '') + '_bothI.txt', 'w').write('\n'.join(both_I) + '\n') if False else None
    print('both Case I:', len(both_I))
    for l in both_I[:3]: print(l[:300])
