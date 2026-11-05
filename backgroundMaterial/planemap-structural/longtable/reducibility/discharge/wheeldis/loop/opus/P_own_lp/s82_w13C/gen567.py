# all d=7 receivers with link and apex letters in {5,6,7}, one per dihedral class, admissible on the given stack -> 'R 7 LINK APEX' lines
import sys, os, itertools, time
E = sys.argv[1]; out = sys.argv[2]
sys.argv = ['pcheck.py', 'none'] + sys.argv[3:]
src = open(os.path.join(E, 'pcheck.py')).read(); cut = src.index("{'xoselftest'")
g = {'__file__': os.path.join(E, 'pcheck.py'), '__name__': 'pcheck_t'}
exec(compile(src[:cut], 'pcheck.py', 'exec'), g); g['load_patterns']()
d = 7; t0 = time.time(); seen = 0; reps = []
for w in itertools.product((5, 6, 7), repeat=7):
    for s in itertools.product((5, 6, 7), repeat=7):
        best = None
        for r in range(d):
            a = (tuple(w[(i + r) % d] for i in range(d)), tuple(s[(i + r) % d] for i in range(d)))
            b = (tuple(w[(r - i) % d] for i in range(d)), tuple(s[(r - i - 1) % d] for i in range(d)))
            for x in (a, b):
                if best is None or x < best: best = x
        if best == (w, s): reps.append((w, s))
print('classes', len(reps), '%.0fs' % (time.time() - t0), flush=True)
n = 0
with open(out, 'w') as f:
    for w, s in reps:
        lk = ''.join(map(str, w)); sv = ''.join(map(str, s))
        if g['admissible'](d, lk, sv) is None: f.write('R 7 %s %s\n' % (lk, sv)); n += 1
print('admissible', n, '%.0fs' % (time.time() - t0))
