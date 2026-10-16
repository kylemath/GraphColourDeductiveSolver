"""EXPLORE round 10: 'LINK:RING2' arguments for defectb7 (ring-2 letters in Layered order, s fixed, p slots '.').
Usage: python3 mkfix.py BINDERS"""
import sys, os
src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'b7match.py')).read()
sys.argv, ARGS = ['b7match.py'], sys.argv[1:]
exec(src.split('B = {}')[0].replace('__file__', repr(os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'b7match.py')))))
for line in open(ARGS[0]):
    f = line.split()
    if len(f) < 2: continue
    lk, sv = f[0], f[1]
    print('%s:%s' % (lk, ''.join(sv[x[1]] if x[0] == 's' else '.' for x in names(lk))))
