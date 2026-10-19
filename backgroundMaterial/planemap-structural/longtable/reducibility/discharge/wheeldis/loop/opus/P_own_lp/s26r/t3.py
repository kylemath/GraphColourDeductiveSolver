import time, sys
from ball import *
C = registry()
D = 7; LK = [7,6,6,5,5,6,6]; SV = [6,6,7,5,6,7,6]
p = [int(c) if c != '9' else 99 for c in sys.argv[1]]
free2 = [('p',0,1),('p',0,2),('p',1,1),('p',2,1),('p',5,1),('p',6,1)]
R2 = {('s', i): SV[i] for i in range(D)}; R2.update(dict(zip(free2, p)))
t0 = time.time()
P, pa, pf, order2, inn3, touch = frame(D, LK, R2)
print('order2', order2); print('n3', len(inn3), 'inn', [inn3[('r',k)] for k in range(len(inn3))])
fd = {('u',): D}
for i in range(D): fd[('w', i)] = LK[i]
for x in order2: fd[x] = R2[x]
unk = [x for x in inn3 if any(R2[y] >= 99 for y in touch[x])]
for x in unk: fd[x] = NEVER
free = [x for x in inn3 if x not in fd]
R = reqsets(C, P, pa, pf, fd, set(free))
print('reqs', len(R), 'time', time.time() - t0)
import collections
print(collections.Counter(len(r) for r in R))
for r, n in sorted(R.items(), key=lambda t: len(t[0]))[:15]: print(sorted(r), n)
