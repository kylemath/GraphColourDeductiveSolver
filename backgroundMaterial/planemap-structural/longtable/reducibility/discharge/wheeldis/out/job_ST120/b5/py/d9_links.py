#!/usr/bin/env python3
"""ST-127 (2): the d = 9..14 link-word search, exactly as RSSTD9Core.linkSurvivors: letters assigned in order
0..d-1; b_i = c+(window_i) once L_{i-2..i+2} are all assigned, 0 for an assigned 9+, else 6; prune when
60 - 10d + sum b_i <= 0; keep full words that are rotation-least (isRotMin). c+ from cert/cplus79.txt (Lean dump).
usage: python3 -I d9_links.py D [OUTFILE]"""
import os, sys
H = os.path.dirname(os.path.abspath(__file__)); B5 = os.path.normpath(os.path.join(H, '..'))
C = {tuple(int(c) for c in l.split()[0]): int(l.split()[1]) for l in open(os.path.join(B5, 'cert', 'cplus79.txt'))}
def survivors(d):
    out = []; L = [0] * d
    def b(i, k):           # k letters assigned (positions 0..k-1)
        idx = [(i + j) % d for j in (-2, -1, 0, 1, 2)]
        if all(x < k for x in idx): return C[tuple(L[x] for x in idx)]
        if i < k and L[i] == 9: return 0
        return 6
    def rec(k):
        bound = 60 - 10 * d + sum(b(i, k) for i in range(d))
        if bound <= 0: return
        if k == d:
            t = tuple(L)
            if t == min(t[r:] + t[:r] for r in range(d)): out.append(t)
            return
        for a in (5, 6, 7, 8, 9):
            L[k] = a; rec(k + 1)
        L[k] = 0
    rec(0); return out
d = int(sys.argv[1]); S = survivors(d)
print('d', d, 'survivors', len(S))
if len(sys.argv) > 2: open(sys.argv[2], 'w').write('\n'.join(''.join(map(str, t)) for t in S) + '\n')
