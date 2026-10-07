#!/usr/bin/env python3
"""Job BR summary from jobbr-walks.jsonl: per IPR seed (fullerene size), longest DL run at the (6,6,6,6,6) hole, start vs best over 4 walks; hits = all-DL cycles."""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
W = [json.loads(l) for l in open(os.path.join(HERE, 'jobbr-walks.jsonl'))]
N = {l.split()[0]: int(l.split()[1]) for l in open(os.path.join(HERE, '../in-ipr.txt'))}
print('walks', len(W), 'errors', sum('error' in w for w in W), 'evaluations', sum(w.get('evaluations', 0) for w in W), 'hits (all-DL cycles)', sum(len(w.get('hits', [])) for w in W))
seeds = sorted({w['seed'] for w in W}, key=lambda s: (N[s], s))
print('%-10s %4s %6s %10s %s' % ('seed', 'n', 'C_N', 'start run', 'best run per walk'))
for s in seeds:
    ws = [w for w in W if w['seed'] == s and 'error' not in w]
    print('%-10s %4d %6s %10d %s' % (s, N[s], 'C%d' % (2 * (N[s] - 2)), ws[0]['start'][1], sorted(w['best'][1] for w in ws)))
b = max((w for w in W if 'error' not in w), key=lambda w: tuple(w['best']))
print('HEADLINE: max all-DL cycles', b['best'][0], '| longest DL run reached', b['best'][1], 'at', b['seed'], 'walk', b['walk'], '| max start run', max(w['start'][1] for w in W if 'error' not in w))
