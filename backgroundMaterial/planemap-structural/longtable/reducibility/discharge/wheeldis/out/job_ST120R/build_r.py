"""ST-120 R: build job_HDRS403 (hD, gen_hd) and job_HCRS403 (CKRS403 + RS403Vkk hC + RS403VAll) from the PASS rows of
verdicts.tsv, and write queue_order.txt (largest ring first). usage (cwd wheeldis): python3 out/job_ST120R/build_r.py"""
import subprocess, os
J = 'out/job_ST120R/'; HD = 'out/job_HDRS403/'; HC = 'out/job_HCRS403/'
for d in (HD + 'lean', HC + 'lean'): os.makedirs(d, exist_ok=True)
V = {l.split('\t')[0]: l.rstrip('\n').split('\t') for l in open(J + 'verdicts.tsv')}
items = [l.rstrip('\n').split('\t') for l in open(J + 'items.tsv')]
ok = [it for it in items if V.get(it[0], [0, 0, 0, 'MISSING'])[3] == 'PASS']
Ds = [it for it in ok if it[1] == 'D']; Cs = [it for it in ok if it[1] == 'C']
Ds.sort(key=lambda it: -int(it[3].split()[1])); Cs.sort(key=lambda it: -int(it[3].split()[1]))
open(HD + 'D.tsv', 'w').write(''.join('%s\t%s\n' % (n, ' '.join(kc.split()[1:])) for n, v, X, kc in Ds))
subprocess.run(['python3', 'out/job_HD0/gen_hd.py', HD + 'D.tsv', HD + 'lean', 'HDRS403', 'hdrs403', '1'], check=True)
with open(HD + 'module_split.tsv', 'w') as f:
    f.write('# index\tmodule\ttheorem\tname\tring\n')
    for i, (n, v, X, kc) in enumerate(Ds): f.write('%d\tHDRS403V%02d\tHDRS403V.hD_%d\t%s\t%s\n' % (i, i, i, n, kc.split()[1]))
open(HC + 'extraC.tsv', 'w').write(''.join('%s\t%s\t%s\n' % (n, ' '.join(kc.split()[1:]), X) for n, v, X, kc in Cs))
env = dict(os.environ, WHEELDIS=os.getcwd(), RMAX='16', ONLY='', EXTRAFILE=HC + 'extraC.tsv')
g = subprocess.run(['python3', 'out/job_OCC13/in/vendor/gen_ccover3.py'], capture_output=True, text=True, env=env).stdout.split('\n')
a_ = [k for k, l in enumerate(g) if l.startswith('def ccEntries')][0]; b_ = max(k for k, l in enumerate(g) if l.startswith('    lbl :='))
ck = open('out/job_HCK3k/lean/CK3K.lean').read().split('\n')
a2 = [k for k, l in enumerate(ck) if l.startswith('def k3kEntries')][0]; b2 = [k for k, l in enumerate(ck) if l.startswith('    lbl :=')][0]
t = '\n'.join(ck[:a2 + 1] + g[a_ + 1:b_ + 1] + ck[b2 + 1:])
t = t.replace('CK3K (Studio, HCK3k, 8 Nov): the K3k C kill b8_u...56556_.....66. = f8_...56556_.....66. of pat_K3g2_C.cfast 6f6dce95 (same literal and X as in CK3C7)',
              'CKRS403 (Studio, ST-120 R, 10 Nov): the %d RSST C2cons configs still without hC (rsst582_lean_coverage d2f91ec5), RSST X, own-engine re-check PASS, gen_ccover3 3c9e7145 EXTRAFILE literals' % len(Cs)).replace('k3k', 'rs403').replace('CK3K', 'CKRS403')
t = t.replace('rs403Entries.length = 1', 'rs403Entries.length = %d' % len(Cs))
open(HC + 'lean/CKRS403.lean', 'w').write(t)
names = [l.split('"')[1] for l in t.split('\n') if l.strip().startswith('{ name := "')]
assert names == [it[0] for it in Cs], 'CK entry order differs from the module split'
for i in range(len(Cs)):
    s = open('out/job_HCK3k/lean/K3KV00.lean').read().replace('CK3K', 'CKRS403').replace('K3KV', 'RS403V').replace('k3k', 'rs403').replace('⟨0,', '⟨%d,' % i).replace('hC_0', 'hC_%d' % i)
    open(HC + 'lean/RS403V%02d.lean' % i, 'w').write(s)
s = open('out/job_HCK3k/lean/K3KVAll.lean').read().replace('import K3KV00', '\n'.join('import RS403V%02d' % i for i in range(len(Cs)))).replace('CK3K', 'CKRS403').replace('K3KV', 'RS403V').replace('k3k', 'rs403').replace('Fin 1', 'Fin %d' % len(Cs)).replace('  · exact hC_0', '\n'.join('  · exact hC_%d' % i for i in range(len(Cs))))
open(HC + 'lean/RS403VAll.lean', 'w').write(s)
with open(HC + 'module_split.tsv', 'w') as f:
    f.write('# index\tmodule\ttheorem\tname\tring\tX\n')
    for i, (n, v, X, kc) in enumerate(Cs): f.write('%d\tRS403V%02d\tRS403V.hC_%d\t%s\t%s\t%s\n' % (i, i, i, n, kc.split()[1], X))
for H, job in ((HD, 'HDRS403'), (HC, 'HCRS403')):
    rs = open('out/job_HCK3k/lean/run.sh').read().replace('hck3k', job.lower()).replace('job_HCK3k', 'job_' + job).replace('HCK3k', job)
    open(H + 'lean/run.sh', 'w').write(rs); os.chmod(H + 'lean/run.sh', 0o755)
# coordinator 15:53Z: the W2p configs (private letters needed; rsst_conf_windows.json 4da44238) first, then the rest; each part largest ring first
W2P = set(open(J + 'w2p_names.txt').read().split())
rows = [(n in W2P, int(kc.split()[1]), 'job_HDRS403', 'HDRS403V%02d' % i) for i, (n, v, X, kc) in enumerate(Ds)] + \
       [(n in W2P, int(kc.split()[1]), 'job_HCRS403', 'RS403V%02d' % i) for i, (n, v, X, kc) in enumerate(Cs)]
rows.sort(key=lambda x: (not x[0], -x[1], x[2]))
rows = [(r, j, m) for w, r, j, m in rows]
open(J + 'queue_order.txt', 'w').write(''.join('%s %s %d\n' % (j, m, r) for r, j, m in rows))
print('D', len(Ds), 'C', len(Cs), 'queue', len(rows), 'not PASS', len(items) - len(ok))
