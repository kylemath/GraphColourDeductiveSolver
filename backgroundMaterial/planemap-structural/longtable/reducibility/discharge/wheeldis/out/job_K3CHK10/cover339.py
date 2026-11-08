"""K3CHK10: rotation-preserving occurrence of V1..V8, U1, U2 on every ST-46 tneg receiver row (out/job_ST46/tneg_receiver_violators.txt)."""
src = open('out/job_K3CHK/rowcheck.py').read().split("out = open(K + 'per_row.tsv'")[0].replace("K = 'out/job_K3CHK/'", "K = 'out/job_K3CHK10/'").replace("open(K + 'configs.kc')", "open('out/job_K3CHK10/V1/cfg.in')")
exec(src)
CFG = {t: open('out/job_K3CHK10/%s/cfg.in' % t).read().strip() for t in ['V%d' % i for i in range(1, 9)]}
CFG.update({t: open('out/job_K3CHK9/%s/cfg.in' % t).read().strip() for t in ('U1', 'U2')})
D = {t: int(CFG[t].split()[0][1:].split('_')[0]) for t in CFG}
rows = [l.split() for l in open('out/job_ST46/tneg_receiver_violators.txt') if l.strip() and not l.startswith('#')]
out = []; tot = 0; per = {t: 0 for t in CFG}; byd = {}
for d, L, S, load in rows:
    d = int(d); hit = [t for t in CFG if D[t] == d and occurs(CFG[t], d, L, S)[1] > 0]
    for t in hit: per[t] += 1
    tot += bool(hit); byd.setdefault(d, [0, 0]); byd[d][0] += 1; byd[d][1] += bool(hit)
    out.append('%d/%s/%s\t%s\t%s' % (d, L, S, load, ','.join(hit) or '-'))
open('out/job_K3CHK10/cover339.tsv', 'w').write('# row\tload(ST-46 tneg)\tkills occurring (rotation-preserving)\n' + '\n'.join(out) + '\n')
print('rows', len(rows), 'covered', tot, 'by d (rows, covered)', byd, 'per kill', per)
