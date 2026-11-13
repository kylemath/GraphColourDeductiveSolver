# W16: the Opus engine (W10's unmodified s67_q7/eng copy) lowerR2 on a certificate, with the FLAGS.md line (families on).
# usage: python3 -I opus_lower.py CERT.json [extra opts]
import sys, os
ENG = '/tmp/swarm-W10/opus_eng/pcheck.py'; K = '/mnt/project-files/swarm/round6/W1-minimal-set/k95f/tab/'
P = '/tmp/swarm-A2/opus/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/'
FL = ['xon', 'apexcls', 'filt16', 'hat5', 'consall', 'l3q', 'lqcap=3', 'l3qV=7,8', 'killtab=' + K + 'kill/kill6',
      'l3qtab=' + K + 'tab_1.json,' + K + 'tab_-1.json', 'l3qtab8=' + K + 'tabV8_1.json,' + K + 'tabV8_-1.json',
      'f2b=' + K + 'rules_studio_keep95p131f.json', 'rpatN=' + P + 's39o/rpatN3.txt', 'root=/tmp/swarm-W10/wd',
      'args=/tmp/swarm-A2/args_A97_remap.txt', 'rpat=' + P + 'rpatD.txt', 'exname=' + K + 'exname_keep95p131f.txt',
      'work=/tmp/swarm-W16/opus_work', 'xcap=3', 'nomax', 'threads=1',
      'cert=' + sys.argv[1]] + {'base': [], 'rrz': ['hatrr', 'zh', 'zr', 'zcap=3'], 'all': ['hatrr', 'zh', 'zr', 'zcap=3', 'q7', 'q7m', 'q7rc', 'q7cap=3']}[os.environ.get('OFAM', 'all')] + sys.argv[2:]
sys.argv = [ENG, 'lowerR2'] + FL
exec(compile(open(ENG).read(), ENG, 'exec'), {'__file__': ENG, '__name__': '__main__'})
