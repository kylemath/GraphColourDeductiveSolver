import sys, os
E = sys.argv[1]; inp = sys.argv[2]; out = sys.argv[3]
sys.argv = ['pcheck.py', 'none'] + sys.argv[4:]
src = open(os.path.join(E, 'pcheck.py')).read(); cut = src.index("{'xoselftest'")
g = {'__file__': os.path.join(E, 'pcheck.py'), '__name__': 'pcheck_t'}
exec(compile(src[:cut], 'pcheck.py', 'exec'), g); g['load_patterns']()
k = n = 0
with open(out, 'w') as f:
    for line in open(inp):
        _, d, lk, sv = line.split(); n += 1
        if g['admissible'](int(d), lk, sv) is None: f.write(line); k += 1
print('kept', k, 'of', n, 'dropped', n - k)
