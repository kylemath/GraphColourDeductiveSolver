"""Aggregate a6_run output by family: holes, classes, hard stars, walks, solved, failures by reason, mean swaps over
par, walks that revisited a star, max steps, coverage check."""
import json, glob, sys, collections
T = collections.defaultdict(collections.Counter); fails = []
for f in sys.argv[1:]:
    for l in open(f):
        r = json.loads(l); t = T[r['family']]
        if 'skip' in r: t['skipped'] += 1; continue
        t['holes'] += 1; t['classes'] += r['classes']; t['hard'] += r['hard']; t['walks'] += r['walks']; t['solved'] += r['solved']
        t['extra'] += r['extra']; t['revisits'] += r['revisits']; t['maxSteps'] = max(t['maxSteps'], r['maxSteps']); t['coverBad'] += not r['coverOK']
        t['sampled_holes'] += r['walks'] < r['hard']
        for w, c in r['why'].items(): t['fail_' + w] += c
        fails += [(r['key'], x) for x in r['fails']]
for fam, t in sorted(T.items()):
    print(fam, dict(t), 'mean swaps over par %.3f' % (t['extra'] / max(1, t['solved'])))
print('FAILURES', len(fails)); [print(f) for f in fails[:10]]
