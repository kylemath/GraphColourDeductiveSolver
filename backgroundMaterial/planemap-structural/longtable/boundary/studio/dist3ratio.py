"""|{d >= 3}| / n over every degree-5 hole of the census shards (dist3 solved every hole), by order."""
import sys, glob, collections
SH = '../../axioms/studio/out/dcyc/shards/*'
st = collections.defaultdict(lambda: [9, 0, 0, None])   # order -> [min ratio, sum, count, argmin]
for f in sorted(glob.glob(SH)):
    for l in open(f):
        p = l.split(); rot = [[int(x) for x in r.split(',')] for r in p[2].split(';')]; n = len(rot); o = int(p[0][1:3])
        for h in range(n):
            if len(rot[h]) != 5: continue
            d = [-1] * n; d[h] = 0; q = [h]
            for u in q:
                for w in rot[u]:
                    if d[w] < 0: d[w] = d[u] + 1; q.append(w)
            k = sum(1 for x in d if x >= 3); r = k / n; s = st[o]
            if r < s[0]: s[0] = r; s[3] = (p[0], h, k, n)
            s[1] += r; s[2] += 1
for o in sorted(st): s = st[o]; print(o, 'min |R|/n %.3f at %s' % (s[0], s[3]), 'mean %.3f' % (s[1] / s[2]))
