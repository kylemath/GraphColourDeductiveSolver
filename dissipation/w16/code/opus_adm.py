# W16: filter receiver labels of a pickle by the Opus engine's own admissible() (A97 stack, FLAGS line); writes the kept pickle.
# usage: python3 -I opus_adm.py IN.pkl OUT.pkl
import sys, os, pickle, collections
IN, OUT = sys.argv[1], sys.argv[2]
ENG = '/tmp/swarm-W10/opus_eng/pcheck.py'; K = '/mnt/project-files/swarm/round6/W1-minimal-set/k95f/tab/'
P = '/tmp/swarm-A2/opus/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/'
FL = ['xon', 'apexcls', 'filt16', 'hat5', 'consall', 'l3q', 'lqcap=3', 'l3qV=7,8', 'killtab=' + K + 'kill/kill6',
      'l3qtab=' + K + 'tab_1.json,' + K + 'tab_-1.json', 'l3qtab8=' + K + 'tabV8_1.json,' + K + 'tabV8_-1.json',
      'f2b=' + K + 'rules_studio_keep95p131f.json', 'rpatN=' + P + 's39o/rpatN3.txt', 'root=/tmp/swarm-W10/wd',
      'args=/tmp/swarm-A2/args_A97_remap.txt', 'rpat=' + P + 'rpatD.txt', 'exname=' + K + 'exname_keep95p131f.txt',
      'work=/tmp/swarm-W16/opus_work', 'xcap=3', 'nomax', 'threads=1', 'hatrr', 'zh', 'zr', 'zcap=3', 'q7', 'q7m', 'q7rc', 'q7cap=3']
sys.argv = [ENG, 'help'] + FL
ns = {'__file__': ENG, '__name__': 'pcheck_w16'}
exec(compile(open(ENG).read(), ENG, 'exec'), ns)
ns['load_patterns']()
labs = pickle.load(open(IN, 'rb')); keep = []; why = collections.Counter()
for lab in labs:
    if lab[0] == 'R':
        r = ns['admissible'](lab[1], ''.join(map(str, lab[2])), ''.join(map(str, lab[3])))
        if r is not None: why[str(r)[:12]] += 1; continue
    keep.append(lab)
pickle.dump(keep, open(OUT, 'wb'))
print('opus_adm: kept %d of %d; dropped receivers %s' % (len(keep), len(labs), dict(why)), flush=True)
