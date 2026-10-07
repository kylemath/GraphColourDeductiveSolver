#!/usr/bin/env python3
"""Track A task 2: summarise anat/*.jsonl -> anat/summary.txt (counts by class type, equality-class anatomy, product test)."""
import json, sys, glob
from collections import Counter, defaultdict
out = []
def P(*a): out.append(' '.join(map(str, a)))
def canon_cyc(seq):
    n = len(seq); c = [tuple(seq[i:] + seq[:i]) for i in range(n)]; return min(c + [tuple(reversed(x)) for x in c])
def canon_ld(ld):
    d = [min(x, 8) for x in ld]; return min(tuple(s[r:] + s[:r]) for s in (d, d[::-1]) for r in range(5))
for fn in sorted(glob.glob('anat/anat-*.jsonl')):
    R = [json.loads(l) for l in open(fn)]
    allc = [(r['name'], h, N, F) for r in R for h, N, F in r['allclasses']]
    P('=====', fn, ': graphs', len(R), 'n', dict(sorted(Counter(r['n'] for r in R).items())), '; holes', len({(r['name'], h) for r in R for h, *_ in r['allclasses']}), '; classes', len(allc))
    P('classes with 4F = N (equality):', sum(4 * F == N for *_, N, F in allc), '; 4F < N (floor broken):', sum(4 * F < N for *_, N, F in allc),
      '; N power of 2:', sum(N & (N - 1) == 0 for *_, N, F in allc), '; N <= 64:', sum(N <= 64 for *_, N, F in allc))
    P('small-class (N, F) histogram:', dict(sorted(Counter((N, F) for *_, N, F in allc if N <= 64).items())))
    A = [(r['name'], h, c) for r in R for h, cs in r['holes'].items() for c in cs if not c.get('skipped')]
    P('analysed classes (N<=64 or 2^k or equality):', len(A), '; skipped large non-2^k:', sum(1 for r in R for cs in r['holes'].values() for c in cs if c.get('skipped')))
    P('  product of independent chain flips (labelled cube):', sum(c['product'] for *_, c in A), '; move graph is a hypercube (unlabelled):', sum(c['hypercube'] for *_, c in A),
      '; single cycle:', sum(bool(c.get('cycle')) for *_, c in A))
    T = defaultdict(Counter)
    for name, h, c in A:
        shape = 'cycle%d' % c['N'] if c.get('cycle') else ('cube' if c['hypercube'] else 'other(degs=%s,E=%d)' % (sorted(c['degs'].items()), c['edges']))
        T[(c['N'], c['F'])][(shape, 'prod' if c['product'] else '-')] += 1
    for k in sorted(T): P('  (N,F)=%s:' % (k,), dict(T[k]))
    # equality anatomy
    E = [(name, h, c) for name, h, c in A if 4 * c['F'] == c['N']]
    P('-- equality classes:', len(E), 'in', len({n for n, *_ in E}), 'graphs')
    pat = Counter(); ldc = Counter(); edgepat = Counter(); sizes = Counter(); fpos = Counter(); chainlink = Counter()
    for name, h, c in E:
        sizes[c['N']] += 1; ldc[canon_ld(c['linkdeg'])] += 1
        if c.get('cycle'):
            seq = ['F' if s['filled'] else s['lock'] for s in c['cycle']]; pat[canon_cyc(seq)] += 1
            m = len(seq); fpos[tuple((b - a) % m for a, b in zip(c['filled_positions'], c['filled_positions'][1:] + c['filled_positions'][:1]))] += 1
            for s in c['cycle']:
                for e in s['edge_to_next']:
                    edgepat[('F' if s['filled'] else s['lock'], e['pair'], len(e['K_link']) + len(e['R_link']))] += 1
        else: pat[('not a cycle', c['N'], c['hypercube'], c['product'])] += 1
    P('   sizes', dict(sizes)); P('   link words (canonical degrees)', dict(ldc))
    P('   cyclic state pattern (F = filled, lock type of unfilled):'); [P('     ', ''.join('%-3s' % x for x in k), v) for k, v in pat.most_common()]
    P('   gaps between consecutive filled states along the cycle:', dict(fpos))
    P('   edge types (from-state type, colour-pair letters of the link word [x = colour absent from link], # link vertices in K u rest):')
    for k, v in sorted(edgepat.items()): P('     ', k, v)
    # list equality classes
    for name, h, c in E[:200]:
        P('   EQ', name, 'hole', h, 'link', c['linkdeg'], 'N', c['N'], 'F', c['F'], 'cycle' if c.get('cycle') else 'NOT-CYCLE', 'filled at', c.get('filled_positions'))
    # non-equality small classes: are they cycles? pattern check
    NE = [(name, h, c) for name, h, c in A if 4 * c['F'] != c['N'] and c.get('cycle')]
    pc = Counter()
    for name, h, c in NE: pc[(c['N'], c['F'], canon_cyc(['F' if s['filled'] else s['lock'] for s in c['cycle']]))] += 1
    P('-- non-equality classes that are single cycles:', len(NE)); [P('     ', k, v) for k, v in pc.most_common(20)]
open('anat/summary.txt', 'w').write('\n'.join(out) + '\n'); print('\n'.join(out))
