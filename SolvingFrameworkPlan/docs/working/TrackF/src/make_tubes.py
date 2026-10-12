#!/usr/bin/env python3
"""Track F: nanotube fullerene duals by spiral shifting (cap pentagon sets fixed, end cap shifted by d faces per period).
Families: (5,5) D5d C60+20k, (5,5) D5h C70+20k, (9,0) IPR C78+18k, (9,0) non-IPR C58+18k (caps with adjacent pentagons)."""
import sys; sys.path.insert(0, 'src'); import tubes, spiral
FAM = {'t55a': (32, [1,7,9,11,13,15], [18,20,22,24,26,32], 10),
       't55b': (37, [1,7,9,11,13,15], [27,29,31,33,35,37], 10),
       't90i': (41, [2,4,6,10,13,16], [26,29,32,36,38,40], 9),
       't90n': (31, [1,2,3,11,13,15], [17,19,21,29,30,31], 9)}
kmax = int(sys.argv[1]) if len(sys.argv) > 1 else 12
for fam, (f0, A, B, d) in FAM.items():
    for k in range(kmax + 1):
        f = f0 + d * k; r = tubes.build(f, [x - 1 for x in A] + [x - 1 + d * k for x in B])
        if r is None: print('FAIL', fam, k, file=sys.stderr); continue
        n = len(r)
        if n > 256: break
        deg = [len(x) for x in r]; p5 = [v for v in range(n) if deg[v] == 5]
        b = tubes.belt(r, p5[:6], p5[6:]); adj55 = sum(1 for u in p5 for v in r[u] if deg[v] == 5) // 2
        print(spiral.line(f'{fam}_C{2*(f-2)}_k{k}_belt{b}_adj{adj55}', r))
