# every canonical non-R6 6-link (all6_words) x every apex word over the class witnesses {5, 7} -> consbasis json (s85 world LP)
import sys, os, json, itertools
E = sys.argv[1]; out = sys.argv[2]
sys.argv = ['pcheck.py', 'none'] + sys.argv[3:]
src = open(os.path.join(E, 'pcheck.py')).read(); cut = src.index("{'gkselftest'")
g = {'__file__': os.path.join(E, 'pcheck.py'), '__name__': 'pcheck_t'}
exec(compile(src[:cut], 'pcheck.py', 'exec'), g)
A6 = g['all6_words'](); L = [[list(map(int, Lw)), list(s)] for Lw in A6 for s in itertools.product((5, 7), repeat=6)]
json.dump(L, open(out, 'w')); print('links', len(A6), 'rows', len(L))
