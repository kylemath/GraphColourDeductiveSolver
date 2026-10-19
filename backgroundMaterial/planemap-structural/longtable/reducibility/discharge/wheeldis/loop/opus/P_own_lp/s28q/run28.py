# driver: exec the s24d engine (pcheck.py + prelay2.py) with st24b flags, then pricer28.py
import sys, os
S28 = os.path.dirname(os.path.abspath(__file__)); E = os.path.join(S28, '..', 's24d'); B = os.path.join(S28, '..')
M = '/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad/P/m/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis'
CERT = os.path.normpath(os.path.join(E, 'cert_st24bL.json'))
sys.argv = [os.path.join(E, 'pcheck.py'), 'none', 'xon', 'apexcls', 'filt16', 'hat5', 'consall', 'xcap=3',
            'killtab=' + os.path.normpath(os.path.join(B, 's25/f/kill/kill6')), 'root=' + M,
            'args=' + os.path.normpath(os.path.join(B, 's25/argsA59.txt')), 'rpat=' + os.path.normpath(os.path.join(B, 'rpatD.txt')),
            'work=/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad/P/wr28q']
src = open(os.path.join(E, 'pcheck.py')).read(); last = src.rstrip().rsplit('\n', 1)
assert "'rowR2': cmd_rowR2" in last[1]
g = {'__file__': os.path.join(E, 'pcheck.py'), '__name__': 'eng', 'S28': S28, 'CERT': CERT}
exec(compile(last[0], os.path.join(E, 'pcheck.py'), 'exec'), g)
exec(compile(open(os.path.join(S28, 'pricer28.py')).read(), 'pricer28.py', 'exec'), g)
