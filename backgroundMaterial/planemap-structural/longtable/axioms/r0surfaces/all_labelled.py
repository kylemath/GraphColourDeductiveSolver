"""Dump every normal-form labelled graph line (H + chords, all labellings) for n: control population."""
import sys, itertools
n = int(sys.argv[1])
def cm(R):
    if not R: yield []; return
    a = R[0]
    for i in range(1, len(R)):
        b = R[i]
        if abs(a - b) == 1: continue
        for m in cm(R[1:i] + R[i + 1:]): yield [(a, b)] + m
H = [(i, (i + 1) % n) for i in range(n)]
for S in itertools.combinations(range(2, n - 1), 3):
    R = [u for u in range(1, n) if u not in S]
    for C in cm(R):
        E = H + [(0, s) for s in S] + C
        for p in itertools.permutations(range(3)):
            fv = [n - 1, n + p[0], 0, n + p[1], n + p[2]]
            print(' '.join(map(str, [n, len(E)] + [x for e in E for x in e] + fv)))
