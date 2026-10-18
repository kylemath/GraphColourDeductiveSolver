"""P2 s9: are the drop44 patterns (as pattern tuples, any source) loaded under a registry? usage: chk_drop.py DROPFILE opts"""
import sys, runpy, os, io, contextlib
drop = [l.split()[0] for l in open(sys.argv[1]) if l.strip() and not l.startswith('#')]
sys.argv = ['pcheck.py', 'none'] + sys.argv[2:]
with contextlib.redirect_stdout(io.StringIO()): G = runpy.run_path(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'pcheck.py'))
G['load_patterns']()
hit = [n for n in drop if G['pname'](n)[1] in G['PATS'][G['pname'](n)[0]]]
print('drop44 names whose pattern is loaded:', len(hit), hit)
