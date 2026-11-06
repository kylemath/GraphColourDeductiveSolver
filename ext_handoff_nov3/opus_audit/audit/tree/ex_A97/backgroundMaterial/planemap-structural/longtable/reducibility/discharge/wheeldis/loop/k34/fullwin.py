"""EXPLORE round 34: windows of the 7/27 certificate row R = d7 link 5675765 s 6577575 beyond B-fixed:
u + all link vertices + a superset of the s-vertices next to S (all letters known from R).  Prints dfast lines.
usage: python3 fullwin.py OUT"""
import sys, os, itertools
W = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
src = open(os.path.join(W, 'gen28.py')).read(); src = src[:src.rindex('arrs = []')]
OUT = sys.argv[1]
sys.argv = ['gen28.py', '/dev/null', '24']; G = {'__file__': os.path.join(W, 'gen28.py'), '__name__': 'g28'}; exec(src, G)
d, lk, sv = 7, '5675765', '6577575'
lines = {}
for k in range(0, 8):
    for SS in itertools.combinations(range(d), k):
        w = [int(c) for c in lk]; s = [int(sv[j]) if j in SS else None for j in range(d)]
        r = G['ringf'](d, w, s)
        L_ = lk; S_ = ''.join(sv[j] if j in SS else '.' for j in range(d))
        key = G['canon_key'](d, L_, S_); nm = 'f%d_%s_%s' % (d, key[1], key[2])
        if nm in lines: continue
        line = G['make'](d, r, None, w, s, nm)
        print(r, SS, nm, 'ok' if line and not line.startswith('RING') else line)
        if line and not line.startswith('RING'): lines[nm] = line
open(OUT, 'w').write(''.join(l + '\n' for l in sorted(lines.values(), key=lambda x: (int(x.split()[1]), x))))
