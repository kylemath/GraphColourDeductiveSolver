"""EXPLORE round 7 (exploratory): B-fixed (receiver at exact degree) configurations S + N(S) + u for the arrangements in
ARRFILEs, S a set of lone fives (|S| >= 2), ring <= RMAX, names not yet in any loop/lone/b*.out or loop/lp/r_*.out.
Usage: python3 loop/lone/bfix.py OUT RMAX ARRFILE [ARRFILE ...]"""
import sys, os, re, glob, collections
HERE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BOUT, BRMAX, BFILES = sys.argv[1], int(sys.argv[2]), sys.argv[3:]
src = open(os.path.join(HERE, 'gen28.py')).read(); src = src[:src.rindex('arrs = []')]
sys.argv = ['gen28.py', '/dev/null', str(BRMAX)]; __file__ = os.path.join(HERE, 'gen28.py'); exec(src)
done = set()
for fn in glob.glob(os.path.join(HERE, 'loop', 'lone', 'b*.out')) + glob.glob(os.path.join(HERE, 'loop', 'lp', 'r_*.out')) + glob.glob(os.path.join(HERE, 'out', 'job28', '*.out')):
    done |= {l.split()[0] for l in open(fn) if l.strip()}
lone = lambda d, lk, sv, i: lk[i] == '5' and lk[(i - 1) % d] in '56' and lk[(i + 1) % d] in '56' and sv[i] in '56' and sv[(i - 1) % d] in '56'
lines = {}; rc = collections.Counter(); na = 0
for fn in BFILES:
    for line in open(fn):
        m = re.search(r'receiver d=(\d+) link (\d+) s (\d+)', line)
        if not m: continue
        d, lk, sv = int(m.group(1)), m.group(2), m.group(3); na += 1
        Lp = {i for i in range(d) if lone(d, lk, sv, i)}
        for (r, k, S, w, s, nm) in variants(d, lk, sv):
            if not set(S) <= Lp or nm in done or nm in lines: continue
            ln = make(d, r, S, w, s, nm)
            if ln and not ln.startswith('RINGMISMATCH'): lines[nm] = ln; rc[(d, r)] += 1
open(BOUT, 'w').write(''.join(l + '\n' for l in sorted(lines.values(), key=lambda x: (int(x.split()[1]), x))))
print('arrangements', na, 'configurations', len(lines), sorted(rc.items()))
