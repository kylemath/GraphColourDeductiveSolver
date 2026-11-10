"""ST-97 (Studio): usage (cwd wheeldis) after_hit.py NN : after a PASS in out/job_ST97/chk/hNN: create the Lean job (C: out/job_HCK5PNN = CK5PNN + K5PNNV00 + K5PNNVAll; D: out/job_HDK5PNN via gen_hd f743a82d: HDK5PNN + V00 + All)
and its drive.sh, append the hit's rows to killed_rows.txt, and append to skip_b96.txt every unscreened window whose rows are all killed."""
import os, sys, shutil, subprocess, glob, re
NN = sys.argv[1]; C = 'out/job_ST97/chk/h%s/' % NN; assert open(C + 'verdict.txt').read().strip() == 'PASS'
kc = open(C + 'cfg.in').read().split(); isC = os.path.exists(C + 'extraC.tsv')
rep = open(C + 'report.md').read(); rows = re.search(r'rows K\d+:(\S+?),? lead', rep) or re.search(r'rows K\d+:(\S+)', rep); rows = rows.group(1).rstrip(',').split(',')
if isC:
    H = 'out/job_HCK5P%s/' % NN; os.makedirs(H + 'lean', exist_ok=True); M = 'CK5P%s' % NN; V = 'K5P%sV' % NN; low = 'k5p%s' % NN
    shutil.copy(C + 'lean/%s.lean' % M, H + 'lean/'); shutil.copy(C + 'extraC.tsv', H)
    for f in ['K3KV00', 'K3KVAll']:
        open(H + 'lean/' + f.replace('K3KV', V) + '.lean', 'w').write(open('out/job_HCK3k/lean/' + f + '.lean').read().replace('CK3K', M).replace('K3KV', V).replace('k3k', low))
    X = open(C + 'extraC.tsv').read().split('\t')[2].strip()
    open(H + 'module_split.tsv', 'w').write('# index\tmodule\ttheorem\tname\tring\tX\n0\t%s00\t%s.hC_0\t%s\t%s\t%s\n' % (V, V, kc[0], kc[1], X))
    mods = [M, V + '00', V + 'All']; job = 'HCK5P%s' % NN
else:
    H = 'out/job_HDK5P%s/' % NN; os.makedirs(H + 'lean', exist_ok=True); M = 'HDK5P%s' % NN
    open(H + 'D.tsv', 'w').write('%s\t%s\n' % (kc[0], ' '.join(kc[1:])))
    subprocess.run(['python3', 'out/job_HD0/gen_hd.py', H + 'D.tsv', H + 'lean', M, 'hdk5p%s' % NN, '1'], check=True)
    mods = [M, M + 'V00', M + 'All']; job = 'HDK5P%s' % NN
rs = open('out/job_HCK3k/lean/run.sh').read().replace('hck3k', job.lower()).replace('job_HCK3k', 'job_' + job).replace('HCK3k', job)
open(H + 'lean/run.sh', 'w').write(rs); os.chmod(H + 'lean/run.sh', 0o755)
open(H + 'drive.sh', 'w').write('#!/bin/zsh\n# %s: %s\ncd $(dirname $0)/lean; %s; echo ALLDONE >> status.txt\n' % (job, ', '.join(mods), '; '.join('./run.sh ' + m for m in mods))); os.chmod(H + 'drive.sh', 0o755)
J = 'out/job_ST97/'
K = {l.strip() for l in open(J + 'killed_rows.txt') if l.strip()}
with open(J + 'killed_rows.txt', 'a') as f:
    for r in rows:
        x = '%d/%s' % (len(r.split('/')[0]), r)
        if x not in K: f.write(x + '\n'); K.add(x)
done = set()
for f in glob.glob(J + 'results/res_K5_*.tsv'):
    for l in open(f): done.add(l.split('\t')[0])
skip = {l.split()[0] for l in open(J + 'skip_b96.txt') if l.strip()}
add = []
for f in sorted(glob.glob(J + 'famK5_r1516_b96_*.tsv')):
    for l in open(f):
        g = l.rstrip('\n').split('\t')
        if not g[0] or g[0].startswith('#') or g[0] in done or g[0] in skip: continue
        rw = ['%d/%s' % (len(r.split('/')[0]), r) for r in g[4].split(':', 1)[1].split(',')]
        if all(r in K for r in rw): add.append(g[0]); skip.add(g[0])
open(J + 'skip_b96.txt', 'a').write(''.join(a + '\n' for a in add))
print(job, 'rows', rows, 'skip +%d' % len(add))
