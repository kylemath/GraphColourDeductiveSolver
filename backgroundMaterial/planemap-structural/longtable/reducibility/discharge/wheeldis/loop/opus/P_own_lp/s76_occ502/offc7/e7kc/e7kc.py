# Usage (from wheeldis/): python3 <this> $PWD e7names.txt > e7kc_rebuilt.txt   (execs gen.py up to its main loop and calls its make())
# Rebuild dfast/kc lines for e<d>_<L>_<S>_<mask> names with gen.py's own builder (make), from the name alone.
import sys, os
HERE = sys.argv[1]; names = [l.split()[0] for l in open(sys.argv[2]) if l.strip()]
src = open(os.path.join(HERE, 'gen.py')).read(); src = src[:src.rindex('for d, lk, sv in arrs:')]
sys.argv = ['gen.py', '/dev/null', '99']; __file__ = os.path.join(HERE, 'gen.py'); exec(src)
for nm in names:
    f = nm.split('_'); d = int(f[0][1:]); L, Sv, mask = f[1], f[2], f[3]
    assert mask == ''.join('1' if c != '.' else '0' for c in L), nm
    w = [int(L[j]) if L[j] in '56' else None for j in range(d)]
    s = [int(Sv[j]) if Sv[j] in '56' else None for j in range(d)]
    r = ringf(d, w, s); key = canon_key(d, L, Sv)
    line = make(d, r, None, w, s, key)
    print(line if line else nm + ' NOTEXT')
