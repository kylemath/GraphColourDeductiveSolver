import collections, gzip, sys
dem = {}
for f in ('../eq_D7_k2.dem', '../eq_D7_k3.dem'):
    for l in open(f):
        n, t = l.split(); dem[n] = t
res = {}
for f in ('part00.cfast', 'part01.cfast', 'k2a.cfast', 'k2b.cfast'):
    cur = None
    for l in open(f):
        if ' r=' in l and not l.startswith(' '): cur = l.split()[0]; res.setdefault(cur, False)
        elif 'C-REDUCIBLE' in l: res[cur] = True
notD = [l.split()[0] for l in open('notD.txt')]
byT = collections.defaultdict(lambda: [0, 0, 0]); byB = collections.defaultdict(lambda: [0, 0, 0])
for n in notD:
    t = dem.get(n, '?'); b = n.split('_')[1].count('B') + n.split('_')[2].count('B')
    i = 2 if n not in res else (0 if res[n] else 1)
    byT[t][i] += 1; byB[b][i] += 1
print('notD configs', len(notD), 'tested', sum(1 for n in notD if n in res))
print('type: C / neither / untested')
for k in sorted(byT): print(' ', k, *byT[k], ' k2' if k.count('+') == 1 else '')
print('free big vertices (B in name): C / neither / untested')
for k in sorted(byB): print(' ', k, *byB[k])
