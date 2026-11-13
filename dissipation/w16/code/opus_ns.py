# W16: load the Opus engine namespace (pcheck.py, A97 stack, FLAGS line, families on) for admissible() calls.
import sys
ENG = '/tmp/swarm-W10/opus_eng/pcheck.py'; K = '/mnt/project-files/swarm/round6/W1-minimal-set/k95f/tab/'
P = '/tmp/swarm-A2/opus/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/'
FL = ['xon', 'apexcls', 'filt16', 'hat5', 'consall', 'l3q', 'lqcap=3', 'l3qV=7,8', 'killtab=' + K + 'kill/kill6',
      'l3qtab=' + K + 'tab_1.json,' + K + 'tab_-1.json', 'l3qtab8=' + K + 'tabV8_1.json,' + K + 'tabV8_-1.json',
      'f2b=' + K + 'rules_studio_keep95p131f.json', 'rpatN=' + P + 's39o/rpatN3.txt', 'root=/tmp/swarm-W10/wd',
      'args=/tmp/swarm-A2/args_A97_remap.txt', 'rpat=' + P + 'rpatD.txt', 'exname=' + K + 'exname_keep95p131f.txt',
      'work=/tmp/swarm-W16/opus_work', 'xcap=3', 'nomax', 'threads=1', 'hatrr', 'zh', 'zr', 'zcap=3', 'q7', 'q7m', 'q7rc', 'q7cap=3']
def load():
    save = list(sys.argv); sys.argv = [ENG, 'help'] + FL
    ns = {'__file__': ENG, '__name__': 'pcheck_w16'}
    exec(compile(open(ENG).read(), ENG, 'exec'), ns)
    ns['load_patterns'](); sys.argv = save
    return ns
