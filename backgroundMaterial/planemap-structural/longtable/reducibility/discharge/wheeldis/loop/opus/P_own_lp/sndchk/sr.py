import sys, os, json, collections
eng = sys.argv[1]; args = sys.argv[2]; kill = sys.argv[3]
root='/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad/P/m/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis'
sys.argv = [os.path.join(eng,'pcheck.py'), 'none', 'xon','apexcls','filt16','hat5','killtab='+kill,'root='+root,'args='+args,
            'work=/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad/chk4/work']
__file__ = sys.argv[0]
src = open(sys.argv[0]).read()
import io, contextlib
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(src, sys.argv[0], 'exec'))
SR = R2_sender_rows()
print('engine', eng, 'sender rows', len(SR))
Q = [('55667',[0,1,0,0,0],[1,1]),('55667',[0,1,0,1,0],[0,0]),('55667',[0,1,0,1,0],[1,0]),('55758',[0,0,0,0,0],[])]
for wd,H,F in Q:
    hit=[cf for w,cf,b in SR if w==wd and b==H+['|']+F]
    print(wd,H,F,'LIVE' if hit else 'absent', len(hit), hit[0] if hit else '')
# all contexts of these words
for wd in ('55667','55758'):
    print(wd, sorted(tuple(b) for w,cf,b in SR if w==wd).__len__())
