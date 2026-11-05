# s78: load the s78 engine namespace (pcheck.py with command 'help', so nothing runs) with the env78 flag set + extra flags.
# usage: from loadeng import load; ns = load(stack='s75', extra=['kstar'])
import sys, os
N = '/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s78_kstar'
B = os.path.dirname(N); SC = '/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad'
W = 'backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis'
def flags(stack='s75', fam='full'):
    T = B + ('/s75_teamA/tab' if stack == 's75' else '/s77_k6patch/tab')
    F = ['xon', 'apexcls', 'filt16', 'hat5', 'consall', 'l3q', 'lqcap=3', 'l3qV=7,8', 'killtab=' + T + '/kill/kill6',
         'l3qtab=%s/tab_1.json,%s/tab_-1.json' % (T, T), 'l3qtab8=%s/tabV8_1.json,%s/tabV8_-1.json' % (T, T), 'f2b=' + T + '/rules_studio_keep95p131f.json']
    if fam in ('rrz', 'full'): F += ['hatrr', 'zh', 'zr', 'zcap=3']
    if fam == 'full': F += ['q7', 'q7m', 'q7rc', 'q7cap=3']
    F += ['rpatN=' + B + '/s39o/rpatN3.txt', 'root=' + SC + '/P/m/' + W, 'args=' + B + '/s33z/reg_A97/args_A97.txt', 'rpat=' + B + '/rpatD.txt',
          'exname=' + T + '/exname_keep95p131f.txt']
    return F
def load(stack='s75', fam='full', extra=(), work=None):
    eng = N + '/eng/pcheck.py'
    sys.argv = [eng, 'help'] + flags(stack, fam) + list(extra) + ['work=' + (work or SC + '/sD/work_tests')]
    ns = {'__file__': eng, '__name__': 'pcheck_s78'}
    import io, contextlib
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf): exec(compile(open(eng).read(), eng, 'exec'), ns)
    ns['_loadlog'] = buf.getvalue()
    return ns
