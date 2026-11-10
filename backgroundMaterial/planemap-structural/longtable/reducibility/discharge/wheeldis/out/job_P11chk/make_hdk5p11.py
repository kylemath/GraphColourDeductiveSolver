"""P11: create out/job_HDK5P11 (HDK5P11 + V00 + All via gen_hd f743a82d) from the PASS of container hit 493fd1a3b63c01029242 (out/job_P11chk/chk/h11). cwd wheeldis."""
import os, subprocess
C = 'out/job_P11chk/chk/h11/'; assert open(C + 'verdict.txt').read().strip() == 'PASS'
kc = open(C + 'cfg.in').read().split()
H = 'out/job_HDK5P11/'; os.makedirs(H + 'lean', exist_ok=True); M = 'HDK5P11'
open(H + 'D.tsv', 'w').write('%s\t%s\n' % (kc[0], ' '.join(kc[1:])))
subprocess.run(['python3', 'out/job_HD0/gen_hd.py', H + 'D.tsv', H + 'lean', M, 'hdk5p11', '1'], check=True)
mods = [M, M + 'V00', M + 'All']
rs = open('out/job_HCK3k/lean/run.sh').read().replace('hck3k', 'hdk5p11').replace('job_HCK3k', 'job_HDK5P11').replace('HCK3k', 'HDK5P11')
open(H + 'lean/run.sh', 'w').write(rs); os.chmod(H + 'lean/run.sh', 0o755)
open(H + 'drive.sh', 'w').write('#!/bin/zsh\n# HDK5P11: %s\ncd $(dirname $0)/lean; %s; echo ALLDONE >> status.txt\n' % (', '.join(mods), '; '.join('./run.sh ' + m for m in mods))); os.chmod(H + 'drive.sh', 0o755)
