"""engine cross-check of cover.py leaves: exec eng_p8/pcheck.py (the LP engine) up to its command table, load_patterns() for the family,
then admissible(d, lk, sv) on every leaf.  'adm' leaves (uncovered completions found by cover.py) must be admissible (None);
'kill' leaves (random completions of a killed placement) must be rejected.  usage: python3 -I chk_engine.py <leaves> <pcheck options...>"""
import sys, os, collections
E = '/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s86_f2b7/eng_p8'
leaves = sys.argv[1]; sys.argv = ['pcheck.py', 'none'] + sys.argv[2:]
src = open(os.path.join(E, 'pcheck.py')).read(); cut = src.rindex("\n{'")
g = {'__file__': os.path.join(E, 'pcheck.py'), '__name__': 'pcheck_t'}
exec(compile(src[:cut], 'pcheck.py', 'exec'), g); g['load_patterns']()
cnt = collections.Counter(); bad = []
for line in open(leaves):
    idx, name, z, kind, lab = line.rstrip('\n').split('\t'); d, lk, sv = lab.split()
    v = g['admissible'](int(d), lk, sv)
    ok = (v is None) if kind == 'adm' else (v is not None)
    cnt[(kind, ok)] += 1
    if not ok: bad.append(line.strip() + '\t' + str(v))
print('engine cross-check', dict(cnt)); [print('  MISMATCH', b) for b in bad[:20]]
