# s33z: class table with zh + hat5 + filt16 + xon builds (no overflow) and separates (a,b,e,f,q,r) at c = 0 (mode-2 distinctness)
import os, sys, itertools, numpy as np
E = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'eng')
M = '/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad/P/m/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis'
B = '/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp'
sys.argv = [os.path.join(E, 'pcheck.py'), 'none', 'root=' + M, 'xon', 'apexcls', 'filt16', 'killtab=' + B + '/s31/f/kill/kill6', 'hat5', 'zh', 'zr', 'hatrr', 'work=/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad/P/wr33t']
src = open(os.path.join(E, 'pcheck.py')).read().rstrip().rsplit('\n', 1)[0]; G = {'__file__': os.path.join(E, 'pcheck.py')}
exec(compile(src, 'pcheck.py', 'exec'), G)
C = G['class_table_R2'](True)
print('class table built: max id %d (< 2^31-1)' % int(C.max()))
bad = 0; seen = {}; ids_of = {}
for a, b, e, f, q, r, s_ in itertools.product(range(5), repeat=7):
    k = int(C[a, b, 0, e, f, 0, q, r, s_]); t = (a, b, e, f, q, r)
    if seen.setdefault(k, t) != t: bad += 1
    ids_of.setdefault(t, set()).add(k)
c1 = set(np.unique(C[:, :, 1])); c0 = set(np.unique(C[:, :, 0])); cx = set(np.unique(C[:, :, 2:]))
print('c=0 positions: %d ids, %d collisions of distinct (a,b,e,f,q,r) (one id may hold several s when the hat5 key agrees) ; overlap of c=0 ids with c=1 / c>=2 ids: %d / %d' % (len(seen), bad, len(c0 & c1), len(c0 & cx)))
