#!/usr/bin/env python3
"""Job BP summary from out/bp{ipr,adv,c12,c24..c27}{,m}.jsonl (picyc.bp --jobbp). Choice = (vertex role x0..x4 / w0..w4 / m0..m4 relative to x_j, partner colour role a/m/A/B);
mask bit = role_index * 4 + partner role (a = alpha, m = mu, A, B). An escape = an image that is neither DL nor a fixed point (filled, lockless or single-lock)."""
import json
from collections import Counter, defaultdict
RN = 'amAB'; ROLES = ['x%d' % i for i in range(5)] + ['w%d' % i for i in range(5)] + ['m%d' % i for i in range(5)]
def choice(b): return ROLES[b // 4] + '/' + RN[b % 4]
TAB = defaultdict(lambda: [0] * 6); MS = defaultdict(Counter); ND = Counter(); NONE = Counter()
for tag in ('ipr', 'adv', 'c12', 'c24', 'c25', 'c26', 'c27'):
    for suf in ('', 'm'):
        try: fh = open('../out/bp%s%s.jsonl' % (tag, suf))
        except FileNotFoundError: print('missing', tag, suf); continue
        for l in fh:
            if '"jobbp"' not in l: continue
            r = json.loads(l); b = r['jobbp']; src = 'IPR' if tag == 'ipr' else ('adv' if tag == 'adv' else 'census')
            ND[(r['pattern'], src)] += b['nDL']; NONE[(r['pattern'], src)] += b['no_escape']
            for k, v in b['tab'].items():
                for i in range(6): TAB[k][i] += v[i]
            for k, v in b['masks'].items():
                key, m = k.rsplit(' ', 1); MS[key][int(m)] += v
print('(2) DL states with NO escaping single swap (pattern, source): nDL / none:'); [print('    ', k, ND[k], NONE[k]) for k in sorted(ND)]
for pat in ('6,6,6,6,6', '5,5,6,6,6', '5,5,7,5,7'):
    groups = [k for k in MS if k.startswith(pat + ' ')]
    if not groups: continue
    print('=' * 20, pat)
    allm = Counter()
    for g in sorted(groups):
        inter = None
        for m in MS[g]: inter = m if inter is None else inter & m
        n = sum(MS[g].values()); allm.update(MS[g])
        always = [choice(b) for b in range(60) if inter and inter >> b & 1]
        print('  %-24s DL states %7d  sigma6 candidates (escape at EVERY such state): %s' % (g, n, ', '.join(always[:12]) if always else 'NONE'))
    # greedy cover over all DL states of this pattern
    left = Counter(allm); cover = []
    while left and any(m for m in left):
        best = max(range(60), key=lambda b: sum(v for m, v in left.items() if m >> b & 1))
        got = sum(v for m, v in left.items() if m >> best & 1)
        if got == 0: break
        cover.append((choice(best), got)); left = Counter({m: v for m, v in left.items() if not m >> best & 1})
    print('  greedy cover of all DL states:', cover, ' uncovered', sum(left.values()))
    print('  (1) escape fraction per (type, word, role/pair), first 40 by total:')
    rows = [(k, v) for k, v in TAB.items() if k.startswith(pat + ' ')]
    for k, v in sorted(rows, key=lambda kv: -kv[1][5])[:40]:
        print('     %-34s n %7d  fixed %.2f filled %.2f lockless %.2f single %.2f DL %.2f  escape %.2f' % (k[len(pat) + 1:], v[5], *(x / v[5] for x in v[:5]), (v[1] + v[2] + v[3]) / v[5]))
