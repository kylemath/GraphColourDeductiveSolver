"""Tables for R0-SCOPE.md from out/ (Long Table, r0surfaces)."""
import json
from collections import Counter
def recs(n): return [json.loads(l) for l in open(f'out/r0enum_n{n}.jsonl')]
print('== exhaustive census (r0enum) + exact genus (genus.c) ==')
for n in (8, 10, 12):
    R = recs(n); G = [l.split() for l in open(f'out/genus_n{n}.txt')]
    og = Counter(int(g[0]) for g in G); eg = Counter(int(g[1].rstrip('*')) for g in G)
    v2 = [r['V2'] for r in R]
    v2eg1 = sum(1 for r, g in zip(R, G) if r['V2'] and int(g[1].rstrip('*')) == 1)
    v2og1 = sum(1 for r, g in zip(R, G) if r['V2'] and int(g[0]) == 1)
    free0 = sum(1 for g in G if len(g) > 3 and g[3] == '0')
    minL = Counter(min(r['R0_L']) for r in R)
    print(n, 'R0', len(R), 'V2', sum(v2), 'V3', sum(r['V3'] for r in R), 'og', dict(og), 'eg', dict(eg),
          'V2&eg1', v2eg1, 'V2&og1', v2og1, 'abstractly planar', free0 if len(G[0]) > 3 else 'n/a', 'minL', dict(minL))
R = recs(14); G = [l.split() for l in open('out/genus_o_n14.txt')]
print(14, 'R0', len(R), 'V2', sum(r['V2'] for r in R), 'V3', sum(r['V3'] for r in R), 'og', dict(Counter(int(g[0]) for g in G)),
      'V2&og1', sum(1 for r, g in zip(R, G) if r['V2'] and g[0] == '1'), 'minL', dict(Counter(min(r['R0_L']) for r in R)))
S = [l.split() for l in open('out/genus_cap1_n14_sample.txt')]
print('   n=14 sample of 300 (exact, eg capped at 1):', dict(Counter((s[0], s[1]) for s in S)))
R = recs(16)
print(16, 'R0', len(R), 'V2', sum(r['V2'] for r in R), 'V3', sum(r['V3'] for r in R), 'minL', dict(Counter(min(r['R0_L']) for r in R)))
A = [l.split() for l in open('out/genus_o_n16_sample.txt')]; B = [l.split() for l in open('out/egheur_n16_sample.txt')]
print('   n=16 sample of 300: (og exact, eg heuristic upper bound):', dict(Counter((a[0], b[0]) for a, b in zip(A, B))))
print('   V3 n=16 exact genus (og eg ng):', dict(Counter(l.strip() for l in open('out/genus_v3_n16.txt'))))
