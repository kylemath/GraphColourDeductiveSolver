#!/usr/bin/env python3
import sys, time; sys.path.insert(0, 'src'); import spiral
for n in range(int(sys.argv[1]), int(sys.argv[2]) + 1, 2):
    t = time.time(); out = spiral.enumerate_all(n, [])
    with open(f'graphs/fall_{n}.txt', 'w') as fh:
        for i, (p, rot, tri) in enumerate(out): fh.write(spiral.line(f'C{n}#{i}', rot) + '\n')
    print(n, len(out), round(time.time() - t, 1), flush=True)
