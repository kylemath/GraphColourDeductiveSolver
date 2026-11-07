"""K3CHK3: occurrence (rotation-preserving, Z-consistent frame of the row itself) of the two 04:24 kills in their target rows, in the
violated rotations given, and in every row still uncovered in binding_coverage.tsv (8f15f4e2). Uses K3CHK's occurs()."""
import collections
src = open('out/job_K3CHK/rowcheck.py').read().split("out = open(K + 'per_row.tsv'")[0].replace("K = 'out/job_K3CHK/'", "K = 'out/job_K3CHK3/'")
exec(src)
tgt = {'b9_u.56.56555_.5.......': [('555657658', '756756558'), ('856756555', '556576578'), ('855565765', '875675655')],
       'b9_u75..65656_5...55...': [('565675676', '566555555')]}
rows = []
for i, l in enumerate(open(K + 'in/binding_coverage.tsv'), 1):
    if l.startswith('#') or not l.strip(): continue
    f = l.rstrip('\n').split('\t'); rows.append((i, f[0], int(f[1]), f[5]))
out = open(K + 'per_row.tsv', 'w'); out.write('# config\twhat\tline\trow\tface-set\trotation-preserving\tPASS/FAIL\n'); cnt = collections.Counter()
for nm, line in CF.items():
    for L, S in tgt[nm]:
        fs, rt = occurs(line, 9, L, S); ok = rt > 0; cnt[(nm, 'target', ok)] += 1
        out.write('%s\ttarget\t-\t9 %s %s\t%d\t%d\t%s\n' % (nm, L, S, fs, rt, 'PASS' if ok else 'FAIL'))
    for i, row, d, cov in rows:
        if cov == 'yes' or d != int(nm[1]): continue
        L, S = row.split('/')
        if (L, S) in tgt[nm]: continue
        fs, rt = occurs(line, d, L, S); ok = rt == 0; cnt[(nm, 'uncovered', ok)] += 1
        out.write('%s\tuncovered\t%d\t%d %s %s\t%d\t%d\t%s\n' % (nm, i, d, L, S, fs, rt, 'PASS' if ok else 'FAIL'))
out.close()
for k, v in sorted(cnt.items()): print(k, v)
