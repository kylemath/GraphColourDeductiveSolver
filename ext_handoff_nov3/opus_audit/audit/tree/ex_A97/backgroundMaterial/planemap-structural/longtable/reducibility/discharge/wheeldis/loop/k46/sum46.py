"""Round 46 part A summary: per sender context, windows run, two-engine kills, smallest kill ring.  usage: python3 sum46.py"""
import os, collections
H = os.path.dirname(os.path.abspath(__file__))
ring = {l.split()[0]: int(l.split()[1]) for l in open(os.path.join(H, 'ctx46_A.txt'))}
ctx = {l.split(' | ')[0]: l.rstrip('\n').split(' | ')[1].split('; ') for l in open(os.path.join(H, 'ctx46_A.map'))}
kill = {}
for l in open(os.path.join(H, 'KILL')): kill.setdefault(l.split()[0], l.split()[1])
done = {l.split()[0] for l in open(os.path.join(H, 'A_kcc.out')) if l[:1] == 'a'}
per = collections.defaultdict(lambda: [0, 0, 99, collections.Counter(), None])
for w, cs in ctx.items():
    for c in cs:
        p = per[c]; p[0] += w in done
        if w in kill:
            p[1] += 1; p[3][kill[w]] += 1
            if ring[w] < p[2]: p[2] = ring[w]; p[4] = w
for c in sorted(per, key=lambda c: (c.split()[3], c)):
    p = per[c]; print('%-34s windows run %4d  kills %4d (%s)  smallest ring %s  %s' % (c, p[0], p[1], dict(p[3]), p[2] if p[1] else '-', p[4] or ''))
