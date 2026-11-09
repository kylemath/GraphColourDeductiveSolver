"""K3CHK13: create out/job_HCK5j (CK5J + K5JV00 + K5JVAll) from the PASS of O1. cwd wheeldis. Templates as ST-67 after_hit.py."""
import os, shutil
C = 'out/job_K3CHK13/O1/'; assert open(C + 'verdict.txt').read().strip() == 'PASS'
kc = open(C + 'cfg.in').read().split()
H = 'out/job_HCK5j/'; os.makedirs(H + 'lean', exist_ok=True); M = 'CK5J'; V = 'K5JV'; low = 'k5j'
t = open(C + 'lean/CK5JO1.lean').read().replace('CK5JO1', M).replace('k5jo1', low)
open(H + 'lean/CK5J.lean', 'w').write(t); shutil.copy(C + 'extraC.tsv', H)
for f in ['K3KV00', 'K3KVAll']:
    open(H + 'lean/' + f.replace('K3KV', V) + '.lean', 'w').write(open('out/job_HCK3k/lean/' + f + '.lean').read().replace('CK3K', M).replace('K3KV', V).replace('k3k', low))
X = open(C + 'extraC.tsv').read().split('\t')[2].strip()
open(H + 'module_split.tsv', 'w').write('# index\tmodule\ttheorem\tname\tring\tX\n0\t%s00\t%s.hC_0\t%s\t%s\t%s\n' % (V, V, kc[0], kc[1], X))
rs = open('out/job_HCK3k/lean/run.sh').read().replace('hck3k', 'hck5j').replace('job_HCK3k', 'job_HCK5j').replace('HCK3k', 'HCK5j')
open(H + 'lean/run.sh', 'w').write(rs); os.chmod(H + 'lean/run.sh', 0o755)
open(H + 'drive.sh', 'w').write('#!/bin/zsh\n# HCK5j: CK5J, K5JV00, K5JVAll\ncd $(dirname $0)/lean; ./run.sh CK5J; ./run.sh K5JV00; ./run.sh K5JVAll; echo ALLDONE >> status.txt\n'); os.chmod(H + 'drive.sh', 0o755)
