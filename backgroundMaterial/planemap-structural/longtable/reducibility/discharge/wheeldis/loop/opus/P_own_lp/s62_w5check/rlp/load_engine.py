# Load the (copied) Opus pcheck engine namespace with the exact options of teamA/R4-A1-motifs/scripts/pc.sh, command 'help'
# (so nothing runs), then expose its functions.  Extra flags can be appended (e.g. q7).
import sys, os
ENG = '/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s62_w5check/eng/pcheck.py'
S = '/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s60_f2b/tab/'
P = '/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/'
BASE = ['xon', 'apexcls', 'filt16', 'hat5', 'consall', 'l3q', 'lqcap=3', 'l3qV=7,8',
        'killtab=' + S + 'kill/kill6',
        'l3qtab=' + S + 'tab_1.json,' + S + 'tab_-1.json',
        'l3qtab8=' + S + 'tabV8_1.json,' + S + 'tabV8_-1.json',
        'f2b=/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad/gcoct26/kill_upgraded/tierA/full2ball_extra_rules.json',
        'rpatN=' + P + 's39o/rpatN3.txt', 'root=/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad/P/m/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis', 'args=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s33z/reg_A97/args_A97.txt',
        'rpat=' + P + 'rpatD.txt', 'exname=' + P + 's40f/exname_rm128.txt', 'work=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s62_w5check/work_rlp',
        'cert=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s62_w5check/certs/certP2full_rat.json', 'xcap=3']
def load(cmd='help', extra=()):
    sys.argv = [ENG, cmd] + BASE + list(extra)
    ns = {'__file__': ENG, '__name__': 'pcheck_w5'}
    exec(compile(open(ENG).read(), ENG, 'exec'), ns)
    return ns
