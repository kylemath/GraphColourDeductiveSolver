"""K3CHK14: create out/job_HDK5m (HDK5M + HDK5MV00 + HDK5MAll via gen_hd f743a82d) from the PASS of Q1. cwd wheeldis. Templates as ST-67 after_hit.py."""
import os, subprocess
C = 'out/job_K3CHK14/Q1/'; assert open(C + 'verdict.txt').read().strip() == 'PASS'
kc = open(C + 'cfg.in').read().split()
H = 'out/job_HDK5m/'; os.makedirs(H + 'lean', exist_ok=True); M = 'HDK5M'
open(H + 'D.tsv', 'w').write('%s\t%s\n' % (kc[0], ' '.join(kc[1:])))
subprocess.run(['python3', 'out/job_HD0/gen_hd.py', H + 'D.tsv', H + 'lean', M, 'hdk5m', '1'], check=True)
mods = [M, M + 'V00', M + 'All']
rs = open('out/job_HCK3k/lean/run.sh').read().replace('hck3k', 'hdk5m').replace('job_HCK3k', 'job_HDK5m').replace('HCK3k', 'HDK5m')
open(H + 'lean/run.sh', 'w').write(rs); os.chmod(H + 'lean/run.sh', 0o755)
open(H + 'drive.sh', 'w').write('#!/bin/zsh\n# HDK5m: %s\ncd $(dirname $0)/lean; %s; echo ALLDONE >> status.txt\n' % (', '.join(mods), '; '.join('./run.sh ' + m for m in mods))); os.chmod(H + 'drive.sh', 0o755)
