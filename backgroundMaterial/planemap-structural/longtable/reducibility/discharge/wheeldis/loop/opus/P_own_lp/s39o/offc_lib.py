"""s39o: load the engine (eng/pcheck.py) as a library with the given options and no command; returns its namespace."""
import os, sys
H = os.path.dirname(os.path.abspath(__file__))
def load(opts):
    sv = sys.argv
    sys.argv = [os.path.join(H, 'eng', 'pcheck.py'), 'none'] + list(opts)
    ns = {'__file__': sys.argv[0], '__name__': 'pcheck_lib'}
    exec(open(sys.argv[0]).read().replace("}.get(CMD, lambda: print(__doc__))()", "}.get(CMD, lambda: None)()"), ns)
    sys.argv = sv
    return ns
