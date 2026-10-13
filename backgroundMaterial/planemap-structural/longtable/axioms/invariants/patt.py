"""order pattern of the v-chord far ends (e0,e1,e3) along H at Hamiltonian states, per run kind."""
import sys, json, gzip
from collections import defaultdict, Counter
pref = sys.argv[1]
runs = defaultdict(list)
for l in gzip.open(pref + '_feat.jsonl.gz', 'rt'):
    r = json.loads(l); runs[r['run']].append(r)
def pat(r):
    p = sorted([('0', r['h_e0']), ('1', r['h_e1']), ('3', r['h_e3'])], key=lambda x: x[1])
    return ''.join(a for a, b in p)
seqs = defaultdict(Counter); single = defaultdict(Counter); trans = defaultdict(Counter)
for rid, s in runs.items():
    s.sort(key=lambda r: r['t']); kind = s[0]['kind']
    ps = [pat(r) for r in s if 'h_e0' in r]
    for p in ps: single[kind][p] += 1
    for a, b in zip(ps, ps[1:]): trans[kind][a + '>' + b] += 1
    if len(ps) >= 3: seqs[kind][' '.join(ps)] += 1
for kind in single:
    print(kind, 'patterns', dict(single[kind]))
    print('   transitions', dict(trans[kind]))
    print('   seqs(>=3)', seqs[kind].most_common(8))
