"""K3CHK9: rotation-preserving occurrence of U1 and U2 on every row of out/job_ST44/tneg_d9_violators.txt (94 d9 rows)."""
src = open('out/job_K3CHK/rowcheck.py').read().split("out = open(K + 'per_row.tsv'")[0].replace("K = 'out/job_K3CHK/'", "K = 'out/job_K3CHK9/'").replace("CF = {", "CF0 = {")
src = src.replace("open(K + 'configs.kc')", "open(K + 'U1/cfg.in')")
exec(src)
U = {t: open('out/job_K3CHK9/%s/cfg.in' % t).read().strip() for t in ('U1', 'U2')}
rows = [l.split() for l in open('out/job_ST44/tneg_d9_violators.txt') if l.strip() and not l.startswith('#')]
cov = {'U1': 0, 'U2': 0}; anyc = 0; out = []
for d, L, S, load in rows:
    r = {t: occurs(U[t], 9, L, S)[1] for t in U}
    for t in U: cov[t] += r[t] > 0
    c = any(v > 0 for v in r.values()); anyc += c
    out.append('%s/%s/%s\t%s\tU1 %d\tU2 %d\t%s' % (d, L, S, load, r['U1'], r['U2'], 'COVERED' if c else 'not covered'))
open('out/job_K3CHK9/cover94.tsv', 'w').write('# row\tload(ST-44 tneg)\tU1 rot-pres embeddings\tU2\tcovered\n' + '\n'.join(out) + '\n')
print('rows', len(rows), 'U1', cov['U1'], 'U2', cov['U2'], 'U1 or U2', anyc)
for o in out:
    if 'not covered' in o: print(o)
