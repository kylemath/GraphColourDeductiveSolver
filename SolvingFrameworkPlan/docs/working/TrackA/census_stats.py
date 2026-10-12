#!/usr/bin/env python3
"""Track A: census statistics from out/census-*.jsonl -> out/census-stats.txt"""
import json, glob, statistics as st
from collections import Counter, defaultdict
R = [json.loads(l) for fn in sorted(glob.glob('out/census-*.jsonl')) for l in open(fn)]
out = []
def P(*a): out.append(' '.join(map(str, a)))
for label, sel in (('census orders 12-27 (complete, plantri -m5 -c4 lists)', lambda r: r['n'] <= 27), ('order 28 appears-free list (in-cfree-28.txt)', lambda r: r['n'] == 28)):
    S = [r for r in R if sel(r)]
    P('==', label, ': graphs', len(S), 'frame', sum(r['frame'] for r in S), 'by order', dict(sorted(Counter(r['n'] for r in S).items())))
    holes = sum(r['deg5'] for r in S); P('degree-5 vertices', holes, '; PureClean', sum(r['npc'] for r in S), '; graphs with 0 PureClean', sum(r['npc'] == 0 for r in S),
      '; graphs with a non-PureClean vertex', sum(r['npc'] < r['deg5'] for r in S))
    P('min #PureClean per graph', min(r['npc'] for r in S), '; deg5 histogram', dict(sorted(Counter(r['deg5'] for r in S).items())))
    m = [r['margin'] for r in S]; w = [r['worst'] for r in S]
    P('margin (max_v min-class F/N): min %.4f median %.4f max %.4f' % (min(m), st.median(m), max(m)))
    P('worst  (min_v min-class F/N): min %.4f median %.4f max %.4f' % (min(w), st.median(w), max(w)))
    allmf = [v for r in S for v in r['minfrac'].values()]
    P('per-vertex min-class F/N: min %.4f; vertices with value < 0.3: %d; = 0.25: %d' % (min(allmf), sum(v < 0.3 for v in allmf), sum(abs(v - 0.25) < 1e-12 for v in allmf)))
    nc = Counter(len(c) for r in S for c in r['classes'].values()); P('classes per hole histogram', dict(sorted(nc.items())))
    small = Counter(tuple(x) for r in S for c in r['classes'].values() for x in c if x[0] < 100); P('small classes (size, F) < 100 states: ', dict(small))
    P('verified by engine 2 (kempe_py):', sum(1 for r in S if r.get('verify')), 'of', len(S), '; mismatches', sum(1 for r in S if r.get('verify') is False))
    P('fewest PureClean (ties by margin):')
    for r in sorted(S, key=lambda r: (r['npc'], r['margin']))[:6]: P('   ', r['name'], 'deg5', r['deg5'], 'npc', r['npc'], 'margin %.4f worst %.4f' % (r['margin'], r['worst']))
    P('lowest margin:')
    for r in sorted(S, key=lambda r: r['margin'])[:6]: P('   ', r['name'], 'deg5', r['deg5'], 'margin %.4f worst %.4f' % (r['margin'], r['worst']))
open('out/census-stats.txt', 'w').write('\n'.join(out) + '\n'); print('\n'.join(out))
