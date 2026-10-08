#!/usr/bin/env python3
"""Track I: exhaustive check of Lemma R (rotation parity) and of its failure without planarity.

Points 0..2m-1 on a circle, each labelled I or O.  B0 = {(0,1),(2,3),...}, B1 = {(1,2),...,(2m-1,0)}.
For every non-crossing matching N_I of the I-points and N_O of the O-points:
    lam(B, N) = number of cycles of B u N.
Lemma R: lam(B0,N) + lam(B1,N) mod 2 depends only on the I/O labelling (not on N).
Also reports the value, tests the conjectured closed form  m + 1 + (#I)/2... (printed, not assumed), and shows that
the statement FAILS if crossing matchings are allowed (the non-planar analogue).
usage: ti_lemmaR.py MMAX"""
import sys, itertools
sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))
from ti_lib import ncm

def allm(pts):
    if not pts: yield []; return
    a = pts[0]
    for k in range(1, len(pts)):
        rest = pts[1:k] + pts[k + 1:]
        for m in allm(rest): yield [(a, pts[k])] + m

def lam(n, B, N):
    adj = {i: [] for i in range(n)}
    for a, b in B + N: adj[a].append(b); adj[b].append(a)
    seen = set(); c = 0
    for s in range(n):
        if s in seen: continue
        c += 1; st = [s]
        while st:
            x = st.pop()
            if x in seen: continue
            seen.add(x); st.extend(adj[x])
    return c

def main():
    mmax = int(sys.argv[1]); bad_nc = 0; bad_all = 0; pats = 0; forms = {}
    for m in range(1, mmax + 1):
        n = 2 * m
        B0 = [(2 * i, 2 * i + 1) for i in range(m)]; B1 = [(2 * i + 1, (2 * i + 2) % n) for i in range(m)]
        for lab in itertools.product('IO', repeat=n):
            I = [i for i in range(n) if lab[i] == 'I']; O = [i for i in range(n) if lab[i] == 'O']
            if len(I) % 2: continue
            pats += 1
            vals = {(lam(n, B0, a + b) + lam(n, B1, a + b)) % 2 for a in ncm(I) for b in ncm(O)}
            if len(vals) != 1: bad_nc += 1
            v = vals.pop()
            forms.setdefault((m + 1 + len(I) // 2) % 2 == v, 0); forms[(m + 1 + len(I) // 2) % 2 == v] += 1
            if n <= 8:
                va = {(lam(n, B0, a + b) + lam(n, B1, a + b)) % 2 for a in allm(I) for b in allm(O)}
                if len(va) != 1: bad_all += 1
        print('m', m, 'patterns', pats, 'Lemma R failures (NC matchings)', bad_nc,
              '| patterns where it fails for arbitrary matchings (n<=8)', bad_all,
              '| closed form m+1+|I|/2 holds/fails', forms, flush=True)

if __name__ == '__main__':
    main()
