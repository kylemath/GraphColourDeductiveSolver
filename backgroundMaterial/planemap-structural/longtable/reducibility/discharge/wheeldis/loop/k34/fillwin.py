"""EXPLORE round 34 part C (second amendment, 08:58Z): windows of R* = the 7/27 certificate row with s1 and s4 left open.
R = d7 link 5675765 s 6577575.  The certificate only reads the three fives' words (s6, s0 at w0; s2, s3 at w3;
s5, s6 at w6), so s1 and s4 (next to no five) are free: an LP row with any letters there has the same load.
A filling (a, b) = (s1, s4) in {5,6,7,8,9}^2 (9 = degree >= 9).  Window = u + all seven link vertices + a subset of
{s0, s2, s3, s5, s6} at R's letters + s1 absent or at a letter 5..8 + s4 likewise.  A window covers every filling
that agrees with it where it fixes s1/s4.  Output: dfast lines, then one 'cov NAME fillings' line per window.
usage: python3 fillwin.py OUT"""
import sys, os, itertools
W = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
src = open(os.path.join(W, 'gen28.py')).read(); src = src[:src.rindex('arrs = []')]
OUT = sys.argv[1]
sys.argv = ['gen28.py', '/dev/null', '24']; G = {'__file__': os.path.join(W, 'gen28.py'), '__name__': 'g28'}; exec(src, G)
d, lk, sv = 7, '5675765', '6577575'
FILL = [(a, b) for a in range(5, 10) for b in range(5, 10)]
seen, rows = {}, []
for a in [None, 5, 6, 7, 8]:
    for b in [None, 5, 6, 7, 8]:
        for k in range(0, 6):
            for SS in itertools.combinations([0, 2, 3, 5, 6], k):
                w = [int(c) for c in lk]
                s = [int(sv[j]) if j in SS else None for j in range(d)]
                s[1], s[4] = a, b
                r = G['ringf'](d, w, s)
                S_ = ''.join(str(s[j]) if s[j] is not None else '.' for j in range(d))
                key = G['canon_key'](d, lk, S_); nm = 'f%d_%s_%s' % (d, key[1], key[2])
                cov = [f for f in FILL if (a is None or f[0] == a) and (b is None or f[1] == b)]
                if nm in seen: seen[nm] = sorted(set(seen[nm]) | set(cov)); continue   # a symmetric image covers its own fillings
                line = G['make'](d, r, None, w, s, nm)
                if not line or line.startswith('RING'): print('skip', nm, line); continue
                seen[nm] = cov; rows.append((r, nm, line))
rows.sort(key=lambda x: (x[0], -len(seen[x[1]]), x[1]))
with open(OUT, 'w') as f:
    for r, nm, line in rows: f.write(line + '\n')
with open(OUT + '.cov', 'w') as f:
    for r, nm, line in rows: f.write('%s %d %s\n' % (nm, r, ' '.join('%d%d' % c for c in seen[nm])))
import collections
print(len(rows), 'windows', sorted(collections.Counter(r for r, *_ in rows).items()), 'covering pairs', sum(len(v) for v in seen.values()))
