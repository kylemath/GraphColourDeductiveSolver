#!/usr/bin/env python3
"""Track F: all fullerene duals C20..C{max} by spiral enumeration + canonical dedup; writes graphs/fall_NN.txt"""
import sys, time; sys.path.insert(0, 'src'); import spiral
mx = int(sys.argv[1])
for n in range(20, mx + 1, 2):
    t = time.time(); out = spiral.enumerate_all(n, [])
    with open(f'graphs/fall_{n}.txt', 'w') as fh:
        for i, (p, rot, tri) in enumerate(out): fh.write(spiral.line(f'C{n}#{i}', rot) + '\n')
    print(n, len(out), 'sepTri', sum(1 for _, rot, tri in out if tri != 2 * len(rot) - 4), round(time.time() - t, 1), flush=True)
