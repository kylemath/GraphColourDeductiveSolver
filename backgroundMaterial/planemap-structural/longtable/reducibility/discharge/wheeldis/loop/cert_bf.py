"""EXPLORE round 5: every B-fixed sender-set configuration (|S| >= 2, ring <= RMAX) of given receiver arrangements, in
dfast format, built with gen28.py's builder.  Usage: python3 loop/cert_bf.py OUT RMAX 'd link s' ['d link s' ...]"""
import sys, os
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
args = sys.argv[1:]; OUTF, RM, ARRS = args[0], int(args[1]), args[2:]
src = open(os.path.join(HERE, 'gen28.py')).read(); src = src[:src.rindex('arrs = []')]
sys.argv = ['gen28.py', '/dev/null', str(RM)]; __file__ = os.path.join(HERE, 'gen28.py'); exec(src)
lines = {}
for a in ARRS:
    d, lk, sv = a.split(); d = int(d)
    for (r, k, S, w, s, nm) in variants(d, lk, sv):
        ln = make(d, r, S, w, s, nm)
        if ln and not ln.startswith('RINGMISMATCH'): lines[nm] = ln; print(a, 'S=%s r=%d %s' % (S, r, nm))
        else: print(a, 'S=%s r=%d %s NOT BUILT %s' % (S, r, nm, ln))
open(OUTF, 'w').write(''.join(l + '\n' for l in sorted(lines.values(), key=lambda x: int(x.split()[1]))))
